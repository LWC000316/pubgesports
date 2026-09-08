import glob
import os
import re
import json

files = glob.glob("intermediate_results/*.js")

analysis = {}

for f in files:
    fname = os.path.basename(f)
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        code = fp.read()
    
    # Supabase from 테이블
    tables = re.findall(r'\.from\(["\']([a-zA-Z0-9_-]+)["\']\)', code)
    # Supabase select
    selects = re.findall(r'\.select\(["\']([^"\']+)["\']\)', code)
    # rpc
    rpcs = re.findall(r'\.rpc\(["\']([a-zA-Z0-9_-]+)["\']', code)
    # external url
    urls = re.findall(r'https?://[a-zA-Z0-9./_#-]+', code)
    urls = [u for u in set(urls) if not any(x in u for x in ["w3.org", "react", "github", "vercel", "twitter"])]
    
    analysis[fname] = {
        "tables": list(set(tables)),
        "selects": list(set(selects)),
        "rpcs": list(set(rpcs)),
        "urls": urls
    }

with open("intermediate_results/chunks_detailed_analysis.json", "w", encoding="utf-8") as out:
    json.dump(analysis, out, ensure_ascii=False, indent=2)

print("청크별 상세 분석 결과:")
for k, v in analysis.items():
    if v["tables"] or v["rpcs"] or v["urls"]:
        print(f"=== {k} ===")
        if v["tables"]:
            print(f"  테이블: {v['tables']}")
        if v["selects"]:
            print(f"  셀렉트 필드: {v['selects'][:3]}")
        if v["rpcs"]:
            print(f"  RPC: {v['rpcs']}")
        if v["urls"]:
            print(f"  외부 URLs: {v['urls']}")
