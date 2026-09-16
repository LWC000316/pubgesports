import json

# 리퀴피디아 이미지 URL 맵 로드
with open("intermediate_results/liquipedia_image_urls.json", "r", encoding="utf-8") as f:
    img_urls = json.load(f)

# 팀별 로고 및 시드 매핑 정의
team_configs = [
    # 1. PRO SEEDS (13팀)
    {
        "name": "DN SOOPers",
        "tag": "DNS",
        "seedType": "pro",
        "logo": img_urls.get("DN SOOPers allmode.png", ""),
        "players": ["Rex", "Gyumin", "Heaven", "DIEL"]
    },
    {
        "name": "Gen.G Esports",
        "tag": "GEN",
        "seedType": "pro",
        "logo": img_urls.get("Gen.G Esports 2026 allmode.png", ""),
        "players": ["seoul", "Salute", "taemin", "BeaN"]
    },
    {
        "name": "T1",
        "tag": "T1",
        "seedType": "pro",
        "logo": img_urls.get("T1 2019 allmode.png", ""),
        "players": ["Rain1ng", "EEND", "Heather", "Type"]
    },
    {
        "name": "Baegopa",
        "tag": "BGP",
        "seedType": "pro",
        "logo": img_urls.get("Baegopa allmode.png", ""),
        "players": ["Pio", "Inonix", "blackwalk", "yugee"]
    },
    {
        "name": "FN Esports",
        "tag": "FN",
        "seedType": "pro",
        "logo": img_urls.get("FN Esports allmode.png", ""),
        "players": ["Starlord", "kkachi", "BreaKers", "Hush"]
    },
    {
        "name": "AZLA PENTAGRAM",
        "tag": "AZLA",
        "seedType": "pro",
        "logo": img_urls.get("PENTAGRAM 2023 darkmode.png", ""),
        "players": ["F1ame", "HAMMER", "Orca", "redzone"]
    },
    {
        "name": "Divine",
        "tag": "DN",
        "seedType": "pro",
        "logo": img_urls.get("Divine KR allmode.png", ""),
        "players": ["Barpo", "Stella", "Tosi", "Daejang"]
    },
    {
        "name": "PHANTOM HEARTS",
        "tag": "PHE",
        "seedType": "pro",
        "logo": img_urls.get("PHANTOM HEARTS darkmode.png", ""),
        "players": ["DAEVA", "King", "GimJun", "ZeniTh"]
    },
    {
        "name": "DAEJEON GAME PT",
        "tag": "DGP",
        "seedType": "pro",
        "logo": img_urls.get("Game PT darkmode.png", ""),
        "players": ["fizzy", "instinct", "PolarBear", "Search"]
    },
    {
        "name": "SENTINEL",
        "tag": "SEN",
        "seedType": "pro",
        "logo": img_urls.get("Sentinel KR allmode.png", ""),
        "players": ["Rascal", "heyden", "HyukSung", "VenTus"]
    },
    {
        "name": "SUPERFECT",
        "tag": "SPF",
        "seedType": "pro",
        "logo": img_urls.get("SUPERFECT Esports allmode.png", ""),
        "players": ["Acid", "TheMinos", "Karwn", "Todol"]
    },
    {
        "name": "Vex E-Sports",
        "tag": "VEX",
        "seedType": "pro",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["Lure", "Nyeong", "ROY", "Solution"]
    },
    {
        "name": "Geekay Esports",
        "tag": "GK",
        "seedType": "pro",
        "logo": img_urls.get("Geekay Esports 2024 allmode.png", ""),
        "players": ["AKaN", "Parkpro", "Seongjang", "EJ"]
    },

    # 2. AMATEUR & QUALIFIER SEEDS (11팀)
    {
        "name": "Eagle Owls",
        "tag": "EOS",
        "seedType": "amateur",
        "logo": img_urls.get("Eagle Owls 22 allmode.png", ""),
        "players": ["SINGAM", "DK", "Right", "Jaechan"]
    },
    {
        "name": "SQUAD X ACADEMY",
        "tag": "SXA",
        "seedType": "amateur",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["BBANG", "Sunday", "HELLPER", "KAL"]
    },
    {
        "name": "Crazy Raccoon",
        "tag": "CR",
        "seedType": "amateur",
        "logo": img_urls.get("Crazy Raccoon 2021 allmode.png", ""),
        "players": ["Glaz", "Gyuyeon", "Ayoh", "GGoBuGi"]
    },
    {
        "name": "SLASH DOOM LAB",
        "tag": "SL",
        "seedType": "amateur",
        "logo": "https://liquipedia.net/commons/images/8/86/Star_Balloon_allmode.png",
        "players": ["Freaky", "Morek", "muel", "vilo"]
    },
    {
        "name": "ISKRA",
        "tag": "ISK",
        "seedType": "amateur",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["ParkChaN", "Genom", "Yong", "Primmie"]
    },
    {
        "name": "The Crown",
        "tag": "TCN",
        "seedType": "amateur",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["CxldMxn", "HanlNu", "2cut", "2heart"]
    },
    {
        "name": "samgukzee",
        "tag": "SGZ",
        "seedType": "amateur",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["GuanYu", "ZhaoYun", "Yubi", "YeoPo"]
    },
    {
        "name": "HESEDIAN",
        "tag": "HSD",
        "seedType": "amateur",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["LOV3", "Glance", "Hyuk", "youth"]
    },
    {
        "name": "CFiVE",
        "tag": "C5",
        "seedType": "amateur",
        "logo": img_urls.get("PUBG 2021 default allmode.png", ""),
        "players": ["Archi", "Malik", "Gray", "Krbyz"]
    },
    {
        "name": "GGWP",
        "tag": "GGWP",
        "seedType": "amateur",
        "logo": "https://liquipedia.net/commons/images/8/8b/GGWP_darkmode.png",
        "players": ["sony", "Geunwon", "naheesoo", "Wanted"]
    },
    {
        "name": "Overwhelm",
        "tag": "OM",
        "seedType": "amateur",
        "logo": img_urls.get("Overwhelm darkmode.png", "") or img_urls.get("Overwhelm allmode.png", ""),
        "players": ["Woong", "night", "Fairy", "FoxVer"]
    }
]

