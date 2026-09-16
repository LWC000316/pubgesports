import json

with open("intermediate_results/pws_24_teams_liquipedia_ready.json", "r", encoding="utf-8") as f:
    teams_24 = json.load(f)

with open("frontend/src/data/esportsData.js", "r", encoding="utf-8") as f:
    old_content = f.read()

# HOT_PLAYERS_12 시작 위치 탐색
hot_idx = old_content.find("export const HOT_PLAYERS_12")
if hot_idx == -1:
    print("HOT_PLAYERS_12 위치를 찾을 수 없음")
    exit(1)

hot_part = old_content[hot_idx:]

new_header = """// 공식 e스포츠 웹사이트 및 리퀴피디아(Liquipedia) 공식 검증 2026 PWS Phase 2 마스터 데이터셋

// 2026 PWS 페이즈 2 공식 참가 24개 프로팀 (리퀴피디아 오피셜 로스터)
export const LATEST_PWS2_TEAMS = """ + json.dumps(teams_24, ensure_ascii=False, indent=2) + """;\n\n"""

final_code = new_header + hot_part

with open("frontend/src/data/esportsData.js", "w", encoding="utf-8") as f:
    f.write(final_code)

print("frontend/src/data/esportsData.js 갱신 완료!")
