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
        # 2019 위키 하위 문서에 Semifinals 가 있고, na-pgcsf 18경기가 조별
        # 다음·결승 앞(11/17)이라 자리가 맞는다.
        "sf": "Semifinals",
        # 2022·2023 의 첫 본선 단계다. 두 해 위키 모두 Group Stage 를 갖고,
        # 그 해 남은 단계는 전부 다른 id 로 잡혀 있다
        # (2022: wb·lbp1·lbp2 = Bracket Stage, gs 4경기 = Grand Survival, gf).
        "gsa": "Group Stage", "gsb": "Group Stage",
    },

    "EWC": {
        # 대회가 본선 단계 둘뿐이고(위키 하위 문서가 Group Stage·Grand Finals
        # 둘뿐이다) 우리 id 도 gs·fs 둘뿐이며 날짜 순서가 맞는다.
        # **fs 는 "Final Stage" 가 아니다** — 위키가 그 단계를 Grand Finals 로
        # 부른다. 2024·2025·2026 셋 다 같은 구조다 (gs 18경기 -> fs 12~18경기).
        "gs": "Group Stage",
        "fs": "Grand Finals",
    },
    "PNC": {
        # 2025 위키 하위 문서는 Final Stage·Survival Stage,
        # 2026 은 Grand Finals·Survival Stage 다.
        #   as-pnc25fs 7/26 18경기 -> Final Stage
        #   as-pnc26ss 6/23 11경기 -> Survival Stage
        # **2025 의 gs 는 비워 둔다.** 그 해 위키에 Group Stage 문서가 없고
        # (남은 것은 Survival Stage 뿐인데) 머리글자도 맞지 않는다.
        "fs": "Final Stage",
        "ss": "Survival Stage",
    },
}

# 같은 시리즈라도 **해마다 단계 이름이 다르다.** 그런 것만 여기 둔다.
# 근거는 그해 리퀴피디아 문서에 실제로 있는 하위 문서 제목이다.
#
# PWS 2026 "PUBG WEEKLY SERIES: KOREA/2026/Phase 1" 하위 문서:
#   Cup/1 ~ Cup/5 · Finals · Weekly Finals · Weekly Stage
#   -> 우리 id 의 c1~c5 가 각 5경기, f 가 27경기로 맞는다.
# PWS 2025 "…/2025/Phase 2" 하위 문서:
#   Grand Finals · Last Chance · Weekly Stage · PGC Points
#   -> f 는 2025 년엔 "Grand Finals" 다. 2025 의 Cup 문서에는 번호가 없으므로
#      그해 c2~c7 에 "Cup 2" 같은 이름을 붙이지 않는다.
STAGE_NAMES_BY_YEAR = {
    # **gs 는 해마다 뜻이 다르다.** 2021·2022 의 gs 는 4경기짜리 Grand Survival
    # 인데 2025 의 gs 는 36경기다. 2025 위키 하위 문서는 Grand Finals·Group
    # Stage·Last Stage 셋이고 우리 id 도 gs·ls·gf 셋이라 자리가 하나씩 맞는다.
    # Grand Survival 은 그해 위키에 아예 없다.
    ("PGC", 2025): {"gs": "Group Stage", "ls": "Last Stage"},
    # 2023 위키에만 Last Chance 문서가 있다 (11/27, 조별과 결승 사이).
    ("PGC", 2023): {"lc": "Last Chance"},
    # PTS 2026 Phase 1 — "PUBG Thailand Series/2026/Phase 1" 의 Format 과
    # `_order.json` 의 경기 날짜를 맞춰 봤다.
    #   Group Stage  4/28~30 & 5/4~6  -> sea-ptsg1 이 4/27~30 · 5/4~6
    #   Grand Finals 5/8~12 · 30경기  -> sea-ptsf1 이 5/8~12 · 31경기 (날짜 일치)
    # **Phase 2 의 w1·w2·ws 는 비워 둔다.** 그쪽은 연기돼 9/21~10/1 로 흩어졌고
    # 위키에 주차별 문서가 없어 어느 조각이 무엇인지 확인되지 않는다.
    ("PTS", 2026): {"g1": "Group Stage", "f1": "Grand Finals"},
    ("PWS", 2025): {"lc": "Last Chance", "f": "Grand Finals"},
    ("PWS", 2026): {"c1": "Cup 1", "c2": "Cup 2", "c3": "Cup 3",
                    "c4": "Cup 4", "c5": "Cup 5", "f": "Finals"},
}

