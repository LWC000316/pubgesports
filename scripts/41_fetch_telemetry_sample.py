# [폐기됨] 타사 사이트(wwcd.lol)의 Supabase 스토리지에서 매치 데이터를 받던 스크립트.
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
    "Authorization": "Bearer " + key
}

file_name = "000c46.json"
urls_to_try = [
    f"{base_url}/storage/v1/object/telemetry/{file_name}",
    f"{base_url}/storage/v1/object/authenticated/telemetry/{file_name}"
]

for u in urls_to_try:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"성공 URL: {u}")
            print(f"키 목록: {list(data.keys()) if isinstance(data, dict) else '리스트 크기 ' + str(len(data))}")
            with open("intermediate_results/sample_match_data.json", "w", encoding="utf-8") as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
            break
    except Exception as e:
        print(f"실패 {u}: {e}")
