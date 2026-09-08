import urllib.request
import json

base_url = "https://sqsouczuiycvtjnfztqs.supabase.co"
key = "sb_publishable_7_ip1nxMniQwwANdx4Kr_Q_4YRr8--4"

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
