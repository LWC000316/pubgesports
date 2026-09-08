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

# 1. kr-pws2f 매치 생성 일자 확인
url = "https://api.pubg.com/tournaments/kr-pws2f"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as res:
    t_data = json.loads(res.read().decode("utf-8"))

matches = t_data.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
sample_m_id = matches[0].get("id")

m_url = f"https://api.pubg.com/shards/tournament/matches/{sample_m_id}"
req2 = urllib.request.Request(m_url, headers=headers)
with urllib.request.urlopen(req2, context=ctx) as res2:
    m_data = json.loads(res2.read().decode("utf-8"))
    created_at = m_data.get("data", {}).get("attributes", {}).get("createdAt")

print(f"kr-pws2f 토너먼트의 실제 경기 일시: {created_at}")

# 2. 전체 PWS 토너먼트 중에서 가장 최근 날짜의 토너먼트 찾기
with open("intermediate_results/pws_tournaments_list.json", "r", encoding="utf-8") as f:
    pws_ids = json.load(f)

print(f"\nPWS 토너먼트 샘플 10개에 대해 경기 일시 샘플링 확인:")
for tid in pws_ids[:10]:
    try:
        t_url = f"https://api.pubg.com/tournaments/{tid}"
        req_t = urllib.request.Request(t_url, headers=headers)
        with urllib.request.urlopen(req_t, context=ctx) as r:
            td = json.loads(r.read().decode("utf-8"))
            ms = td.get("data", {}).get("relationships", {}).get("matches", {}).get("data", [])
            if ms:
                first_m = ms[0].get("id")
                m_url_check = f"https://api.pubg.com/shards/tournament/matches/{first_m}"
                req_m = urllib.request.Request(m_url_check, headers=headers)
                with urllib.request.urlopen(req_m, context=ctx) as rm:
                    md = json.loads(rm.read().decode("utf-8"))
                    dt = md.get("data", {}).get("attributes", {}).get("createdAt")
                    print(f" - [{tid}] 매치수: {len(ms)}, 일시: {dt}")
    except Exception as e:
        print(f" - [{tid}] 실패: {e}")
