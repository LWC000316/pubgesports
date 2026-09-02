import urllib.request
import json
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

# twire.gg의 주요 엔드포인트 탐색
# 1. Twire tournament leaderboard
twire_urls = [
    "https://twire.gg/api/v1/tournaments",
    "https://twire.gg/api/tournament",
    "https://api.twire.gg/v1/pubg/tournaments",
    "https://twire.gg/en/pubg/tournaments/pgs-4-2024",
    "https://twire.gg/en/pubg/teams"
]

print("=== Testing Twire.gg URLs ===")
for url in twire_urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as res:
            print(f"[SUCCESS] {url} -> Status: {res.getcode()}, Content-Type: {res.headers.get('Content-Type')}")
            content = res.read(300).decode('utf-8', errors='ignore')
            print("Preview:", content[:150], "\n")
    except Exception as e:
        print(f"[FAIL] {url} -> {e}")
