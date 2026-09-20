import urllib.request
import json
import ssl
import os

os.makedirs("primary_data", exist_ok=True)
os.makedirs("secondary_data", exist_ok=True)

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것
url = "https://api.pubg.com/tournaments"

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

# 1. Primary Data 저장
with open("primary_data/pubg_official_tournaments_all.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

tournaments = data.get("data", [])
print(f"Total Tournaments: {len(tournaments)}")

# PWS, PCL, PGS, PGC, PNC, EWC 키워드 매칭
keywords = ["pws", "pcl", "pgs", "pgc", "pnc", "ewc"]
filtered = []
for t in tournaments:
    t_id = t.get("id", "").lower()
    for kw in keywords:
        if kw in t_id:
            filtered.append({"id": t.get("id"), "keyword": kw.upper()})
            break

print(f"\nFiltered Target Tournaments: {len(filtered)}")
for item in filtered[:25]:
    print(f" - [{item['keyword']}] {item['id']}")

# Secondary Data 저장
with open("secondary_data/filtered_major_tournaments.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)
