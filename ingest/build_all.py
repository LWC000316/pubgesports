#!/usr/bin/env python3
"""
내려받은 대회 원본을 모두 집계한다.

  python ingest/build_all.py              # 원본이 있는 것 전부
  python ingest/build_all.py --force      # 이미 만든 것도 다시
  python ingest/build_all.py --series PGS

대회 이름·연도·회차·단계·분류는 모두 id 에서 뽑는다 (stage_label.py).
공식 API 가 이름을 주지 않기 때문이다. 집계는 네트워크를 쓰지 않으므로
규칙을 고칠 때마다 몇 분이면 전부 다시 만들 수 있다.
"""

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "intermediate_results" / "tournaments"
OUT_DIR = PROJECT_ROOT / "primary_data" / "tournaments"
LIST = Path(__file__).with_name("stage_ids.txt")


def main():
    ap = argparse.ArgumentParser(description="대회 원본 일괄 집계")
    ap.add_argument("--force", action="store_true", help="이미 만든 것도 다시 만든다")
    ap.add_argument("--series", default=None, help="이 시리즈만")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    rows = [l.split("\t") for l in LIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    done = skipped = failed = 0
    problems = []
    for date, series, tid in rows:
        if args.series and series != args.series:
            continue
        raw = RAW_DIR / tid
        if not raw.is_dir() or not any(raw.glob("match_*.json")):
            skipped += 1
            continue
        if (OUT_DIR / ("%s.json" % tid)).is_file() and not args.force:
            skipped += 1
            continue
        r = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("build_tournament_seed.py")), tid],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            done += 1
            head = [l for l in r.stdout.splitlines() if l.startswith("경기 ")]
            print("  %s %-6s %-14s %s" % (date, series, tid, head[0] if head else ""))
            for l in r.stdout.splitlines():
                if "배점표가 확인되지" in l or "중단된 경기" in l or "시기가 달라" in l:
                    problems.append("%s: %s" % (tid, l.strip()))
        else:
            failed += 1
            problems.append("%s: 실패 - %s" % (tid, (r.stderr or r.stdout).strip()[:200]))

    print("\n만듦 %d · 건너뜀 %d · 실패 %d" % (done, skipped, failed))
    if problems:
        print("\n확인할 것 %d건:" % len(problems))
        for x in problems[:40]:
            print("  ", x)
        if len(problems) > 40:
            print("   ... 외 %d건" % (len(problems) - 40))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
