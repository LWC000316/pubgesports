#!/usr/bin/env python3
"""
사람이 정리한 장비 파일을 시드에 넣는다.

장비는 자동 수집 경로가 없다. 리퀴피디아에도, 공식 API 에도, 감도 시트에도 없다.
선수가 자기 방송국 게시판이나 유튜브 설명란에 올린 글을 사람이 읽어 옮겨 적는다.
그 결과물이 `ingest/*_gear_*.json` 이고 이 스크립트가 시드에 반영한다.

**출처와 기준일을 반드시 같이 넣는다.** 장비는 감도보다 자주 바뀌고 출처끼리
어긋난다 — Salute 는 유튜브 설명과 SOOP 공지의 마우스·키보드·패드·헤드셋이
전부 달랐다. 어디서 언제 가져왔는지가 없으면 나중에 되짚을 수 없다.

    python ingest/apply_gear.py ingest/pws_gear_2026_09_30.json --dry-run
    python ingest/apply_gear.py ingest/pws_gear_2026_09_30.json
    cd backend && SEED_MODE=always ./gradlew bootRun
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 화면이 항상 보여주는 다섯 칸. 그 외 카테고리는 값이 있을 때만 덧붙는다.
KNOWN = {"MOUSE", "MOUSEPAD", "KEYBOARD", "HEADSET", "MONITOR",
         "EARPHONE", "DAC", "MIC", "MOUSEFEET", "ARMSLEEVE"}


def main():
    ap = argparse.ArgumentParser(description="장비 파일을 시드에 반영")
    ap.add_argument("gearfile")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    doc = json.loads(Path(args.gearfile).read_text(encoding="utf-8"))
    entries = doc["players"]

    seeds = {}
    for path in sorted(PROJECT_ROOT.glob("primary_data/*_teams_verified.json")):
        seeds[path] = json.loads(path.read_text(encoding="utf-8"))

    touched, applied, missing, unknown_cat = set(), [], [], set()

    for entry in entries:
        found = None
        for path, teams in seeds.items():
            for team in teams:
                if team.get("league") != entry["league"] or team["name"] != entry["team"]:
                    continue
                for player in team.get("players", []):
                    if player["nickname"] == entry["nickname"]:
                        found = (path, player)
        if not found:
            missing.append("%s / %s / %s" % (entry["league"], entry["team"], entry["nickname"]))
            continue

        path, player = found
        gears = []
        for g in entry["gears"]:
            cat = g["category"].upper()
            if cat not in KNOWN:
                unknown_cat.add(cat)
            item = {"category": cat, "name": g["name"]}
            if g.get("brand"):
                item["brand"] = g["brand"]
            # 출처는 장비 항목마다 붙인다. 한 선수의 장비를 여러 글에서 모을 수 있다.
            item["sourceUrl"] = entry["sourceUrl"]
            item["collectedAt"] = entry["collectedAt"]
            gears.append(item)
        player["gears"] = gears
        touched.add(path)
        applied.append((entry["nickname"], entry["team"], len(gears), entry["collectedAt"]))

    print("반영 %d명 / 시드에서 못 찾음 %d명" % (len(applied), len(missing)))
    for nick, team, n, when in applied:
        print("  %-10s %-16s 장비 %2d종  기준 %s" % (nick, team, n, when))
    if missing:
        print("\n못 찾은 선수:")
        for m in missing:
            print("  %s" % m)
    if unknown_cat:
        print("\n처음 보는 카테고리(화면에 덧붙어 나온다): %s" % sorted(unknown_cat))

    if args.dry_run:
        print("\n--dry-run 이라 파일을 쓰지 않았습니다.")
        return 0

    for path in sorted(touched):
        path.write_text(json.dumps(seeds[path], ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print("기록: %s" % path.relative_to(PROJECT_ROOT))

    print("\n다음: cd backend && SEED_MODE=always ./gradlew bootRun")
    return 0


if __name__ == "__main__":
    sys.exit(main())
