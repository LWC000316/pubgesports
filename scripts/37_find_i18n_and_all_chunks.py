import re
import glob
import urllib.request
import os

base_url = "https://wwcd.lol"

# 모든 js 파일에서 assets 경로 정규식 검색
all_js = glob.glob("intermediate_results/*.js")
found_assets = set()

for j in all_js:
    with open(j, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    matches = re.findall(r'assets/[a-zA-Z0-9._-]+\.js', c)
    found_assets.update(matches)

print(f"발견된 에셋 수: {len(found_assets)}")

downloaded = 0
for a in found_assets:
    local = "intermediate_results/" + os.path.basename(a)
    if not os.path.exists(local):
        try:
            urllib.request.urlretrieve(base_url + "/" + a, local)
            downloaded += 1
            print(f"다운로드: {a}")
        except Exception as e:
            print(f"실패 {a}: {e}")

print(f"새로 다운로드된 파일 수: {downloaded}")
