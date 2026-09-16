import json

with open("intermediate_results/liquipedia_24_teams_perfect.json", "r", encoding="utf-8") as f:
    lq_teams = json.load(f)

# 팀별 메타정보 및 태그 매핑
team_tag_map = {
    "SOOPers": {"tag": "DNS", "korean": "디엔 숲퍼스", "id": "dns"},
    "Gen.G Esports": {"tag": "GEN", "korean": "젠지 이스포츠", "id": "geng"},
    "T1": {"tag": "T1", "korean": "티원", "id": "t1"},
    "Baegopa": {"tag": "BGP", "korean": "배고파", "id": "bgp"},
    "FN Esports": {"tag": "FN", "korean": "에프엔 이스포츠 (포천)", "id": "fn"},
    "PENTAGRAM": {"tag": "AZLA", "korean": "아즐라 펜타그램", "id": "azla"},
    "Divine (Korean team)": {"tag": "DN", "korean": "디바인", "id": "dn"},
    "PHANTOM HEARTS": {"tag": "PHE", "korean": "팬텀 하츠 이스포츠", "id": "phe"},
    "GAMEPT": {"tag": "DGP", "korean": "대전 게임피티", "id": "dgp"},
    "SENTINEL": {"tag": "SEN", "korean": "센티넬", "id": "sen"},
    "spf": {"tag": "SPF", "korean": "슈퍼펙트", "id": "spf"},
    "Vex E-Sports": {"tag": "VEX", "korean": "벡스 이스포츠", "id": "vex"},
    "Geekay Esports": {"tag": "GK", "korean": "긱에이 이스포츠", "id": "gk"},
    "Eagle Owls": {"tag": "EOS", "korean": "이글 아울스", "id": "eos"},
    "SQUAD X ACADEMY": {"tag": "SXA", "korean": "스쿼드 엑스 아카데미", "id": "sxa"},
    "Crazy Raccoon": {"tag": "CR", "korean": "크레이지 라쿤", "id": "cr"},
    "SLASH DOOM LAB": {"tag": "SL", "korean": "슬래시 둠 랩", "id": "sl"},
    "ISKRA": {"tag": "ISK", "korean": "이스크라", "id": "isk"},
    "The Crown": {"tag": "TCN", "korean": "더 크라운", "id": "tcn"},
    "samgukzee": {"tag": "SGZ", "korean": "삼국지", "id": "sgz"},
    "HESEDIAN": {"tag": "HSD", "korean": "헤세디안 (구 Qx)", "id": "hsd"},
    "cfive": {"tag": "C5", "korean": "씨파이브", "id": "c5"},
    "GGWP (Korean team)": {"tag": "GGWP", "korean": "지지더블유피", "id": "ggwp"},
    "Overwhelm": {"tag": "OM", "korean": "오버웸 (구 아레떼)", "id": "om"}
}

frontend_teams = []
for idx, item in enumerate(lq_teams, 1):
    raw_name = item["team"]
    info = team_tag_map.get(raw_name, {
        "tag": raw_name[:3].upper(),
        "korean": raw_name,
        "id": raw_name.lower()[:4]
    })
    
    clean_name = raw_name.replace(" (Korean team)", "")
    if clean_name == "spf":
        clean_name = "SUPERFECT"
    elif clean_name == "cfive":
        clean_name = "CFiVE"
    elif clean_name == "PENTAGRAM":
        clean_name = "AZLA PENTAGRAM"
    
    roster_objs = []
    for p in item["players"]:
        roster_objs.append({
            "nickname": p,
            "realName": p,
            "role": "Player",
            "dpi": 800,
            "sens": 32,
            "mouse": "Logitech G PRO X Superlight"
        })
        
    frontend_teams.append({
        "id": info["id"],
        "name": clean_name,
        "koreanName": info["korean"],
        "tag": info["tag"],
        "league": "PWS",
        "rank": idx,
        "description": f"2026 PWS Phase 2 리퀴피디아 공식 검증 참가팀 ({info['korean']})",
        "roster": roster_objs
    })

print(f"변환된 프론트엔드 팀 데이터: {len(frontend_teams)}개")

with open("intermediate_results/pws_24_teams_liquipedia_ready.json", "w", encoding="utf-8") as out:
    json.dump(frontend_teams, out, ensure_ascii=False, indent=2)
