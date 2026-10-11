#!/usr/bin/env python3
"""
매치로그를 만들 대회를 골라 한꺼번에 추출한다.

  python ingest/build_match_logs_all.py --list        # 대상만 보여주고 끝
  python ingest/build_match_logs_all.py               # 글로벌 결승 (기본)
  python ingest/build_match_logs_all.py --all-global  # 글로벌 전 단계
  python ingest/build_match_logs_all.py --series PWS

## 왜 전부 만들지 않나

리더보드와 선수 스탯은 이미 받아 둔 경기 JSON 만으로 나온다. 그런데
**매치로그는 경기당 33MB 짜리 텔레메트리를 따로 내려받아야** 한다
(API 호출은 추가로 들지 않지만 내려받는 양이 그렇다).

334단계 전부면 약 3,500경기 = 155GB 를 받아 저장소가 1.2GB 늘어난다.
글로벌 4종(PGC·PGS·PNC·EWC)의 결승 단계만 하면 15GB 에 110MB 다.
예선 경기의 선수 동선을 들여다볼 일은 거의 없다. 나중에 특정 대회가
필요해지면 `build_match_log.py <대회id>` 한 줄이면 된다.
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "intermediate_results" / "tournaments"
OUT_DIR = PROJECT_ROOT / "primary_data" / "matchlogs"
LIST = Path(__file__).with_name("stage_ids.txt")

_spec = importlib.util.spec_from_file_location(
    "stage_label", Path(__file__).with_name("stage_label.py"))
stage_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage_label)

GLOBAL = {"PGC", "PGS", "PNC", "EWC"}
# 결승으로 볼 단계. stage_label 이 이름을 붙여 준 것만 쓴다 — 모르는 코드를
# 결승으로 넘겨짚지 않는다.
FINAL_STAGES = {"Grand Finals", "Final Stage"}


def targets(args):
    rows = [l.split("\t") for l in LIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for date, series, tid in rows:
        if getattr(args, "all", False):
            pass                   # 전 단계. 비용이 크니 --list 로 먼저 볼 것
        elif args.series and series != args.series:
            continue
        elif not args.series:
            if series not in GLOBAL:
                continue
            _, _, _, stage = stage_label.parse_id(tid, int(date[:4]))
            if not args.all_global and stage not in FINAL_STAGES:
                continue
        raw = RAW_DIR / tid
        n = len(list(raw.glob("match_*.json"))) if raw.is_dir() else 0
        have = len(list((OUT_DIR / tid).glob("*.json"))) if (OUT_DIR / tid).is_dir() else 0
        out.append((date, series, tid, n, have))
    return out


def main():
    ap = argparse.ArgumentParser(description="매치로그 일괄 추출")
    ap.add_argument("--list", action="store_true", help="대상만 보여주고 끝낸다")
    ap.add_argument("--all-global", action="store_true", help="글로벌의 모든 단계")
    ap.add_argument("--all", action="store_true",
                    help="수집한 전 단계. 약 7,300경기 · 서버 내려받기 236GB · "
                         "저장소 약 600MB 증가 (git 압축 후)")
    ap.add_argument("--series", default=None, help="이 시리즈만 (단계를 가리지 않는다)")
    ap.add_argument("--keep-telemetry", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="이미 만든 매치로그도 다시 뽑는다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    rows = targets(args)
    todo = rows if args.force else [r for r in rows if r[3] > r[4]]
    # --force 면 전부 다시 뽑으므로 이미 만든 것도 비용에 넣는다.
    pending = (sum(r[3] for r in rows) if args.force
               else sum(max(0, r[3] - r[4]) for r in rows))
    print("대상 %d단계 · 경기 %d개 (이미 만든 것 제외 %d개)"
          % (len(rows), sum(r[3] for r in rows), pending))
    print("예상 내려받기 약 %.1fGB · 저장소 증가 약 %dMB"
          % (pending * 33 / 1024, pending * 250 // 1024))
    for date, series, tid, n, have in rows:
        mark = "받을 것" if n > have else ("원본없음" if n == 0 else "완료")
        print("  %s %-5s %-14s 경기 %3d · 로그 %3d  %s" % (date, series, tid, n, have, mark))
    if args.list:
        return 0
    if not todo:
        print("\n새로 만들 것이 없습니다.")
        return 0

    script = str(Path(__file__).with_name("build_match_log.py"))
    for date, series, tid, n, have in todo:
        cmd = [sys.executable, script, tid]
        if args.keep_telemetry:
            cmd.append("--keep-telemetry")
        if args.force:
            cmd.append("--force")
        print("\n=== %s %s (%d경기) ===" % (series, tid, n))
        r = subprocess.run(cmd)
        if r.returncode != 0:
            print("  실패: %s" % tid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
