import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

js_url = "https://twire.gg/static/js/main.fe0e34f5.chunk.js"
req = urllib.request.Request(js_url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as res:
    code = res.read().decode('utf-8', errors='ignore')

print("Twire JS Length:", len(code))
urls = set(re.findall(r'https?://[a-zA-Z0-9_\-\./]+', code))
print("Found URLs in Twire bundle:")
for u in list(urls)[:15]:
    print(" -", u)

# API 엔드포인트 패턴 검색
api_endpoints = set(re.findall(r'"(/api/[^"]+)"', code))
print("\nAPI paths:", list(api_endpoints)[:10])
