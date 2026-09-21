"""
리그 하나의 시드 초안을 만든다.

출력 스키마는 primary_data/pws2_teams_verified.json 과 동일하다. DataInitializer 가
그 형식만 읽기 때문이다.

이 스크립트는 초안만 만든다. 결과를 바로 primary_data/ 에 넣지 말고
verify_seed.py 로 검사한 뒤 리퀴피디아 원문과 대조해야 한다.

  1) 필드 확인   python ingest/build_league_seed.py --dump-fields --page "<리퀴피디아 문서명>"
  2) 초안 생성   python ingest/build_league_seed.py --league PCL --page "<문서명>" \
                     --region CN --seed-map ingest/seed_types_pcl.json \
                     --out intermediate_results/pcl_seed_draft.json
  3) 검사        python ingest/verify_seed.py intermediate_results/pcl_seed_draft.json

선수 세팅(mouseDpi·generalSens·mouseName)은 **넣지 않는다.** 리퀴피디아에 없는 값이고
지어낸 기본값을 시드에 넣지 않는 것이 이 프로젝트의 원칙이다.
"""

import argparse
import json
import sys
from pathlib import Path

from liquipedia_client import LiquipediaClient, use_utf8_output

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# LPDB 응답 → 시드 스키마 매핑.
#
# 주의: 이 이름들은 실제 응답으로 확인하기 전까지 추정이다. 키를 받은 뒤
# --dump-fields 로 진짜 필드명을 보고 여기를 먼저 고칠 것.
# 각 항목은 후보 목록이며 응답에 있는 첫 번째 키를 쓴다.
# ---------------------------------------------------------------------------
TEAM_NAME_KEYS = ["name", "pagename", "team"]
TEAM_TAG_KEYS = ["shortname", "abbreviation", "template"]
TEAM_LOGO_KEYS = ["logourl", "imageurl", "image", "logo"]
TEAM_REGION_KEYS = ["region", "locations", "location"]

PLAYER_NICK_KEYS = ["id", "name", "pagename"]
PLAYER_REAL_KEYS = ["nationalityromanized", "romanizedname", "name"]
PLAYER_TEAM_KEYS = ["team", "teampagename"]
PLAYER_ROLE_KEYS = ["position", "role"]


def pick(row, keys):
    """후보 키 중 값이 있는 첫 번째를 돌려준다. 없으면 None."""
    for k in keys:
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
        if isinstance(v, (int, float)):
            return v
    return None


def quote_or(field, values):
    """LPDB 조건식의 OR 묶음. [[team::A]] OR [[team::B]] ..."""
    return " OR ".join("[[%s::%s]]" % (field, v) for v in values)


def fetch_participants(client, page, limit):
    """대회 문서의 참가팀 목록을 placement 데이터포인트에서 뽑는다."""
    rows = client.query("placement", conditions="[[pagename::%s]]" % page, limit=limit)
    names, seen = [], set()
    for r in rows:
        n = pick(r, ["opponentname", "participant", "team", "name"])
        if n and n not in seen:
            seen.add(n)
            names.append(n)
    return names, rows


def fetch_rosters(client, team_names, batch=8):
    """팀별 현역 로스터. 호출 수를 아끼려고 OR 조건으로 묶어서 보낸다."""
    by_team = {}
    for i in range(0, len(team_names), batch):
        chunk = team_names[i:i + batch]
        cond = "(%s) AND [[status::active]]" % quote_or("team", chunk)
        rows = client.query("squadplayer", conditions=cond, limit=200)
        for r in rows:
            team = pick(r, PLAYER_TEAM_KEYS)
            nick = pick(r, PLAYER_NICK_KEYS)
            if not team or not nick:
                continue
            by_team.setdefault(team, []).append({
                "nickname": nick,
                "realName": pick(r, PLAYER_REAL_KEYS),
                "role": pick(r, PLAYER_ROLE_KEYS) or "Player",
            })
    return by_team


def fetch_team_meta(client, team_names, batch=8):
    meta = {}
    for i in range(0, len(team_names), batch):
        chunk = team_names[i:i + batch]
        rows = client.query("team", conditions=quote_or("name", chunk), limit=200)
        for r in rows:
            n = pick(r, TEAM_NAME_KEYS)
            if n:
                meta[n] = r
    return meta


