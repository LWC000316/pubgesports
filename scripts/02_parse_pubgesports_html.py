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

url = "https://pubgesports.com/ko/tournament"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as response:
    html = response.read().decode('utf-8', errors='ignore')

print(f"pubgesports.com HTML Length: {len(html)}")

# window.__NUXT__ 또는 API 호출 링크 탐색
nuxt_match = re.search(r'window\.__NUXT__\s*=\s*(.*?);<\/script>', html, re.DOTALL)
if nuxt_match:
    print("[FOUND] window.__NUXT__ found!")
    nuxt_data = nuxt_match.group(1)
    print(f"NUXT Data preview: {nuxt_data[:300]}...")

# script 태그 내 js 파일 목록 탐색
scripts = re.findall(r'<script src="([^"]+)"', html)
print(f"Script tags found ({len(scripts)}):")
for s in scripts[:5]:
    print(" -", s)

# twire.gg HTML 확인
twire_url = "https://twire.gg/en/pubg/tournaments"
req_twire = urllib.request.Request(twire_url, headers=headers)
with urllib.request.urlopen(req_twire, context=ctx) as response:
    twire_html = response.read().decode('utf-8', errors='ignore')

print(f"\ntwire.gg HTML Length: {len(twire_html)}")
twire_next = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', twire_html, re.DOTALL)
if twire_next:
    print("[FOUND] twire.gg __NEXT_DATA__ JSON found!")
    data = json.loads(twire_next.group(1))
    print("twire.gg keys:", list(data.keys()))
    if 'props' in data:
        print("twire.gg pageProps keys:", list(data['props'].get('pageProps', {}).keys()))
else:
    print("[INFO] Checking twire scripts...")
    t_scripts = re.findall(r'<script [^>]*src="([^"]+)"', twire_html)
    for ts in t_scripts[:5]:
        print(" - twire script:", ts)
