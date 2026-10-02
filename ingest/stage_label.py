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
# ws·ss·c1~c5·s22 등은 아직 뭔지 모르므로 비워 둔다 — 리퀴피디아로 확인되면
# 여기에 추가하면 된다.
STAGE_NAMES = {
    "gf": "Grand Finals",
    "gs": "Group Stage",
    "gsg": "Group Stage",
    "fs": "Final Stage",
    "fsg": "Final Stage",
}

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

    return series, edition, code, STAGE_NAMES.get(code)


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
