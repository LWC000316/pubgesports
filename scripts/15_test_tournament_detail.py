import os
import urllib.request
import json
import ssl

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것
tournament_id = "as-pgs9gf"
url = f"https://api.pubg.com/tournaments/{tournament_id}"

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

print(f"Tournament {tournament_id} Data:")
matches = data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
print(f"Associated Matches count: {len(matches)}")
if matches:
    print(f"First 3 match IDs: {[m.get('id') for m in matches[:3]]}")
