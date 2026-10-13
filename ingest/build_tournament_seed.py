#!/usr/bin/env python3
"""
내려받은 대회 경기 원본을 읽어 순위표 시드를 만든다. **네트워크를 쓰지 않는다.**

  powershell -NoProfile -File ingest/fetch_tournament.ps1 as-pgs9gf   # 먼저 받고
  python ingest/build_tournament_seed.py as-pgs9gf                    # 집계

결과: primary_data/tournaments/<대회id>.json

## 팀 이름을 알아내는 방법

공식 API 의 `roster.relationships.team` 은 **항상 null 이다.** 경기 데이터만으로는
어느 팀인지 알 수 없다. 두 단계로 찾는다.

  1. 참가자 닉네임을 우리 시드(primary_data/*_teams_verified.json)에서 찾는다.
     로스터 4명 중 다수가 같은 팀이면 그 팀으로 본다.
  2. 못 찾으면 인게임 아이디 접두사(`17_tiantian` -> `17`)를 팀 표시로 쓰고
     `resolved: false` 로 남긴다. **팀 이름을 지어내지 않는다.**

## 점수를 계산하지 않는 이유

순위 점수는 대회 규정마다 다르다(PGC 포인트, 슈퍼 포인트 등). 규정을 확인하지 않고
표를 만들면 지어낸 값이 된다. 그래서 **API 가 직접 주는 것만** 집계한다 —
경기 수, 총 킬, 1위 횟수(WWCD), 평균 순위, 최고 순위.
공식 점수가 필요해지면 그때 규정을 확인해 별도 필드로 추가한다.
"""

import argparse
import importlib.util
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

_spec = importlib.util.spec_from_file_location(
    "stage_label", Path(__file__).with_name("stage_label.py"))
stage_label = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage_label)
# PowerShell 의 Set-Content -Encoding UTF8 은 BOM 을 붙이므로 원본은 utf-8-sig 로 읽는다.
RAW_DIR = PROJECT_ROOT / "intermediate_results" / "tournaments"
OUT_DIR = PROJECT_ROOT / "primary_data" / "tournaments"


def fold(text):
    d = unicodedata.normalize("NFD", (text or "").strip())
    return "".join(c for c in d if unicodedata.category(c) != "Mn").upper()


# 순위 점수 배점표. **공식 API 는 배점표를 주지 않으므로 바깥에서 확인한 것만 넣는다.**
#
# 확인되지 않은 시대는 여기에 넣지 않는다. 그러면 그 대회의 점수 열이 비고
# (placementPoints / totalPoints / avgPoints 가 null), 화면은 킬·치킨·평균순위만
# 보여준다. 틀린 점수를 맞는 것처럼 보여주느니 비워 두는 쪽이 낫다.
#
# `verifiedBy` 는 무엇으로 확인했는지다. 비어 있으면 아직 확인 전이라는 뜻이고,
# 그런 표는 쓰이지 않는다.
PLACEMENT_TABLES = [
    {
        # 리퀴피디아 경기 템플릿에서 그대로 읽은 값이다. **7개 연도·3개 시리즈
        # 28경기가 전부 같은 표**라 2019년부터 한 구간으로 둔다.
        #   PGC  2019(결승·조별) 2021(결승·Weekly Finals) 2022 2023 2024 2025
        #   PCL  2026 Autumn Stage S
        #   PVS  2026 Phase 1·2
        # 2020년은 PGC 가 열리지 않았다 (공식 API 목록에도 2020년 PGC 가 없다).
        # `python ingest/verify_scoring.py` 로 다시 확인할 수 있다.
        "name": "PUBG 이스포츠 표준",
        "fromYear": 2019, "toYear": 9999,
        "points": {1: 10, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 1},
        "killPoint": 1,
        "verifiedBy": "리퀴피디아 PGC 2019·2021~2025 · PCL 2026 · PVS 2026 "
                      "(CC-BY-SA 3.0, 28경기)",
    },
    # **2018년은 넣지 않는다.** PGI 2018 시절이라 형식이 달랐고 확인하지 않았다.
    # 그 해 대회는 점수 열이 빈 채로 나간다.
]


