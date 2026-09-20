import urllib.request
import json
import ssl
import os

os.makedirs("primary_data", exist_ok=True)
os.makedirs("secondary_data", exist_ok=True)

api_key = os.environ["PUBG_API_KEY"]  # 환경변수로 주입한다. 키를 코드에 적지 말 것

url = "https://api.pubg.com/shards/tournament/tournaments"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print(f"=== Calling Official PUBG Developer API ({url}) ===")
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as res:
        status = res.getcode()
        body = res.read().decode("utf-8")
        data = json.loads(body)
        
        print(f"[SUCCESS] Status Code: {status}")
        
        # primary_data에 원본 API 응답 저장
        with open("primary_data/official_pubg_api_tournaments.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        tournaments = data.get("data", [])
        print(f"Total Official Tournaments retrieved: {len(tournaments)}")
        
        # PWS, PCL, PGS, PGC, PNC, EWC 관련 토너먼트 필터링 확인
        keywords = ["PWS", "PCL", "PGS", "PGC", "PNC", "EWC"]
        matched = []
        for t in tournaments:
            t_id = t.get("id", "")
            if any(k.lower() in t_id.lower() for k in keywords):
                matched.append(t_id)
                
        print(f"\nMatched Key Tournaments ({len(matched)}):")
        for m in matched[:20]:
            print(f" * {m}")

except urllib.error.HTTPError as e:
    print(f"[HTTP ERROR] Code: {e.code}, Reason: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"[ERROR]: {e}")
