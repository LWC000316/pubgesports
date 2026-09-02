with open("primary_data/pubgesports_tournament_2024.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# NUXT 함수 내부 문자열 리터럴 및 배열 추출
nuxt_match = re.search(r'window\.__NUXT__\s*=\s*\((.*?)\)\((.*?)\);', html, re.DOTALL)
if nuxt_match:
    fn_body = nuxt_match.group(1)
    args_str = nuxt_match.group(2)
    print("Found NUXT IIFE structure!")
    
    # 토너먼트 이름 관련 문자열 검색
    tournaments = re.findall(r'"([^"]*(?:PWS|PGS|PGC|PCL|Series|Championship|Phase)[^"]*)"', html, re.IGNORECASE)
    print(f"\nUnique Tournaments found ({len(set(tournaments))}):")
    for t in list(set(tournaments))[:20]:
        print(" *", t)

# 팀 관련 이름 검색
teams = re.findall(r'"([^"]*(?:KWANGDONG|Gen\.G|Danawa|Twisted|Soniqs|CERBERUS|17Gaming|FaZe|NAVI|Dplus|T1)[^"]*)"', html, re.IGNORECASE)
print(f"\nTeams found ({len(set(teams))}):")
for tm in list(set(teams))[:20]:
    print(" *", tm)
