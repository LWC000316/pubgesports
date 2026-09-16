import urllib.request
import json
import ssl
import os
import time

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNjM4MjBkMC04NGRjLTAxM2YtNjgxMS03ZTUyYjRmOWRlYzkiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzg3OTAwNzgyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InB1Ymdlc3BvcnRzX3NlIn0.m7No-1f2HTUil7JUfTyAF0CdpXbYqCPHsEWI4u8Fc4I"

headers = {
    "Authorization": "Bearer " + api_key,
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

tournament_id = "kr-pws2s11"
url = f"https://api.pubg.com/tournaments/{tournament_id}"

def fetch_with_retry(request, context, max_retries=5):
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(request, context=context) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            if err.code == 429:
                wait_seconds = 6 * (attempt + 1)
                print(f"Rate limit 도달 (429). {wait_seconds}초 대기 후 재시도...")
                time.sleep(wait_seconds)
            else:
                raise err
    raise Exception("최대 재시도 횟수 초과")

req = urllib.request.Request(url, headers=headers)
t_data = fetch_with_retry(req, ctx)

os.makedirs("primary_data", exist_ok=True)
os.makedirs("intermediate_results", exist_ok=True)

with open(f"primary_data/tournament_{tournament_id}.json", "w", encoding="utf-8") as f:
    json.dump(t_data, f, ensure_ascii=False, indent=2)

matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
print(f"[{tournament_id}] 총 매치 수: {len(matches)}")

match_results = []
teams_dict = {}

for m_idx, m in enumerate(matches):
    m_id = m.get("id")
    m_url = f"https://api.pubg.com/shards/tournament/matches/{m_id}"
    print(f"매치 {m_idx + 1}/{len(matches)} 조회 중: {m_id}")
    time.sleep(1.0)
    
    req_m = urllib.request.Request(m_url, headers=headers)
    m_data = fetch_with_retry(req_m, ctx)
    
    with open(f"primary_data/match_{m_id}.json", "w", encoding="utf-8") as f:
        json.dump(m_data, f, ensure_ascii=False, indent=2)
        
    included = m_data.get("included", [])
    
    rosters = [item for item in included if item.get("type") == "roster"]
    participants = {item.get("id"): item.get("attributes", {}).get("stats", {}) for item in included if item.get("type") == "participant"}
    
    match_rosters = []
    for r in rosters:
        r_stats = r.get("attributes", {}).get("stats", {})
        r_rank = r_stats.get("rank")
        r_team_id = r_stats.get("teamId")
        
        p_ids = [p.get("id") for p in r.get("relationships", {}).get("participants", {}).get("data", [])]
        player_stats_list = []
        team_name_candidate = None
        
        for pid in p_ids:
            p_stat = participants.get(pid, {})
            name = p_stat.get("name", "")
            player_stats_list.append({
                "name": name,
                "kills": p_stat.get("kills", 0),
                "damage": round(p_stat.get("damageDealt", 0), 1)
            })
            if "_" in name:
                parts = name.split("_")
                team_name_candidate = parts[0]
            elif " " in name:
                parts = name.split(" ")
                team_name_candidate = parts[0]
        
        t_tag = team_name_candidate or f"Team_{r_team_id}"
        if t_tag not in teams_dict:
            teams_dict[t_tag] = set()
        for p in player_stats_list:
            teams_dict[t_tag].add(p["name"])
            
        match_rosters.append({
            "rank": r_rank,
            "teamTag": t_tag,
            "players": player_stats_list
        })
        
    match_results.append({
        "matchId": m_id,
        "createdAt": m_data.get("data", {}).get("attributes", {}).get("createdAt"),
        "rosters": match_rosters
    })

serializable_teams = {k: sorted(list(v)) for k, v in teams_dict.items()}

with open("intermediate_results/latest_pws_extracted_teams.json", "w", encoding="utf-8") as f:
    json.dump(serializable_teams, f, ensure_ascii=False, indent=2)

with open("intermediate_results/latest_pws_matches_summary.json", "w", encoding="utf-8") as f:
    json.dump(match_results, f, ensure_ascii=False, indent=2)

print("\n=== 최신 2026 PWS Phase 2 참가 팀 및 선수 명단 ===")
for t, pl in sorted(serializable_teams.items()):
    print(f"팀 [{t}] (선수 {len(pl)}명): {', '.join(pl)}")
