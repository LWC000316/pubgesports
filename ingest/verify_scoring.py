#!/usr/bin/env python3
"""
리퀴피디아에서 대회의 **경기별 배점표**를 뽑아 확인한다.

  python ingest/verify_scoring.py                      # 캐시에 있는 것만 (호출 없음)
  python ingest/verify_scoring.py --page PUBG_Global_Championship/2019
  python ingest/verify_scoring.py --page A --page B    # 여러 장

## 왜 필요한가

공식 PUBG API 는 **배점표를 주지 않는다.** 순위 점수를 계산하려면 바깥에서
확인해야 하고, 확인하지 못한 대회는 점수를 비워 두는 것이
`build_tournament_seed.py` 의 규칙이다 (PLACEMENT_TABLES 의 verifiedBy).

## 무엇을 근거로 삼나

리퀴피디아의 경기 템플릿이 배점을 그대로 담고 있다.

    {{Match|finished=true |p_kill=1 |p1=10 |p2=6 |p3=5 |p4=4 |p5=3 |p6=2 |p7=1 |p8=1
            |map1={{Map|...}} ...}}

`p_kill` 이 킬 1개당 점수, `p1..pN` 이 순위 점수다. **`p_kill` 이 붙은 것만 본다** —
같은 문서에 상금 배분이나 시즌 포인트(`p1=450`, `p1=50` 등)가 함께 있어서
그것과 섞으면 안 된다.

리퀴피디아 문서는 CC-BY-SA 3.0 이다.
"""

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "intermediate_results" / "liquipedia_cache"

_spec = importlib.util.spec_from_file_location(
    "mediawiki_client", Path(__file__).with_name("mediawiki_client.py"))
mw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mw)

# p_kill 바로 뒤에 붙는 p1..pN 만 경기별 배점이다.
SCORING = re.compile(r'p_kill\s*=\s*([\d.]+)((?:\s*\|\s*p\d+\s*=\s*\d+)+)')


def tables_in(wikitext):
    """(킬점수, ((순위, 점수), ...)) -> 등장 횟수"""
    out = Counter()
    for m in SCORING.finditer(wikitext):
        pts = tuple(sorted((int(a), int(b)) for a, b in
                           re.findall(r'p(\d+)\s*=\s*(\d+)', m.group(2))))
        out[(float(m.group(1)), pts)] += 1
    return out


def from_cache():
    """이미 받아 둔 응답에서만 찾는다. 네트워크를 쓰지 않는다."""
    found = {}
    for f in sorted(CACHE_DIR.glob("*.json")):
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        url = doc.get("url", "")
        if "prop=wikitext" not in url:
            continue
        wt = (doc.get("body", {}).get("parse", {}).get("wikitext", {}) or {}).get("*", "")
        t = tables_in(wt) if wt else None
        if t:
            page = re.search(r'page=([^&]+)', url).group(1).replace('%2F', '/')
            found[page] = t
    return found


def describe(kill_point, points):
    return ("킬 %g점 · " % kill_point) + " ".join("%d위=%d" % p for p in points)


def main():
    ap = argparse.ArgumentParser(description="리퀴피디아에서 경기별 배점표 확인")
    ap.add_argument("--page", action="append", default=[],
                    help="리퀴피디아 문서 제목. 여러 번 줄 수 있다")
    ap.add_argument("--refresh", action="store_true", help="캐시를 무시하고 다시 받는다")
    args = ap.parse_args()
    mw.use_utf8_output()

    found = from_cache()
    if args.page:
        client = mw.MediaWikiClient()
        for page in args.page:
            try:
                wt = client.wikitext(page, refresh=args.refresh)
            except SystemExit as e:
                print("%s -> %s" % (page, e))
                continue
            t = tables_in(wt)
            found[page] = t
            if not t:
                print("%s -> 경기 템플릿에 배점이 없습니다 (p_kill 을 못 찾음)." % page)

    if not found:
        print("확인된 배점표가 없습니다.")
        return 1

    agree = Counter()
    for page in sorted(found):
        if not found[page]:
            continue
        print("== %s" % page)
        for key, n in found[page].most_common():
            print("   %3d경기 | %s" % (n, describe(*key)))
            agree[key] += n

    print("\n-- 종합 --")
    for key, n in agree.most_common():
        print("  %4d경기에서 확인: %s" % (n, describe(*key)))
    if len(agree) > 1:
        print("\n표가 여러 개입니다. 연도·대회별로 갈라서 PLACEMENT_TABLES 에 넣으세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