# **id 구조로는 풀 수 없는 것만** 손으로 적는다. (회차, 단계이름).
# 근거는 전부 리퀴피디아 문서의 날짜이고, `_order.json` 의 실제 경기 날짜와
# 맞춰 봤다 — 넘겨짚은 것은 하나도 없다.
#
# PCL 2026 — 한 해에 Spring 과 Autumn 이 있는데 id 에 시즌이 없다. 그대로 두면
#   결승이 둘인 한 덩어리가 된다. 위키 "PUBG Champions League/2026/{Spring,Autumn}":
#     Spring Grand Finals 5/8~10 · 15경기  = cn-pclf    5/8~10 · 15경기
#     Autumn Stage B 8/26~30 + Stage A 8/31~9/4 = cn-pcl26ab 8/26~9/4 · 하루 5경기 50경기
#     Autumn Stage S 9/11~21               = cn-pclas26 9/11~21 하루 5경기 (+9/25 1경기)
#     Autumn Grand Finals 9/25~27 · 15경기  = cn-pclaf26 9/25~27 · 15경기
#   cn-pcl26t 는 같은 날짜에 하루 2~3경기가 따로 있는 별개의 id 라 비워 둔다.
#
# PVS 2026 — 위키 "PUBG Vietnam Series/2026/Phase 1" 이 4/10~5/3 (4주),
#   Phase 2 가 9/4~ 다. 우리 id 의 첫·끝 경기 날짜와 그대로 같다.
#   sea-vnc262 (6/13~7/19, 5주) 는 Phase 2 앞의 Cup (위키 Phase 2/Cup/Week 1~5).
#
# PTS 2026 — Phase 1 이 4~5월, Phase 2 가 9월이다 (연기돼 10/1 까지).
#   Phase 2 의 w1·w2·ws 는 어느 조각이 무엇인지 위키에 없어 단계 이름은 비운다.
EXPLICIT = {
    "cn-pclf":    ("Spring", "Grand Finals"),
    "cn-pcl26ab": ("Autumn", "Stage B·A"),
    "cn-pclas26": ("Autumn", "Stage S"),
    "cn-pclaf26": ("Autumn", "Grand Finals"),
    "cn-pcl26t":  ("Autumn", None),

    "sea-vn26p1": ("Phase 1", None),
    "sea-vnc262": ("Phase 2", "Cup"),
    "sea-vn26p2": ("Phase 2", None),

    "sea-ptsg1":  ("Phase 1", "Group Stage"),
    "sea-ptsf1":  ("Phase 1", "Grand Finals"),
    "sea-ptsw1":  ("Phase 2", None),
    "sea-ptsw2":  ("Phase 2", None),
    "sea-ptsws":  ("Phase 2", None),
}

# 어느 시리즈에서나 같은 뜻인 것만 둔다. 위에서 못 찾으면 여기를 본다.
STAGE_NAMES_ANY = {
    "gf": "Grand Finals",
}

