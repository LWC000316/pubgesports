#!/usr/bin/env python3
"""
이미 만들어진 대회 집계 파일의 OVERALL 만 다시 계산한다.

  python ingest/rescore_overall.py          # 전부
  python ingest/rescore_overall.py --check  # 바꾸지 않고 결과만 보여준다

## 왜 따로 있나

`build_all.py` 는 **경기 원본이 있는 단계만** 다시 만든다. 그런데 서버(GitHub
Actions)는 원본을 보관하지 않으므로, 서버가 만든 단계는 로컬에서 다시 만들 수 없다.
OVERALL 계산식을 고치면 그 단계들만 옛 값으로 남는다.

다행히 OVERALL 에 필요한 값(경기 수·킬·기절·평균 데미지·평균 생존)이 집계 파일
안에 이미 다 있다. 그래서 원본 없이 집계 파일만 보고 다시 매길 수 있다.

계산식 자체는 `build_tournament_seed.py` 의 것을 그대로 쓴다 — 두 벌로 두면
어긋난다.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "primary_data" / "tournaments"

_spec = importlib.util.spec_from_file_location(
    "bts", Path(__file__).with_name("build_tournament_seed.py"))
bts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bts)


def rescore(doc):
    """(바뀐 선수 수, 배틀로얄 여부). doc 을 제자리에서 고친다."""
    players = doc.get("players") or []
    if not players:
        return 0, True

    survivals = sorted(p["avgSurvival"] for p in players)
    played = sorted(p["matches"] for p in players)
    median_survival = survivals[len(survivals) // 2]
    median_matches = played[len(played) // 2] or 1
    is_br = median_survival >= bts.BR_MIN_MEDIAN_SURVIVAL

    changed = 0
    for p in players:
        m = max(p["matches"], 1)
        if is_br:
            raw = bts.overall_raw(p["kills"] / m, p["avgDamage"],
                                  p["avgSurvival"] / 60, p["knocks"] / m)
            new = bts.overall_score(raw, p["matches"], median_matches)
        else:
            new = None
        if new != p.get("overall"):
            changed += 1
        p["overall"] = new

    # 배틀로얄이 아니면 overall 이 None 이라 킬로 세운다 (빌더와 같은 규칙).
    players.sort(key=lambda r: (-(r["overall"] or 0), -r["kills"]))
    return changed, is_br


def main():
    ap = argparse.ArgumentParser(description="집계 파일의 OVERALL 재계산")
    ap.add_argument("--check", action="store_true", help="바꾸지 않고 보여만 준다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    files = sorted(OUT_DIR.glob("*.json"))
    touched = non_br = 0
    for f in files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        changed, is_br = rescore(doc)
        if not is_br:
            non_br += 1
            print("  배틀로얄 아님 -> OVERALL 비움: %s" % doc["id"])
        if changed and not args.check:
            f.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        if changed:
            touched += 1

    print("\n%s %d / %d 단계 (배틀로얄 아님 %d)"
          % ("바뀔 것:" if args.check else "고침:", touched, len(files), non_br))
    return 0


if __name__ == "__main__":
    sys.exit(main())
