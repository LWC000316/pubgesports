import urllib.request
import json

base_url = "https://sqsouczuiycvtjnfztqs.supabase.co"
key = "sb_publishable_7_ip1nxMniQwwANdx4Kr_Q_4YRr8--4"

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
