"""
리그 시드 초안을 리퀴피디아 **MediaWiki API** 로 만든다. API 키가 필요 없다.

LPDB v3 를 쓰는 build_league_seed.py 와 같은 일을 하지만 승인 키 없이 동작한다.
현재 PWS 데이터도 이 경로로 수집됐다(scripts/59·63·65).

출력 스키마는 primary_data/pws2_teams_verified.json 과 동일하다. DataInitializer 가
그 형식만 읽기 때문이다.

  1) 구조 확인   python ingest/mediawiki_client.py "<문서명>" --what wikitext
  2) 초안 생성   python ingest/build_league_seed_mediawiki.py --page "<문서명>" \
                     --league PCL --region CN --seed-map ingest/seed_types_pcl.json \
                     --out intermediate_results/pcl_seed_draft.json
  3) 로고 받기   위 명령에 --download-logos 추가
  4) 검사        python ingest/verify_seed.py <초안> --compare-league PCL
  5) 사람이 원문과 대조한 뒤 primary_data/<리그>_teams_verified.json 으로 옮긴다

선수 세팅(mouseDpi·generalSens·mouseName)은 **넣지 않는다.** 리퀴피디아에 없는 값이다.
PWS 는 scripts/60 이 전원에게 800/32/동일 마우스를 일괄로 붙여서 지금도 가짜값이 남아 있다.
같은 실수를 반복하지 않는다.

트로피도 수집하지 않는다. 팀 문서의 1위 기록을 사람이 읽어 확인해야 한다(보고서 26·27).
"""

import argparse
import html as html_mod
import json
import re
import sys
import urllib.request
from pathlib import Path

from mediawiki_client import MediaWikiClient, use_utf8_output

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_DIR = PROJECT_ROOT / "frontend" / "public" / "logos" / "teams"

# 리퀴피디아 팀 코드 뒤에 붙는 동명이인 구분자. 약칭에는 들어가지 않는다.
DISAMBIGUATORS = {"cn", "kr", "eu", "na", "sea", "jp", "tw", "br"}


def code_to_tag(code):
    """
    '{{Opponent|jdg}}' 의 코드를 약칭으로 바꾼다.

    리퀴피디아에는 팀 약칭 필드가 없다(팀 문서 인포박스에도, Template: 에도 없음).
    그래서 내부 코드를 대문자로 올리고 구분자만 떼어 쓴다 — **추정값**이며
    실제 팀 약칭과 다를 수 있다. 시드의 tagSource 로 그 사실을 남긴다.
    """
    parts = code.strip().split()
    if len(parts) > 1 and parts[-1].lower() in DISAMBIGUATORS:
        parts = parts[:-1]
    return " ".join(parts).upper()


def clean_team_name(name):
    """
    리퀴피디아는 동명 팀을 문서명으로 구분한다 — 'ZEAL (Chinese team)'.
    화면에는 팀 이름만 쓰므로 그 접미사를 뗀다. scripts/60 이 PWS 에서
    ' (Korean team)' 에 대해 했던 것과 같은 처리다.
    """
    return re.sub(r"\s*\((?:[A-Za-z]+\s+)?team\)\s*$", "", name).strip()


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def parse_participants(wikitext, include_subs):
    """
    Participants 절에서 [(코드, [선수...])] 를 문서 등장 순서대로 뽑는다.

    구조:
      ==Participants==
      ===Stage S===
      {{TeamParticipants
      |{{Opponent|jdg
        |players={{Persons
          |{{Person|Dec12th|flag=cn}}
          |{{Person|Donzz|flag=cn|status=sub}}
          |{{Person|MiF|role=Coach|type=staff}}
      ...
    """
    m = re.search(r"==\s*Participants\s*==(.*?)(?=\n==[^=])", wikitext, re.S)
    if not m:
        raise SystemExit("Participants 절을 찾지 못했습니다. 문서 구조를 먼저 확인하세요.")
    section = m.group(1)

    entries = []
    # Opponent 블록의 시작 위치들을 잡고, 다음 블록 직전까지를 본문으로 본다.
    starts = [mm for mm in re.finditer(r"\{\{Opponent\|([^|\n}]+)", section)]
    for i, mm in enumerate(starts):
        code = mm.group(1).strip()
        end = starts[i + 1].start() if i + 1 < len(starts) else len(section)
        body = section[mm.end():end]

        players = []
        for pm in re.finditer(r"\{\{Person\|([^|}\n]+)([^}]*)\}\}", body):
            nick = pm.group(1).strip()
            attrs = pm.group(2)
            if "type=staff" in attrs or "role=Coach" in attrs:
                continue  # 코치·스태프 제외
            is_sub = "status=sub" in attrs
            if is_sub and not include_subs:
                continue
            players.append({"nickname": nick, "sub": is_sub})
        entries.append({"code": code, "players": players})
    return entries


