import json

# 팀별 로컬 로고 및 공식 우승 트로피(Titles) 데이터
team_configs = [
    # 1. PRO SEEDS (13팀)
    {
        "name": "DN SOOPers",
        "tag": "DNS",
        "seedType": "pro",
        "logo": "/logos/teams/dns.png",
        "trophies": [
            {"name": "PGC", "count": 1},
            {"name": "PWS", "count": 4}
        ],
        "players": ["Rex", "Gyumin", "Heaven", "DIEL"]
    },
    {
        "name": "Gen.G Esports",
        "tag": "GEN",
        "seedType": "pro",
        "logo": "/logos/teams/geng.png",
        "trophies": [
            {"name": "PGC", "count": 2},
            {"name": "PWS", "count": 3}
        ],
        "players": ["seoul", "Salute", "taemin", "BeaN"]
    },
    {
        "name": "T1",
        "tag": "T1",
        "seedType": "pro",
        "logo": "/logos/teams/t1.png",
        "trophies": [
            {"name": "PWS", "count": 1},
            {"name": "PKL", "count": 1}
        ],
        "players": ["Rain1ng", "EEND", "Heather", "Type"]
    },
    {
        "name": "Baegopa",
        "tag": "BGP",
        "seedType": "pro",
        "logo": "/logos/teams/bgp.png",
        "trophies": [
            {"name": "PWS", "count": 1}
        ],
        "players": ["Pio", "Inonix", "blackwalk", "yugee"]
    },
    {
        "name": "FN Esports",
        "tag": "FN",
        "seedType": "pro",
        "logo": "/logos/teams/fn.png",
        "trophies": [
            {"name": "BSC", "count": 1}
        ],
        "players": ["Starlord", "kkachi", "BreaKers", "Hush"]
    },
    {
        "name": "AZLA PENTAGRAM",
        "tag": "AZLA",
        "seedType": "pro",
        "logo": "/logos/teams/azla.png",
        "trophies": [
            {"name": "PWS", "count": 1},
            {"name": "BSC", "count": 2}
        ],
        "players": ["F1ame", "HAMMER", "Orca", "redzone"]
    },
    {
        "name": "Divine",
        "tag": "DN",
        "seedType": "pro",
        "logo": "/logos/teams/dn.png",
        "trophies": [],
        "players": ["Barpo", "Stella", "Tosi", "Daejang"]
    },
    {
        "name": "PHANTOM HEARTS",
        "tag": "PHE",
        "seedType": "pro",
        "logo": "/logos/teams/phe.png",
        "trophies": [],
        "players": ["DAEVA", "King", "GimJun", "ZeniTh"]
    },
    {
        "name": "DAEJEON GAME PT",
        "tag": "DGP",
        "seedType": "pro",
        "logo": "/logos/teams/dgp.png",
        "trophies": [
            {"name": "BSC", "count": 1}
        ],
        "players": ["fizzy", "instinct", "PolarBear", "Search"]
    },
    {
        "name": "SENTINEL",
        "tag": "SEN",
        "seedType": "pro",
        "logo": "/logos/teams/sen.png",
        "trophies": [],
        "players": ["Rascal", "heyden", "HyukSung", "VenTus"]
    },
    {
        "name": "SUPERFECT",
        "tag": "SPF",
        "seedType": "pro",
        "logo": "/logos/teams/spf.png",
        "trophies": [],
        "players": ["Acid", "TheMinos", "Karwn", "Todol"]
    },
    {
        "name": "Vex E-Sports",
        "tag": "VEX",
        "seedType": "pro",
        "logo": "",
        "trophies": [],
        "players": ["Lure", "Nyeong", "ROY", "Solution"]
    },
    {
        "name": "Geekay Esports",
        "tag": "GK",
        "seedType": "pro",
        "logo": "/logos/teams/gk.png",
        "trophies": [
            {"name": "PWS", "count": 1}
        ],
        "players": ["AKaN", "Parkpro", "Seongjang", "EJ"]
    },

    # 2. QUALIFIER SEEDS (11팀)
    {
        "name": "Eagle Owls",
        "tag": "EOS",
        "seedType": "amateur",
        "logo": "/logos/teams/eos.png",
        "trophies": [],
        "players": ["SINGAM", "DK", "Right", "Jaechan"]
    },
    {
        "name": "SQUAD X ACADEMY",
        "tag": "SXA",
        "seedType": "amateur",
        "logo": "",
        "trophies": [],
        "players": ["BBANG", "Sunday", "HELLPER", "KAL"]
    },
    {
        "name": "Crazy Raccoon",
        "tag": "CR",
        "seedType": "amateur",
        "logo": "/logos/teams/cr.png",
        "trophies": [
            {"name": "PWS", "count": 1}
        ],
        "players": ["Glaz", "Gyuyeon", "Ayoh", "GGoBuGi"]
    },
    {
        "name": "SLASH DOOM LAB",
        "tag": "SL",
        "seedType": "amateur",
        "logo": "/logos/teams/sl.png",
        "trophies": [],
        "players": ["Freaky", "Morek", "muel", "vilo"]
    },
    {
        "name": "ISKRA",
        "tag": "ISK",
        "seedType": "amateur",
        "logo": "",
        "trophies": [],
        "players": ["ParkChaN", "Genom", "Yong", "Primmie"]
    },
    {
        "name": "The Crown",
        "tag": "TCN",
        "seedType": "amateur",
        "logo": "",
        "trophies": [],
        "players": ["CxldMxn", "HanlNu", "2cut", "2heart"]
    },
    {
        "name": "samgukzee",
        "tag": "SGZ",
        "seedType": "amateur",
        "logo": "",
        "trophies": [],
        "players": ["GuanYu", "ZhaoYun", "Yubi", "YeoPo"]
    },
    {
        "name": "HESEDIAN",
        "tag": "HSD",
        "seedType": "amateur",
        "logo": "",
        "trophies": [],
        "players": ["LOV3", "Glance", "Hyuk", "youth"]
    },
    {
        "name": "CFiVE",
        "tag": "C5",
        "seedType": "amateur",
        "logo": "",
        "trophies": [],
        "players": ["Archi", "Malik", "Gray", "Krbyz"]
    },
    {
        "name": "GGWP",
        "tag": "GGWP",
        "seedType": "amateur",
        "logo": "/logos/teams/ggwp.png",
        "trophies": [],
        "players": ["sony", "Geunwon", "naheesoo", "Wanted"]
    },
    {
        "name": "Overwhelm",
        "tag": "OM",
        "seedType": "amateur",
        "logo": "/logos/teams/om.png",
        "trophies": [],
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
        "trophies": t["trophies"],
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
  PWS: "/logos/tournaments/pws.png",
  PCL: "/logos/tournaments/pcl.png",
  EMEA: "/logos/tournaments/emea.png",
  AMER: "/logos/tournaments/amer.png",
  APAC: "/logos/tournaments/apac.png"
};

export const LATEST_PWS2_TEAMS = """ + json.dumps(final_teams, ensure_ascii=False, indent=2) + """;\n\n"""

with open("frontend/src/data/esportsData.js", "w", encoding="utf-8") as f:
    f.write(header + hot_part)

print(f"로컬 로고 및 트로피 데이터 주입 완료!")
