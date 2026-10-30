#!/usr/bin/env python3
"""
히트엔딩 집계 — **여러 경기를 모아 맵마다 어디가 중요한지** 센다.

  python ingest/build_heat.py            # 전부
  python ingest/build_heat.py --check    # 쓰지 않고 결과만 보여준다

`primary_data/heat/<맵>.json` 을 만든다. 네트워크를 쓰지 않는다 — 이미 뽑아 둔
매치로그와 경쟁전 자기장만 읽는다.

## 자기장 개편 이후만 센다 (2026-06-17, 업데이트 42.1)

**섞으면 어느 쪽도 아닌 평균이 된다.** 그날 경쟁전·이스포츠에 "안전 구역
위치 보정 강도 완화"가 들어갔는데, 그게 바로 이 화면이 재는 값이다.
예전에는 2019~2026 여덟 해를 한 덩어리로 세어 표본 수(2,978경기)만 커 보이고
뜻은 없었다. 이제 **개편 이후만** 담는다.

## 출처를 가른다

| 출처 | 무엇 | 담는 층 |
|---|---|---|
| `esports` | 프로 대회 (우리 매치로그) | 엔딩·낙하·사망·자기장 |
| `competitive` | 공개 경쟁전 (`ingest/collect_ranked_zones.py`) | 엔딩·자기장 |

**둘은 자기장 설정이 같다** (개발일지 "블루존 개편", pubg.com/ko/news/10280).
그래도 **합쳐서 한 숫자로 보여주지 않는다** — 출처가 다르면 갈라서 보여주는
것이 맞다. 일반전은 애초에 받지 않는다. 일반전만 따로 조정됐기 때문이다.

경쟁전에는 낙하·사망이 없다. 자기장만 뽑아 왔기 때문이다(경기당 2KB).

## 무엇을 세나

- `ending`  마지막 자기장의 중심. "이 맵은 어디서 끝나는가"
- `landing` 착지 지점. "어디로 내리는가"
- `death`   사망 지점. "어디서 죽는가"
- `zones`   **페이즈마다 그 칸이 자기장 안에 든 경기 수.** 사용자가 처음 말한
            "지형 중 어느 부분이 서클에 많이 걸치는가" 가 이것이다. 마지막 한
            점만 보는 `ending` 과 다른 질문이고, 페이즈를 넘기면 그대로 서클이
            줄어드는 모습이 된다

## 지어내지 않는 것

- 지명을 붙이지 않는다. 우리에게 지명 데이터가 없다
- 출처마다 경기 수를 적는다. 표본이 20경기에 못 미치면 내보내지 않는다
- 페이즈마다 **몇 경기가 기여했는지**를 같이 적는다 — 뒤로 갈수록 일찍 끝난
  경기가 빠지는데, 그걸 안 보여주면 "P8 은 표본이 적다"는 것이 숨는다
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "primary_data" / "matchlogs"
RANKED_DIR = PROJECT_ROOT / "primary_data" / "ranked_zones"
TOURNEY_DIR = PROJECT_ROOT / "primary_data" / "tournaments"
OUT_DIR = PROJECT_ROOT / "primary_data" / "heat"

# 자기장 개편일. 이 날부터의 경기만 센다.
REWORK = "2026-06-17"

# 점 밀도 격자 한 변. 8km 맵이면 한 칸이 160m 로, 교전 한 판이 들어가는 크기다.
GRID = 50

# 자기장 층만 더 곱게 센다. 50칸으로는 가장자리가 계단처럼 보인다.
# 희소 목록이 아니라 **빽빽한 배열**로 담으므로 100칸이어도 페이즈당 1만 개
# 정수면 된다.
ZONE_GRID = 100

# 담을 페이즈 수. P1 은 지도 전체라 뜻이 없어 빼고 P2 부터 담는다.
MAX_PHASE = 9

# 출처마다 이보다 적으면 내보내지 않는다. 몇 경기로 "이 맵은 여기서
# 끝난다"고 말할 수 없다.
MIN_MATCHES = 20

# 이름이 겹치거나 지도 그림이 없는 맵. (화면 이름, 쓸 그림, 덧붙일 말)
ALIASES = {
    "Erangel_Main": ("Erangel (2019~2020)", "Baltic_Main",
                     "리마스터 전 에란겔입니다. 지도 그림은 현재판이라 지형이 조금 다릅니다."),
}


def cell(v, g):
    return min(g - 1, max(0, int(v * g)))


def new_bucket():
    return {
        "label": None, "matches": 0, "stages": set(),
        "ending": Counter(), "landing": Counter(), "death": Counter(),
        "endPoints": [],
        "zones": defaultdict(lambda: [np.zeros((ZONE_GRID, ZONE_GRID), dtype=np.int32), 0]),
    }


def phases_from(circles):
    """반경이 줄다 멈추는 순간이 다음 구역 예고다."""
    if not circles:
        return []
    out = [circles[0]]
    shrinking = False
    for a, b in zip(circles, circles[1:]):
        if b["r"] < a["r"] - 1e-9:
            shrinking = True
        elif shrinking:
            out.append(b)
            shrinking = False
    return out


def add_zones(bucket, phases, gx, gy):
    # **첫 원은 건너뛴다.** phases[0] 은 경기 시작 때의 지도 전체(반지름 0.71)라
    # 모든 칸이 100%가 되어 뜻이 없다. 이걸 P2 로 세는 바람에 지도가 통째로
    # 빨갛게 나왔다. 두 출처 모두 phases[0] = P1 이라 규칙이 같다.
    for k, c in enumerate(phases[1:MAX_PHASE], start=2):
        inside = (gx - c["x"]) ** 2 + (gy - c["y"]) ** 2 <= c["r"] ** 2
        z = bucket["zones"][k]
        z[0] += inside
        z[1] += 1


def stage_dates():
    """단계 -> 시작일. 경기에 startedAt 이 없는 옛 로그를 위한 대비책."""
    out = {}
    for f in TOURNEY_DIR.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        out[d.get("id")] = d.get("startDate")
    return out


def main():
    ap = argparse.ArgumentParser(description="히트엔딩 집계")
    ap.add_argument("--check", action="store_true", help="쓰지 않고 보여만 준다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    az = (np.arange(ZONE_GRID) + 0.5) / ZONE_GRID
    gx, gy = np.meshgrid(az, az, indexing="ij")

    # 맵 -> 출처 -> 바구니
    maps = defaultdict(lambda: defaultdict(new_bucket))
    sdates = stage_dates()

    # 1. 이스포츠 — 우리 매치로그. 개편 이후만.
    skipped_old = 0
    for f in LOG_DIR.glob("*/*.json"):
        if f.name.startswith("_"):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        key = d.get("map")
        if not key:
            continue
        when = (d.get("startedAt") or sdates.get(f.parent.name) or "")[:10]
        if not when or when < REWORK:
            skipped_old += 1
            continue

        m = maps[key]["esports"]
        m["label"] = d.get("mapLabel") or key
        m["matches"] += 1
        m["stages"].add(f.parent.name)

        circles = [c for c in (d.get("circles") or []) if c.get("r")]
        if circles:
            last = circles[-1]
            m["ending"][(cell(last["x"], GRID), cell(last["y"], GRID))] += 1
            m["endPoints"].append((round(last["x"], 4), round(last["y"], 4)))
        add_zones(m, phases_from(circles), gx, gy)

        for l in d.get("landings") or []:
            m["landing"][(cell(l["x"], GRID), cell(l["y"], GRID))] += 1
        for k in d.get("kills") or []:
            if k.get("x") is not None:
                m["death"][(cell(k["x"], GRID), cell(k["y"], GRID))] += 1

    # 2. 경쟁전 — 자기장만 뽑아 둔 것. 애초에 개편 이후뿐이다
    #    (공식 API 가 최근 14일만 보관한다).
    for f in RANKED_DIR.glob("*/*.json"):
        if f.name.startswith("_"):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        key = d.get("map")
        if not key or (d.get("createdAt") or "")[:10] < REWORK:
            continue
        m = maps[key]["competitive"]
        m["label"] = d.get("mapLabel") or key
        m["matches"] += 1
        ph = d.get("phases") or []
        if ph:
            last = ph[-1]
            m["ending"][(cell(last["x"], GRID), cell(last["y"], GRID))] += 1
            m["endPoints"].append((round(last["x"], 4), round(last["y"], 4)))
        add_zones(m, ph, gx, gy)

    print("개편(%s) 이전이라 건너뛴 이스포츠 경기: %d\n" % (REWORK, skipped_old))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for key in sorted(maps, key=lambda k: -sum(b["matches"] for b in maps[k].values())):
        srcs = maps[key]
        label, image, note = ALIASES.get(key, (None, key, None))
        label = label or next((b["label"] for b in srcs.values() if b["label"]), key)

        kept = {}
        line = []
        for name in ("esports", "competitive"):
            b = srcs.get(name)
            n = b["matches"] if b else 0
            line.append("%s %d%s" % (name, n, "" if n >= MIN_MATCHES else "(적음)"))
            if not b or n < MIN_MATCHES:
                continue
            kept[name] = {
                "matches": n,
                "stages": len(b["stages"]),
                "layers": {
                    lname: {
                        "max": max(c.values()) if c else 0,
                        "total": sum(c.values()),
                        "cells": [[i, j, v] for (i, j), v in
                                  sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))],
                    } for lname, c in (("ending", b["ending"]),
                                       ("landing", b["landing"]),
                                       ("death", b["death"])) if c
                },
                "endPoints": sorted(b["endPoints"]),
                "zones": [
                    {
                        "phase": k,
                        "matches": b["zones"][k][1],
                        "max": int(b["zones"][k][0].max()),
                        "top": sorted(
                            ([int(i), int(j), int(b["zones"][k][0][i, j])]
                             for i, j in zip(*np.nonzero(b["zones"][k][0]))),
                            key=lambda c: (-c[2], c[0], c[1]))[:200],
                        "counts": b["zones"][k][0].ravel(order="C").tolist(),
                    }
                    for k in sorted(b["zones"])
                ],
            }

        print("%-14s %-9s  %s" % (key, label, " · ".join(line)))
        if not kept or args.check:
            continue

        doc = {
            "map": key,
            "mapLabel": label,
            "image": image,
            "mapNote": note,
            "grid": GRID,
            "zoneGrid": ZONE_GRID,
            "since": REWORK,
            "note": "2026-06-17 자기장 개편 이후 경기만 셉니다. 그 전과는 안전 구역 "
                    "위치 보정이 달라 섞을 수 없습니다.",
            "sources": kept,
        }
        (OUT_DIR / ("%s.json" % key)).write_text(
            json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + chr(10),
            encoding="utf-8")
        written += 1

    print("\n내보낸 맵 %d (출처마다 최소 %d경기)" % (written, MIN_MATCHES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
