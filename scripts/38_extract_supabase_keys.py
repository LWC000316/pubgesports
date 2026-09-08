import re
import urllib.request
import json

with open("intermediate_results/supabaseClient-BuEEPi6L.js", "r", encoding="utf-8") as f:
    text = f.read()

# supabase url 찾기
urls = re.findall(r'https://sqsouczuiycvtjnfztqs\.supabase\.co', text)
keys = re.findall(r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+', text)

print(f"Supabase URLs: {urls}")
print(f"Keys: {keys}")

if urls and keys:
    supa_url = urls[0]
    anon_key = keys[0]
    
    # OpenAPI 스키마 조회 시도 (Supabase PostgREST는 루트 /rest/v1/ 에서 스키마를 반환함)
    req = urllib.request.Request(
        supa_url + "/rest/v1/?apikey=" + anon_key,
        headers={
            "apikey": anon_key,
            "Authorization": "Bearer " + anon_key
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            schema = json.loads(resp.read().decode("utf-8"))
            definitions = schema.get("definitions", {})
            print(f"발견된 Supabase 테이블 목록: {list(definitions.keys())}")
            with open("intermediate_results/supabase_schema.json", "w", encoding="utf-8") as sf:
                json.dump(definitions, sf, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"스펙 조회 실패: {e}")
