import urllib.request
import json
import ssl

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNjM4MjBkMC04NGRjLTAxM2YtNjgxMS03ZTUyYjRmOWRlYzkiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzg3OTAwNzgyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InB1Ymdlc3BvcnRzX3NlIn0.m7No-1f2HTUil7JUfTyAF0CdpXbYqCPHsEWI4u8Fc4I"

headers = {
    "Authorization": "Bearer " + api_key,
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# kr-pws2f 토너먼트 조회
url = "https://api.pubg.com/tournaments/kr-pws2f"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as res:
    t_data = json.loads(res.read().decode("utf-8"))

matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
print(f"kr-pws2f 매치 수: {len(matches)}")

teams_found = {}
# 마지막 매치 2개 조회
for m in matches[-2:]:
    m_id = m.get("id")
    m_url = f"https://api.pubg.com/shards/tournament/matches/{m_id}"
    req2 = urllib.request.Request(m_url, headers=headers)
    with urllib.request.urlopen(req2, context=ctx) as res2:
        m_data = json.loads(res2.read().decode("utf-8"))
        included = m_data.get("included", [])
        rosters = [item for item in included if item.get("type") == "roster"]
        participants = {p.get("id"): p.get("attributes", {}).get("stats", {}) for p in included if p.get("type") == "participant"}
        
        for r in rosters:
            rank = r.get("attributes", {}).get("stats", {}).get("rank")
            team_id = r.get("attributes", {}).get("stats", {}).get("teamId")
            p_refs = r.get("relationships", {}).get("participants", {}).get("data", [])
            p_names = [participants.get(pr.get("id"), {}).get("name") for pr in p_refs if participants.get(pr.get("id"), {}).get("name")]
            if p_names:
                tag = p_names[0].split("_")[0] if "_" in p_names[0] else "TEAM"
                if tag not in teams_found:
                    teams_found[tag] = {
                        "tag": tag,
                        "rank": rank,
                        "players": set(p_names)
                    }
                else:
                    teams_found[tag]["players"].update(p_names)

res_list = []
for k, v in teams_found.items():
    res_list.append({
        "tag": v["tag"],
        "rank": v["rank"],
        "players": sorted(list(v["players"]))
    })

res_list.sort(key=lambda x: x["rank"] if x["rank"] is not None else 99)

print(f"PWS 2 파이널 공식 16개 참가팀:")
for t in res_list:
    print(f" #{t['rank']} [{t['tag']}] 로스터: {t['players']}")

with open("intermediate_results/pws2_final_16_teams.json", "w", encoding="utf-8") as out:
    json.dump(res_list, out, ensure_ascii=False, indent=2)
