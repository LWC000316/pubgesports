import os
import urllib.request
import json
import ssl
import re

os.makedirs("primary_data", exist_ok=True)
os.makedirs("secondary_data", exist_ok=True)
os.makedirs("intermediate_results", exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

url = "https://pubgesports.com/ko/tournament?YEAR=2024&REGION_TYPE=ALL"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as res:
    html = res.read().decode('utf-8', errors='ignore')

with open("primary_data/pubgesports_tournament_2024.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Saved primary_data/pubgesports_tournament_2024.html (Length:", len(html), ")")

# 토너먼트 ID 및 이름 추출
# Nuxt 데이터 파싱
tournament_matches = re.findall(r'(\/ko\/tournament\/[0-9]+)', html)
print(f"Found tournament IDs: {set(tournament_matches)}")
