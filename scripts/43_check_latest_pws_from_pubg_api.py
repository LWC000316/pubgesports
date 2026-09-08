import urllib.request
import json
import ssl
import os

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNjM4MjBkMC04NGRjLTAxM2YtNjgxMS03ZTUyYjRmOWRlYzkiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzg3OTAwNzgyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InB1Ymdlc3BvcnRzX3NlIn0.m7No-1f2HTUil7JUfTyAF0CdpXbYqCPHsEWI4u8Fc4I"
url = "https://api.pubg.com/tournaments"

headers = {
    "Authorization": "Bearer " + api_key,
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as res:
        data = json.loads(res.read().decode("utf-8"))
except Exception as e:
    print("API 에러:", e)
    data = {"data": []}

tournaments = data.get("data", [])
pws_list = [t.get("id") for t in tournaments if "pws" in t.get("id", "").lower()]

print("총 토너먼트 수:", len(tournaments))
print("PWS 관련 토너먼트 수:", len(pws_list))
print("PWS 토너먼트 ID 목록 (최근 순):")
for p in pws_list:
    print(" ", p)

with open("intermediate_results/pws_tournaments_list.json", "w", encoding="utf-8") as f:
    json.dump(pws_list, f, ensure_ascii=False, indent=2)
