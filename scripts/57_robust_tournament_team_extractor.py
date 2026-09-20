import urllib.request
import json
import ssl
import time
import os

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것

headers = {
    "Authorization": "Bearer " + api_key,
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_with_retry(request, context, max_retries=5):
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(request, context=context) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            if err.code == 429:
                wait_seconds = 6 * (attempt + 1)
                time.sleep(wait_seconds)
            else:
                raise err
    raise Exception("최대 재시도 횟수 초과")

def extract_match_rosters(match_id):
    """단일 매치에서 참가팀 및 로스터를 추출하며, 이상 징후를 필터링하는 함수"""
    m_url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
    req_m = urllib.request.Request(m_url, headers=headers)
    m_data = fetch_with_retry(req_m, ctx)
    
    included = m_data.get("included", [])
    rosters = [item for item in included if item.get("type") == "roster"]
    participants = {
        item.get("id"): item.get("attributes", {}).get("stats", {})
        for item in included if item.get("type") == "participant"
    }
    
    # 이상 징후 검증: 일반적인 배틀그라운드 e스포츠는 매치당 16개 팀 참가
    team_count = len(rosters)
    is_valid_match = (14 <= team_count <= 16)
    
    match_teams = {}
    for r in rosters:
        r_stats = r.get("attributes", {}).get("stats", {})
        r_rank = r_stats.get("rank")
        p_ids = [p.get("id") for p in r.get("relationships", {}).get("participants", {}).get("data", [])]
        
        player_names = []
        team_tag = None
        for pid in p_ids:
            p_stat = participants.get(pid, {})
            name = p_stat.get("name", "")
            if name:
                player_names.append(name)
                if not team_tag:
                    if "_" in name:
                        team_tag = name.split("_")[0]
                    elif " " in name:
                        team_tag = name.split(" ")[0]
                        
        if not team_tag:
            team_tag = f"Unknown_{r_stats.get('teamId')}"
            
        match_teams[team_tag] = player_names
        
    return {
        "matchId": match_id,
        "teamCount": team_count,
        "isValid": is_valid_match,
        "teams": match_teams
    }

def get_tournament_teams(tournament_ids, max_target_teams=24):
    """
    여러 토너먼트 ID(Day 1, Day 2 등 또는 서킷 토너먼트)를 순회하며
    모든 팀이 출전할 때까지 누적(Union) 수집하는 메인 로직
    """
    total_accumulated_teams = {}
    verified_matches = 0
    anomaly_matches = 0
    
    for t_id in tournament_ids:
        print(f"\n[토너먼트 분석 시작] ID: {t_id}")
        t_url = f"https://api.pubg.com/tournaments/{t_id}"
        req_t = urllib.request.Request(t_url, headers=headers)
        try:
            t_data = fetch_with_retry(req_t, ctx)
        except Exception as e:
            print(f"토너먼트 {t_id} 조회 실패: {e}")
            continue
            
        matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
        print(f" - 등록된 매치 수: {len(matches)}")
        
        for m_info in matches:
            m_id = m_info.get("id")
            time.sleep(0.7)
            
            try:
                res = extract_match_rosters(m_id)
            except Exception as e:
                print(f"   - 매치 {m_id} 에러: {e}")
                continue
                
            # 이상 징후 필터링 검증
            if not res["isValid"]:
                print(f"   - [경고: 이상 징후 매치 제외] 매치 {m_id} (팀 수: {res['teamCount']})")
                anomaly_matches += 1
                continue
                
            verified_matches += 1
            for tag, players in res["teams"].items():
                if tag not in total_accumulated_teams:
                    total_accumulated_teams[tag] = set()
                for p in players:
                    total_accumulated_teams[tag].add(p)
                    
            print(f"   - 매치 {m_id[:8]} 완료 -> 현재 누적 수집 팀 수: {len(total_accumulated_teams)}팀")
            
            # 목표 팀 수(24팀)에 도달하면 조기 완료 가능
            if len(total_accumulated_teams) >= max_target_teams:
                print(f"   * 목표 팀 수({max_target_teams}팀) 수집 완료!")
                break
                
        if len(total_accumulated_teams) >= max_target_teams:
            break
            
    # 최종 직렬화 가능한 형태로 변환
    structured_result = []
    for tag in sorted(total_accumulated_teams.keys()):
        structured_result.append({
            "teamTag": tag,
            "playerCount": len(total_accumulated_teams[tag]),
            "players": sorted(list(total_accumulated_teams[tag]))
        })
        
    return {
        "totalTeamsCount": len(structured_result),
        "verifiedMatchesCount": verified_matches,
        "anomalyMatchesCount": anomaly_matches,
        "teams": structured_result
    }

if __name__ == "__main__":
    os.makedirs("intermediate_results", exist_ok=True)
    os.makedirs("secondary_data", exist_ok=True)
    
    # 본선 1일차(kr-pws2s11) + 본선 직전 최근 서킷 예선들(kr-pws2c5, kr-pws2c4)을 순차 누적
    # 2일차(kr-pws2s12)가 열리면 kr-pws2s12만 넣어도 24팀이 100% 자동 완성됨!
    target_tournaments = [
        "kr-pws2s11",
        "kr-pws2c5",
        "kr-pws2c4",
        "kr-pws2c3"
    ]
    
    print("=== 스마트 팀 추출 및 누적 파이프라인 가동 ===")
    result = get_tournament_teams(target_tournaments, max_target_teams=24)
    
    output_path = "secondary_data/pws_2026_phase2_all_teams.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print("\n==========================================")
    print(f"수집 완료: 총 {result['totalTeamsCount']}개 팀 확보")
    print(f"정상 검증 매치: {result['verifiedMatchesCount']}개, 이상 제외 매치: {result['anomalyMatchesCount']}개")
    print("==========================================")
    for idx, t in enumerate(result["teams"][:24], start=1):
        print(f"{idx:2d}. 팀 [{t['teamTag']}] (선수 {t['playerCount']}명): {', '.join(t['players'])}")
