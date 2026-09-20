import os
import urllib.request
import json
import ssl

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것

endpoints = [
    "https://api.pubg.com/tournaments",
    "https://api.pubg.com/shards/steam/tournaments",
    "https://api.pubg.com/shards/kakao/tournaments",
    "https://api.pubg.com/status"
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for url in endpoints:
    print(f"\n--- Testing: {url} ---")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as res:
            print(f"[SUCCESS] Status: {res.getcode()}")
            body = res.read().decode("utf-8")
            data = json.loads(body)
            data_items = data.get("data", [])
            print(f"Items count: {len(data_items) if isinstance(data_items, list) else data_items}")
            if isinstance(data_items, list) and len(data_items) > 0:
                print("First 3 items:", [d.get("id") for d in data_items[:3]])
    except urllib.error.HTTPError as e:
        print(f"[FAIL] HTTP {e.code}: {e.read().decode('utf-8')[:200]}")
    except Exception as e:
        print(f"[ERROR]: {e}")
