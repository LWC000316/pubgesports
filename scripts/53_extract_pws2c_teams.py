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

all_teams = set()
circuits = ["kr-pws2c1", "kr-pws2c2", "kr-pws2c3", "kr-pws2c4", "kr-pws2c5"]

for cid in circuits:
    url = f"https://api.pubg.com/tournaments/{cid}"
    req = urllib.request.Request(url, headers=headers)
    try:
        t_data = fetch_with_retry(req, ctx)
        matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
        if matches:
            m_id = matches[0].get("id")
            m_url = f"https://api.pubg.com/shards/tournament/matches/{m_id}"
            time.sleep(1.0)
            req_m = urllib.request.Request(m_url, headers=headers)
            m_data = fetch_with_retry(req_m, ctx)
            for item in m_data.get("included", []):
                if item.get("type") == "participant":
                    name = item.get("attributes", {}).get("stats", {}).get("name", "")
                    if "_" in name:
                        tag = name.split("_")[0]
                        all_teams.add(tag)
                    elif " " in name:
                        tag = name.split(" ")[0]
                        all_teams.add(tag)
        print(f"[{cid}] 누적 추출 팀 수: {len(all_teams)}")
    except Exception as e:
        print(f"[{cid}] 에러: {e}")

print("PWS 서킷 전체 참여 팀 목록:")
for t in sorted(list(all_teams)):
    print(t)
