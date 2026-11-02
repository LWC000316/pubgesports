#!/usr/bin/env python3
"""
공식 API 의 대회 목록을 다시 받아 **작업 목록(`stage_ids.txt`)을 갱신한다.**

  python ingest/refresh_stage_ids.py            # 받아서 갱신
  python ingest/refresh_stage_ids.py --check     # 받기만 하고 쓰지 않는다
  python ingest/refresh_stage_ids.py --offline   # 이미 받아 둔 목록으로만 갱신

## 왜 이게 없어서 문제였나

`stage_ids.txt` 는 **한 번 손으로 만든 334줄**이었고, 그 원본
(`intermediate_results/all_tournaments.json`)은 2026-10-02 에 받은 것이었다.
수집 워크플로는 그 목록에 적힌 단계만 받으므로, **그 뒤에 열린 대회는 목록에
없어서 영원히 들어오지 않았다** — 10월에 치른 PGS 가 사이트에 안 보인 이유가
이것이다. "새 경기가 왜 실시간으로 안 들어오나"의 답은 수집기가 느린 것이
아니라 **받을 것의 목록이 늙어 있었다**는 것이다.

이제 수집 워크플로가 매번 먼저 이것을 돌린다. 목록 호출은 **API 1회**다.

## 무엇을 남기나

공식 API 가 아는 대회 id 전부(2018년부터 1,194개) 중 **본선 단계만** 남긴다.
기준은 둘이고 둘 다 `stage_label.py` 의 것을 그대로 쓴다 — 규칙을 두 벌로
두면 어긋난다.

  1. `parse_id` 가 시리즈를 알아보는 것 (PGC/PGS/PNC/EWC/PWS/PCL/EMEA/AMER/PTS/PVS)
  2. `is_qualifier` 가 아닌 것 (예선·오픈·클랜전은 뺀다)

이 규칙으로 2026-10-02 목록을 다시 돌려 **기존 334줄과 한 글자도 다르지 않게**
나오는 것을 확인했다. 그래서 갱신이 기존 작업 목록을 흔들지 않는다.

파일 형식은 `날짜<TAB>시리즈<TAB>id`, **새것이 위**다. `fetch_all.ps1` 이
위에서부터 읽으므로 새 대회가 먼저 받아진다.
"""

import argparse
import importlib.util
import json
import os
import sys
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIST_RAW = PROJECT_ROOT / "intermediate_results" / "all_tournaments.json"
WORKLIST = Path(__file__).with_name("stage_ids.txt")
API = "https://api.pubg.com/tournaments"

_spec = importlib.util.spec_from_file_location(
    "sl", Path(__file__).with_name("stage_label.py"))
sl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sl)


def fetch_list(key):
    req = urllib.request.Request(API, headers={
        "Authorization": "Bearer %s" % key,
        "Accept": "application/vnd.api+json",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def read_raw():
    # 예전 PowerShell 스크립트가 BOM 을 붙여 저장했다. utf-8-sig 로 둘 다 읽힌다.
    return json.loads(LIST_RAW.read_text(encoding="utf-8-sig"))


def main_stages(doc):
    """(날짜, 시리즈, id) 목록. 새것이 위."""
    out = []
    for r in doc.get("data", []):
        tid = r.get("id")
        created = (r.get("attributes") or {}).get("createdAt") or ""
        year = int(created[:4]) if created[:4].isdigit() else None
        series = sl.parse_id(tid, year)[0]
        if not series or sl.is_qualifier(tid):
            continue
        out.append((created[:10], series, tid))
    out.sort(reverse=True)
    return out


def main():
    ap = argparse.ArgumentParser(description="대회 작업 목록 갱신")
    ap.add_argument("--check", action="store_true", help="쓰지 않고 보여만 준다")
    ap.add_argument("--offline", action="store_true",
                    help="받지 않고 이미 저장된 목록으로만 갱신한다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    if args.offline:
        doc = read_raw()
        print("저장된 목록을 씁니다 (받지 않음).")
    else:
        key = os.environ.get("PUBG_API_KEY")
        if not key:
            print("PUBG_API_KEY 가 없습니다.", file=sys.stderr)
            return 1
        try:
            doc = fetch_list(key)
        except Exception as e:
            print("목록을 받지 못했습니다: %s" % e, file=sys.stderr)
            if not LIST_RAW.exists():
                return 1
            print("저장된 목록으로 갱신만 합니다.")
            doc = read_raw()
        else:
            if not args.check:
                LIST_RAW.parent.mkdir(parents=True, exist_ok=True)
                LIST_RAW.write_text(
                    json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")

    stages = main_stages(doc)
    old = []
    if WORKLIST.exists():
        old = [l for l in WORKLIST.read_text(encoding="utf-8").splitlines() if l.strip()]
    old_ids = set(l.split("\t")[-1] for l in old)
    fresh = [s for s in stages if s[2] not in old_ids]

    print("대회 목록 %d개 · 본선 단계 %d개 · 기존 작업 목록 %d줄"
          % (len(doc.get("data", [])), len(stages), len(old)))
    if fresh:
        print("\n새 단계 %d개:" % len(fresh))
        for d, s, tid in fresh:
            print("   %s  %-5s %s" % (d, s, sl.display_name(tid,
                  int(d[:4]) if d[:4].isdigit() else None)))
    else:
        print("\n새 단계가 없습니다.")

    # **사라진 id 는 지우지 않는다.** 공식 API 가 옛 대회를 목록에서 빼는 일이
    # 있는데, 우리는 그 단계의 집계를 이미 갖고 있다. 지우면 다음 실행이
    # "없는 단계"로 보고 화면에서 사라진다.
    missing = [i for i in old_ids if i not in set(s[2] for s in stages)]
    if missing:
        print("\n목록에서 빠졌지만 그대로 두는 id %d개: %s"
              % (len(missing), " ".join(sorted(missing)[:8])))

    keep = {l.split("\t")[-1]: l for l in old}
    merged = ["\t".join(s) for s in stages]
    merged += [keep[i] for i in sorted(missing)]
    if args.check:
        print("\n--check 라 쓰지 않았습니다.")
        return 0
    WORKLIST.write_text("\n".join(merged) + "\n", encoding="utf-8")
    print("\n%s %d줄 (새 %d)" % (WORKLIST.name, len(merged), len(fresh)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
