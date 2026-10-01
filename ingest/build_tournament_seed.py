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
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# PowerShell 의 Set-Content -Encoding UTF8 은 BOM 을 붙이므로 원본은 utf-8-sig 로 읽는다.
RAW_DIR = PROJECT_ROOT / "intermediate_results" / "tournaments"
OUT_DIR = PROJECT_ROOT / "primary_data" / "tournaments"


def fold(text):
    d = unicodedata.normalize("NFD", (text or "").strip())
    return "".join(c for c in d if unicodedata.category(c) != "Mn").upper()


def overall_score(kills, avg_damage, avg_survival_min, knocks):
    """
    선수 종합 점수.

    공식 API 는 종합 점수를 주지 않는다. 이 계수는 wwcd.lol 이 공개한 PGS 9
    Grand Final 통합 스탯의 OVERALL 값 28건에 최소제곱으로 맞춰 얻은 것이다
    (최대오차 0.48 - OVERALL 이 정수 표시라 반올림 범위 안).

    주의: 표본이 전원 15경기라 **총합 기준인지 경기당 평균 기준인지 구분할 수
    없었다.** 경기 수가 다른 대회에서는 어긋날 수 있다. 킬·기절은 총합,
    데미지·생존은 경기당 평균으로 둔 것이 그 표본에 가장 잘 맞았다.
    """
    return (kills * 1.5414
            + avg_damage * 0.0863
            + avg_survival_min * 0.9057
            + knocks * 0.3157)


def load_our_players():
    """폴딩한 닉네임 -> [(리그, 팀, 닉네임)]"""
    index = defaultdict(list)
    for path in sorted(PROJECT_ROOT.glob("primary_data/*_teams_verified.json")):
        for team in json.loads(path.read_text(encoding="utf-8")):
            for player in team.get("players", []):
                index[fold(player["nickname"])].append(
                    (team.get("league"), team["name"], player["nickname"]))
    return index


def split_ingame_id(name):
    """`17_tiantian` -> ('17', 'tiantian'). 접두사가 없으면 (None, 원본)."""
    if "_" in name:
        prefix, rest = name.split("_", 1)
        if rest:
            return prefix, rest
    return None, name


def resolve_team(participant_names, our_players, prefix_only=False):
    """
    로스터 참가자 이름들로 팀을 찾는다.
    우리 시드에서 찾은 팀이 과반이면 그 팀, 아니면 인게임 접두사를 쓴다.
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
                votes[(hits[0][0], hits[0][1])] += 1
                break
    if votes:
        (league, team), n = max(votes.items(), key=lambda kv: kv[1])
        if n * 2 >= len(participant_names):        # 과반
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
    first = json.loads(match_files[0].read_text(encoding="utf-8-sig"))
    sample = [p["attributes"]["stats"]["name"]
              for p in first.get("included", []) if p.get("type") == "participant"]
    anon = [n for n in sample if re.fullmatch(r"[A-Za-z]+-Player-\d+", n or "")]
    if sample and len(anon) > len(sample) / 2:
        raise SystemExit(
            "참가자 이름이 익명화돼 있습니다 (%s 등 %d/%d명).\n"
            "선수도 팀도 알 수 없어 순위표를 만들지 않습니다. 진행을 멈춥니다."
            % (anon[0], len(anon), len(sample)))

    teams = defaultdict(lambda: {"matches": 0, "kills": 0, "wwcd": 0,
                                 "ranks": [], "league": None, "resolved": False})
    players = defaultdict(lambda: {"kills": 0, "damage": 0.0, "matches": 0,
                                   "knocks": 0, "assists": 0, "survived": 0,
                                   "headshots": 0, "longestKill": 0.0, "revives": 0,
                                   "team": None, "league": None})
    maps = []

    for f in match_files:
        doc = json.loads(f.read_text(encoding="utf-8-sig"))
        included = doc.get("included", [])
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
                names, our_players, prefix_only=args.team_from_prefix)
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
        standings.append({
            "team": name,
            "league": t["league"],
            "teamResolved": t["resolved"],
            "matches": t["matches"],
            "kills": t["kills"],
            "wwcd": t["wwcd"],
            "bestRank": min(ranks) if ranks else None,
            "avgRank": round(sum(ranks) / len(ranks), 2) if ranks else None,
        })
    # 점수가 없으므로 치킨 -> 킬 -> 평균 순위 로 세운다. 공식 순위가 아니다.
    standings.sort(key=lambda r: (-r["wwcd"], -r["kills"],
                                  r["avgRank"] if r["avgRank"] is not None else 99))
    for i, row in enumerate(standings, 1):
        row["rank"] = i

    player_rows = []
    for n, v in players.items():
        m = max(v["matches"], 1)
        avg_damage = v["damage"] / m
        avg_survival_min = v["survived"] / m / 60
        player_rows.append({
            "nickname": n,
            "team": v["team"],
            "league": v["league"],
            "matches": v["matches"],
            "overall": round(overall_score(v["kills"], avg_damage,
                                           avg_survival_min, v["knocks"])),
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
    player_rows.sort(key=lambda r: (-r["overall"], -r["kills"]))

    meta_file = raw / "tournament.json"
    created = None
    if meta_file.exists():
        created = json.loads(meta_file.read_text(encoding="utf-8-sig")) \
            .get("data", {}).get("attributes", {}).get("createdAt")

    doc = {
        "id": args.tournament_id,
        "name": args.name or args.tournament_id,
        "category": args.category,
        "source": "https://api.pubg.com/tournaments/%s" % args.tournament_id,
        "createdAt": created,
        "matchCount": len(match_files),
        "maps": sorted(set(m for m in maps if m)),
        "note": "순위 점수는 대회 규정마다 달라 계산하지 않았다. "
                "API 가 직접 주는 값(킬·순위·WWCD)만 담는다.",
        "standings": standings,
        "players": player_rows,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / ("%s.json" % args.tournament_id)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    unresolved = [s["team"] for s in standings if not s["teamResolved"]]
    print("경기 %d개 · 팀 %d개 · 선수 %d명 -> %s"
          % (len(match_files), len(standings), len(player_rows),
             out.relative_to(PROJECT_ROOT)))
    if unresolved:
        print("우리 시드에서 팀을 못 찾아 인게임 접두사를 쓴 팀 %d개: %s"
              % (len(unresolved), unresolved))
    print("\n상위 8팀:")
    for s in standings[:8]:
        print("  %2d. %-24s 치킨 %d · 킬 %3d · 평균순위 %s"
              % (s["rank"], s["team"], s["wwcd"], s["kills"], s["avgRank"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
