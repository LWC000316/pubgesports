#!/usr/bin/env python3
"""
PUBG PRO SENS 구글 시트의 감도를 시드 파일에 반영한다.

출처: https://docs.google.com/spreadsheets/d/1TQ3xYMgFVXIq7hmA0Fr4WZuj4wPiDT3sVqf65E3QcYg
      (Discord 서버 PUBG PRO SENS 의 #프로감도-파일 에서 안내되는 시트.
       관리자가 대략 한 달에 한 번 갱신한다고 적혀 있다.)

감도·장비는 리퀴피디아에도 공식 API 에도 없어서 사람이 모아야 하는 데이터다.
이 시트가 그 수작업의 결과물이라 여기서 받아 시드에 넣는다.

컬럼 대응 (2026-09-29 사용자 확인):
    DPI          -> mouseDpi
    일반감도      -> generalSens
    수직감도      -> verticalMultiplier
    스코프감도    -> adsSens
    2/3/4/6/8배율 -> scope2x/3x/4x/6x/8xSens
    해상도        -> resolution

시트에 없는 항목(FOV, 화면 모드, 렌더링 크기, 장비)은 **건드리지 않는다.**
기본값을 지어내지 않는다 — 없으면 화면에 '미등록' 이 뜨는 것이 옳다.

    python ingest/apply_sens_sheet.py --dry-run     # 무엇이 바뀌는지만 본다
    python ingest/apply_sens_sheet.py               # 시드 파일에 기록
    python ingest/apply_sens_sheet.py --csv <파일>  # 내려받아 둔 CSV 로

반영 뒤에는 SEED_MODE=always 로 한 번 기동해야 DB 에 들어간다.
"""

import argparse
import csv
import io
import json
import sys
import unicodedata
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_GLOB = "primary_data/*_teams_verified.json"

SHEET_ID = "1TQ3xYMgFVXIq7hmA0Fr4WZuj4wPiDT3sVqf65E3QcYg"
SHEET_CSV = "https://docs.google.com/spreadsheets/d/%s/export?format=csv&gid=0" % SHEET_ID

# 시트 컬럼 -> 시드 setting 키
COLUMN_MAP = [
    ("DPI", "mouseDpi", int),
    ("일반감도", "generalSens", float),
    ("수직감도", "verticalMultiplier", float),
    ("스코프감도", "adsSens", float),
    ("2배율감도", "scope2xSens", float),
    ("3배율감도", "scope3xSens", float),
    ("4배율감도", "scope4xSens", float),
    ("6배율감도", "scope6xSens", float),
    ("8배율감도", "scope8xSens", float),
    ("해상도", "resolution", str),
]

# 값이 이 범위를 벗어나면 옮겨 적다가 칸이 밀린 것으로 보고 건너뛴다.
# 실제로 tigger 행이 일반감도 1.09 / 수직감도 37 로 두 칸이 뒤바뀌어 있었다.
SANITY = {
    "mouseDpi": (100, 3200),
    "generalSens": (1, 100),
    "verticalMultiplier": (0.3, 3.0),
    "adsSens": (1, 100),
    "scope2xSens": (1, 100),
    "scope3xSens": (1, 100),
    "scope4xSens": (1, 100),
    "scope6xSens": (1, 100),
    "scope8xSens": (1, 100),
}


def fold(text):
    """발음부호를 떼고 대문자로 맞춘 비교용 문자열."""
    decomposed = unicodedata.normalize("NFD", (text or "").strip())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn").upper()


