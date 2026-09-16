import urllib.request
import json
import ssl
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

qx_stats = {
    "Qx_Glance": {"kills": 0, "damage": 0.0, "matches": 0},
    "Qx_Hyuk": {"kills": 0, "damage": 0.0, "matches": 0},
    "Qx_LOV3": {"kills": 0, "damage": 0.0, "matches": 0},
    "Qx_youth": {"kills": 0, "damage": 0.0, "matches": 0}
}

circuits = ["kr-pws2c5", "kr-pws2c4"]

for cid in circuits:
    url = f"https://api.pubg.com/tournaments/{cid}"
    req = urllib.request.Request(url, headers=headers)
    try:
        t_data = fetch_with_retry(req, ctx)
        matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
        for m in matches[:3]:
            m_id = m.get("id")
            m_url = f"https://api.pubg.com/shards/tournament/matches/{m_id}"
            time.sleep(0.7)
            req_m = urllib.request.Request(m_url, headers=headers)
            m_data = fetch_with_retry(req_m, ctx)
            for item in m_data.get("included", []):
                if item.get("type") == "participant":
                    name = item.get("attributes", {}).get("stats", {}).get("name", "")
                    if name in qx_stats:
                        st = item.get("attributes", {}).get("stats", {})
                        qx_stats[name]["kills"] += st.get("kills", 0)
                        qx_stats[name]["damage"] += st.get("damageDealt", 0.0)
                        qx_stats[name]["matches"] += 1
    except Exception as e:
        print(f"[{cid}] 에러: {e}")

for k, v in qx_stats.items():
    v["damage"] = round(v["damage"], 1)

print("=== Qx 팀 선수별 스탯 요약 ===")
for p, s in qx_stats.items():
    print(f"{p}: {s['matches']}매치, {s['kills']}킬, {s['damage']}데미지")

with open("intermediate_results/qx_detailed_stats.json", "w", encoding="utf-8") as f:
    json.dump(qx_stats, f, ensure_ascii=False, indent=2)