def _full_size_image(src):
    """
    리퀴피디아가 주는 썸네일 URL 을 원본 URL 로 바꾼다.
      /commons/images/thumb/f/f0/17_Gaming_allmode.png/44px-17_Gaming_allmode.png
      -> /commons/images/f/f0/17_Gaming_allmode.png
    """
    if not src:
        return None
    m = re.match(r"(/commons/images/)thumb/(.+?\.(?:png|jpg|jpeg|gif|svg))/[^/]+$",
                 src, re.I)
    if m:
        src = m.group(1) + m.group(2)
    return "https://liquipedia.net" + src if src.startswith("/") else src


def fetch_team_display(client, page):
    """
    렌더된 HTML 의 Participants 영역에서 (정식 팀명, 로고 URL) 을 등장 순서대로 뽑는다.
    위키 원문은 내부 코드만 주므로 정식명은 여기서만 얻을 수 있다.

    카드 하나가 compact/full 두 번 렌더되므로 연속 중복을 접는다.
    HTML 엔티티가 섞여 있어(`&#95;` = `_`) 먼저 언이스케이프한다.
    """
    doc = html_mod.unescape(
        client.get({"action": "parse", "page": page, "prop": "text"})["parse"]["text"]["*"])

    m = re.search(r'id="Participants".*?(?=<h2)', doc, re.S)
    scope = m.group(0) if m else doc

    out = []
    for bm in re.finditer(r'class="block-team[^"]*"(.*?)</span></div>', scope, re.S):
        block = bm.group(1)
        am = re.search(r'<a href="/pubg/([^"]+)"[^>]*title="([^"]+)"', block)
        if not am:
            continue
        im = re.search(r'<img[^>]+src="([^"]+)"', block)
        entry = {
            "name": clean_team_name(am.group(2)),
            "page": am.group(1),
            "logo": _full_size_image(im.group(1) if im else None),
        }
        # 같은 팀이 바로 뒤에 다시 나오면(compact/full) 건너뛴다
        if out and out[-1]["page"] == entry["page"]:
            continue
        out.append(entry)
    return out


def download_logos(teams, contact):
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    ok, failed = [], []
    for t in teams:
        url, tag = t.get("_logoRemote"), t.get("tag")
        if not url or not tag:
            failed.append(t["name"])
            continue
        dest = LOGO_DIR / ("%s.png" % tag.lower().replace(" ", "_"))
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "PUBGProVault/1.0 (%s)" % contact})
            with urllib.request.urlopen(req, timeout=30) as resp:
                dest.write_bytes(resp.read())
            ok.append(dest.name)
        except Exception as e:
            failed.append("%s (%s)" % (t["name"], e))
    return ok, failed


