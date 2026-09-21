"""
시드 초안 검사기.

수집 스크립트가 만든 초안을 그대로 믿지 않기 위한 도구다. 네트워크를 쓰지 않으며
다음 네 가지를 본다.

  1. 스키마    DataInitializer 가 읽는 키가 다 있는가, seedType/league 가 유효한가
  2. 플레이스홀더  지어낸 값이 섞여 있는가 (placeholder 로고, "Pro <닉>" 본명, 전원 동일 세팅)
  3. 로스터    인원이 기대치와 다른 팀
  4. 차이      레거시/기존 시드와 팀 구성이 어떻게 다른가

사용
  python ingest/verify_seed.py primary_data/pws2_teams_verified.json
  python ingest/verify_seed.py primary_data/pcl_teams_verified.json --compare-league PCL
"""

import argparse
import json
from collections import Counter
from pathlib import Path

from liquipedia_client import use_utf8_output

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEGACY_SEED = PROJECT_ROOT / "primary_data" / "official_teams_and_rosters.json"

# DataInitializer.loadVerifiedTeams 가 실제로 읽는 키.
REQUIRED_TEAM_KEYS = ["name", "tag", "seedType", "logoUrl", "league", "region"]
VALID_SEED_TYPES = {"pro", "amateur"}

# LeagueTeamGrid.jsx 는 seedType 이 pro/amateur 인 팀만 그린다.
# 그 외 값은 어느 구획에도 들어가지 못해 화면에서 사라진다.


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_schema(teams):
    problems = []
    seen = {}
    for i, t in enumerate(teams):
        label = t.get("name") or "#%d (name 없음)" % i
        for key in REQUIRED_TEAM_KEYS:
            if key not in t:
                problems.append("%s: '%s' 키 없음" % (label, key))
        if not t.get("name"):
            problems.append("#%d: name 이 비어 있음 (적재되지 않는다)" % i)
        if not t.get("league"):
            problems.append("%s: league 가 비어 있음 (적재에서 건너뛴다)" % label)
        st = t.get("seedType")
        if st not in VALID_SEED_TYPES:
            problems.append(
                "%s: seedType 이 '%s' - pro/amateur 가 아니면 화면에 안 나온다" % (label, st))
        key = (t.get("name") or "").lower()
        if key in seen:
            problems.append("%s: 팀명 중복 (Team.name 은 unique 제약)" % label)
        seen[key] = True
    return problems


def check_placeholders(teams):
    warnings = []
    all_players = [(t.get("name"), p) for t in teams for p in (t.get("players") or [])]

    for t in teams:
        logo = t.get("logoUrl") or ""
        if "placeholder" in logo.lower():
            warnings.append("%s: 로고가 플레이스홀더 (%s)" % (t.get("name"), logo))
        elif logo.startswith("http"):
            warnings.append("%s: 로고가 외부 URL - 로컬 파일로 내려받아야 한다 (%s)"
                            % (t.get("name"), logo))

    templated = [n for n, p in all_players
                 if p.get("realName") == "Pro %s" % p.get("nickname")]
    if templated:
        warnings.append("realName 이 'Pro <닉네임>' 템플릿인 선수 %d명" % len(templated))

    for field in ("mouseDpi", "generalSens", "mouseName"):
        values = [p.get(field) for _, p in all_players if p.get(field) is not None]
        if not values:
            continue
        counts = Counter(values)
        top, n = counts.most_common(1)[0]
        if len(values) >= 8 and n == len(values):
            warnings.append(
                "%s 가 %d명 전원 동일한 값(%s) - 실측이 아니라 기본값일 가능성이 높다"
                % (field, n, top))
    return warnings


def check_rosters(teams, expected):
    rows = []
    for t in teams:
        n = len(t.get("players") or [])
        if n != expected:
            rows.append((t.get("name"), n))
    return rows


def diff_against_legacy(teams, league):
    if not LEGACY_SEED.exists():
        return None
    legacy = [t for t in load(LEGACY_SEED) if (t.get("league") or "").upper() == league.upper()]
    if not legacy:
        return None
    new_names = {t.get("name") for t in teams}
    old_names = {t.get("name") for t in legacy}
    return {
        "legacy_count": len(legacy),
        "draft_count": len(teams),
        "only_in_draft": sorted(new_names - old_names),
        "only_in_legacy": sorted(old_names - new_names),
        "in_both": sorted(new_names & old_names),
    }


def main():
    use_utf8_output()
    ap = argparse.ArgumentParser(description="시드 초안을 검사한다")
    ap.add_argument("seed", help="검사할 시드 JSON 경로")
    ap.add_argument("--compare-league", default=None,
                    help="레거시 시드의 이 리그와 팀 구성을 비교한다 (예: PCL)")
    ap.add_argument("--roster-size", type=int, default=4, help="팀당 기대 인원 (기본 4)")
    args = ap.parse_args()

    teams = load(args.seed)
    if not isinstance(teams, list):
        raise SystemExit("최상위가 배열이 아닙니다. DataInitializer 가 읽지 못합니다.")

    print("=== %s ===" % args.seed)
    print("팀 %d개, 선수 %d명"
          % (len(teams), sum(len(t.get("players") or []) for t in teams)))
    by_seed = Counter(t.get("seedType") for t in teams)
    print("seedType: %s" % dict(by_seed))
    print("league: %s" % dict(Counter(t.get("league") for t in teams)))
    print("트로피 보유 팀: %d개" % sum(1 for t in teams if t.get("trophies")))

    problems = check_schema(teams)
    print("\n[1] 스키마 - %s" % ("이상 없음" if not problems else "%d건" % len(problems)))
    for p in problems:
        print("  X %s" % p)

    warnings = check_placeholders(teams)
    print("\n[2] 플레이스홀더 - %s" % ("이상 없음" if not warnings else "%d건" % len(warnings)))
    for w in warnings:
        print("  ! %s" % w)

    odd = check_rosters(teams, args.roster_size)
    print("\n[3] 로스터 인원 %d명이 아닌 팀 - %d개" % (args.roster_size, len(odd)))
    for name, n in odd:
        print("  - %s: %d명" % (name, n))

    league = args.compare_league
    if league is None and teams:
        league = teams[0].get("league")
    d = diff_against_legacy(teams, league) if league else None
    print("\n[4] 레거시 %s 비교" % league)
    if not d:
        print("  비교할 레거시 데이터가 없습니다.")
    else:
        print("  레거시 %d팀 / 초안 %d팀, 공통 %d팀"
              % (d["legacy_count"], d["draft_count"], len(d["in_both"])))
        print("  초안에만 있음 (%d): %s" % (len(d["only_in_draft"]), d["only_in_draft"]))
        print("  레거시에만 있음 (%d): %s" % (len(d["only_in_legacy"]), d["only_in_legacy"]))

    print("\n검사는 형식만 본다. 팀명·로스터·트로피가 맞는지는 리퀴피디아 원문과 대조해야 한다.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