def load_sheet(csv_path):
    if csv_path:
        text = Path(csv_path).read_text(encoding="utf-8")
    else:
        req = urllib.request.Request(SHEET_CSV, headers={"User-Agent": "PUBGProVault/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
    return [r for r in csv.DictReader(io.StringIO(text)) if (r.get("닉네임") or "").strip()]


def parse_setting(row):
    """시트 한 줄에서 setting 딕셔너리를 만든다. 값이 없거나 이상하면 그 키를 뺀다."""
    setting, skipped = {}, []
    for column, key, caster in COLUMN_MAP:
        raw = (row.get(column) or "").strip()
        if raw in ("", "-"):
            continue
        try:
            value = caster(raw)
        except ValueError:
            skipped.append("%s=%r" % (column, raw))
            continue
        lo_hi = SANITY.get(key)
        if lo_hi and not (lo_hi[0] <= value <= lo_hi[1]):
            skipped.append("%s=%s (범위 밖)" % (column, value))
            continue
        setting[key] = value
    return setting, skipped


def index_seeds():
    """폴딩한 닉네임 -> [(파일, 팀, 선수 dict, 리그, 팀태그)]"""
    index = {}
    for path in sorted(PROJECT_ROOT.glob(SEED_GLOB)):
        teams = json.loads(path.read_text(encoding="utf-8"))
        for team in teams:
            for player in team.get("players", []):
                index.setdefault(fold(player["nickname"]), []).append(
                    (path, teams, team, player))
    return index


def pick_candidate(candidates, row):
    """
    동명이인은 시트의 소속팀·지역으로 가린다. 그래도 하나로 좁혀지지 않으면
    **짐작하지 않고 건너뛴다.** 어느 선수인지 모른 채 감도를 붙이면 안 된다.
    """
    if len(candidates) == 1:
        return candidates[0], None

    sheet_team = fold(row.get("소속팀"))
    narrowed = [c for c in candidates
                if sheet_team and (fold(c[3].get("tag")) == sheet_team
                                   or sheet_team in fold(c[2]["name"]))]
    if len(narrowed) == 1:
        return narrowed[0], None

    sheet_region = fold(row.get("지역"))
    REGION_LEAGUES = {"EU": {"EMEA"}, "AMER": {"AMER"}, "AS": {"PWS", "PCL"},
                      "APAC": {"PTS", "PVS"}}
    leagues = REGION_LEAGUES.get(sheet_region, set())
    narrowed = [c for c in (narrowed or candidates) if c[2].get("league") in leagues]
    if len(narrowed) == 1:
        return narrowed[0], None

    return None, "후보 %d명: %s" % (
        len(candidates), [(c[2].get("league"), c[2]["name"]) for c in candidates])


def main():
    ap = argparse.ArgumentParser(description="PUBG PRO SENS 시트를 시드에 반영")
    ap.add_argument("--csv", default=None, help="내려받아 둔 CSV 경로")
    ap.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않는다")
    args = ap.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    rows = load_sheet(args.csv)
    index = index_seeds()
    print("시트 %d명 / 시드 고유 닉네임 %d개" % (len(rows), len(index)))

    applied, unmatched, ambiguous, problems = [], [], [], []
    touched = {}

    for row in rows:
        nick = row["닉네임"].strip()
        candidates = index.get(fold(nick))
        if not candidates:
            unmatched.append(nick)
            continue

        chosen, why = pick_candidate(candidates, row)
        if chosen is None:
            ambiguous.append((nick, why))
            continue

        setting, skipped = parse_setting(row)
        if skipped:
            # 한 칸이라도 이상하면 그 줄은 통째로 버린다. 칸이 밀린 행에서 일부만
            # 가져오면 멀쩡해 보이는 틀린 값이 들어간다 — tigger 행은 일반감도와
            # 수직감도가 서로 뒤바뀌어 있었고, 수직(37)만 걸러내면 일반(1.09)이
            # 범위 안이라 그대로 통과한다.
            problems.append((nick, skipped))
            continue
        if not setting:
            continue

        path, teams, team, player = chosen
        player["setting"] = setting
        touched[path] = teams
        applied.append((team.get("league"), team["name"], player["nickname"], len(setting)))

    print("\n반영 %d명 / 시드에 없음 %d명 / 모호 %d명"
          % (len(applied), len(unmatched), len(ambiguous)))

    by_league = {}
    for league, _team, _nick, _n in applied:
        by_league[league] = by_league.get(league, 0) + 1
    print("리그별:", by_league)

    if problems:
        print("\n값이 이상해 건너뛴 항목:")
        for nick, skipped in problems:
            print("  %-16s %s" % (nick, ", ".join(skipped)))
    if ambiguous:
        print("\n어느 선수인지 좁혀지지 않아 건너뜀:")
        for nick, why in ambiguous:
            print("  %-16s %s" % (nick, why))

    if args.dry_run:
        print("\n--dry-run 이라 파일을 쓰지 않았습니다.")
        return 0

    for path, teams in touched.items():
        path.write_text(json.dumps(teams, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print("기록: %s" % path.relative_to(PROJECT_ROOT))

    print("\n다음: cd backend && SEED_MODE=always ./gradlew bootRun")
    return 0


if __name__ == "__main__":
    sys.exit(main())
