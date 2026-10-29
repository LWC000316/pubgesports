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
- `zones`   **페이즈마다 그 칸이 자기장 안에 든 경기 수.** 사용자가 처음
            말한 "지형 중 어느 부분이 서클에 많이 걸치는가" 가 이것이다.
            마지막 한 점만 보는 `ending` 과 다른 질문이고, 페이즈를 넘기면
            그대로 서클이 줄어드는 모습이 된다.

P1 은 지도 전체라 뜻이 없어 빼고 P2 부터 담는다. 경기마다 페이즈 수가
달라서(보통 8~9) 페이즈별로 **몇 경기가 기여했는지**를 같이 적는다 —
안 그러면 뒤쪽 페이즈가 표본이 적다는 것이 숨는다.

## 언제 경기인지 반드시 가른다

**섞으면 어느 쪽도 아닌 평균이 된다.** 우리 매치로그는 2019~2026 여덟 해에
걸쳐 있는데 그 사이 자기장 규칙과 맵이 여러 번 바뀌었다. 8년치를 한 덩어리로
세면 표본 수(2,978경기)만 커 보이고 뜻은 없다.

그래서 **구간마다 따로 센다** (`PERIODS`). 기본은 최근 2년이고, 전체도 함께
담아 화면에서 고르게 한다. 맵마다 구간별 경기 수를 적으므로, 그 구간에
경기가 없는 맵(비켄디는 2024년이, 사녹은 2020년이 마지막이다)은 화면에서
아예 빠진다.

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

import numpy as np
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "primary_data" / "matchlogs"
OUT_DIR = PROJECT_ROOT / "primary_data" / "heat"

# 격자 한 변. 8km 맵이면 한 칸이 160m 로, 교전 한 판이 들어가는 크기다.
GRID = 50

# 자기장 층만 더 곱게 센다. 50칸으로는 가장자리가 계단처럼 보인다.
# 희소 목록([i,j,n])이 아니라 **빽빽한 배열**로 담으므로 100칸이어도
# 페이즈당 1만 개 정수면 된다 (맵당 8페이즈, 약 200KB).
ZONE_GRID = 100

# 집계 구간. (키, 화면 이름, 시작연도, 끝연도). None 이면 제한 없음.
# **최근 2년이 기본**이다 — 지금 통하는 규칙이 그것이기 때문이다.
PERIODS = [
    ("recent", "2025~26", 2025, None),
    ("all", "전체 (2019~)", None, None),
]
# 표본이 이보다 적은 맵은 내보내지 않는다. 몇 경기로 "이 맵은 여기서 끝난다"
# 고 말할 수 없다.
MIN_MATCHES = 20

# 담을 페이즈 수. P1 은 지도 전체라 빼고, 뒤쪽은 표본이 급격히 준다.
MAX_PHASE = 9

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

    # 칸 중심 좌표. 자기장 안인지 한 번에 재려고 미리 만들어 둔다.
    az = (np.arange(ZONE_GRID) + 0.5) / ZONE_GRID
    gx, gy = np.meshgrid(az, az, indexing="ij")

    maps = defaultdict(lambda: {
        "label": None, "matches": 0, "stages": set(),
        "ending": Counter(), "landing": Counter(), "death": Counter(),
        "endPoints": [],
        # 페이즈 -> (칸별 누적, 기여 경기 수)
        "zones": defaultdict(
            lambda: [np.zeros((ZONE_GRID, ZONE_GRID), dtype=np.int32), 0]),
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

        # 페이즈마다 자기장 안에 든 칸을 센다. 페이즈는 반경이 줄다 멈추는
        # 순간부터다 (`derivePhases` 와 같은 규칙).
        phases, shrinking = [], False
        for a, b in zip(circles, circles[1:]):
            if b["r"] < a["r"] - 1e-9:
                shrinking = True
            elif shrinking:
                phases.append(b)
                shrinking = False
        for k, c in enumerate(phases[:MAX_PHASE - 1], start=2):
            inside = (gx - c["x"]) ** 2 + (gy - c["y"]) ** 2 <= c["r"] ** 2
            z = m["zones"][k]
            z[0] += inside
            z[1] += 1

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
            # 페이즈별 자기장 포함 빈도. 0 인 칸은 빼서 파일을 줄인다.
            "zoneGrid": ZONE_GRID,
            # **빽빽한 배열로 담는다.** [i,j,n] 세 쌍으로 담으면 값이 있는 칸이
            # 1만 개에 가까워 파일이 세 배가 된다. 행 우선으로 편 정수 배열이면
            # 그대로 격자가 되고 화면에서 바로 쓴다.
            "zones": [
                {
                    "phase": k,
                    "matches": m["zones"][k][1],
                    "max": int(m["zones"][k][0].max()),
                    # 가장 잦은 칸 다섯 — 화면 목록에 쓴다 (좌표로 동점 고정).
                    "top": sorted(
                        ([int(i), int(j), int(m["zones"][k][0][i, j])]
                         for i, j in zip(*np.nonzero(m["zones"][k][0]))),
                        key=lambda c: (-c[2], c[0], c[1]))[:200],
                    "counts": m["zones"][k][0].ravel(order="C").tolist(),
                }
                for k in sorted(m["zones"])
            ],
        }
        (OUT_DIR / ("%s.json" % key)).write_text(
            json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + chr(10),
            encoding="utf-8")
        written += 1

    print("\n내보낸 맵 %d (최소 %d경기)" % (written, MIN_MATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