final_teams = []
for idx, t in enumerate(team_configs, 1):
    roster = []
    for p in t["players"]:
        roster.append({
            "nickname": p,
            "realName": p,
            "role": "Player",
            "dpi": 800,
            "sens": 32,
            "mouse": "Logitech G PRO X Superlight"
        })
    final_teams.append({
        "id": t["name"].lower().replace(" ", "_").replace("-", "_").replace(".", ""),
        "name": t["name"],
        "tag": t["tag"],
        "seedType": t["seedType"],
        "logo": t["logo"],
        "league": "PWS",
        "roster": roster
    })

# frontend/src/data/esportsData.js 읽기 및 갱신
with open("frontend/src/data/esportsData.js", "r", encoding="utf-8") as f:
    code = f.read()

hot_idx = code.find("export const HOT_PLAYERS_12")
hot_part = code[hot_idx:]

header = """// 2026 PUBG WEEKLY SERIES: KOREA Phase 2 공식 오피셜 참가팀 데이터셋

export const TOURNAMENT_LOGOS = {
  PWS: "https://liquipedia.net/commons/images/9/93/PUBG_WEEKLY_SERIES_KOREA_icon_darkmode.png",
  PCL: "https://liquipedia.net/commons/images/d/d3/PUBG_Champions_League_darkmode.png",
  EMEA: "https://liquipedia.net/commons/images/f/f3/Eu_hd.png",
  AMER: "https://liquipedia.net/commons/images/8/8a/PUBG_Americas_Series_darkmode.png",
  APAC: "https://liquipedia.net/commons/images/1/12/Asia-pacific_flag_hd.png"
};

export const LATEST_PWS2_TEAMS = """ + json.dumps(final_teams, ensure_ascii=False, indent=2) + """;\n\n"""

with open("frontend/src/data/esportsData.js", "w", encoding="utf-8") as f:
    f.write(header + hot_part)

print(f"공식 PWS 24개 팀 (프로 13, 아마추어 11) 데이터 주입 완료!")
