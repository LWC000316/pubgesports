#!/usr/bin/env python3
"""
이미 만들어진 집계 파일의 **id 에서 유도되는 값**만 다시 매긴다.

  python ingest/refresh_labels.py

회차·단계코드·단계이름·연도가 대상이다. 전부 id 와 첫 경기 날짜만 있으면 구할 수
있으므로 경기 원본이 없어도 된다.

## 왜 필요한가

`build_all.py` 는 **경기 원본이 있는 단계만** 다시 만든다. 서버(GitHub Actions)는
원본을 보관하지 않으니, 서버가 만든 단계는 로컬에서 다시 만들 수 없다. 그래서
`stage_label.py` 의 규칙을 고치면 그 단계들만 옛 값으로 남는다 — 실제로 PWS 2025
단계 9개가 회차 "111"·"133" 으로 남아 가짜 대회로 쪼개져 있었다.

규칙 자체는 `stage_label.py` 것을 그대로 쓴다. 두 벌로 두면 어긋난다.
"""

import importlib.util
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "primary_data" / "tournaments"

_spec = importlib.util.spec_from_file_location(
    "stage_label", Path(__file__).with_name("stage_label.py"))
stage_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage_label)


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    changed = 0
    for f in sorted(OUT_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        year = d.get("year")
        series, edition, code, stage = stage_label.parse_id(d["id"], year)
        before = (d.get("edition"), d.get("stageCode"), d.get("stage"))
        after = (edition, code, stage)
        if before == after:
            continue
        d["edition"], d["stageCode"], d["stage"] = after
        # 이름은 official_names.py 가 다시 붙인다. 공식 이름이 없는 단계만
        # 여기서 id 기반 이름으로 되돌린다.
        if not d.get("officialName"):
            d["name"] = stage_label.display_name(d["id"], year)
        f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
        changed += 1
        print("   %-14s %s -> %s" % (d["id"], before, after))

    print("\n다시 매긴 단계: %d" % changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
