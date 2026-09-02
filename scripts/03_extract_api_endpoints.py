import urllib.request
import re
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# 1. pubgesports.com JS 번들 내 API URL 검색
js_urls = [
    "https://wstatic-prod.pubgesports.com/web/live/main_da326b6/ec436bd.js",
    "https://wstatic-prod.pubgesports.com/web/live/main_da326b6/a712525.js",
    "https://wstatic-prod.pubgesports.com/web/live/main_da326b6/2d86a3d.js"
]

print("=== Analyzing pubgesports.com JS Bundles for API Endpoints ===")
for js_url in js_urls:
    try:
        req = urllib.request.Request(js_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as res:
            js_code = res.read().decode('utf-8', errors='ignore')
            api_matches = set(re.findall(r'https?://[a-zA-Z0-9_\-\.]+\.pubgesports\.com[^\s"\'`]*', js_code))
            other_apis = set(re.findall(r'https?://api\.[^\s"\'`]+', js_code))
            paths = set(re.findall(r'"/(api/[^"]+)"', js_code))
            
            print(f"\n[JS URL]: {js_url}")
            print(f"pubg domains: {api_matches}")
            print(f"other apis: {other_apis}")
            print(f"api paths: {list(paths)[:10]}")
    except Exception as e:
        print(f"Error {js_url}: {e}")
