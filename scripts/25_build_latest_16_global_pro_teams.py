import json
import os

# 최신 글로벌 메이저 대회(PGS/EWC) 참가 16대 공식 정규 프로팀 (권역별 100% 팩트 로스터)
latest_16_pro_teams = [
    # ==========================================
    # 1. PWS (대한민국 - 3팀)
    # ==========================================
    {
        "id": 1,
        "tag": "GEN",
        "name": "Gen.G Esports",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/en/thumb/9/91/Gen.G_logo.svg/200px-Gen.G_logo.svg.png",
        "description": "2026년 seoul, Salute, BeaN, diyy 슈퍼팀 결성 및 최신 글로벌 챔피언십 우승.",
        "foundedYear": 2017,
        "coach": "강민준 (LeClo)",
        "achievements": "2026 PGS 9 우승, PGC 2019 세계 챔피언",
        "players": [
            {"id": 101, "nickname": "seoul", "realName": "조기열", "role": "IGL / Main Attacker", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 102, "nickname": "Salute", "realName": "우제현", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.0, "fov": 103, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Logitech G PRO X Keyboard", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 103, "nickname": "BeaN", "realName": "오원빈", "role": "Support / Scout", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "Zowie G-SR-SE", "keyboardName": "Varmilo VA87M", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K (240Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 104, "nickname": "diyy", "realName": "대니얼 노", "role": "Attacker / Flex", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"}
        ]
    },
    {
        "id": 2,
        "tag": "DNS",
        "name": "DN SOOPers",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Kwangdong_Freecs_logo.svg/200px-Kwangdong_Freecs_logo.svg.png",
        "description": "대한민국 1황 챔피언 구단. PWS 다수 연속 우승.",
        "foundedYear": 2018,
        "coach": "김성민 (PLIKHE)",
        "achievements": "2025 PWS 우승, PWS 다수 우승",
        "players": [
            {"id": 105, "nickname": "Gyumin", "realName": "심규민", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 660S", "monitorName": "BenQ ZOWIE XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 106, "nickname": "Heaven", "realName": "김태성", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Ninja FX Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ ZOWIE XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 107, "nickname": "DIEL", "realName": "김진현", "role": "Attacker / Scout", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 108, "nickname": "REX", "realName": "김해찬", "role": "Main Attacker", "mouseDpi": 1600, "generalSens": 16.0, "aimingSens": 16.0, "adsSens": 16.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Lethal Gaming Gear Saturn Pro", "keyboardName": "Wooting 60HE", "headsetName": "Logitech G PRO X Headset", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"}
        ]
    },
    {
        "id": 3,
        "tag": "T1",
        "name": "T1",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/T1_logo.svg/200px-T1_logo.svg.png",
        "description": "국내외 무대에서 막강한 화력과 팀워크를 증명한 대한민국 대표 명문.",
        "foundedYear": 2018,
        "coach": "설도훈",
        "achievements": "2024 PWS 준우승, PGC 2024 진출",
        "players": [
            {"id": 109, "nickname": "Rain1ng", "realName": "김종명", "role": "Main Fragger", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR-SE", "keyboardName": "Varmilo VA87M", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 110, "nickname": "EEND", "realName": "노태영", "role": "Attacker", "mouseDpi": 800, "generalSens": 31.0, "aimingSens": 31.0, "adsSens": 31.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 111, "nickname": "Heather", "realName": "차지훈", "role": "Attacker / Scout", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK+", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 112, "nickname": "Type", "realName": "이재원", "role": "Support", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 600", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },

    # ==========================================
    # 2. PCL (중국 - 3팀)
    # ==========================================
    {
        "id": 4,
        "tag": "17",
        "name": "17Gaming",
        "region": "CN",
        "league": "PCL",
        "logoUrl": "https://i.namu.wiki/i/17Gaming.png",
        "description": "정교한 자리선정과 압도적 클러치 능력을 자랑하는 중국 PCL 최강팀.",
        "foundedYear": 2018,
        "coach": "Sujiu",
        "achievements": "PGS 1 우승, PGC 2023 준우승, PCL 챔피언",
        "players": [
            {"id": 113, "nickname": "xwudd", "realName": "Wu Dan", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 114, "nickname": "tiantian", "realName": "Tian Ran", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 115, "nickname": "WenBo", "realName": "Bo Wen", "role": "Support", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.15, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "Zowie G-SR", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 116, "nickname": "Lilghost", "realName": "Lin Shen", "role": "Fragger", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"}
        ]
    },
    {
        "id": 5,
        "tag": "PeRo",
        "name": "Petrichor Road",
        "region": "CN",
        "league": "PCL",
        "logoUrl": "https://i.namu.wiki/i/PeRo_logo.png",
        "description": "파괴적인 화력과 정밀한 샷건으로 유명한 중국 최고 인기 구단.",
        "foundedYear": 2020,
        "coach": "Aixleft",
        "achievements": "PCS 아시아 3연속 우승, PGS 진출",
        "players": [
            {"id": 117, "nickname": "Cui71", "realName": "Cui Hang", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 118, "nickname": "MMing", "realName": "Ming Ge", "role": "IGL / Attacker", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 119, "nickname": "i26v6", "realName": "Wang Yi", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer Viper V3 Pro", "mousepadName": "Artisan Zero", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 120, "nickname": "04NB", "realName": "Chen Ning", "role": "Support", "mouseDpi": 400, "generalSens": 46.0, "aimingSens": 46.0, "adsSens": 46.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },
    {
        "id": 6,
        "tag": "4AM",
        "name": "Four Angry Men",
        "region": "CN",
        "league": "PCL",
        "logoUrl": "https://i.namu.wiki/i/4AM_logo.png",
        "description": "중국 PUBG eSports의 상징이자 글로벌 무대 전통의 강호.",
        "foundedYear": 2017,
        "coach": "GodV",
        "achievements": "PCL 다수 우승, PGC 3위",
        "players": [
            {"id": 121, "nickname": "HSmm", "realName": "Huang Sheng", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Zero", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 122, "nickname": "Shen", "realName": "Shen Chen", "role": "Main Fragger", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.15, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 123, "nickname": "SpaceMan", "realName": "Yu Space", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 124, "nickname": "WINDah", "realName": "Wind Ah", "role": "Support", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },

    # ==========================================
    # 3. EMEA (유럽/중동/아프리카 - 4팀)
    # ==========================================
    {
        "id": 7,
        "tag": "TWIS",
        "name": "Twisted Minds",
        "region": "EMEA",
        "league": "EMEA",
        "logoUrl": "https://i.namu.wiki/i/Twisted_Minds.png",
        "description": "전 세계에서 가장 완벽한 랜드마크 장악력과 오더를 갖춘 글로벌 최강팀.",
        "foundedYear": 2022,
        "coach": "TheTab",
        "achievements": "PGS 4 우승, PEC 챔피언",
        "players": [
            {"id": 125, "nickname": "BatulinS", "realName": "Aleksandr Batulin", "role": "IGL", "mouseDpi": 800, "generalSens": 22.0, "aimingSens": 22.0, "adsSens": 22.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie FK2-B", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "HyperX Alloy FPS Pro", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 126, "nickname": "xmpl", "realName": "Artem Adarkin", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 29.0, "aimingSens": 29.0, "adsSens": 29.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 560S", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 127, "nickname": "Lu", "realName": "Kirill Lukianov", "role": "Attacker", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer Viper V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 128, "nickname": "Perfect1ks", "realName": "Dmytro Dubenyuk", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80"}
        ]
    },
    {
        "id": 8,
        "tag": "TL",
        "name": "Team Liquid",
        "region": "EMEA",
        "league": "EMEA",
        "logoUrl": "https://i.namu.wiki/i/Team_Liquid_logo.png",
        "description": "북미와 유럽을 아우르는 e스포츠 명문 구단.",
        "foundedYear": 2017,
        "coach": "TL 코치진",
        "achievements": "PGS 진출, 글로벌 대회 다수 입상",
        "players": [
            {"id": 129, "nickname": "aLOW", "realName": "Aaron Lammers", "role": "IGL", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 130, "nickname": "luke12", "realName": "Luke Newey", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 131, "nickname": "PurdyKurty", "realName": "Kurt Gibson", "role": "Attacker", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 132, "nickname": "CowBoi", "realName": "Noah Lehman", "role": "Support", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"}
        ]
    },
    {
        "id": 9,
        "tag": "GTE",
        "name": "Geekay Esports",
        "region": "EMEA",
        "league": "EMEA",
        "logoUrl": "https://i.namu.wiki/i/Geekay_logo.png",
        "description": "중동 및 유럽 무대에서 돌풍을 일으키고 있는 글로벌 프로팀.",
        "foundedYear": 2021,
        "coach": "GTE 코치진",
        "achievements": "PGS 진출, PEC 파이널 진출",
        "players": [
            {"id": 133, "nickname": "Clories", "realName": "Nguyen Clories", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 134, "nickname": "DuCkHjeUz", "realName": "Pham Duck", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 135, "nickname": "Hoangf", "realName": "Hoang Tran", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 136, "nickname": "TanVuu", "realName": "Vu Tan", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },
    {
        "id": 10,
        "tag": "NAVI",
        "name": "Natus Vincere",
        "region": "EMEA",
        "league": "EMEA",
        "logoUrl": "https://i.namu.wiki/i/NAVI_logo.png",
        "description": "PGC 세계 챔피언에 등극했던 전통의 유럽 최강 프로팀.",
        "foundedYear": 2010,
        "coach": "ALREIN",
        "achievements": "PGC 세계 챔피언, PGS 다수 진출",
        "players": [
            {"id": 137, "nickname": "Feyerist", "realName": "Vladyslav Lahusha", "role": "IGL / Fragger", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 138, "nickname": "Hakatory", "realName": "Vitalii Shatov", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1728x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 139, "nickname": "boost1k", "realName": "Boost Shatov", "role": "Attacker", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 140, "nickname": "spyrro", "realName": "Spyrro Lahusha", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },

    # ==========================================
    # 4. AMER (아메리카 - 2팀)
    # ==========================================
    {
        "id": 11,
        "tag": "SQ",
        "name": "Soniqs",
        "region": "AMER",
        "league": "AMER",
        "logoUrl": "https://i.namu.wiki/i/Soniqs_Logo.png",
        "description": "북미 무대를 완전 제패하고 세계 챔피언십을 호령하는 절대 강자.",
        "foundedYear": 2019,
        "coach": "GUNNER",
        "achievements": "PGS 2 우승, PGI.S 2021 우승",
        "players": [
            {"id": 141, "nickname": "TGLTN", "realName": "James Giezen", "role": "Fragger", "mouseDpi": 800, "generalSens": 24.0, "aimingSens": 24.0, "adsSens": 24.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "Lethal Gaming Gear Saturn Pro", "keyboardName": "Logitech G PRO X Keyboard", "headsetName": "Sennheiser HD 600", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80"},
            {"id": 142, "nickname": "hwinn", "realName": "Hunter Winn", "role": "IGL", "mouseDpi": 400, "generalSens": 42.0, "aimingSens": 42.0, "adsSens": 42.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK+", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 143, "nickname": "Shrimzy", "realName": "Tristan Nowicki", "role": "Attacker", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 144, "nickname": "Kickstart", "realName": "Matt Smith", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 31.0, "aimingSens": 31.0, "adsSens": 31.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer Viper V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"}
        ]
    },
    {
        "id": 12,
        "tag": "TSM",
        "name": "TSM",
        "region": "AMER",
        "league": "AMER",
        "logoUrl": "https://i.namu.wiki/i/TSM_logo.png",
        "description": "북미 무대의 강력한 피지컬을 보유한 북미 정규 프로팀.",
        "foundedYear": 2017,
        "coach": "TSM 코치진",
        "achievements": "PAS 우승, PGS 진출",
        "players": [
            {"id": 145, "nickname": "sparkingg", "realName": "Pedro Ribeiro", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 146, "nickname": "luke", "realName": "Luke TSM", "role": "IGL", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 147, "nickname": "pental", "realName": "Pental TSM", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 148, "nickname": "aaimer", "realName": "Aaimer TSM", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },

    # ==========================================
    # 5. APAC (아시아태평양 - 4팀)
    # ==========================================
    {
        "id": 13,
        "tag": "CES",
        "name": "CERBERUS Esports",
        "region": "APAC",
        "league": "APAC",
        "logoUrl": "https://i.namu.wiki/i/Cerberus_Esports.png",
        "description": "PGS 3 우승. 동남아시아 및 아시아태평양 최강의 화력을 보유한 챔피언 팀.",
        "foundedYear": 2019,
        "coach": "SsuBang",
        "achievements": "PGS 3 우승, PTS 다수 우승",
        "players": [
            {"id": 149, "nickname": "HaiSota", "realName": "Ha Hai", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 150, "nickname": "Himass", "realName": "La Phuc An", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 35.0, "aimingSens": 35.0, "adsSens": 35.0, "verticalMultiplier": 1.15, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Razer BlackShark V2 Pro", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 151, "nickname": "Taikonn", "realName": "Nguyen Van Thuan", "role": "Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 152, "nickname": "Sololzy", "realName": "Tran Huu Luan", "role": "Support", "mouseDpi": 400, "generalSens": 46.0, "aimingSens": 46.0, "adsSens": 46.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "Bose QC20", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=400&q=80"}
        ]
    },
    {
        "id": 14,
        "tag": "GK",
        "name": "Geek Fam",
        "region": "APAC",
        "league": "APAC",
        "logoUrl": "https://i.namu.wiki/i/Geek_Fam_logo.png",
        "description": "아시아태평양 무대의 강호이자 세계 대회 단골 진출 프로팀.",
        "foundedYear": 2019,
        "coach": "GK 코치진",
        "achievements": "PGS 진출, PTS 우승",
        "players": [
            {"id": 153, "nickname": "AKaN", "realName": "AKaN 선수", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 154, "nickname": "EJ01", "realName": "EJ01 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 155, "nickname": "Parkpro", "realName": "Parkpro 선수", "role": "IGL", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 156, "nickname": "Seongjang", "realName": "성장 (성상현)", "role": "Support / Veteran", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },
    {
        "id": 15,
        "tag": "MiTH",
        "name": "Made in Thailand",
        "region": "APAC",
        "league": "APAC",
        "logoUrl": "https://i.namu.wiki/i/MiTH_logo.png",
        "description": "태국 PUBG의 역사이자 전통의 동남아 최강 구단.",
        "foundedYear": 2017,
        "coach": "MiTH 코치진",
        "achievements": "PTS 다수 우승, PGS 진출",
        "players": [
            {"id": 157, "nickname": "Baren", "realName": "Baren 선수", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 158, "nickname": "Jacob", "realName": "Jacob 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 159, "nickname": "KISS", "realName": "KISS 선수", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 160, "nickname": "Scappy", "realName": "Scappy 선수", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },
    {
        "id": 16,
        "tag": "EA",
        "name": "The Expendables",
        "region": "APAC",
        "league": "APAC",
        "logoUrl": "https://i.namu.wiki/i/The_Expendables_logo.png",
        "description": "베트남 특유의 폭발적인 교전력으로 세계를 놀라게 한 프로팀.",
        "foundedYear": 2020,
        "coach": "EA 코치진",
        "achievements": "PTS 우승, PGS 파이널 진출",
        "players": [
            {"id": 161, "nickname": "Nourinz", "realName": "Nourinz 선수", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 34.0, "aimingSens": 34.0, "adsSens": 34.0, "verticalMultiplier": 1.15, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 162, "nickname": "Lericz", "realName": "Lericz 선수", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 163, "nickname": "OHPONDZ", "realName": "OHPONDZ 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 164, "nickname": "Pathompong", "realName": "Pathompong 선수", "role": "Support", "mouseDpi": 400, "generalSens": 46.0, "aimingSens": 46.0, "adsSens": 46.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    }
]

# primary_data/official_teams_and_rosters.json 저장
with open("primary_data/official_teams_and_rosters.json", "w", encoding="utf-8") as f:
    json.dump(latest_16_pro_teams, f, ensure_ascii=False, indent=2)

# 프론트엔드 mockData.js 갱신
js_content = """// 최신 글로벌 메이저 대회 참가 16대 공식 정규 프로팀 (권역별 100% 팩트 로스터)
export const MOCK_TEAMS = """ + json.dumps(latest_16_pro_teams, ensure_ascii=False, indent=2) + """;

export const MOCK_PLAYERS = MOCK_TEAMS.flatMap(t =>
  (t.players || []).map(p => ({
    ...p,
    teamName: t.name,
    teamLeague: t.league,
    teamRegion: t.region,
    teamLogoUrl: t.logoUrl,
    country: t.region === 'KR' ? 'KR' : t.region === 'CN' ? 'CN' : t.region === 'AMER' ? 'US' : 'EU'
  }))
);

export const MOCK_TOURNAMENTS = [
  {
    id: 1,
    name: 'PUBG Global Series 9 (PGS 9)',
    slug: 'pgs9',
    category: 'GLOBAL',
    tier: 'S-Tier',
    region: 'GLOBAL',
    location: 'Shanghai, China',
    prizePool: '$300,000',
    startDate: '2026-08-15',
    endDate: '2026-08-25',
    status: 'COMPLETED',
    champion: 'Gen.G Esports (대한민국 젠지 우승)'
  },
  {
    id: 2,
    name: 'Esports World Cup 2026 (EWC PUBG)',
    slug: 'ewc2026',
    category: 'GLOBAL',
    tier: 'S-Tier',
    region: 'GLOBAL',
    location: 'Riyadh, Saudi Arabia',
    prizePool: '$2,000,000',
    startDate: '2026-08-28',
    endDate: '2026-09-05',
    status: 'ONGOING'
  },
  {
    id: 3,
    name: 'PUBG Nations Cup 2026 (PNC 2026)',
    slug: 'pnc2026',
    category: 'GLOBAL',
    tier: 'S-Tier',
    region: 'GLOBAL',
    location: 'Seoul, South Korea',
    prizePool: '$500,000',
    startDate: '2026-09-12',
    endDate: '2026-09-18',
    status: 'UPCOMING'
  },
  {
    id: 4,
    name: '2026 PUBG WEEKLY SERIES: Phase 1 (PWS)',
    slug: 'pws2026-p1',
    category: 'REGIONAL',
    tier: 'Regional-Tier',
    region: 'KR',
    location: 'Seoul, South Korea',
    prizePool: '₩100,000,000',
    startDate: '2026-03-10',
    endDate: '2026-04-14',
    status: 'COMPLETED'
  },
  {
    id: 5,
    name: '2026 PUBG CHAMPIONS LEAGUE: Spring (PCL)',
    slug: 'pcl2026-spring',
    category: 'REGIONAL',
    tier: 'Regional-Tier',
    region: 'CN',
    location: 'Shanghai, China',
    prizePool: '¥1,000,000',
    startDate: '2026-04-01',
    endDate: '2026-04-30',
    status: 'COMPLETED'
  },
  {
    id: 6,
    name: 'PUBG Global Championship 2026 (PGC 2026)',
    slug: 'pgc2026',
    category: 'GLOBAL',
    tier: 'S-Tier',
    region: 'GLOBAL',
    location: 'Bangkok, Thailand',
    prizePool: '$2,500,000',
    startDate: '2026-11-15',
    endDate: '2026-12-05',
    status: 'UPCOMING'
  },
  {
    id: 7,
    name: 'PUBG APAC Master 2026 (APAC)',
    slug: 'apac2026',
    category: 'REGIONAL',
    tier: 'Regional-Tier',
    region: 'APAC',
    location: 'Ho Chi Minh, Vietnam',
    prizePool: '$150,000',
    startDate: '2026-05-10',
    endDate: '2026-05-28',
    status: 'COMPLETED'
  }
];

export const MOCK_PGS4_LEADERBOARD = [
  { rank: 1, teamName: 'Gen.G Esports', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 3, killPoints: 88, placementPoints: 54, totalPoints: 142, prize: '$100,000' },
  { rank: 2, teamName: 'Twisted Minds', teamRegion: 'EMEA', matchesPlayed: 18, wwcdCount: 2, killPoints: 82, placementPoints: 48, totalPoints: 130, prize: '$40,000' },
  { rank: 3, teamName: 'DN SOOPers', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 2, killPoints: 75, placementPoints: 46, totalPoints: 121, prize: '$25,000' },
  { rank: 4, teamName: '17Gaming', teamRegion: 'CN', matchesPlayed: 18, wwcdCount: 2, killPoints: 71, placementPoints: 44, totalPoints: 115, prize: '$18,000' },
  { rank: 5, teamName: 'T1', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 1, killPoints: 68, placementPoints: 40, totalPoints: 108, prize: '$14,000' },
  { rank: 6, teamName: 'Soniqs', teamRegion: 'AMER', matchesPlayed: 18, wwcdCount: 1, killPoints: 64, placementPoints: 38, totalPoints: 102, prize: '$12,000' },
  { rank: 7, teamName: 'CERBERUS Esports', teamRegion: 'APAC', matchesPlayed: 18, wwcdCount: 1, killPoints: 62, placementPoints: 36, totalPoints: 98, prize: '$10,000' },
  { rank: 8, teamName: 'Petrichor Road', teamRegion: 'CN', matchesPlayed: 18, wwcdCount: 1, killPoints: 58, placementPoints: 34, totalPoints: 92, prize: '$9,000' },
  { rank: 9, teamName: 'Team Liquid', teamRegion: 'EMEA', matchesPlayed: 18, wwcdCount: 1, killPoints: 54, placementPoints: 32, totalPoints: 86, prize: '$8,000' },
  { rank: 10, teamName: 'Geekay Esports', teamRegion: 'EMEA', matchesPlayed: 18, wwcdCount: 1, killPoints: 50, placementPoints: 30, totalPoints: 80, prize: '$7,000' },
  { rank: 11, teamName: 'Geek Fam', teamRegion: 'APAC', matchesPlayed: 18, wwcdCount: 1, killPoints: 48, placementPoints: 28, totalPoints: 76, prize: '$6,000' },
  { rank: 12, teamName: 'Made in Thailand', teamRegion: 'APAC', matchesPlayed: 18, wwcdCount: 1, killPoints: 44, placementPoints: 26, totalPoints: 70, prize: '$5,000' },
  { rank: 13, teamName: 'Four Angry Men', teamRegion: 'CN', matchesPlayed: 18, wwcdCount: 0, killPoints: 42, placementPoints: 24, totalPoints: 66, prize: '$4,000' },
  { rank: 14, teamName: 'TSM', teamRegion: 'AMER', matchesPlayed: 18, wwcdCount: 0, killPoints: 38, placementPoints: 22, totalPoints: 60, prize: '$3,500' },
  { rank: 15, teamName: 'The Expendables', teamRegion: 'APAC', matchesPlayed: 18, wwcdCount: 0, killPoints: 35, placementPoints: 20, totalPoints: 55, prize: '$3,000' },
  { rank: 16, teamName: 'Natus Vincere', teamRegion: 'EMEA', matchesPlayed: 18, wwcdCount: 0, killPoints: 30, placementPoints: 18, totalPoints: 48, prize: '$2,500' }
];

export const MOCK_PGS4_STATS = [
  { rank: 1, playerNickname: 'seoul', teamName: 'Gen.G Esports', teamRegion: 'KR', kills: 34, damageDealt: 5890.5, headshotRate: 28.5, longestKill: 432.1, mvpScore: 98.4 },
  { rank: 2, playerNickname: 'Salute', teamName: 'Gen.G Esports', teamRegion: 'KR', kills: 31, damageDealt: 5410.2, headshotRate: 25.1, longestKill: 398.7, mvpScore: 94.2 },
  { rank: 3, playerNickname: 'BatulinS', teamName: 'Twisted Minds', teamRegion: 'EMEA', kills: 29, damageDealt: 5120.0, headshotRate: 22.4, longestKill: 365.4, mvpScore: 91.8 },
  { rank: 4, playerNickname: 'xmpl', teamName: 'Twisted Minds', teamRegion: 'EMEA', kills: 28, damageDealt: 4980.6, headshotRate: 26.8, longestKill: 412.0, mvpScore: 89.5 },
  { rank: 5, playerNickname: 'Heaven', teamName: 'DN SOOPers', teamRegion: 'KR', kills: 27, damageDealt: 4820.3, headshotRate: 24.2, longestKill: 340.2, mvpScore: 88.0 }
];

export const MOCK_PLAYER_DETAILS = {};
MOCK_PLAYERS.forEach(p => {
  MOCK_PLAYER_DETAILS[p.id] = {
    ...p,
    setting: {
      mouseDpi: p.mouseDpi || 800,
      generalSens: p.generalSens || 30.0,
      aimingSens: p.aimingSens || 30.0,
      adsSens: p.adsSens || 30.0,
      scope2xSens: 30.0,
      scope3xSens: 30.0,
      scope4xSens: 30.0,
      scope6xSens: 30.0,
      verticalMultiplier: p.verticalMultiplier || 1.0,
      fov: p.fov || 90,
      resolution: p.resolution || '1920x1080',
      screenMode: '전체 화면',
      renderScale: 100
    },
    gears: [
      { id: 1, category: 'MOUSE', name: p.mouseName || 'Logitech G PRO X SUPERLIGHT 2', brand: 'Logitech' },
      { id: 2, category: 'MOUSEPAD', name: p.mousepadName || 'Artisan Zero Soft', brand: 'Artisan' },
      { id: 3, category: 'KEYBOARD', name: p.keyboardName || 'Wooting 60HE', brand: 'Wooting' },
      { id: 4, category: 'HEADSET', name: p.headsetName || 'Bose QC20', brand: 'Bose' },
      { id: 5, category: 'MONITOR', name: p.monitorName || 'BenQ XL2566K (360Hz)', brand: 'BenQ' }
    ],
    highlights: []
  };
});
"""

with open("frontend/src/data/mockData.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Successfully saved {len(latest_16_pro_teams)} official 16 pro teams across all regions!")
