import urllib.request
import json
import re
import os

os.makedirs("intermediate_results", exist_ok=True)
os.makedirs("primary_data", exist_ok=True)

base_url = "https://wwcd.lol"

# 1. HTML 가져오기
html_path = "primary_data/wwcd_index.html"
urllib.request.urlretrieve(base_url, html_path)

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# 2. 번들 자바스크립트 파일 찾기
js_files = re.findall(r'src="(/assets/[^"]+\.js)"', html_content)
preload_files = re.findall(r'href="(/assets/[^"]+\.js)"', html_content)
css_files = re.findall(r'href="(/assets/[^"]+\.css)"', html_content)

all_assets = list(set(js_files + preload_files + css_files))

asset_contents = {}
for asset in all_assets:
    asset_url = base_url + asset
    local_name = "intermediate_results/" + os.path.basename(asset)
    try:
        urllib.request.urlretrieve(asset_url, local_name)
        with open(local_name, "r", encoding="utf-8", errors="ignore") as f:
            asset_contents[asset] = f.read()
    except Exception as e:
        print(f"Error fetching {asset}: {e}")

# 3. Supabase 설정 및 쿼리 테이블 탐색
supabase_info = {}
for asset, text in asset_contents.items():
    # supabase url 및 key 패턴 탐색
    urls = re.findall(r'https://[a-zA-Z0-9_-]+\.supabase\.co', text)
    if urls:
        supabase_info["supabase_urls"] = list(set(urls))
    
    # anon key 패턴 탐색
    anon_keys = re.findall(r'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[a-zA-Z0-9._-]+', text)
    if anon_keys:
        supabase_info["anon_keys"] = list(set(anon_keys))
        
    # from("테이블명") 패턴 탐색
    tables = re.findall(r'\.from\(["\']([a-zA-Z0-9_]+)["\']\)', text)
    if tables:
        supabase_info.setdefault("tables", set()).update(tables)
        
    # 라우트 및 페이지 경로 탐색
    routes = re.findall(r'path:\s*["\'](/[^"\']*)["\']', text)
    if routes:
        supabase_info.setdefault("routes", set()).update(routes)

if "tables" in supabase_info:
    supabase_info["tables"] = sorted(list(supabase_info["tables"]))
if "routes" in supabase_info:
    supabase_info["routes"] = sorted(list(supabase_info["routes"]))

with open("intermediate_results/wwcd_analysis.json", "w", encoding="utf-8") as f:
    json.dump(supabase_info, f, ensure_ascii=False, indent=2)

print("분석 완료. 결과 요약:")
print(json.dumps(supabase_info, ensure_ascii=False, indent=2))
