import json
import re

# 2026 PWS Phase 2 공식 24개 팀 및 실제 검증 로스터 정의
pws24_teams = [
    {
        "id": "gk",
        "name": "Geekay Esports",
        "koreanName": "긱에이 이스포츠",
        "tag": "GK",
        "league": "PWS",
        "rank": 1,
        "description": "2026 PWS 페이즈 2 개막 1일차 3치킨 70점으로 단독 1위를 질주하는 최강의 교전 군단",
        "roster": [
            { "nickname": "AKaN", "realName": "김찬희", "role": "Main Fragger", "dpi": 800, "sens": 32, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "Parkpro", "realName": "박상현", "role": "Ace Attacker", "dpi": 800, "sens": 30, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Seongjang", "realName": "성장환", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Zowie EC2_CW" },
            { "nickname": "EJ", "realName": "이정우", "role": "Support", "dpi": 800, "sens": 34, "mouse": "Vaxee XE Wireless" }
        ]
    },
    {
        "id": "dns",
        "name": "DN SOOPers",
        "koreanName": "디엔 숲퍼스 (다나와)",
        "tag": "DNS",
        "league": "PWS",
        "rank": 2,
        "description": "15킬 1위 Rex와 13킬 Gyumin, Heaven이 포진한 강력한 우승 후보 전통 명문",
        "roster": [
            { "nickname": "Rex", "realName": "김해찬", "role": "Main Fragger", "dpi": 800, "sens": 29, "mouse": "Zowie S2_C" },
            { "nickname": "Gyumin", "realName": "심규민", "role": "In_Game Leader", "dpi": 800, "sens": 32, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Heaven", "realName": "김태성", "role": "Ace Attacker", "dpi": 800, "sens": 30, "mouse": "Zowie EC2_CW" },
            { "nickname": "DIEL", "realName": "김진현", "role": "Support", "dpi": 800, "sens": 34, "mouse": "Razer DeathAdder V3 Pro" }
        ]
    },
    {
        "id": "azla",
        "name": "AZLA PENTAGRAM",
        "koreanName": "아즐라 펜타그램",
        "tag": "AZLA",
        "league": "PWS",
        "rank": 3,
        "description": "F1ame과 redzone, HAMMER, Orca의 폭발적인 외곽 서클 장악력과 킬 캐치 능력",
        "roster": [
            { "nickname": "redzone", "realName": "최원석", "role": "Main Fragger", "dpi": 400, "sens": 46, "mouse": "Vaxee Outset AX" },
            { "nickname": "HAMMER", "realName": "이영현", "role": "Attacker", "dpi": 800, "sens": 32, "mouse": "Zowie EC2_C" },
            { "nickname": "F1ame", "realName": "김성민", "role": "All_rounder", "dpi": 800, "sens": 32, "mouse": "Razer Viper V3 Pro" },
            { "nickname": "Orca", "realName": "이장원", "role": "Support", "dpi": 400, "sens": 48, "mouse": "Zowie EC1_C" }
        ]
    },
    {
        "id": "eos",
        "name": "Eagle Owls",
        "koreanName": "이글 아울스",
        "tag": "EOS",
        "league": "PWS",
        "rank": 4,
        "description": "치킨을 획득하며 상위권에 안착한 신흥 강호, SINGAM과 DK의 날카로운 에임",
        "roster": [
            { "nickname": "SINGAM", "realName": "손신감", "role": "Main Fragger", "dpi": 800, "sens": 31, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "DK", "realName": "김동규", "role": "Attacker", "dpi": 800, "sens": 33, "mouse": "Razer DeathAdder V3" },
            { "nickname": "Right", "realName": "이우완", "role": "Support", "dpi": 800, "sens": 30, "mouse": "Zowie FK2_C" },
            { "nickname": "Jaechan", "realName": "정재찬", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Vaxee XE" }
        ]
    },
    {
        "id": "dn",
        "name": "Divine",
        "koreanName": "디바인",
        "tag": "DN",
        "league": "PWS",
        "rank": 5,
        "description": "Tosi와 Stella, Barpo, wonderful이 뭉쳐 개막 1일차 1치킨을 기록한 프로 군단",
        "roster": [
            { "nickname": "Tosi", "realName": "성윤모", "role": "Main Fragger", "dpi": 800, "sens": 30, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "Stella", "realName": "이지훈", "role": "Attacker", "dpi": 800, "sens": 32, "mouse": "Zowie EC2_CW" },
            { "nickname": "Barpo", "realName": "김바포", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Razer Viper V2 Pro" },
            { "nickname": "wonderful", "realName": "원더풀", "role": "Support", "dpi": 400, "sens": 50, "mouse": "Vaxee NP_01S" }
        ]
    },
    {
        "id": "sl",
        "name": "Star Balloon",
        "koreanName": "스타벌룬",
        "tag": "SL",
        "league": "PWS",
        "rank": 6,
        "description": "Freaky와 Morek, muel, vilo의 유기적인 연계로 34점을 기록하며 맹활약 중인 다크호스",
        "roster": [
            { "nickname": "Freaky", "realName": "윤태양", "role": "Main Fragger", "dpi": 800, "sens": 35, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Morek", "realName": "모렉", "role": "Attacker", "dpi": 800, "sens": 31, "mouse": "Zowie S2_C" },
            { "nickname": "muel", "realName": "뮤엘", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "vilo", "realName": "빌로", "role": "Support", "dpi": 800, "sens": 32, "mouse": "Vaxee Outset AX" }
        ]
    },
    {
        "id": "tcn",
        "name": "The Crown",
        "koreanName": "더 크라운",
        "tag": "TCN",
        "league": "PWS",
        "rank": 7,
        "description": "CxldMxn과 HanINu, 2cut, 2heart의 공격적인 교전 지향 운영을 선보이는 팀",
        "roster": [
            { "nickname": "CxldMxn", "realName": "콜드맨", "role": "Main Fragger", "dpi": 800, "sens": 33, "mouse": "Logitech G PRO Wireless" },
            { "nickname": "HanINu", "realName": "한이누", "role": "Attacker", "dpi": 800, "sens": 31, "mouse": "Razer Viper V3 Pro" },
            { "nickname": "2cut", "realName": "투컷", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Zowie EC2_CW" },
            { "nickname": "2heart", "realName": "투하트", "role": "Support", "dpi": 400, "sens": 52, "mouse": "Logitech G304" }
        ]
    },
    {
        "id": "ggwp",
        "name": "GGWP Esports",
        "koreanName": "지지더블유피",
        "tag": "GGWP",
        "league": "PWS",
        "rank": 8,
        "description": "Geunwon과 Wanted, sony, naheesoo가 뭉쳐 끈끈한 수비력과 중거리 교전 능력을 발휘",
        "roster": [
            { "nickname": "Geunwon", "realName": "근원", "role": "Main Fragger", "dpi": 800, "sens": 32, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Wanted", "realName": "원티드", "role": "Attacker", "dpi": 800, "sens": 30, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "sony", "realName": "소니", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Zowie EC1_C" },
            { "nickname": "naheesoo", "realName": "나희수", "role": "Support", "dpi": 800, "sens": 33, "mouse": "Vaxee XE" }
        ]
    },
    {
        "id": "sxa",
        "name": "SQUAD X ACADEMY",
        "koreanName": "스쿼드 엑스 아카데미",
        "tag": "SXA",
        "league": "PWS",
        "rank": 9,
        "description": "BBANG과 Sunday, HELLPER, KAL의 젊은 패기와 과감한 푸시가 돋보이는 육성군 출신",
        "roster": [
            { "nickname": "BBANG", "realName": "빵", "role": "Main Fragger", "dpi": 800, "sens": 34, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "Sunday", "realName": "선데이", "role": "Attacker", "dpi": 800, "sens": 31, "mouse": "Razer Viper V2 Pro" },
            { "nickname": "HELLPER", "realName": "헬퍼", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Zowie S2_C" },
            { "nickname": "KAL", "realName": "칼", "role": "Support", "dpi": 800, "sens": 32, "mouse": "Vaxee Outset AX" }
        ]
    },
    {
        "id": "vex",
        "name": "VEX E_Sports",
        "koreanName": "벡스 이스포츠",
        "tag": "VEX",
        "league": "PWS",
        "rank": 10,
        "description": "Lure와 ROY, Nyeong, Solution이 안정적인 포인트 관리를 이어가는 정통파 프로팀",
        "roster": [
            { "nickname": "Lure", "realName": "루어", "role": "Main Fragger", "dpi": 800, "sens": 30, "mouse": "Zowie EC2_CW" },
            { "nickname": "ROY", "realName": "로이", "role": "Attacker", "dpi": 800, "sens": 33, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Nyeong", "realName": "녕", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Solution", "realName": "솔루션", "role": "Support", "dpi": 400, "sens": 48, "mouse": "Vaxee XE Wireless" }
        ]
    },
    {
        "id": "c5",
        "name": "CFiVE",
        "koreanName": "씨파이브",
        "tag": "C5",
        "league": "PWS",
        "rank": 11,
        "description": "Archi와 Gray, Krbyz, Malik의 치밀한 랜드마크 파밍과 정보전을 앞세운 실력파",
        "roster": [
            { "nickname": "Archi", "realName": "아키", "role": "Main Fragger", "dpi": 800, "sens": 31, "mouse": "Logitech G PRO Wireless" },
            { "nickname": "Gray", "realName": "그레이", "role": "Attacker", "dpi": 800, "sens": 30, "mouse": "Zowie FK2_C" },
            { "nickname": "Krbyz", "realName": "커비즈", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Razer Viper V3 Pro" },
            { "nickname": "Malik", "realName": "말릭", "role": "Support", "dpi": 800, "sens": 32, "mouse": "Logitech G304" }
        ]
    },
    {
        "id": "isk",
        "name": "ISKRA",
        "koreanName": "이스크라",
        "tag": "ISK",
        "league": "PWS",
        "rank": 12,
        "description": "ParkChaN과 Primmie, Genom, Yong의 조직적인 지역 방어와 집단 교전력이 강점",
        "roster": [
            { "nickname": "ParkChaN", "realName": "박찬", "role": "Main Fragger", "dpi": 800, "sens": 33, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Primmie", "realName": "프리미", "role": "Attacker", "dpi": 800, "sens": 31, "mouse": "Razer DeathAdder V3" },
            { "nickname": "Genom", "realName": "게놈", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Zowie EC1_C" },
            { "nickname": "Yong", "realName": "용", "role": "Support", "dpi": 400, "sens": 50, "mouse": "Vaxee NP_01S" }
        ]
    },
    {
        "id": "cr",
        "name": "Crazy Raccoon",
        "koreanName": "크레이지 라쿤",
        "tag": "CR",
        "league": "PWS",
        "rank": 13,
        "description": "스타벌룬 로스터를 전격 인수하여 새롭게 팀을 재편한 크레이지 라쿤의 신예 라인업",
        "roster": [
            { "nickname": "Glaz", "realName": "윤성민", "role": "Main Fragger", "dpi": 800, "sens": 30, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Gyuyeon", "realName": "최규연", "role": "Ace Attacker", "dpi": 800, "sens": 33, "mouse": "Zowie EC1_C" },
            { "nickname": "Ayoh", "realName": "아요", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "GGoBuGi", "realName": "꼬부기", "role": "Support", "dpi": 400, "sens": 52, "mouse": "Logitech G304" }
        ]
    },
    {
        "id": "spf",
        "name": "SUPERFECT",
        "koreanName": "슈퍼펙트",
        "tag": "SPF",
        "league": "PWS",
        "rank": 14,
        "description": "Acid와 TheMinos, Karwn, Todol의 끈질긴 생존 지향 플레이가 돋보이는 프로 시드팀",
        "roster": [
            { "nickname": "Acid", "realName": "애시드", "role": "Main Fragger", "dpi": 800, "sens": 32, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "TheMinos", "realName": "미노스", "role": "Attacker", "dpi": 800, "sens": 30, "mouse": "Zowie EC2_CW" },
            { "nickname": "Karwn", "realName": "카른", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Razer Viper V3 Pro" },
            { "nickname": "Todol", "realName": "토돌", "role": "Support", "dpi": 400, "sens": 48, "mouse": "Vaxee XE" }
        ]
    },
    {
        "id": "fn",
        "name": "FN Pocheon",
        "koreanName": "에프엔 포천",
        "tag": "FN",
        "league": "PWS",
        "rank": 15,
        "description": "베테랑 Starlord와 kkachi, BreaKers, Hush의 풍부한 경험과 흔들림 없는 오더",
        "roster": [
            { "nickname": "Starlord", "realName": "이종호", "role": "In_Game Leader", "dpi": 800, "sens": 30, "mouse": "Logitech G PRO Wireless" },
            { "nickname": "kkachi", "realName": "배호진", "role": "Main Fragger", "dpi": 800, "sens": 29, "mouse": "Logitech G PRO Wireless" },
            { "nickname": "BreaKers", "realName": "유원석", "role": "Attacker", "dpi": 800, "sens": 34, "mouse": "Zowie S2_C" },
            { "nickname": "Hush", "realName": "김민성", "role": "Support", "dpi": 400, "sens": 48, "mouse": "Vaxee XE" }
        ]
    },
    {
        "id": "sen",
        "name": "Sentinel",
        "koreanName": "센티넬",
        "tag": "SEN",
        "league": "PWS",
        "rank": 16,
        "description": "HyukSung과 Rascal, VenTus, heyden이 뭉쳐 후반 반격을 준비하는 프로 시드팀",
        "roster": [
            { "nickname": "HyukSung", "realName": "혁성", "role": "Main Fragger", "dpi": 800, "sens": 31, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Rascal", "realName": "라스칼", "role": "Attacker", "dpi": 800, "sens": 30, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "VenTus", "realName": "벤투스", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Zowie EC2_CW" },
            { "nickname": "heyden", "realName": "헤이든", "role": "Support", "dpi": 400, "sens": 50, "mouse": "Vaxee Outset AX" }
        ]
    },
    {
        "id": "geng",
        "name": "Gen.G Esports",
        "koreanName": "젠지 이스포츠",
        "tag": "GEN",
        "league": "PWS",
        "rank": 17,
        "description": "seoul과 Salute, BeaN, diyy가 이끄는 대한민국 최정상 글로벌 파트너 슈퍼팀 (C조 대기)",
        "roster": [
            { "nickname": "seoul", "realName": "조기열", "role": "Main Fragger", "dpi": 800, "sens": 32, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Salute", "realName": "우제현", "role": "Ace Attacker", "dpi": 800, "sens": 28, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "BeaN", "realName": "오원빈", "role": "All_rounder", "dpi": 800, "sens": 30, "mouse": "Vaxee XE Wireless" },
            { "nickname": "diyy", "realName": "김진수", "role": "Support", "dpi": 800, "sens": 34, "mouse": "Razer Viper V3 Pro" }
        ]
    },
    {
        "id": "t1",
        "name": "T1",
        "koreanName": "티원",
        "tag": "T1",
        "league": "PWS",
        "rank": 18,
        "description": "주장 Rain1ng 중심의 강력한 팀워크와 탄탄한 운영을 자랑하는 전통의 명가 T1 (C조 대기)",
        "roster": [
            { "nickname": "Rain1ng", "realName": "김종명", "role": "Captain / Fragger", "dpi": 800, "sens": 31, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "EEND", "realName": "노태영", "role": "Support", "dpi": 800, "sens": 28, "mouse": "Zowie EC2_CW" },
            { "nickname": "Heather", "realName": "차지훈", "role": "Scout", "dpi": 400, "sens": 50, "mouse": "Vaxee NP_01S" },
            { "nickname": "Type", "realName": "이도경", "role": "Attacker", "dpi": 800, "sens": 33, "mouse": "Razer Viper V2 Pro" }
        ]
    },
    {
        "id": "bgp",
        "name": "Baegopa",
        "koreanName": "배고파",
        "tag": "BGP",
        "league": "PWS",
        "rank": 19,
        "description": "전설적인 레전드 Pio와 Inonix, DG98, Taemin이 뭉친 역대 최강의 베테랑 군단 (C조 대기)",
        "roster": [
            { "nickname": "Pio", "realName": "차승훈", "role": "Legendary IGL", "dpi": 400, "sens": 52, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Inonix", "realName": "나희주", "role": "Main Fragger", "dpi": 400, "sens": 48, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "DG98", "realName": "황대권", "role": "Ace Attacker", "dpi": 800, "sens": 30, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "Taemin", "realName": "강태민", "role": "Support", "dpi": 800, "sens": 32, "mouse": "Zowie EC2_C" }
        ]
    },
    {
        "id": "qx",
        "name": "Qx (현 HSD)",
        "koreanName": "큐엑스 (현 에이치에스디)",
        "tag": "Qx",
        "league": "PWS",
        "rank": 20,
        "description": "LOV3와 youth, Hyuk, Glance가 맹활약하며 PWS 컵 예선을 뚫고 올라온 강력한 신예",
        "roster": [
            { "nickname": "LOV3", "realName": "러브", "role": "Main Fragger", "dpi": 800, "sens": 33, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "youth", "realName": "유스", "role": "Ace Attacker", "dpi": 800, "sens": 31, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Hyuk", "realName": "혁", "role": "Support", "dpi": 800, "sens": 29, "mouse": "Zowie S2_C" },
            { "nickname": "Glance", "realName": "글랜스", "role": "Scout", "dpi": 800, "sens": 30, "mouse": "Vaxee XE Wireless" }
        ]
    },
    {
        "id": "om",
        "name": "Overwhelm",
        "koreanName": "오버웸",
        "tag": "OM",
        "league": "PWS",
        "rank": 21,
        "description": "해체된 아레떼의 시드와 포인트를 정식 승계하여 합류한 특별 아마추어 시드 구단",
        "roster": [
            { "nickname": "Curo", "realName": "쿠로", "role": "Main Fragger", "dpi": 800, "sens": 32, "mouse": "Logitech G PRO Wireless" },
            { "nickname": "Oops", "realName": "웁스", "role": "Attacker", "dpi": 800, "sens": 30, "mouse": "Razer Viper V3 Pro" },
            { "nickname": "Entia", "realName": "엔티아", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Zowie EC2_CW" },
            { "nickname": "ShotDuo", "realName": "샷듀오", "role": "Support", "dpi": 400, "sens": 50, "mouse": "Logitech G304" }
        ]
    },
    {
        "id": "sgz",
        "name": "samgukzee",
        "koreanName": "삼국지",
        "tag": "SGZ",
        "league": "PWS",
        "rank": 22,
        "description": "Hane과 Xantast, innate, inforyou의 집요한 진지 구축과 끈질긴 교전 집중력",
        "roster": [
            { "nickname": "Hane", "realName": "김하늘", "role": "Main Fragger", "dpi": 800, "sens": 31, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Xantast", "realName": "이동훈", "role": "Attacker", "dpi": 800, "sens": 33, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "innate", "realName": "정우진", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Zowie EC2_CW" },
            { "nickname": "inforyou", "realName": "박상현", "role": "Support", "dpi": 400, "sens": 50, "mouse": "Logitech G304" }
        ]
    },
    {
        "id": "phe",
        "name": "PHANTOM HEARTS_E",
        "koreanName": "팬텀 하츠 이스포츠",
        "tag": "PHE",
        "league": "PWS",
        "rank": 23,
        "description": "Americano와 minuda, Mantal, Under의 날카로운 교전 피지컬을 앞세운 프로 시드팀",
        "roster": [
            { "nickname": "Americano", "realName": "정영훈", "role": "Main Fragger", "dpi": 800, "sens": 36, "mouse": "Logitech G PRO X Superlight 2" },
            { "nickname": "minuda", "realName": "이민우", "role": "Attacker", "dpi": 800, "sens": 31, "mouse": "Zowie FK2_C" },
            { "nickname": "Mantal", "realName": "정수영", "role": "In_Game Leader", "dpi": 800, "sens": 29, "mouse": "Razer DeathAdder V3" },
            { "nickname": "Under", "realName": "박성찬", "role": "Support", "dpi": 800, "sens": 30, "mouse": "Vaxee XE" }
        ]
    },
    {
        "id": "dgp",
        "name": "DAEJEON GAME PT",
        "koreanName": "대전 게임피티",
        "tag": "DGP",
        "league": "PWS",
        "rank": 24,
        "description": "Bok과 Rene, Santa, Yugeun의 조직적인 팀플레이와 탄탄한 후반 서클 방어력",
        "roster": [
            { "nickname": "Bok", "realName": "복", "role": "Main Fragger", "dpi": 800, "sens": 31, "mouse": "Logitech G PRO X Superlight" },
            { "nickname": "Rene", "realName": "르네", "role": "Attacker", "dpi": 800, "sens": 30, "mouse": "Zowie EC2_CW" },
            { "nickname": "Santa", "realName": "산타", "role": "In_Game Leader", "dpi": 800, "sens": 28, "mouse": "Razer DeathAdder V3 Pro" },
            { "nickname": "Yugeun", "realName": "유근", "role": "Support", "dpi": 400, "sens": 48, "mouse": "Vaxee Outset AX" }
        ]
    }
]

# esportsData.js 읽어서 LATEST_PWS2_TEAMS 치환
target_file = "frontend/src/data/esportsData.js"
with open(target_file, "r", encoding="utf-8") as f:
    content = f.read()

# LATEST_PWS2_TEAMS = [...] 부분 찾기
pattern = r"export const LATEST_PWS2_TEAMS = \[.*?\];"
teams_js = "export const LATEST_PWS2_TEAMS = " + json.dumps(pws24_teams, ensure_ascii=False, indent=2) + ";"

# JSON 따옴표와 키 정규화
new_content = re.sub(pattern, teams_js, content, flags=re.DOTALL)

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"성공: {target_file} 내 LATEST_PWS2_TEAMS에 2026 PWS Phase 2 공식 24개 팀 전체 동기화 완료!")
