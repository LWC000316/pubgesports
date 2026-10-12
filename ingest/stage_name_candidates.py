#!/usr/bin/env python3
"""
이름이 안 붙은 단계와, 그 대회의 **리퀴피디아 하위 문서 제목**을 나란히 보여 준다.

  python ingest/stage_name_candidates.py           # 전부
  python ingest/stage_name_candidates.py EWC PNC   # 시리즈만

네트워크를 쓰지 않는다. `intermediate_results/liquipedia_pages.json` 에 받아 둔
문서 제목 목록(allpages, 가벼운 호출)만 읽는다.

## 왜 이렇게 하나

단계 이름의 근거는 **리퀴피디아에 그 제목의 문서가 실제로 있다는 것**이다
(`official_names.py` 와 같은 규칙). 하위 문서 제목이 곧 그 대회의 단계 목록이라,
`action=parse` 로 본문을 긁지 않고도 "이 대회에 어떤 단계가 있었는지" 를 알 수 있다.
`action=parse` 는 30초 간격이 필요하고 2초로 때렸다가 하루 차단당한 적이 있다.

**이 도구는 후보를 보여 줄 뿐 이름을 붙이지 않는다.** 코드와 제목을 맞추는 것은
사람이 보고 판단한다 — 같은 코드가 시리즈마다 다른 뜻이기 때문이다. 실제로:

- EWC `fs` 는 "Final Stage" 가 아니라 **Grand Finals** 다 (2025·2026 문서 확인)
- PNC `fs` 는 Final Stage(2025), `ss` 는 Survival Stage(2026)
- PNC 2025 의 `gs` 는 위키에 Group Stage 문서가 없다. 머리글자도 안 맞으니 **비워 둔다**
- PGS `ws` 는 Winners Stage, PGC `ws` 는 Weekly Survival

확인한 것만 `stage_label.py` 의 STAGE_NAMES 에 적는다.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOURNAMENTS = PROJECT_ROOT / "primary_data" / "tournaments"
PAGES = PROJECT_ROOT / "intermediate_results" / "liquipedia_pages.json"

# 단계가 아니라 참가 자격·통계 문서다. 단계 후보에서 뺀다.
NOT_A_STAGE = ("Qualifier", "Statistics", "/Points", "Qualification",
               "Team Appearances", "Player appearances", "Matches", "Results")


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    only = {a.upper() for a in sys.argv[1:]}
    pages = json.loads(PAGES.read_text(encoding="utf-8"))

    unnamed = defaultdict(list)
    named = total = 0
    for f in sorted(TOURNAMENTS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        total += 1
        if d.get("stage"):
            named += 1
            continue
        unnamed[(d.get("series"), d.get("year"))].append(
            (d["id"], d.get("stageCode"), d.get("matchCount"), d.get("startDate")))

    print("이름 있는 단계 %d / %d\n" % (named, total))

    for (series, year), rows in sorted(unnamed.items(),
                                       key=lambda kv: (str(kv[0][0]), kv[0][1] or 0)):
        if only and series not in only:
            continue
        titles = [t for t in pages.get(series, [])
                  if re.search(r"/%s(/|$)" % year, t)]
        subs = sorted(t for t in titles
                      if t.count("/") >= 2 and not any(x in t for x in NOT_A_STAGE))
        print("== %s %s" % (series, year))
        for tid, code, n, date in sorted(rows, key=lambda r: r[3] or ""):
            print("    %-16s code=%-6s %4s경기  %s" % (tid, code, n, date))
        if subs:
            for t in subs:
                print("    위키: %s" % t.split("/", 2)[-1])
        else:
            print("    위키: (하위 문서 없음 — 본문을 봐야 한다)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
