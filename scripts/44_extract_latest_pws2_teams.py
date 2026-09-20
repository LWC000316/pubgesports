import urllib.request
import json
import ssl
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

# kr-pws2 토너먼트 조회
target_tournaments = ["kr-pws2c5", "kr-pws2c4", "kr-pws2c3", "kr-pws2c2", "kr-pws2c1", "kr-pws2f"]

pws2_matches = []
for t_id in target_tournaments:
    url = f"https://api.pubg.com/tournaments/{t_id}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            t_data = json.loads(res.read().decode("utf-8"))
            matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
            print(f"{t_id}: 매치 수 {len(matches)}")
            if matches:
                pws2_matches.extend([m.get("id") for m in matches])
    except Exception as e:
        print(f"{t_id} 조회 실패: {e}")

print(f"발견된 PWS 2 매치 총 수: {len(pws2_matches)}")

# 최신 매치 1~2개에서 팀 및 선수 명단 추출
teams_found = {}
sample_matches = pws2_matches[:3]

for m_id in sample_matches:
    m_url = f"https://api.pubg.com/shards/tournament/matches/{m_id}"
    req = urllib.request.Request(m_url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            m_data = json.loads(res.read().decode("utf-8"))
            included = m_data.get("included", [])
            # roster 객체 탐색
            rosters = [item for item in included if item.get("type") == "roster"]
            participants = {p.get("id"): p.get("attributes", {}).get("stats", {}) for p in included if p.get("type") == "participant"}
            
            for r in rosters:
                team_id = r.get("attributes", {}).get("stats", {}).get("teamId")
                rank = r.get("attributes", {}).get("stats", {}).get("rank")
                p_refs = r.get("relationships", {}).get("participants", {}).get("data", [])
                p_names = []
                for pr in p_refs:
                    p_stat = participants.get(pr.get("id"), {})
                    p_name = p_stat.get("name")
                    if p_name:
                        p_names.append(p_name)
                
                # 팀명 추출 (선수 닉네임의 접두사 등에서 팀명 판별)
                if p_names:
                    sample_name = p_names[0]
                    team_tag = sample_name.split("_")[0] if "_" in sample_name else "Team"
                    if team_tag not in teams_found:
                        teams_found[team_tag] = {
                            "teamTag": team_tag,
                            "teamId": team_id,
                            "players": set(p_names)
                        }
                    else:
                        teams_found[team_tag]["players"].update(p_names)
    except Exception as e:
        print(f"매치 {m_id} 조회 실패: {e}")

result = []
for k, v in teams_found.items():
    result.append({
        "teamTag": v["teamTag"],
        "players": sorted(list(v["players"]))
    })

print(f"추출된 PWS 2 팀 목록 ({len(result)}개):")
for t in result:
    print(f" - {t['teamTag']}: {t['players']}")

with open("intermediate_results/latest_pws2_teams_raw.json", "w", encoding="utf-8") as out:
    json.dump(result, out, ensure_ascii=False, indent=2)
