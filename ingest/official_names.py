#!/usr/bin/env python3
"""
대회의 공식 이름을 붙인다.

  python ingest/official_names.py --check   # 바꾸지 않고 결과만 보여준다
  python ingest/official_names.py           # 집계 파일에 반영

## 왜 필요한가

공식 PUBG API 는 **대회 이름을 주지 않는다.** id 와 날짜뿐이다. 그래서 지금까지
화면에 "PGS 7" 처럼 id 의 번호를 그대로 썼는데, 그건 크래프톤 내부 번호이지
사람들이 부르는 이름이 아니다. 리퀴피디아는 같은 대회를
"PUBG Global Series 2026 Circuit 3 Series 1" 이라고 부른다.

## 어떻게 확인하나

리퀴피디아 문서 **제목이 곧 공식 이름**이다. 시리즈별 문서 목록을
`intermediate_results/liquipedia_pages.json` 에 받아 두고(allpages, 가벼운 호출),
우리 (시리즈·연도·회차)로 제목을 추측해 **그 목록에 실제로 있을 때만** 쓴다.
없으면 지금 이름을 그대로 둔다 — 지어내지 않는다.

리퀴피디아는 CC-BY-SA 3.0 이고 화면에 출처를 적는다.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "stage_label", Path(__file__).with_name("stage_label.py"))
stage_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage_label)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "primary_data" / "tournaments"
PAGES = PROJECT_ROOT / "intermediate_results" / "liquipedia_pages.json"

# 시리즈 -> 리퀴피디아 문서 접두사
BASE = {
    "PGS": "PUBG Global Series",
    "PGC": "PUBG Global Championship",
    "PNC": "PUBG Nations Cup",
    "EWC": "Esports World Cup",
    "PWS": "PUBG WEEKLY SERIES",
    "PCL": "PUBG Champions League",
    "EMEA": "PUBG EMEA Championship",
    "AMER": "PUBG Americas Series",
    "PTS": "PUBG Thailand Series",
    "PVS": "PUBG Vietnam Series",
}

# 단계 코드 앞글자로 시즌을 가르는 시리즈. EMEA 는 fp2=Fall, sp2=Spring 이다.
#
# **EMEA 에만 쓴다.** 날짜로 검증한 것이 EMEA 뿐이기 때문이다 (s* 는 전부 3~5월,
# f* 는 전부 8~10월, 2023~2026년 17단계가 예외 없이 맞는다). PCL 은 시즌이
# Spring·Summer·Autumn 넷이라 `s` 가 Spring 인지 Summer 인지 가릴 수 없다.
# 실제로 이 규칙을 PCL 에 쓰다가 **9월에 치른 cn-pclpo 가 "2022 Spring" 으로
# 찍혀 있었다.** 2019·2020·2022 PCL 이 다 그랬다.
SEASON_BY_SERIES = {"EMEA": {"f": "Fall", "s": "Spring"}}


def candidates(series, year, edition, codes):
    """그 대회일 법한 문서 제목들. 앞에 있는 것부터 본다."""
    base = BASE.get(series)
    if not base or not year:
        return []
    out = []

    if series == "PGS" and edition and edition.isdigit():
        # pgs1~pgs9 는 날짜상 3개씩 묶이고 매 3번째가 결승이다.
        # 위키는 Circuit 1~4 x (Series 1 / Series 2 / Series Final) 로 부른다.
        n = int(edition)
        circuit, pos = (n - 1) // 3 + 1, (n - 1) % 3 + 1
        tail = "Series Final" if pos == 3 else "Series %d" % pos
        out.append("%s/%d/Circuit %d/%s" % (base, year, circuit, tail))
        out.append("%s/%d/%s" % (base, year, edition))

    if edition:
        out.append("%s/%d/Phase %s" % (base, year, edition))
        out.append("%s/%d/%s" % (base, year, edition))

    # 시즌제(EMEA·PCL)는 단계 코드 앞글자가 시즌이다.
    #
    # **한 해에 시즌이 둘 이상 섞여 있으면 쓰지 않는다.** 우리는 (시리즈·연도·회차)
    # 로 묶는데 이 시리즈들은 회차가 없어서 Spring 과 Fall 이 한 덩어리가 된다.
    # 그대로 이름을 붙이면 Spring 단계에 "Fall" 이 찍힌다. 묶음을 시즌별로 가르는
    # 것이 제대로 된 해결이고, 그 전까지는 이름을 비워 둔다.
    by_prefix = SEASON_BY_SERIES.get(series)
    if by_prefix:
        # **모든 단계가 같은 시즌으로 읽힐 때만** 쓴다. 하나라도 읽히지 않으면
        # 그 단계가 다른 시즌일 수 있다 — 예전에는 읽히지 않는 코드를 그냥
        # 건너뛰어서, 한 단계만 s* 여도 묶음 전체에 Spring 이 찍혔다.
        seasons = {by_prefix.get(c[0]) if c else None for c in codes}
        if len(seasons) == 1 and None not in seasons:
            out.append("%s/%d/%s" % (base, year, seasons.pop()))

    # 연도 하나가 곧 대회인 시리즈 (PGC·PNC·EWC)
    out.append("%s/%d" % (base, year))
    return out


def official_name(title):
    """문서 제목을 화면용 이름으로. 'A/2026/Circuit 3/Series 1' -> 'A 2026 Circuit 3 Series 1'"""
    return title.replace("/", " ")


def main():
    ap = argparse.ArgumentParser(description="대회에 공식 이름 붙이기")
    ap.add_argument("--check", action="store_true", help="바꾸지 않고 보여만 준다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    if not PAGES.is_file():
        raise SystemExit(
            "%s 가 없습니다. 리퀴피디아 문서 목록을 먼저 받아야 합니다." % PAGES)
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    known = {s: set(v) for s, v in pages.items()}

    docs = []
    groups = {}
    for f in sorted(OUT_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        docs.append((f, d))
        groups.setdefault((d.get("series"), d.get("year"), d.get("edition")),
                          []).append(d)

    resolved = {}
    for key, members in groups.items():
        series, year, edition = key
        codes = [m.get("stageCode") or "" for m in members]
        for title in candidates(series, year, edition, codes):
            if title in known.get(series, ()):
                resolved[key] = title
                break

    hit = len(resolved)
    print("공식 이름을 찾은 대회: %d / %d" % (hit, len(groups)))
    for key in sorted(resolved, key=lambda k: (k[0], -(k[1] or 0), str(k[2]))):
        print("   %-5s %s %-5s -> %s" % (key[0], key[1], key[2], resolved[key]))

    missing = [k for k in groups if k not in resolved]
    if missing:
        print("\n못 찾은 대회 %d개 (지금 이름 유지):" % len(missing))
        for k in sorted(missing, key=lambda k: (k[0], -(k[1] or 0), str(k[2])))[:20]:
            print("   %-5s %s 회차=%s" % (k[0], k[1], k[2]))

    if args.check:
        return 0

    changed = cleared = 0
    for f, d in docs:
        key = (d.get("series"), d.get("year"), d.get("edition"))
        title = resolved.get(key)
        if not title:
            # 전에 붙였던 이름이 지금 규칙으로는 안 나오면 **지운다.**
            # 그대로 두면 틀린 이름이 영원히 남는다 (PCL 의 가짜 "Spring").
            if d.get("officialName"):
                d.pop("officialName", None)
                d["name"] = stage_label.display_name(d["id"], d.get("year"))
                f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + chr(10),
                             encoding="utf-8")
                cleared += 1
            continue
        name = official_name(title)
        # 단계 이름이 있으면 뒤에 붙인다: "... Circuit 3 Series 1 Final Stage"
        if d.get("stage"):
            name = "%s %s" % (name, d["stage"])
        if d.get("officialName") != title or d.get("name") != name:
            d["officialName"] = title
            d["name"] = name
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
            changed += 1
    print("\n이름을 바꾼 단계: %d · 틀린 이름을 지운 단계: %d" % (changed, cleared))
    return 0


if __name__ == "__main__":
    sys.exit(main())
