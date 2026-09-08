import json
import os

with open("primary_data/official_teams_and_rosters.json", "r", encoding="utf-8") as f:
    official_data = json.load(f)

print(f"공식 팀 데이터 수: {len(official_data)}")

# PWS 또는 한국 관련 팀 필터링
pws_teams = []
for t in official_data:
    region = t.get("region", "")
    league = t.get("league", "")
    name = t.get("name", "")
    if region == "KR" or league == "PWS" or any(k in name.lower() for k in ["freecs", "danawa", "gen.g", "dplus", "t1", "azla", "gnl", "game pt"]):
        pws_teams.append({
            "name": t.get("name"),
            "koreanName": t.get("koreanName", t.get("name")),
            "logoUrl": t.get("logoUrl"),
            "region": region,
            "league": league,
            "players": [p.get("nickname") for p in t.get("players", [])]
        })

print(f"발견된 공식 PWS/한국 팀 수: {len(pws_teams)}")
for pt in pws_teams:
    print(f" - {pt['name']} ({pt['league']}): {pt['players']}")

with open("intermediate_results/official_pws_extracted.json", "w", encoding="utf-8") as out:
    json.dump(pws_teams, out, ensure_ascii=False, indent=2)