def placement_table(year):
    """그 연도에 쓸 배점표. 확인된 것이 없으면 None."""
    try:
        y = int(year)
    except (TypeError, ValueError):
        return None
    for t in PLACEMENT_TABLES:
        if t["fromYear"] <= y <= t["toYear"] and t.get("verifiedBy"):
            return t
    return None


# OVERALL 환산 기준. 전 대회(배틀로얄만) 선수 26,624명의 원점수 분포에서
# **상위 0.1% 지점이 약 165점**이었고, 그 수준을 100 으로 둔다. 다시 구하려면
# 이 파일의 raw 식으로 전 대회를 돌려 99.9 분위를 보면 된다.
OVERALL_REFERENCE = 165.0

# 배틀로얄이 아닌 단계는 OVERALL 을 매기지 않는다. 중앙 생존 시간으로 가른다 —
# 배틀로얄은 1,000초대인데 TDM·아레나 같은 모드는 150~400초대다. 실제로
# as-pgs5tm 은 중앙 데미지 4 · 생존 309초였고, 거기에 배틀로얄 계수를 쓰니
# 한 선수가 918점이 나왔다.
BR_MIN_MEDIAN_SURVIVAL = 600


def overall_raw(kills_per_match, avg_damage, avg_survival_min, knocks_per_match):
    """
    환산 전 원점수. **네 값이 모두 경기당**이다.

    계수는 wwcd.lol 이 공개한 PGS 9 Grand Final 의 OVERALL 28건에 최소제곱으로
    맞춰 얻었다(최대오차 0.48). 그 표본이 전원 15경기였던 탓에 킬·기절을 총합으로
    두어도 맞아떨어졌는데, **그게 결함이었다** — 데미지·생존은 경기당인데 킬·기절만
    총합이라 경기 수가 늘면 점수가 끝없이 커졌다. 275경기 단계에서 617점이 나왔다.
    그래서 킬·기절도 경기당으로 바꾸고 15를 곱해 15경기 대회 기준으로 맞춘다.
    PGS 9(15경기)에서는 고치기 전과 같은 값이 나온다.
    """
    return (kills_per_match * 15 * 1.5414
            + avg_damage * 0.0863
            + avg_survival_min * 0.9057
            + knocks_per_match * 15 * 0.3157)


def overall_score(raw, matches, median_matches):
    """
    0~100 점. 100 을 넘지 않는다.

    표본이 적으면 경기당 수치를 그대로 믿을 수 없다 — 156경기 대회에서 1경기만
    뛴 선수가 1위로 올라오던 일이 있었다. 그 단계의 중앙 출전 수에 못 미치는
    만큼 깎는다. 다 뛴 선수는 그대로다.
    """
    shrunk = raw * min(1.0, matches / median_matches if median_matches else 1.0)
    return min(100, round(shrunk / OVERALL_REFERENCE * 100))


def load_our_players():
    """폴딩한 닉네임 -> [(리그, 팀, 닉네임, 팀태그)]"""
    index = defaultdict(list)
    for path in sorted(PROJECT_ROOT.glob("primary_data/*_teams_verified.json")):
        for team in json.loads(path.read_text(encoding="utf-8")):
            for player in team.get("players", []):
                index[fold(player["nickname"])].append(
                    (team.get("league"), team["name"], player["nickname"],
                     team.get("tag")))
    return index


def split_ingame_id(name):
    """`17_tiantian` -> ('17', 'tiantian'). 접두사가 없으면 (None, 원본)."""
    if "_" in name:
        prefix, rest = name.split("_", 1)
        if rest:
            return prefix, rest
    return None, name


