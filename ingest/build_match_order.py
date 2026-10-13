#!/usr/bin/env python3
"""
매치로그가 있는 단계마다 **경기 순서**를 적어 둔다.

  python ingest/build_match_order.py            # 전부
  python ingest/build_match_order.py as-pgs9gf  # 한 단계만

`primary_data/matchlogs/<단계>/_order.json` 을 만든다.

## 왜 필요한가

매치로그 파일 이름은 경기 UUID 라 **정렬해도 경기 순서가 아니다.** 화면에서는
"1경기 2경기 …" 로 보여 주는데, 실제로 PGS 9 결승의 `15b203fc` 는 8/23 마지막
경기인데도 UUID 순으로는 맨 앞이라 "1경기" 로 찍혀 있었다.

순서는 공식 API 의 경기 `createdAt` 에만 있다. 텔레메트리에는 경기 시작 절대
시각이 있지만(LogMatchStart) 이미 뽑아 둔 2,487 경기에는 안 적혀 있다. 그래서
**받아 둔 원본이 아직 있을 때** 순서를 따로 적어 둔다 — 원본은 곧 버려진다
(서버는 아예 보관하지 않는다).

원본이 없는 단계는 건너뛴다. 그 단계는 다음 수집 때 적힌다.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "primary_data" / "matchlogs"
RAW_DIR = PROJECT_ROOT / "intermediate_results" / "tournaments"
AGG_DIR = PROJECT_ROOT / "primary_data" / "tournaments"


def load(path):
    # PowerShell 의 Set-Content -Encoding UTF8 은 BOM 을 붙인다.
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build(stage_dir):
    """(적은 경기 수, 건너뛴 이유). 이유가 None 이면 성공."""
    raw = RAW_DIR / stage_dir.name
    if not raw.is_dir():
        return 0, "원본 없음"

    have = {f.stem for f in stage_dir.glob("*.json") if not f.name.startswith("_")}
    rows = []
    for f in raw.glob("match_*.json"):
        try:
            d = load(f)
        except (ValueError, OSError):
            continue
        mid = d.get("data", {}).get("id")
        attr = d.get("data", {}).get("attributes") or {}
        if mid in have and attr.get("createdAt"):
            rows.append({"id": mid, "startedAt": attr["createdAt"],
                         "map": attr.get("mapName")})
    if not rows:
        return 0, "원본에 경기 시각이 없음"

    rows.sort(key=lambda r: r["startedAt"])
    fix_dates(stage_dir.name, rows)
    missing = have - {r["id"] for r in rows}
    out = {"matches": rows}
    if missing:
        # 일부만 아는 순서는 "1경기" 라는 번호를 거짓으로 만든다. 사실만 적는다.
        out["unordered"] = sorted(missing)
    (stage_dir / "_order.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(rows), None


def fix_dates(stage_id, rows):
    """집계 파일의 대회 날짜를 **실제 첫·마지막 경기 날짜**로 맞춘다.

    `build_tournament_seed.py` 가 오래도록 경기 파일을 **이름(UUID) 순**으로
    정렬해 그 첫 번째의 날짜를 시작일로 썼다. 아무 경기나 된다는 뜻이다 —
    PVS 2026 Phase 1 은 4/10 시작인데 4/19 로 적혀 있었다. 빌더는 고쳤지만
    서버가 만든 집계는 원본이 없어 다시 만들 수 없으므로 여기서 고친다.
    """
    f = AGG_DIR / ("%s.json" % stage_id)
    if not f.is_file():
        return
    d = json.loads(f.read_text(encoding="utf-8"))
    start, end = rows[0]["startedAt"][:10], rows[-1]["startedAt"][:10]
    # 매치로그가 그 단계의 일부만 있을 수 있다. 그때는 범위를 좁히지 않는다.
    if len(rows) < (d.get("matchCount") or 0):
        return
    if d.get("startDate") == start and d.get("endDate") == end:
        return
    d["startDate"], d["endDate"] = start, end
    f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + chr(10),
                 encoding="utf-8")


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    only = sys.argv[1:]
    stages = sorted(d for d in LOG_DIR.iterdir() if d.is_dir())
    if only:
        stages = [d for d in stages if d.name in only]

    done = skipped = 0
    reasons = {}
    for d in stages:
        n, why = build(d)
        if why:
            skipped += 1
            reasons[why] = reasons.get(why, 0) + 1
        else:
            done += 1
            print("   %-14s %d 경기" % (d.name, n))

    print("\n순서를 적은 단계 %d · 건너뜀 %d" % (done, skipped))
    for why, n in sorted(reasons.items()):
        print("   %s: %d" % (why, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