def build(args, client):
    names, raw = fetch_participants(client, args.page, args.limit)
    if not names:
        raise SystemExit(
            "참가팀을 찾지 못했습니다. --dump-fields 로 응답을 먼저 확인하세요.\n"
            "문서명: %s" % args.page)

    seed_map = {}
    if args.seed_map:
        raw_map = json.loads(Path(args.seed_map).read_text(encoding="utf-8"))
        # 밑줄로 시작하는 키는 설명용 메모다.
        seed_map = {k: v for k, v in raw_map.items() if not k.startswith("_")}
        missing = [n for n in seed_map if n not in names]
        if missing:
            # 이름 표기가 다르면 조용히 빠지므로 반드시 알린다.
            print("경고: seed-map 에 있지만 참가자 목록에 없는 팀 %d개: %s" % (len(missing), missing))
        if args.only_mapped:
            names = [n for n in names if n in seed_map]

    rosters = fetch_rosters(client, names)
    meta = fetch_team_meta(client, names)

    teams = []
    for n in names:
        m = meta.get(n, {})
        teams.append({
            "name": pick(m, TEAM_NAME_KEYS) or n,
            "tag": pick(m, TEAM_TAG_KEYS),
            # seedType 은 대회 구조를 사람이 판단해서 넣는다. 자동으로 정하지 않는다.
            "seedType": seed_map.get(n, args.seed_type),
            "logoUrl": pick(m, TEAM_LOGO_KEYS),
            "league": args.league,
            "region": pick(m, TEAM_REGION_KEYS) or args.region,
            # 트로피는 수집하지 않는다. 팀 페이지의 1위 기록을 사람이 확인해서 채운다.
            "trophies": [],
            "players": rosters.get(n, []),
        })
    return teams, raw


def main():
    use_utf8_output()
    ap = argparse.ArgumentParser(description="리그 시드 초안 생성")
    ap.add_argument("--page", required=True, help="리퀴피디아 대회 문서명")
    ap.add_argument("--league", help="시드에 기록할 리그 코드 (PCL 등)")
    ap.add_argument("--region", default=None, help="팀 지역 기본값 (CN 등)")
    ap.add_argument("--seed-type", default=None,
                    help="seed-map 에 없는 팀의 seedType. pro/amateur 만 화면에 나온다")
    ap.add_argument("--seed-map", default=None, help="팀명→seedType JSON")
    ap.add_argument("--only-mapped", action="store_true",
                    help="seed-map 에 있는 팀만 시드에 넣는다 (예: PCL 은 Stage S 24팀만)")
    ap.add_argument("--out", default=None, help="초안 출력 경로")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--wiki", default="pubg")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--dump-fields", action="store_true",
                    help="매핑하지 않고 응답 원본의 키만 보여준다")
    args = ap.parse_args()

    client = LiquipediaClient(wiki=args.wiki, offline=args.offline)

    if args.dump_fields:
        for dp, cond in (("placement", "[[pagename::%s]]" % args.page),
                         ("squadplayer", None),
                         ("team", None)):
            rows = client.query(dp, conditions=cond, limit=2)
            print("=== %s: %d건 ===" % (dp, len(rows)))
            if rows:
                print("키: %s" % sorted(rows[0].keys()))
                print(json.dumps(rows[0], ensure_ascii=False, indent=2)[:2000])
            print()
        print("남은 호출 %d회" % client.remaining_calls())
        return 0

    if not args.league:
        raise SystemExit("--league 가 필요합니다.")

    teams, _ = build(args, client)
    out = args.out or (PROJECT_ROOT / "intermediate_results" /
                       ("%s_seed_draft.json" % args.league.lower()))
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(teams, ensure_ascii=False, indent=2), encoding="utf-8")

    print("초안 %d팀 → %s" % (len(teams), out))
    print("남은 호출 %d회" % client.remaining_calls())
    print("\n다음: python ingest/verify_seed.py %s --compare-league %s" % (out, args.league))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