def seed_years():
    """우리 시드가 어느 시점의 로스터인지. primary_data/_sources.json 이 근거다."""
    f = PROJECT_ROOT / "primary_data" / "_sources.json"
    if not f.is_file():
        return set()
    doc = json.loads(f.read_text(encoding="utf-8"))
    leagues = doc.get("leagues", doc)
    out = set()
    for v in leagues.values():
        if isinstance(v, dict) and v.get("collectedAt"):
            out.add(v["collectedAt"][:4])
    return out


def resolve_team(participant_names, our_players, prefix_only=False,
                 contemporaneous=True):
    """
    로스터 참가자 이름들로 팀을 찾는다.

    우리 시드는 2026년 로스터다. 선수가 이적하면 **옛날 팀이 지금 팀 이름으로**
    찍힌다 — 2021 PGC 의 GEN_Asura 가 Baegopa 로, 2019 의 NAVI_ceh9 가 S8UL 로
    나왔다. 그래서 과반 투표만으로는 믿지 않고 두 가지 중 하나를 더 본다.

      1. 그 대회가 시드와 **같은 시기**면 이적 위험이 없으므로 그대로 믿는다.
      2. 다른 시기면 시드의 팀 태그가 **인게임 접두사와 정확히 같을** 때만 믿는다.
         접두사는 그 대회 당시의 태그라 시대와 무관하게 맞는 검사다. 태그가
         비어 있는 리그(리퀴피디아 수집분 대부분)는 이 경로로 통과하지 못한다.

    둘 다 아니면 접두사를 쓴다. 접두사는 언제나 사실이다.
    """
    if prefix_only:
        prefixes = [split_ingame_id(n)[0] for n in participant_names]
        prefixes = [p for p in prefixes if p]
        if prefixes:
            return None, max(set(prefixes), key=prefixes.count), True
        return None, "UNKNOWN", False

    votes = defaultdict(int)
    for raw in participant_names:
        prefix, nick = split_ingame_id(raw)
        for cand in (nick, raw):
            hits = our_players.get(fold(cand))
            if hits and len(hits) == 1:
                votes[(hits[0][0], hits[0][1], hits[0][3])] += 1
                break

    prefixes = [split_ingame_id(n)[0] for n in participant_names]
    prefixes = [p for p in prefixes if p]
    common = max(set(prefixes), key=prefixes.count) if prefixes else None

    if votes:
        (league, team, tag), n = max(votes.items(), key=lambda kv: kv[1])
        # 과반만으로는 모자란다. 선수가 이적하면 **옛날 팀이 지금 팀 이름으로**
        # 찍힌다 (2021 PGC 의 GEN_Asura 가 Baegopa 로, 2019 의 NAVI 가 S8UL 로
        # 나왔다). 인게임 접두사가 곧 그 대회 당시의 팀 태그이므로, 우리가 찾은
        # 팀의 태그와 접두사가 같을 때만 이름을 믿는다. 다르면 접두사를 쓴다 —
        # 접두사는 언제나 사실이다.
        if n * 2 >= len(participant_names):
            if contemporaneous:
                # 시드와 같은 시기면 이적 위험이 없다. 태그 표기가 접두사와
                # 달라도(VITALITY vs VIT) 그대로 믿는다.
                return league, team, True
            if tag and common and fold(tag) == fold(common):
                # 다른 시기면 태그가 접두사와 정확히 같을 때만 믿는다.
                return league, team, True

    prefixes = [split_ingame_id(n)[0] for n in participant_names]
    prefixes = [p for p in prefixes if p]
    if prefixes:
        common = max(set(prefixes), key=prefixes.count)
        return None, common, False
    return None, "UNKNOWN", False


