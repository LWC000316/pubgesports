import re
import json

with open("intermediate_results/index-BVrWBIgE.js", "r", encoding="utf-8") as f:
    text = f.read()

# 1. 메뉴 라벨 및 네비게이션 항목 찾기
labels = re.findall(r'["\']([가-힣A-Za-z0-9\s·/]{2,20})["\']', text)

# 2. 메뉴 텍스트 후보 필터링
nav_candidates = []
keywords = ["대회", "선수", "팀", "순위", "스탯", "시뮬레이터", "리더보드", "로드투", "기록", "경기", "Road to", "Stats", "Player", "Team", "Simulator"]
for l in labels:
    if any(k in l for k in keywords):
        nav_candidates.append(l.strip())

nav_candidates = sorted(list(set(nav_candidates)))

# 3. 라우트 정의 객체 패턴 검색
routes = re.findall(r'path:\s*["\']([^"\']+)["\']', text)
routes += re.findall(r'to:\s*["\']([^"\']+)["\']', text)
routes += re.findall(r'href:\s*["\'](/[^"\']+)["\']', text)

with open("intermediate_results/wwcd_nav_analysis.json", "w", encoding="utf-8") as out:
    json.dump({
        "nav_candidates": nav_candidates[:100],
        "routes": sorted(list(set(routes)))
    }, out, ensure_ascii=False, indent=2)

print("네비게이션 및 라우트 분석 완료")