def main():
    use_utf8_output()
    ap = argparse.ArgumentParser(description="MediaWiki 로 리그 시드 초안 생성")
    ap.add_argument("--page", required=True, help="리퀴피디아 대회 문서명")
    ap.add_argument("--league", required=True, help="시드에 기록할 리그 코드 (PCL 등)")
    ap.add_argument("--region", default=None, help="팀 지역 기본값 (CN 등)")
    ap.add_argument("--seed-map", default=None, help="팀명→seedType JSON")
    ap.add_argument("--include-subs", action="store_true",
                    help="status=sub 선수도 로스터에 넣는다 (코치는 항상 제외)")
    ap.add_argument("--download-logos", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    client = MediaWikiClient(offline=args.offline)

    wt = client.wikitext(args.page)
    entries = parse_participants(wt, args.include_subs)
    displays = fetch_team_display(client, args.page)

    print("위키 원문 Opponent %d개 / 렌더 HTML 팀 %d개" % (len(entries), len(displays)))
    if len(entries) != len(displays):
        raise SystemExit(
            "개수가 맞지 않아 코드↔정식명 대응을 신뢰할 수 없습니다.\n"
            "순서 대응 대신 다른 방법이 필요합니다. 진행을 멈춥니다.")

    # 순서 대응. 아래에서 seed-map 과 대조해 이름이 전부 맞는지 검증한다.
    for e, d in zip(entries, displays):
        e.update(d)

    seed_map = {}
    if args.seed_map:
        raw = json.loads(Path(args.seed_map).read_text(encoding="utf-8"))
        seed_map = {k: v for k, v in raw.items() if not k.startswith("_")}

    by_name = {e["name"]: e for e in entries}
    missing = [n for n in seed_map if n not in by_name]
    if missing:
        raise SystemExit(
            "seed-map 의 팀 %d개를 문서에서 찾지 못했습니다: %s\n"
            "표기가 다르거나 순서 대응이 어긋난 것입니다. 진행을 멈춥니다."
            % (len(missing), missing))

    targets = [by_name[n] for n in seed_map] if seed_map else entries

    teams = []
    for e in targets:
        tag = code_to_tag(e["code"])
        players = [{
            "nickname": p["nickname"],
            "realName": p["nickname"],   # 리퀴피디아 참가팀 표에는 본명이 없다
            "role": "Sub" if p["sub"] else "Player",
        } for p in e["players"]]

        teams.append({
            "id": slugify(e["name"]),
            "name": e["name"],
            "tag": tag,
            # tag 는 리퀴피디아 내부 코드에서 유도한 추정값이다. 팀 약칭 데이터가 없다.
            "tagSource": "liquipedia-opponent-code",
            "seedType": seed_map.get(e["name"]),
            "logoUrl": "/logos/teams/%s.png" % tag.lower().replace(" ", "_"),
            "league": args.league,
            "region": args.region or "",
            "trophies": [],              # 수집하지 않는다. 사람이 확인해서 채운다
            "players": players,
            "_logoRemote": e.get("logo"),
            "_liquipediaPage": e.get("page"),
        })

    if args.download_logos:
        ok, failed = download_logos(teams, client.contact)
        print("로고 저장 %d개" % len(ok))
        if failed:
            print("로고 실패 %d개: %s" % (len(failed), failed))
        for t in teams:
            if not (LOGO_DIR / Path(t["logoUrl"]).name).exists():
                t["logoUrl"] = ""   # 없으면 비운다. TeamCard 가 태그를 표시한다

    for t in teams:
        t.pop("_logoRemote", None)

    out = Path(args.out or (PROJECT_ROOT / "intermediate_results" /
                            ("%s_seed_draft.json" % args.league.lower())))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(teams, ensure_ascii=False, indent=2), encoding="utf-8")

    pro = sum(1 for t in teams if t["seedType"] == "pro")
    am = sum(1 for t in teams if t["seedType"] == "amateur")
    subs = sum(1 for t in teams for p in t["players"] if p["role"] == "Sub")
    print("초안 %d팀 (pro %d / amateur %d), 선수 %d명(교체 %d) → %s"
          % (len(teams), pro, am,
             sum(len(t["players"]) for t in teams), subs, out))
    print("\n다음: python ingest/verify_seed.py %s --compare-league %s" % (out, args.league))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