def main():
    ap = argparse.ArgumentParser(description="대회 경기 원본 -> 순위표 시드")
    ap.add_argument("tournament_id")
    ap.add_argument("--name", default=None, help="화면에 쓸 대회 이름")
    ap.add_argument("--category", default=None,
                    choices=["global", "regional", "scrim"], help="분류")
    ap.add_argument("--series", default=None,
                    help="시리즈 코드. 글로벌은 PGS·PNC·EWC·PGC, 지역은 리그 코드"
                         " (PWS·PCL·EMEA·AMER·PTS·PVS). 대회 탭이 이걸로 묶는다")
    ap.add_argument("--team-from-prefix", action="store_true",
                    help="팀을 우리 명단이 아니라 인게임 아이디 접두사로 정한다. "
                         "네이션스컵(PNC)처럼 팀이 클럽이 아니라 국가인 대회용 — "
                         "그냥 두면 선수가 소속 클럽으로 묶여 'KOR' 이 아니라 "
                         "'DN SOOPers' 가 나온다")
    args = ap.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    raw = RAW_DIR / args.tournament_id
    if not raw.is_dir():
        raise SystemExit("원본이 없습니다: %s\n먼저 fetch_tournament.ps1 을 돌리세요." % raw)

    match_files = sorted(raw.glob("match_*.json"))
    if not match_files:
        raise SystemExit("경기 파일이 없습니다: %s" % raw)

    our_players = load_our_players()

    # 참가자 이름이 익명화된 대회가 있다 (EWC 2026 은 전원 `EWC-Player-23` 형태).
    # 선수도 팀도 알 수 없으니 그럴듯한 표를 만들지 않고 멈춘다.
    # 공식 API 가 알려준 경기 수와 실제로 받은 수를 대조한다. 네트워크 오류로 몇
    # 경기가 빠지면 순위표가 조용히 틀어지는데, 집계 결과가 한 번 생기면
    # fetch_all.ps1 -SkipBuilt 가 그 단계를 영원히 건너뛰어 영영 드러나지 않는다.
    listed = None
    tfile = raw / "tournament.json"
    if tfile.is_file():
        try:
            tdoc = json.loads(tfile.read_text(encoding="utf-8-sig"))
            listed = len([m for m in tdoc.get("included", [])
                          if m.get("type") == "match"])
        except (ValueError, OSError):
            listed = None

    first = json.loads(match_files[0].read_text(encoding="utf-8-sig"))
    sample = [p["attributes"]["stats"]["name"]
              for p in first.get("included", []) if p.get("type") == "participant"]
    anon = [n for n in sample if re.fullmatch(r"[A-Za-z]+-Player-\d+", n or "")]
    if sample and len(anon) > len(sample) / 2:
        # 종료코드 2 = **의도된 거부**. 오류가 아니다. build_all.py 가 이걸 보고
        # "실패"가 아니라 "거부"로 센다 — 안 그러면 거부 한 건 때문에 일괄 집계
        # 전체가 실패로 끝나고, CI 에서는 뒤따르는 커밋 단계가 통째로 날아간다.
        # 2026-10-06 실행에서 EWC 거부 1건에 102단계·5시간치 수집이 날아갔다.
        print("참가자 이름이 익명화돼 있습니다 (%s 등 %d/%d명). "
              "선수도 팀도 알 수 없어 순위표를 만들지 않습니다."
              % (anon[0], len(anon), len(sample)))
        raise SystemExit(2)

    teams = defaultdict(lambda: {"matches": 0, "kills": 0, "wwcd": 0,
                                 "ranks": [], "league": None, "resolved": False})
    players = defaultdict(lambda: {"kills": 0, "damage": 0.0, "matches": 0,
                                   "knocks": 0, "assists": 0, "survived": 0,
                                   "headshots": 0, "longestKill": 0.0, "revives": 0,
                                   "team": None, "league": None})
    maps = []
    voided = []

    # 이 대회가 우리 시드와 같은 시기인지. 팀 이름 해석을 믿어도 되는지를 가른다.
    #
    # **경기 날짜 순으로 봐야 한다.** match_files 는 파일 이름(경기 UUID) 순이라
    # 그 첫 번째는 아무 경기나 된다. 그대로 쓰면 대회 시작일이 엉뚱해진다 —
    # PVS 2026 Phase 1 이 실제 4/10 시작인데 4/19 로 적혀 있었다.
    def _created(path):
        try:
            d = json.loads(path.read_text(encoding="utf-8-sig"))
            return (d.get("data", {}).get("attributes", {}).get("createdAt") or "")
        except (ValueError, OSError):
            return ""

    dated = sorted(((_created(f), f) for f in match_files), key=lambda t: t[0] or "~")
    first_date = (dated[0][0] or "")[:10]
    last_date = (dated[-1][0] or "")[:10]
    event_year = first_date[:4]
    auto_series, auto_edition, auto_code, auto_stage = stage_label.parse_id(
        args.tournament_id, int(event_year) if event_year.isdigit() else None)
    contemporaneous = event_year in seed_years()
    table = placement_table(event_year)
    if not table:
        print("%s 년 배점표가 확인되지 않아 점수 열을 비웁니다. "
              "킬·치킨·평균순위만 담습니다." % (event_year or "?"))
    if not contemporaneous:
        print("%s 년 대회다. 우리 시드(%s)와 시기가 달라 태그가 확인되는 팀만 "
              "이름을 쓰고 나머지는 인게임 접두사로 둔다."
              % (event_year or "?", "/".join(sorted(seed_years())) or "없음"))

    for f in match_files:
        doc = json.loads(f.read_text(encoding="utf-8-sig"))
        included = doc.get("included", [])

        # 중단되고 재경기한 판을 걸러낸다. 공식 API 는 그런 경기도 그대로 준다.
        # 정상 경기는 순위가 1..N 으로 퍼지는데, 중단된 판은 1위 하나에 나머지
        # 전원 꼴찌로 기록된다. 그대로 넣으면 순위 점수·평균·선수 기록이 전부
        # 어긋난다 (PVS 2026 Phase 2 의 2be5c1e7: 757초 · 18킬, 정상은 1700초 · 60킬).
        rosters = [r for r in included if r.get("type") == "roster"]
        ranks_seen = {r.get("attributes", {}).get("stats", {}).get("rank")
                      for r in rosters}
        ranks_seen.discard(None)
        if rosters and len(ranks_seen) * 2 < len(rosters):
            voided.append((f.stem.replace("match_", "")[:8], len(rosters),
                           sorted(ranks_seen)))
            continue

        maps.append(doc.get("data", {}).get("attributes", {}).get("mapName"))

        by_id = {p["id"]: p for p in included if p.get("type") == "participant"}

        for roster in (r for r in included if r.get("type") == "roster"):
            pids = [p["id"] for p in
                    roster.get("relationships", {}).get("participants", {}).get("data", [])]
            names = [by_id[i]["attributes"]["stats"]["name"]
                     for i in pids if i in by_id]
            if not names:
                continue

            league, team, resolved = resolve_team(
                names, our_players,
                prefix_only=args.team_from_prefix or auto_series == "PNC",
                contemporaneous=contemporaneous)
            rank = roster.get("attributes", {}).get("stats", {}).get("rank")

            kills = 0
            for i in pids:
                p = by_id.get(i)
                if not p:
                    continue
                s = p["attributes"]["stats"]
                kills += int(s.get("kills") or 0)
                _, nick = split_ingame_id(s["name"])
                rec = players[nick]
                rec["kills"] += int(s.get("kills") or 0)
                rec["damage"] += float(s.get("damageDealt") or 0)
                rec["knocks"] += int(s.get("DBNOs") or 0)
                rec["assists"] += int(s.get("assists") or 0)
                rec["survived"] += int(s.get("timeSurvived") or 0)
                rec["headshots"] += int(s.get("headshotKills") or 0)
                rec["revives"] += int(s.get("revives") or 0)
                rec["longestKill"] = max(rec["longestKill"],
                                         float(s.get("longestKill") or 0))
                rec["matches"] += 1
                rec["team"] = team
                rec["league"] = league

            t = teams[team]
            t["matches"] += 1
            t["kills"] += kills
            t["league"] = league or t["league"]
            t["resolved"] = t["resolved"] or resolved
            if rank is not None:
                t["ranks"].append(int(rank))
                if int(rank) == 1:
                    t["wwcd"] += 1

    standings = []
    for name, t in teams.items():
        ranks = t["ranks"]
        if table:
            place_pts = sum(table["points"].get(r, 0) for r in ranks)
            kill_pts = t["kills"] * table["killPoint"]
            total_pts = place_pts + kill_pts
            avg_pts = round(total_pts / t["matches"], 2) if t["matches"] else None
        else:
            place_pts = kill_pts = total_pts = avg_pts = None
        standings.append({
            "team": name,
            "league": t["league"],
            "teamResolved": t["resolved"],
            "matches": t["matches"],
            "kills": t["kills"],
            "wwcd": t["wwcd"],
            "placementPoints": place_pts,
            "killPoints": kill_pts,
            "totalPoints": total_pts,
            "avgPoints": avg_pts,
            "bestRank": min(ranks) if ranks else None,
            "avgRank": round(sum(ranks) / len(ranks), 2) if ranks else None,
        })
    match_counts = [r["matches"] for r in standings]
    if table:
        # 합계 -> 순위점수 -> 치킨 순. 동점은 대회 규정마다 다르게 깨지므로
        # 이 순서가 공식 타이브레이커와 일치한다고 단정하지 말 것.
        standings.sort(key=lambda r: (-r["totalPoints"], -r["placementPoints"], -r["wwcd"]))
    else:
        # 배점표를 모르니 점수로 세울 수 없다. 치킨 -> 킬 -> 평균순위 로 두되
        # 이것은 공식 순위가 아니다.
        standings.sort(key=lambda r: (-r["wwcd"], -r["kills"],
                                      r["avgRank"] if r["avgRank"] is not None else 99))
    for i, row in enumerate(standings, 1):
        row["rank"] = i

    player_rows = []
    # 이 단계가 배틀로얄인지, 선수들이 보통 몇 경기를 뛰었는지 먼저 본다.
    # 둘 다 OVERALL 을 매기는 데 필요하다.
    survivals = sorted(v["survived"] / max(v["matches"], 1) for v in players.values())
    played = sorted(v["matches"] for v in players.values())
    median_survival = survivals[len(survivals) // 2] if survivals else 0
    median_matches = played[len(played) // 2] if played else 1
    is_br = median_survival >= BR_MIN_MEDIAN_SURVIVAL
    if players and not is_br:
        print("중앙 생존이 %d초라 배틀로얄로 보지 않습니다. OVERALL 을 비웁니다 "
              "(TDM·아레나 등 다른 모드로 추정)." % median_survival)

    for n, v in players.items():
        m = max(v["matches"], 1)
        avg_damage = v["damage"] / m
        avg_survival_min = v["survived"] / m / 60
        raw_score = overall_raw(v["kills"] / m, avg_damage,
                                avg_survival_min, v["knocks"] / m)
        player_rows.append({
            "nickname": n,
            "team": v["team"],
            "league": v["league"],
            "matches": v["matches"],
            "overall": (overall_score(raw_score, v["matches"], median_matches)
                        if is_br else None),
            "kills": v["kills"],
            "knocks": v["knocks"],
            "assists": v["assists"],
            "headshots": v["headshots"],
            "revives": v["revives"],
            "damage": round(v["damage"], 1),
            "avgDamage": round(avg_damage, 1),
            "avgSurvival": round(v["survived"] / m),
            "longestKill": round(v["longestKill"], 1),
        })
    # 배틀로얄이 아닌 단계는 overall 이 None 이다. 그럴 때는 킬로 세운다.
    player_rows.sort(key=lambda r: (-(r["overall"] or 0), -r["kills"]))

    meta_file = raw / "tournament.json"
    created = None
    if meta_file.exists():
        created = json.loads(meta_file.read_text(encoding="utf-8-sig")) \
            .get("data", {}).get("attributes", {}).get("createdAt")

    doc = {
        "id": args.tournament_id,
        "name": args.name or stage_label.display_name(
            args.tournament_id, int(event_year) if event_year.isdigit() else None),
        "category": args.category or (
            "global" if auto_series in ("PGC", "PGS", "PNC", "EWC") else "regional"),
        "series": args.series or auto_series,
        "year": int(event_year) if event_year.isdigit() else None,
        # 회차·단계는 id 에서 뽑는다. 공식 API 는 대회 이름을 주지 않는다.
        # 단계 이름은 확인된 코드(gf·gs·fs)만 채워지고 나머지는 null 이다 —
        # 화면은 그런 단계를 날짜와 경기 수로 구별한다. stage_label.py 참고.
        "edition": auto_edition,
        "stageCode": auto_code,
        "stage": auto_stage,
        "startDate": first_date,
        "endDate": last_date,
        "source": "https://api.pubg.com/tournaments/%s" % args.tournament_id,
        "createdAt": created,
        "matchCount": len(match_files) - len(voided),
        "maps": sorted(set(m for m in maps if m)),
        "scoring": ({"table": table["name"], "verifiedBy": table["verifiedBy"]}
                    if table else None),
        # 팀마다 뛴 경기 수가 다르면 합계 점수로 줄 세우는 것이 뜻을 잃는다.
        # 여러 로비로 나뉘었거나 중간에 탈락이 있는 단계다 (수집한 61단계 중 15개).
        # 화면이 이 값을 보고 "이 단계는 팀마다 경기 수가 다르다"고 알린다.
        # 공식 API 목록의 경기 수와, 중단돼 뺀 경기 수.
        # listed - voided > matchCount 면 네트워크 오류로 덜 받은 것이다.
        # 중단 경기를 뺀 것(voided)과 못 받은 것을 구별하려고 둘 다 담는다.
        "matchesListed": listed,
        "matchesVoided": len(voided),
        "matchesPerTeam": ({"min": min(match_counts), "max": max(match_counts)}
                           if match_counts and min(match_counts) != max(match_counts)
                           else None),
        "note": ("순위 점수는 %s 배점으로 계산했다 (출처: %s)."
                 % (table["name"], table["verifiedBy"]) if table else
                 "이 대회의 배점표를 확인하지 못해 순위 점수를 계산하지 않았다. "
                 "공식 API 는 배점표를 주지 않는다. 아래는 API 가 직접 주는 "
                 "값(킬·치킨·순위)뿐이며, 나열 순서는 공식 순위가 아니다."),
        "standings": standings,
        "players": player_rows,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / ("%s.json" % args.tournament_id)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if listed is not None and listed - len(voided) > len(match_files) - len(voided):
        print("경고: 공식 API 는 %d경기라는데 %d경기만 받았습니다 (%d경기 누락). "
              "ingest/fetch_all.ps1 을 다시 돌리면 빠진 것만 받습니다."
              % (listed, len(match_files), listed - len(match_files)))

    if voided:
        print("중단된 경기 %d개를 뺐습니다 (순위가 흩어지지 않음):" % len(voided))
        for mid, n, rr in voided:
            print("  %s · 팀 %d개인데 순위가 %s 뿐" % (mid, n, rr))

    unresolved = [s["team"] for s in standings if not s["teamResolved"]]
    print("경기 %d개 · 팀 %d개 · 선수 %d명 -> %s"
          % (len(match_files) - len(voided), len(standings), len(player_rows),
             out.relative_to(PROJECT_ROOT)))
    if unresolved:
        print("우리 시드에서 팀을 못 찾아 인게임 접두사를 쓴 팀 %d개: %s"
              % (len(unresolved), unresolved))
    print("\n상위 8팀:")
    for s in standings[:8]:
        print("  %2d. %-24s 치킨 %d · 킬 %3d · %s"
              % (s["rank"], s["team"], s["wwcd"], s["kills"],
                 ("합계 %d점" % s["totalPoints"]) if s["totalPoints"] is not None
                 else "평균순위 %s" % s["avgRank"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
