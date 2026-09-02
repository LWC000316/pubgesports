import json

# 1. 최신 글로벌 대회 (PGS 9 그랜드 파이널) 매치 데이터 내 PWS 팀 분석
with open("primary_data/api_match_15b203fc-c696-4f59-9f78-f486ab113d81.json", "r", encoding="utf-8") as f:
    pgs_match = json.load(f)

included = pgs_match.get("included", [])
pgs_korean_teams = set()
for item in included:
    if item.get("type") == "participant":
        p_name = item.get("attributes", {}).get("stats", {}).get("name", "")
        if p_name.startswith("GEN_") or p_name.startswith("DNS_") or p_name.startswith("T1_"):
            tag = p_name.split("_")[0]
            pgs_korean_teams.add(tag)

print(f"1. 최신 글로벌 세계 대회 (PGS 9 그랜드 파이널) 참가 PWS 한국 팀: {len(pgs_korean_teams)}팀 ({', '.join(pgs_korean_teams)})")

# 2. 최신 PWS 정규 시즌 대회 (PWS Phase) 본선 참가팀 분석
with open("primary_data/pws_all_extracted_teams.json", "r", encoding="utf-8") as f:
    pws_all = json.load(f)

print(f"2. 공식 API 상의 PWS 정규 시즌 전체 참가팀 누적: 총 {len(pws_all)}개 팀")
print("3. PWS 정규 시즌 본선(그랜드 파이널) 정규 슬롯: 16개 팀")
