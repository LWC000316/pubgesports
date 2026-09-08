import os
import glob
import re
import json

files = glob.glob("intermediate_results/*.js")
print(f"다운로드된 JS 파일 수: {len(files)}")

report = {}

for fpath in files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # 1. API 키, URL
    keys = re.findall(r'eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9._-]{20,}\.[a-zA-Z0-9._-]+', content)
    apis = re.findall(r'https?://[a-zA-Z0-9._-]+', content)
    
    # 2. Supabase 테이블 또는 RPC
    from_matches = re.findall(r'\.from\(["\']([^"\']+)["\']\)', content)
    rpc_matches = re.findall(r'\.rpc\(["\']([^"\']+)["\']\)', content)
    
    # 3. 주요 라우트 및 컴포넌트 이름
    routes = re.findall(r'path:\s*["\']([^"\']+)["\']', content)
    
    # 4. PUBG API 또는 외부 데이터 소스 언급
    pubg_matches = re.findall(r'api\.pubg\.com[^\s"\'`)]*', content)
    twire_matches = re.findall(r'twire\.gg[^\s"\'`)]*', content)
    
    report[fname] = {
        "size": len(content),
        "keys": list(set(keys)),
        "apis": list(set([a for a in apis if "w3.org" not in a])),
        "from_tables": list(set(from_matches)),
        "rpc_calls": list(set(rpc_matches)),
        "routes": list(set(routes)),
        "pubg_api": list(set(pubg_matches)),
        "twire_api": list(set(twire_matches))
    }

with open("intermediate_results/deep_wwcd_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("심층 분석 결과:")
for k, v in report.items():
    print(f"--- 파일: {k} (크기: {v['size']}) ---")
    print(f"  APIs: {v['apis']}")
    print(f"  Tables: {v['from_tables']}")
    print(f"  RPCs: {v['rpc_calls']}")
    print(f"  Routes: {v['routes']}")
    if v['keys']:
        print(f"  Found JWT Keys: {len(v['keys'])}개")
