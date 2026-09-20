import urllib.request
import json
import ssl
import time
import os

os.makedirs("primary_data", exist_ok=True)
os.makedirs("secondary_data", exist_ok=True)

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. 크래프톤 공식 API에서 실제 주요 토너먼트(PGS 9 등)의 매치 데이터 호출
target_tournament_id = "as-pgs9gf"
url = f"https://api.pubg.com/tournaments/{target_tournament_id}"

print(f"=== 1. 공식 API 토너먼트 ({target_tournament_id}) 매치 목록 조회 ===")
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as res:
    t_data = json.loads(res.read().decode("utf-8"))

match_ids = [m.get("id") for m in t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])]
print(f"총 {len(match_ids)}개 매치 확인. (Rate limit 보호를 위해 3개 매치 표본 파싱)")

# 2. 매치 데이터를 직접 조회하여 실제 참가 팀 및 선수 닉네임 동적 추출
extracted_players = {}
extracted_teams = {}

for match_id in match_ids[:3]:
    match_url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"
    print(f"\n[API 호출] 매치 ID: {match_id}")
    
    try:
        m_req = urllib.request.Request(match_url, headers=headers)
        with urllib.request.urlopen(m_req, context=ctx) as m_res:
            m_data = json.loads(m_res.read().decode("utf-8"))
            
            # primary_data에 원본 매치 응답 저장
            with open(f"primary_data/api_match_{match_id}.json", "w", encoding="utf-8") as f:
                json.dump(m_data, f, ensure_ascii=False, indent=2)
                
            included = m_data.get("included", [])
            
            # participant (선수) 및 roster (팀) 파싱
            for item in included:
                if item.get("type") == "participant":
                    p_id = item.get("id")
                    stats = item.get("attributes", {}).get("stats", {})
                    name = stats.get("name", "")
                    
                    if name:
                        extracted_players[p_id] = {
                            "name": name,
                            "kills": stats.get("kills", 0),
                            "damage": stats.get("damageDealt", 0),
                            "headshots": stats.get("headshotKills", 0)
                        }
                        
            for item in included:
                if item.get("type") == "roster":
                    r_stats = item.get("attributes", {}).get("stats", {})
                    team_id = r_stats.get("teamId")
                    rank = r_stats.get("rank")
                    
                    # 소속 선수 ID 매핑
                    p_refs = [p.get("id") for p in item.get("relationships", {}).get("participants", {}).get("data", [])]
                    roster_players = [extracted_players.get(pid, {}).get("name") for pid in p_refs if pid in extracted_players]
                    
                    if team_id not in extracted_teams:
                        extracted_teams[team_id] = {
                            "teamId": team_id,
                            "rank": rank,
                            "players": roster_players
                        }
                    else:
                        # 신규 발견 선수 병합
                        for p_name in roster_players:
                            if p_name and p_name not in extracted_teams[team_id]["players"]:
                                extracted_teams[team_id]["players"].append(p_name)
                                
        time.sleep(1.5) # 10 RPM 준수
    except Exception as e:
        print(f"매치 파싱 에러: {e}")

print("\n=== [공식 API 직접 추출 결과] ===")
print(f"공식 API에서 추출된 총 팀 수: {len(extracted_teams)}")
print(f"공식 API에서 추출된 총 선수 수: {len(extracted_players)}")

print("\n--- 실제 추출된 팀별 선수 로스터 (공식 API 원본) ---")
for tid, tinfo in list(extracted_teams.items())[:10]:
    print(f" * Team #{tid} (Rank #{tinfo['rank']}): {', '.join(tinfo['players'])}")

# secondary_data에 추출된 원시 로스터 저장
with open("secondary_data/api_extracted_rosters.json", "w", encoding="utf-8") as f:
    json.dump(extracted_teams, f, ensure_ascii=False, indent=2)

print("\nSaved secondary_data/api_extracted_rosters.json")
