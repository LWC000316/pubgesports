import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

print("=== 1. Testing pubgesports.com ===")
urls_to_test = [
    "https://pubgesports.com/ko/tournament",
    "https://pubgesports.com/api/v1/tournaments",
    "https://pubgesports.com/api/v1/teams",
    "https://api.pubgesports.com/v1/tournaments",
    "https://api.pubgesports.com/v1/teams"
]

for url in urls_to_test:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            status = response.getcode()
            content_type = response.headers.get('Content-Type', '')
            content = response.read(500).decode('utf-8', errors='ignore')
            print(f"[SUCCESS] {url} -> Status: {status}, Type: {content_type}")
            print(f"Preview: {content[:150]}...\n")
    except Exception as e:
        print(f"[FAILED] {url} -> {e}")

print("=== 2. Testing twire.gg ===")
twire_urls = [
    "https://twire.gg/en/pubg/tournaments",
    "https://api.twire.gg/v1/tournaments",
    "https://api.twire.gg/tournaments"
]
for url in twire_urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            status = response.getcode()
            content_type = response.headers.get('Content-Type', '')
            content = response.read(500).decode('utf-8', errors='ignore')
            print(f"[SUCCESS] {url} -> Status: {status}, Type: {content_type}")
            print(f"Preview: {content[:150]}...\n")
    except Exception as e:
        print(f"[FAILED] {url} -> {e}")
