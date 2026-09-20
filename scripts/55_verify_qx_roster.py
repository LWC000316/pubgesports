import os
import urllib.request
import json
import ssl
import time

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

qx_players = {}
circuits = ["kr-pws2c5", "kr-pws2c4", "kr-pws2c3"]

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
                    if name.upper().startswith("QX_") or name.upper().startswith("QX ") or name.upper().startswith("QX-"):
                        if name not in qx_players:
                            qx_players[name] = 0
                        qx_players[name] += 1
    except Exception as e:
        print(f"[{cid}] 에러: {e}")

print("=== Qx 전체 선수 및 출전 매치 수 ===")
for p, cnt in sorted(qx_players.items()):
    print(f" - {p}: {cnt}회 출전")

with open("intermediate_results/qx_roster.json", "w", encoding="utf-8") as f:
    json.dump(list(qx_players.keys()), f, ensure_ascii=False, indent=2)
