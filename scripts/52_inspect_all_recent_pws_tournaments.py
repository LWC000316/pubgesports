import urllib.request
import json
import ssl

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
with urllib.request.urlopen(req, context=ctx) as res:
    data = json.loads(res.read().decode("utf-8"))

tournaments = data.get("data", [])
pws_2026 = []
for t in tournaments:
    tid = t.get("id", "")
    if "pws" in tid.lower() and ("pws2" in tid.lower() or "pws" in tid.lower()):
        pws_2026.append(tid)

print(f"전체 토너먼트 중 PWS 관련 토너먼트 상위 40개:")
for t in pws_2026[:40]:
    print(" ", t)
