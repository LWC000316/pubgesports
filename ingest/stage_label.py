#!/usr/bin/env python3
"""
대회 id 에서 시리즈·회차·단계를 뽑는다.

공식 API 는 **대회 이름을 주지 않는다.** id 만 준다 (`as-pgs7fsg`). 그래서
화면에 쓸 이름을 id 에서 뽑되, **확인한 것만 이름을 붙이고 나머지는 비운다.**
이름이 없는 단계는 화면에서 날짜와 경기 수로 구별된다 — 그건 데이터에서
나온 사실이라 지어낼 여지가 없다.

`as-pgs7fsg` -> 시리즈 PGS · 회차 7 · 단계코드 fsg · 단계이름 "Final Stage"
`as-pgs7ws`  -> 시리즈 PGS · 회차 7 · 단계코드 ws  · 단계이름 None
"""

import re

# 접두사(지역) 뒤에 오는 시리즈 표식.
SERIES = [
    ("PGC", "pgc"), ("PGS", "pgs"), ("PNC", "pnc"), ("EWC", "ewc"),
    ("PWS", "pws"), ("PCL", "pcl"), ("EMEA", "pec"), ("AMER", "pas"),
    ("PTS", "pts"), ("PVS", "vn"),
]

# **확인된 것만 넣는다.** 추측으로 채우면 화면에 지어낸 이름이 뜬다.
#
# **같은 코드가 시리즈마다 다른 단계를 뜻한다.** 그래서 시리즈별로 가른다.
#   ws -> PGS 는 Winners Stage, PGC 는 Weekly Survival
#   gs -> PGS 는 Group Stage,   PGC 는 Grand Survival
# 평평한 표로 두면 PGC 2021 의 as-pgcws 에 "Winners Stage" 라는 틀린 이름이 붙는다.
#
# 근거 (리퀴피디아, CC-BY-SA 3.0):
#   PGS — "PUBG Global Series/2026/Circuit 3/Series 1" 의 Format 절.
#         경기 수가 맞아떨어진다: 조별 9 · Winners 5 · Survival 5
#         = as-pgs7gsg 9 · as-pgs7ws 5 · as-pgs7ss 5
#   PGC — "PUBG Global Championship/2021/" 하위 문서 목록.
#         Bottom 16 / Grand Finals / Grand Survival / Rank Decision /
#         Weekly Finals / Weekly Survival 이 우리 id 9개와 일대일로 맞는다.
#
# 확인하지 못한 코드는 비워 둔다. 화면은 그런 단계를 코드와 날짜·경기 수로
# 구별하는데, 셋 다 데이터에서 나온 사실이라 지어낼 여지가 없다.
STAGE_NAMES = {
    "PGS": {
        "gs": "Group Stage", "gsg": "Group Stage",
        "ws": "Winners Stage",
        "ss": "Survival Stage",
        "fs": "Final Stage", "fsg": "Final Stage",
        "gf": "Grand Finals",
    },
    "PGC": {
        "gf": "Grand Finals",
        "gs": "Grand Survival",
        "ws": "Weekly Survival",
        "wf": "Weekly Finals",
        "bm": "Bottom 16",
        "rd": "Rank Decision",
    },
}

# 어느 시리즈에서나 같은 뜻인 것만 둔다. 위에서 못 찾으면 여기를 본다.
STAGE_NAMES_ANY = {
    "gf": "Grand Finals",
}

# 코드 뒤 숫자를 이름에 붙여도 되는 것들. **여러 번 열리는 단계만 넣는다.**
# PGC 2021 의 Weekly Finals 는 주차별로 wf1·wf2·wf3 가 있어 번호가 뜻을 갖지만,
# Grand Finals 는 as-pgcgf4 하나뿐이라 "Grand Finals 4" 로 쓰면 결승이 네 번
# 있었던 것처럼 읽힌다. 그런 코드는 숫자를 떼고 이름만 쓴다.
NUMBERED_STAGES = {
    "PGC": {"wf", "bm"},
}

# 코드가 숫자를 품은 구조일 때. 평평한 표로는 안 되는 것들만 둔다.
#
# PWS — 리퀴피디아 "PUBG WEEKLY SERIES/2026/Phase 2" 의 Format 과 달력으로 확인했다.
#   Weekly Stage 는 3그룹 라운드로빈(AvsB·BvsC·AvsC) 이고 대결당 5경기,
#   Weekly Finals 는 10경기다. 우리 id 의 경기 수와 날짜가 그대로 맞는다:
#     s11·s12·s13 각 5경기 (9/9~9/11)  = Weekly Stage 1 의 세 대결
#     wf1 10경기 (9/12~13)             = Weekly Finals 1
#     s31·s32·s33 각 5경기 (9/23~25)   = Weekly Stage 3
#     wf3 10경기 (9/26~27)             = Weekly Finals 3
STAGE_PATTERNS = {
    # EMEA·AMER — "PUBG EMEA Championship/2026/Fall" 과 "PUBG Americas Series/2026/2"
    # 의 Format 절이 같은 구조를 말한다. 경기 수가 그대로 맞는다.
    #   Cup       -> c1~c5 각 5경기
    #   Playoffs  -> "2 stages, each 3 days, 5 matches per day" = 15경기 -> p1·p2
    #   Finals    -> f1 (하나뿐이라 번호를 붙이지 않는다)
    # EMEA 코드의 앞 f 는 시즌(Fall)이다. 문서가 2026/Fall 이고 코드가 전부 f 로
    # 시작한다. Spring 쪽 글자는 확인하지 않아 넣지 않는다.
    "EMEA": [
        (re.compile(r'^fc(\d+)$'), "Fall Cup %s"),
        (re.compile(r'^fp(\d+)$'), "Fall Playoff %s"),
        (re.compile(r'^ff\d*$'), "Fall Finals"),
        # Spring 도 같은 구조다 ("PUBG EMEA Championship/2026/Spring" Format:
        # Playoffs 2 stages x 3 days x 5 matches = 15경기). 우리 sp2 가 15경기
        # 5/2 로 "May 1st-3rd" 와 맞고, sf2 가 15경기 5/8 로 그 뒤 Finals 다.
        # Spring Cup 코드(sc*)는 데이터에 없어 넣지 않는다.
        (re.compile(r'^sp(\d+)$'), "Spring Playoff %s"),
        (re.compile(r'^sf\d*$'), "Spring Finals"),
    ],
    "AMER": [
        (re.compile(r'^c(\d+)$'), "Cup %s"),
        (re.compile(r'^p(\d+)$'), "Playoff %s"),
        (re.compile(r'^f\d*$'), "Finals"),
    ],
    "PWS": [
        (re.compile(r'^s(\d)(\d)$'), "Weekly Stage %s-%s"),
        (re.compile(r'^wf(\d+)$'), "Weekly Finals %s"),
    ],
}

