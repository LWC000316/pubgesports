import urllib.request
import gzip
import json
import re

url = "https://liquipedia.net/pubg/api.php?action=parse&page=PUBG_WEEKLY_SERIES/2026/Phase_2&prop=text&format=json"
req = urllib.request.Request(url, headers={
    "User-Agent": "PUBGEsportsPlatform/1.0 (contact@pubgproject.local)",
    "Accept-Encoding": "gzip"
})

with urllib.request.urlopen(req) as resp:
    raw = resp.read()
    if resp.info().get("Content-Encoding") == "gzip":
        raw = gzip.decompress(raw)
    data = json.loads(raw.decode("utf-8"))

html = data.get("parse", {}).get("text", {}).get("*", "")

# 1. 대회 메인 로고 (PWS 로고)
infobox_logo = re.findall(r'<div class="infobox-image[^"]*">\s*<a[^>]*>\s*<img[^>]+src="([^">]+)"', html)
print("PWS 대회 로고:", infobox_logo)

# 2. 팀별 로고 탐색
# 리퀴피디아의 Opponent/TeamCard HTML 구조 탐색
pattern = r'<div class="teamcard[^"]*">([\s\S]*?)</div>\s*</div>'
cards = re.findall(r'<center[^>]*><b><a[^>]*title="([^"]+)"[^>]*>([^<]+)</a>[\s\S]*?<img[^>]+src="([^">]+)"', html)
print("발견된 팀 로고 쌍 개수:", len(cards))

# 모든 이미지 중 로고성 이미지 확인
all_imgs = re.findall(r'<img[^>]+src="([^">]+)"[^>]*alt="([^"]*)"', html)
logos_found = {}
for src, alt in all_imgs:
    if "logo" in alt.lower() or "logo" in src.lower() or any(t in alt.lower() for t in ["soop", "gen.g", "t1", "baegopa", "geekay", "slash", "raccoon", "pentagram", "divine"]):
        full_src = "https://liquipedia.net" + src if src.startswith("/") else src
        logos_found[alt] = full_src

print(f"추출된 주요 로고 목록 ({len(logos_found)}개):")
for k, v in list(logos_found.items())[:20]:
    print(f" {k}: {v}")

with open("intermediate_results/extracted_logos.json", "w", encoding="utf-8") as f:
    json.dump({"pws_logo": infobox_logo, "logos": logos_found}, f, ensure_ascii=False, indent=2)
