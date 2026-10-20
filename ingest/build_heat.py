#!/usr/bin/env python3
"""
히트엔딩 집계 — **여러 경기를 모아 맵마다 어디가 중요한지** 센다.

  python ingest/build_heat.py            # 전부
  python ingest/build_heat.py --check    # 쓰지 않고 결과만 보여준다

`primary_data/heat/<맵>.json` 을 만든다. 네트워크를 쓰지 않는다 — 이미 뽑아 둔
매치로그만 읽는다.

## 무엇을 세나

한 경기 복기는 매치로그가 한다. 여기서 보려는 것은 **한 경기로는 안 보이는
것**이다. 세 가지를 맵 격자에 쌓는다.

- `ending`  마지막 자기장의 중심. "이 맵은 어디서 끝나는가"
- `landing` 착지 지점. "어디로 내리는가"
- `death`   사망 지점. "어디서 죽는가"

## 지어내지 않는 것

- 지명을 붙이지 않는다. 우리에게 지명 데이터가 없다. 좌표는 지도 위에 그대로
  찍고, 사람이 지도를 보고 읽는다
- 표본 수를 같이 적는다. 비켄디 15경기와 에란겔 1,198경기를 같은 무게로
  보여 주면 거짓이 된다. 화면에서도 경기 수를 같이 띄운다
- **우리가 가진 매치로그만 센다.** 전체 프로 경기가 아니다
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "primary_data" / "matchlogs"
OUT_DIR = PROJECT_ROOT / "primary_data" / "heat"

# 격자 한 변. 8km 맵이면 한 칸이 160m 로, 교전 한 판이 들어가는 크기다.
GRID = 50
# 표본이 이보다 적은 맵은 내보내지 않는다. 몇 경기로 "이 맵은 여기서 끝난다"
# 고 말할 수 없다.
MIN_MATCHES = 20

# 이름이 겹치거나 지도 그림이 없는 맵. (화면 이름, 쓸 그림, 덧붙일 말)
#
# `Erangel_Main` 은 2019~2020년 에란겔의 옛 내부 이름이고 지금은 `Baltic_Main`
# 이다. 둘 다 "Erangel" 로 내보내면 화면에 같은 이름이 둘 나온다. **합치지는
# 않는다** — 리마스터로 지형이 달라졌으니 한 덩어리로 세면 거짓이 된다.
# 옛 맵 그림은 우리에게 없어서 현재판을 쓰되, 다르다는 것을 화면에 적는다.
ALIASES = {
    "Erangel_Main": ("Erangel (2019~2020)", "Baltic_Main",
                     "리마스터 전 에란겔입니다. 지도 그림은 현재판이라 지형이 조금 다릅니다."),
}


def cell(v):
    return min(GRID - 1, max(0, int(v * GRID)))


def main():
    ap = argparse.ArgumentParser(description="히트엔딩 집계")
    ap.add_argument("--check", action="store_true", help="쓰지 않고 보여만 준다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    maps = defaultdict(lambda: {
        "label": None, "matches": 0, "stages": set(),
        "ending": Counter(), "landing": Counter(), "death": Counter(),
        "endPoints": [],
    })

    files = [f for f in LOG_DIR.glob("*/*.json") if not f.name.startswith("_")]
    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        key = d.get("map")
        if not key:
            continue
        m = maps[key]
        m["label"] = d.get("mapLabel") or key
        m["matches"] += 1
        m["stages"].add(f.parent.name)

        # 마지막 자기장 = 경기가 끝난 자리. 반지름이 0 인 기록은 버린다.
        circles = [c for c in (d.get("circles") or []) if c.get("r")]
        if circles:
            last = circles[-1]
            m["ending"][(cell(last["x"]), cell(last["y"]))] += 1
            m["endPoints"].append((round(last["x"], 4), round(last["y"], 4)))

        for l in d.get("landings") or []:
            m["landing"][(cell(l["x"]), cell(l["y"]))] += 1
        for k in d.get("kills") or []:
            if k.get("x") is not None:
                m["death"][(cell(k["x"]), cell(k["y"]))] += 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for key, m in sorted(maps.items(), key=lambda kv: -kv[1]["matches"]):
        enough = m["matches"] >= MIN_MATCHES
        print("%-14s %-9s %5d경기 · 단계 %3d · 착지 %6d · 사망 %6d %s" % (
            key, m["label"], m["matches"], len(m["stages"]),
            sum(m["landing"].values()), sum(m["death"].values()),
            "" if enough else "← 표본이 적어 건너뜀"))
        if not enough or args.check:
            continue

        # 경기 수가 맵마다 다르므로 **경기당 값**도 같이 준다. 화면에서 맵을
        # 바꿔도 색이 같은 뜻을 갖게 하려는 것이다.
        label, image, note = ALIASES.get(key, (m["label"], key, None))
        doc = {
            "map": key,
            "mapLabel": label,
            # 그림 파일 이름. 보통 맵 이름과 같지만 옛 맵은 현재판을 빌려 쓴다.
            "image": image,
            "mapNote": note,
            "matches": m["matches"],
            "stages": len(m["stages"]),
            "grid": GRID,
            "note": "우리가 뽑아 둔 매치로그만 센 값이다. 전체 프로 경기가 아니다.",
            "layers": {
                name: {
                    "max": max(c.values()) if c else 0,
                    "total": sum(c.values()),
                    # **동점끼리도 순서를 고정한다.** 안 그러면 돌릴 때마다
                    # 파일이 달라져, 새 경기가 하나도 없는데도 다섯 시간마다
                    # 커밋이 쌓인다 (실제로 그랬다).
                    "cells": [[i, j, n] for (i, j), n in
                              sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))],
                } for name, c in (("ending", m["ending"]),
                                  ("landing", m["landing"]),
                                  ("death", m["death"]))
            },
            "endPoints": sorted(m["endPoints"]),
        }
        (OUT_DIR / ("%s.json" % key)).write_text(
            json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + chr(10),
            encoding="utf-8")
        written += 1

    print("\n내보낸 맵 %d (최소 %d경기)" % (written, MIN_MATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