# 코드 뒤 숫자를 이름에 붙여도 되는 것들. **여러 번 열리는 단계만 넣는다.**
# PGC 2021 의 Weekly Finals 는 주차별로 wf1·wf2·wf3 가 있어 번호가 뜻을 갖지만,
# Grand Finals 는 as-pgcgf4 하나뿐이라 "Grand Finals 4" 로 쓰면 결승이 네 번
# 있었던 것처럼 읽힌다. 그런 코드는 숫자를 떼고 이름만 쓴다.
# EMEA 단계 코드의 앞글자 = 시즌. 날짜로 검증했다(위 parse_id 주석 참고).
EMEA_SEASONS = {"f": "Fall", "s": "Spring"}

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
    # EMEA 는 시즌이 회차로 올라갔으므로 여기서는 시즌 뒤의 글자만 본다
    # (fc1 -> 회차 Fall · 코드 c1).
    "EMEA": [
        (re.compile(r'^c(\d+)$'), "Cup %s"),
        (re.compile(r'^p(\d+)$'), "Playoff %s"),
        (re.compile(r'^f\d*$'), "Finals"),
    ],
    "AMER": [
        (re.compile(r'^c(\d+)$'), "Cup %s"),
        (re.compile(r'^p(\d+)$'), "Playoff %s"),
        (re.compile(r'^f\d*$'), "Finals"),
    ],
    "PWS": [
        # 숫자만 두면 "2-3" 이 무엇인지 읽히지 않는다. 주차·일차로 적는다.
        (re.compile(r'^s(\d)(\d)$'), "Weekly Stage %s주차 %s일차"),
        (re.compile(r'^(\d)(\d)$'), "Weekly Stage %s주차 %s일차"),
        (re.compile(r'^wf(\d+)$'), "Weekly Finals %s주차"),
    ],
}

_TRAILING_NUM = re.compile(r'^([a-z]+)(\d+)$')


def stage_name(series, code, year=None):
    """확인된 이름만 돌려준다. 모르면 None."""
    if not code:
        return None
    # 해마다 다른 것이 먼저다. 시리즈 공통 규칙이 그해를 덮어쓰면 안 된다.
    by_year = STAGE_NAMES_BY_YEAR.get((series, year), {})
    if code in by_year:
        return by_year[code]
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

    # PWS 2025 는 글자 없이 숫자만 셋 붙인다: pws<페이즈><주차><일차>.
    # 그대로 두면 pws241 의 회차가 "241" 이 되어 **단계 하나가 대회 하나로**
    # 쪼개진다 (2025년 PWS 가 PWS 141·211·…·243 처럼 15개 가짜 대회가 됐다).
    #
    # id 구조만으로 확인된다: 211·212·213 이 8/26·8/28·8/30 으로 2일 간격이고,
    # 211 -> 221 -> 231 -> 241 이 8/26 -> 9/2 -> 9/9 -> 9/16 으로 정확히 7일
    # 간격이다. 2026년은 같은 것을 pws2s23 처럼 s 를 넣어 쓴다.
    if series == "PWS" and not code and edition and len(edition) == 3:
        edition, code = edition[0], edition[1:]

    # EMEA 는 한 해에 Spring 과 Fall 을 치르는데 회차 번호가 없다. 그대로 두면
    # 둘이 한 덩어리로 묶여 화면에서 구별되지 않고, 공식 이름도 못 붙는다
    # (Spring 단계에 "Fall" 이 찍힐 위험 때문에 막아 뒀었다).
    # **단계 코드 앞글자가 시즌**이라 그걸 회차로 올린다.
    #
    # 날짜로 검증했다 — 2023~2026년 17단계가 예외 없이 맞는다:
    #   s* 는 전부 3~5월, f* 는 전부 8~10월.
    # 리퀴피디아 EMEA 문서에도 시즌이 Fall·Spring 둘뿐이다.
    #
    # **PCL 은 하지 않는다.** 시즌이 Autumn·Fall·Spring·Summer 넷이라
    # `s` 가 Spring 인지 Summer 인지 가릴 수 없다. 확인되면 그때 넣는다.
    if series == "EMEA" and code and code[0] in EMEA_SEASONS:
        edition = EMEA_SEASONS[code[0]]
        code = code[1:] or None
        # 시즌 뒤에 연도만 남는 형태가 있다 (eu-pecs26 -> s + 26).
        if yy and code == yy:
            code = None

    # AMER 은 회차 뒤에 두 자리 연도를 붙인다: am-pas126 = PAS 1 (2026).
    # 앞에 붙는 경우(pgc23gf)는 위에서 처리했고, 이쪽은 뒤에 붙는다.
    if yy and edition and len(edition) > 2 and edition.endswith(yy):
        edition = edition[:-2] or None

    if tournament_id in EXPLICIT:
        ed, st = EXPLICIT[tournament_id]
        return series, ed, code, st

    return series, edition, code, stage_name(series, code, year)


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
