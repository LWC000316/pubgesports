#!/usr/bin/env python3
"""
시드 데이터가 아직 최신인지 확인한다. **아무것도 쓰지 않는다.**

세 가지를 본다:

  1. 더 최근 대회가 열렸는가
     시리즈의 하위 문서를 전부 나열해 지금 가리키는 것보다 나중에 시작한 대회를 찾는다.
     PTS 가 이 검사가 없어서 5개월 지난 Phase 1 을 붙들고 있었다 — 그때 이미
     Phase 2 가 시작해 있었고, 바꾸니 24팀 중 9팀이 교체됐다.

  2. 지금 대회의 참가팀·로스터가 시드와 다른가
     대회가 진행 중이면 로스터가 바뀐다. 다르다고 무조건 고쳐야 하는 건 아니다 —
     이 저장소는 '대회 시점 명단'을 보관하므로 대회가 끝난 뒤에 맞추는 것이 맞다.

  3. 대회가 끝났는데 그 뒤로 다시 수집하지 않았는가
     진행 중에 수집한 데이터는 최종 명단이 아니다.

판정은 하지만 수정은 하지 않는다. 무엇을 다시 수집할지는 사람이 정한다.

    python ingest/check_freshness.py              # 여섯 리그 전부
    python ingest/check_freshness.py --league PTS # 하나만
    python ingest/check_freshness.py --offline    # 캐시만 사용

조치가 필요하면 종료 코드 1 을 돌려준다.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mediawiki_client import MediaWikiClient          # noqa: E402
from build_league_seed_mediawiki import (             # noqa: E402
    parse_participants,
    parse_participants_html,
    fetch_team_display,
    use_utf8_output,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES = PROJECT_ROOT / "primary_data" / "_sources.json"

OK, WARN, STALE = "OK", "WARN", "STALE"


def load_sources():
    doc = json.loads(SOURCES.read_text(encoding="utf-8"))
    return doc["leagues"]


def newer_tournaments(client, series_prefix, current_page, current_start):
    """
    같은 시리즈에서 지금 것보다 나중에 시작한 대회를 찾는다.

    문서명은 `시리즈/연도/이름` 이라 슬래시가 정확히 2개인 것만 본선 문서다.
    (`.../Cup`, `.../Stage_S` 같은 하위 문서를 걸러낸다.)
    """
    found = []
    for year in (date.today().year, date.today().year + 1):
        resp = client.get({
            "action": "query", "list": "allpages",
            "apprefix": "%s/%d" % (series_prefix, year),
            "aplimit": "200", "apfilterredir": "nonredirects",
        })
        for p in resp.get("query", {}).get("allpages", []):
            title = p["title"]
            if title.count("/") != 2:
                continue
            page = title.replace(" ", "_")
            if page == current_page:
                continue
            found.append(page)

    if current_start is None:
        # 지금 대회의 시작일을 모르면 순서를 매길 수 없다. 자동 판정 대신 형제 문서를
        # 나열해 사람이 보게 한다 (PVS 2026 Phase 2 는 인포박스 날짜가 비어 있다).
        return None, sorted(found)

    newer = []
    for page in found:
        start = tournament_dates(client, page)[0]
        if start is not None and start > current_start:
            newer.append((page, start))
    return newer, []


def tournament_dates(client, page):
    wt = client.wikitext(page)
    m = re.search(r"\{\{Infobox league(.*?)\n\}\}", wt, re.S)
    body = m.group(1) if m else ""

    def field(key):
        mm = re.search(r"\|" + key + r"=([^|\n}]*)", body)
        value = mm.group(1).strip() if mm else ""
        return value or None

    return field("sdate"), field("edate")


def live_rosters(client, page, rosters_from_html):
    """대회 문서에서 현재 참가팀과 로스터를 읽는다. 시드와 같은 형태로 돌려준다."""
    if rosters_from_html:
        return {r["name"]: {p["nickname"] for p in r["players"]}
                for r in parse_participants_html(client, page, include_subs=True)}

    entries = parse_participants(client.wikitext(page), include_subs=True)
    displays = fetch_team_display(client, page)
    if len(entries) != len(displays):
        raise SystemExit(
            "%s: 원문 %d개 / 렌더 %d개로 개수가 어긋납니다. 대조할 수 없습니다."
            % (page, len(entries), len(displays)))
    return {d["name"]: {p["nickname"] for p in e["players"]}
            for e, d in zip(entries, displays)}


def check_league(client, league, meta, today):
    findings = []
    level = OK

    seed = json.loads((PROJECT_ROOT / meta["seedFile"]).read_text(encoding="utf-8"))
    # 시드 표기가 위키와 다른 팀은 _sources.json 의 teamAliases 로 대응시킨다.
    # 짐작으로 이름을 맞추지 않는다 — 사람이 확인해 적어 둔 것만 쓴다.
    alias = meta.get("teamAliases", {})
    seed_rosters = {alias.get(t["name"], t["name"]): {p["nickname"] for p in t["players"]}
                    for t in seed}

    # 1. 더 최근 대회
    newer, undated_siblings = newer_tournaments(
        client, meta["seriesPrefix"], meta["page"], meta.get("tournamentStart"))
    if newer:
        level = STALE
        for page, start in newer:
            findings.append("더 최근 대회: %s (시작 %s)" % (page, start))
    if undated_siblings:
        # 사람이 최신이라고 확인해 둔 대회는 더 묻지 않는다.
        confirmed = meta.get("latestConfirmedAt")
        if confirmed:
            findings.append("시작일이 없어 자동 판정은 못 하나 %s 에 사람이 최신으로 확인함"
                            % confirmed)
        else:
            level = WARN if level == OK else level
            findings.append("이 대회에 시작일이 없어 최신 여부를 자동 판정할 수 없다. "
                            "형제 문서: %s" % undated_siblings)

    # 2. 참가팀·로스터 변동
    try:
        live = live_rosters(client, meta["page"], meta.get("rostersFromHtml", False))
    except SystemExit as exc:
        findings.append("대조 실패: %s" % exc)
        return STALE, findings

    gone = sorted(set(seed_rosters) - set(live))
    # 시드가 문서 참가팀의 부분집합인 리그가 있다(PCL 은 40팀 중 Stage S 24팀).
    # 그런 리그에서 '위키에만 있는 팀'은 정상이다.
    added = [] if meta.get("subset") else sorted(set(live) - set(seed_rosters))
    changed = sorted(n for n in seed_rosters if n in live and seed_rosters[n] != live[n])

    if gone or added:
        level = STALE
        if gone:
            findings.append("시드에만 있는 팀 %d개: %s" % (len(gone), gone))
        if added:
            findings.append("위키에만 있는 팀 %d개: %s" % (len(added), added))
    if changed:
        level = STALE if level == STALE else WARN
        findings.append("로스터가 달라진 팀 %d개: %s" % (len(changed), changed))

    # 3. 대회 종료 후 재수집 여부
    end = meta.get("tournamentEnd")
    collected = meta.get("collectedAt")
    if end and collected:
        if collected < end <= today.isoformat():
            level = STALE
            findings.append("대회가 %s 에 끝났는데 수집은 %s 라 최종 명단이 아니다"
                            % (end, collected))
        elif end > today.isoformat():
            findings.append("대회 진행 중 (%s 종료 예정) — 종료 후 재수집 필요" % end)

    return level, findings


def main():
    use_utf8_output()
    ap = argparse.ArgumentParser(description="시드 최신성 점검 (읽기 전용)")
    ap.add_argument("--league", default=None, help="한 리그만 본다 (PTS 등)")
    ap.add_argument("--offline", action="store_true", help="캐시만 사용한다")
    args = ap.parse_args()

    client = MediaWikiClient(offline=args.offline)
    sources = load_sources()
    today = date.today()

    if args.league:
        key = args.league.upper()
        if key not in sources:
            raise SystemExit("모르는 리그: %s (가능: %s)" % (key, ", ".join(sources)))
        sources = {key: sources[key]}

    print("=== 시드 최신성 점검 (%s) ===\n" % today.isoformat())
    worst = OK
    for league, meta in sources.items():
        level, findings = check_league(client, league, meta, today)
        mark = {OK: "OK   ", WARN: "WARN ", STALE: "STALE"}[level]
        print("[%s] %-5s %s" % (mark, league, meta["page"]))
        for f in findings:
            print("        - %s" % f)
        if not findings:
            print("        - 위키와 동일")
        print()
        if level == STALE or (level == WARN and worst == OK):
            worst = level

    if worst == OK:
        print("점검한 %d개 리그 모두 최신입니다." % len(sources))
        return 0

    print("조치가 필요한 리그가 있습니다. 재수집 절차는 ingest/README.md 를 보세요.")
    print("STALE = 다시 수집해야 한다 / WARN = 대회 진행 중이라 예상된 변동일 수 있다")
    return 1


if __name__ == "__main__":
    sys.exit(main())
