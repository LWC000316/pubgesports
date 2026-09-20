# [폐기됨] 타사 사이트(wwcd.lol)의 Supabase 스토리지를 조회하던 스크립트.
# 남의 인프라 자격증명을 레포에 두지 않기 위해 엔드포인트와 키를 제거했다.
# 자기장 데이터는 primary_data/match_*.json 의 asset URL 로 크래프톤 공식
# 텔레메트리를 받는 경로를 쓴다. 이 파일은 조사 이력 기록용으로만 남긴다.
import os
import urllib.request
import json

base_url = os.environ.get("WWCD_SUPABASE_URL", "")
key = os.environ.get("WWCD_SUPABASE_KEY", "")

headers = {
    "apikey": key,
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json"
}

# 1. 스토리지 버킷 목록 확인
try:
    req = urllib.request.Request(base_url + "/storage/v1/bucket", headers=headers)
    with urllib.request.urlopen(req) as resp:
        buckets = json.loads(resp.read().decode("utf-8"))
        print(f"스토리지 버킷 목록: {[b.get('id') for b in buckets]}")
except Exception as e:
    print(f"버킷 조회 실패: {e}")

# 2. 'telemetry' 버킷 내부 파일 목록 확인 시도
try:
    post_data = json.dumps({"prefix": "", "limit": 20}).encode("utf-8")
    req = urllib.request.Request(base_url + "/storage/v1/object/list/telemetry", data=post_data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        files = json.loads(resp.read().decode("utf-8"))
        print(f"telemetry 버킷 내부 파일 샘플 (20개): {[f.get('name') for f in files]}")
        with open("intermediate_results/telemetry_sample.json", "w", encoding="utf-8") as out:
            json.dump(files, out, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"telemetry 파일 목록 조회 실패: {e}")