_TRAILING_NUM = re.compile(r'^([a-z]+)(\d+)$')


def stage_name(series, code):
    """확인된 이름만 돌려준다. 모르면 None."""
    if not code:
        return None
    for rx, fmt in STAGE_PATTERNS.get(series, ()):
        m = rx.match(code)
        if m:
            return fmt % m.groups()

    table = STAGE_NAMES.get(series, {})
    if code in table:
        return table[code]
    if code in STAGE_NAMES_ANY:
        return STAGE_NAMES_ANY[code]

    m = _TRAILING_NUM.match(code)
    if not m:
        return None
    base, num = m.group(1), m.group(2)
    name = table.get(base) or STAGE_NAMES_ANY.get(base)
    if not name:
        return None
    return ("%s %s" % (name, num)
            if base in NUMBERED_STAGES.get(series, set()) else name)


# **미해결: PGS 의 회차 번호는 공식 브랜딩과 다르다.**
# 리퀴피디아는 PGS 2026 을 "Circuit 1~4 x (Series 1 / Series 2 / Series Final)"
# 로 부른다. 우리 id 의 pgs1~pgs9 는 날짜상 정확히 3개씩 묶이고 매 3번째가 gf 로
# 끝나므로 pgs7 = Circuit 3 Series 1 에 대응한다 — 이건 경기 수까지 맞아 확인됐다
# (위키 Format: 조별 9 · Winners 5 · Survival 5 = as-pgs7gsg/ws/ss 와 동일).
# 나머지 회차는 같은 규칙일 것으로 보이나 하나씩 확인하지 않았으므로 지금은
# id 의 번호를 그대로 "PGS 7" 로 쓴다. 전부 확인되면 Circuit/Series 로 바꾼다.

# 예선·오픈·컵은 본선 목록에서 빼는 데 쓴다.
QUALIFIER = re.compile(r'(q[a-z]?\d?|qual|cup|open|ot\d?|tt|pim|cq|oq|of)$')


def parse_id(tournament_id, year=None):
    """
    (시리즈, 회차, 단계코드, 단계이름). 모르는 값은 None.

    `year` 를 주면 id 에 박힌 두 자리 연도를 떼어낸다. `as-pgc23gf` 의 23 은
    회차가 아니라 2023 년이고, `sea-vn26p2` 의 26 도 마찬가지다. 연도를 안 주면
    구별할 길이 없어 그대로 둔다.
    """
    i = (tournament_id or "").lower()
    series = next((n for n, p in SERIES if p in i), None)
    if not series:
        return None, None, None, None

    body = re.split(r'[-_]', i, 1)[-1]
    pat = dict(SERIES)[series]
    m = re.search(pat + r'(\d*)', body)
    edition = m.group(1) or None
    code = body[m.end():] or None

    yy = str(year)[2:] if year else None
    if yy and edition == yy:              # pgc23gf -> 23 은 연도다
        edition = None
    elif yy and edition and edition.startswith(yy) and len(edition) > 2:
        edition = edition[2:]             # pgs26 3 같은 형태
    if yy and code and code.startswith(yy):
        code = code[2:] or None           # vn|26p2 -> p2

    return series, edition, code, stage_name(series, code)


def is_qualifier(tournament_id):
    return bool(QUALIFIER.search((tournament_id or "").lower()))


def display_name(tournament_id, year=None):
    """화면에 쓸 이름. 모르는 부분은 넣지 않는다."""
    series, edition, code, stage = parse_id(tournament_id, year)
    if not series:
        return tournament_id
    parts = [series]
    if edition:
        parts.append(edition)
    elif year:
        parts.append(str(year))
    if stage:
        parts.append(stage)
    elif code:
        parts.append("(%s)" % code)
    return " ".join(parts)


if __name__ == "__main__":
    import sys
    year = None
    args = sys.argv[1:]
    if args and args[0].isdigit() and len(args[0]) == 4:
        year, args = int(args[0]), args[1:]
    for tid in args:
        print(tid, "->", parse_id(tid, year), "|", display_name(tid, year))
