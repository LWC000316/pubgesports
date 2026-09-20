import os
import urllib.request
import json
import ssl

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것
match_id = "15b203fc-c696-4f59-9f78-f486ab113d81"
url = f"https://api.pubg.com/shards/tournament/matches/{match_id}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as res:
    data = json.loads(res.read().decode("utf-8"))

print(f"Match {match_id} Success!")
included = data.get("included", [])

# 참가 팀 및 선수 스탯 파싱
rosters = [item for item in included if item.get("type") == "roster"]
participants = [item for item in included if item.get("type") == "participant"]

print(f"Total Teams (Rosters) in Match: {len(rosters)}")
print(f"Total Players (Participants) in Match: {len(participants)}")

# 1위 팀 및 상위 선수 샘플 출력
for r in rosters[:3]:
    stats = r.get("attributes", {}).get("stats", {})
    print(f" - Team Rank: #{stats.get('rank')}, Won: {stats.get('won')}, Team ID: {stats.get('teamId')}")

for p in participants[:5]:
    p_stats = p.get("attributes", {}).get("stats", {})
    print(f" * Player: {p_stats.get('name')}, Kills: {p_stats.get('kills')}, Damage: {p_stats.get('damageDealt')}, Headshots: {p_stats.get('headshotKills')}")
