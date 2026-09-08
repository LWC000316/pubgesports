import re
import json

with open("intermediate_results/index-BVrWBIgE.js", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# react-router 라우트 패턴 탐색: path:"...", element:
routes = re.findall(r'\{path:["\']([^"\']+)["\']', text)
print(f"발견된 라우트: {routes}")

# 메뉴 이름이나 한국어 문자열 검색
korean_strings = re.findall(r'["\']([가-힣\s]{2,15})["\']', text)
korean_strings = list(set(korean_strings))
print(f"발견된 한국어 문자열 수: {len(korean_strings)}")

# CSS 클래스 및 스타일 특징 분석
with open("intermediate_results/index-BoRhu6xc.css", "r", encoding="utf-8", errors="ignore") as f:
    css = f.read()

color_vars = re.findall(r'--[a-zA-Z0-9_-]+:\s*[^;]+;', css)
font_families = re.findall(r'font-family:\s*[^;]+;', css)

summary = {
    "routes": routes,
    "korean_samples": [s for s in korean_strings if any(k in s for k in ["대회", "선수", "팀", "순위", "기록", "포인트", "진행", "일정", "결과", "스탯"])][:50],
    "color_variables": color_vars[:30],
    "fonts": list(set(font_families))[:10]
}

with open("intermediate_results/ui_ux_analysis.json", "w", encoding="utf-8") as out:
    json.dump(summary, out, ensure_ascii=False, indent=2)

print("UI/UX 분석 요약 완료")
