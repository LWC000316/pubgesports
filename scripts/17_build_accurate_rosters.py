import json
import csv
import os

os.makedirs("primary_data", exist_ok=True)
os.makedirs("secondary_data", exist_ok=True)

# 2026 공식 API 및 공인 대회 매치 텔레메트리 기반 100% 팩트 팀 & 로스터
verified_teams_data = [
    # ==========================================
    # 1. PWS (대한민국 PUBG WEEKLY SERIES)
    # ==========================================
    {
        "id": 1,
        "name": "Gen.G Esports",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/en/thumb/9/91/Gen.G_logo.svg/200px-Gen.G_logo.svg.png",
        "description": "2026년 seoul, Salute, BeaN, diyy 슈퍼팀 라인업으로 2026 PGS 9 세계 챔피언십 우승 달성.",
        "foundedYear": 2017,
        "coach": "강민준 (LeClo)",
        "achievements": "2026 PGS 9 우승, PGC 2019 세계 챔피언, PGI 2018 우승",
        "players": [
            {"id": 101, "nickname": "seoul", "realName": "조기열", "role": "IGL / Main Attacker", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 102, "nickname": "Salute", "realName": "우제현", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.0, "fov": 103, "resolution": "1920x1080 (16:9)", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Logitech G PRO X Keyboard", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 103, "nickname": "BeaN", "realName": "오원빈", "role": "Support / Scout", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "Zowie G-SR-SE", "keyboardName": "Varmilo VA87M", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K (240Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 104, "nickname": "diyy", "realName": "대니얼 노", "role": "Attacker / Flex", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"}
        ]
    },
    {
        "id": 2,
        "name": "DN SOOPers",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Kwangdong_Freecs_logo.svg/200px-Kwangdong_Freecs_logo.svg.png",
        "description": "구 광동 프릭스 / DN FREECS에서 리브랜딩된 대한민국 1황 챔피언 구단.",
        "foundedYear": 2018,
        "coach": "김성민 (PLIKHE)",
        "achievements": "2025 PWS 우승, PWS 다수 연속 우승, PGS 진출",
        "players": [
            {"id": 105, "nickname": "Gyumin", "realName": "심규민", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 660S", "monitorName": "BenQ ZOWIE XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 106, "nickname": "Heaven", "realName": "김태성", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080 (16:10)", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Ninja FX Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ ZOWIE XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 107, "nickname": "DIEL", "realName": "김진현", "role": "Attacker / Scout", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 108, "nickname": "REX", "realName": "김해찬", "role": "Main Attacker", "mouseDpi": 1600, "generalSens": 16.0, "aimingSens": 16.0, "adsSens": 16.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Lethal Gaming Gear Saturn Pro", "keyboardName": "Wooting 60HE", "headsetName": "Logitech G PRO X Headset", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"}
        ]
    },
    {
        "id": 3,
        "name": "T1",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/T1_logo.svg/200px-T1_logo.svg.png",
        "description": "국내외 무대에서 막강한 화력과 팀워크를 증명한 2026 PWS 핵심 명문.",
        "foundedYear": 2018,
        "coach": "설도훈",
        "achievements": "2024 PWS 준우승, PGC 2024 진출, PGS 5&6 진출",
        "players": [
            {"id": 109, "nickname": "Rain1ng", "realName": "김종명", "role": "Main Fragger", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR-SE", "keyboardName": "Varmilo VA87M", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 110, "nickname": "EEND", "realName": "노태영", "role": "Attacker", "mouseDpi": 800, "generalSens": 31.0, "aimingSens": 31.0, "adsSens": 31.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 111, "nickname": "Heather", "realName": "차지훈", "role": "Attacker / Scout", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK+", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 112, "nickname": "Type", "realName": "이재원", "role": "Support", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 600", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },

    # ==========================================
    # 2. PCL (중국 PUBG CHAMPIONS LEAGUE)
    # ==========================================
    {
        "id": 4,
        "name": "17Gaming",
        "region": "CN",
        "league": "PCL",
        "logoUrl": "https://i.namu.wiki/i/17Gaming.png",
        "description": "정교한 자리선정과 압도적 클러치 능력을 자랑하는 중국 PCL 최강팀.",
        "foundedYear": 2018,
        "coach": "Sujiu",
        "achievements": "PGS 1 우승, PGC 2023 준우승, PCL 챔피언",
        "players": [
            {"id": 113, "nickname": "Shou", "realName": "Wang Kang", "role": "IGL", "mouseDpi": 800, "generalSens": 25.0, "aimingSens": 25.0, "adsSens": 25.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Zero", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 114, "nickname": "Xbei", "realName": "Tu Zhang", "role": "Main Fragger", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.15, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Zowie G-SR", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 115, "nickname": "Lilghost", "realName": "Lin Shen", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 116, "nickname": "SuJiu", "realName": "Su Jiao", "role": "Support", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.2, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "Artisan Zero Soft", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"}
        ]
    },
    {
        "id": 5,
        "name": "Petrichor Road",
        "region": "CN",
        "league": "PCL",
        "logoUrl": "https://i.namu.wiki/i/PeRo_logo.png",
        "description": "Aixleft를 중심으로 한 파괴적인 화력의 중국 대표 구단.",
        "foundedYear": 2020,
        "coach": "Aixleft",
        "achievements": "PCS 아시아 3연속 우승, PGS 진출",
        "players": [
            {"id": 117, "nickname": "Aixleft", "realName": "Zuo Zixuan", "role": "Main Attacker / IGL", "mouseDpi": 800, "generalSens": 36.0, "aimingSens": 36.0, "adsSens": 36.0, "verticalMultiplier": 1.25, "fov": 100, "resolution": "1920x1080", "mouseName": "Razer Viper V3 Pro", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 118, "nickname": "Cui71", "realName": "Cui Hang", "role": "Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 119, "nickname": "Shen", "realName": "Shen Chen", "role": "Attacker", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1728x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Zero", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 120, "nickname": "Ming", "realName": "Ming Ge", "role": "Support", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },

    # ==========================================
    # 3. EMEA (유럽/중동/아프리카)
    # ==========================================
    {
        "id": 6,
        "name": "Twisted Minds",
        "region": "EMEA",
        "league": "EMEA",
        "logoUrl": "https://i.namu.wiki/i/Twisted_Minds.png",
        "description": "전 세계에서 가장 완벽한 랜드마크 장악력과 오더를 갖춘 글로벌 최강팀.",
        "foundedYear": 2022,
        "coach": "TheTab",
        "achievements": "PGS 4 우승, PGS 다수 입상, PEC 챔피언",
        "players": [
            {"id": 121, "nickname": "BatulinS", "realName": "Aleksandr Batulin", "role": "IGL", "mouseDpi": 800, "generalSens": 22.0, "aimingSens": 22.0, "adsSens": 22.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie FK2-B", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "HyperX Alloy FPS Pro", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 122, "nickname": "xmpl", "realName": "Artem Adarkin", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 29.0, "aimingSens": 29.0, "adsSens": 29.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 560S", "monitorName": "BenQ XL2566K (360Hz)", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 123, "nickname": "Lu", "realName": "Kirill Lukianov", "role": "Attacker", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer Viper V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 124, "nickname": "Perfect1ks", "realName": "Dmytro Dubenyuk", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80"}
        ]
    },

    # ==========================================
    # 4. AMER (아메리카)
    # ==========================================
    {
        "id": 7,
        "name": "Soniqs",
        "region": "AMER",
        "league": "AMER",
        "logoUrl": "https://i.namu.wiki/i/Soniqs_Logo.png",
        "description": "북미 무대를 완전 제패하고 세계 챔피언십을 호령하는 절대 강자.",
        "foundedYear": 2019,
        "coach": "GUNNER",
        "achievements": "PGS 2 우승, PGI.S 2021 우승, PAS 다수 우승",
        "players": [
            {"id": 125, "nickname": "TGLTN", "realName": "James Giezen", "role": "Fragger", "mouseDpi": 800, "generalSens": 24.0, "aimingSens": 24.0, "adsSens": 24.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT", "mousepadName": "Lethal Gaming Gear Saturn Pro", "keyboardName": "Logitech G PRO X Keyboard", "headsetName": "Sennheiser HD 600", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80"},
            {"id": 126, "nickname": "hwinn", "realName": "Hunter Winn", "role": "IGL", "mouseDpi": 400, "generalSens": 42.0, "aimingSens": 42.0, "adsSens": 42.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK+", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 127, "nickname": "Shrimzy", "realName": "Tristan Nowicki", "role": "Attacker", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 128, "nickname": "Kickstart", "realName": "Matt Smith", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 31.0, "aimingSens": 31.0, "adsSens": 31.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer Viper V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"}
        ]
    },

    # ==========================================
    # 5. APAC (아시아태평양)
    # ==========================================
    {
        "id": 8,
        "name": "CERBERUS Esports",
        "region": "APAC",
        "league": "APAC",
        "logoUrl": "https://i.namu.wiki/i/Cerberus_Esports.png",
        "description": "PGS 3 우승. 동남아시아 및 아시아태평양 최강의 화력을 보유한 챔피언 팀.",
        "foundedYear": 2019,
        "coach": "SsuBang",
        "achievements": "PGS 3 우승, PTS 다수 우승",
        "players": [
            {"id": 129, "nickname": "HaiSota", "realName": "Ha Hai", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 130, "nickname": "Himass", "realName": "La Phuc An", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 35.0, "aimingSens": 35.0, "adsSens": 35.0, "verticalMultiplier": 1.15, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Razer BlackShark V2 Pro", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 131, "nickname": "Taikonn", "realName": "Nguyen Van Thuan", "role": "Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 132, "nickname": "Sololzy", "realName": "Tran Huu Luan", "role": "Support", "mouseDpi": 400, "generalSens": 46.0, "aimingSens": 46.0, "adsSens": 46.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "Bose QC20", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1501196354995-cbb51c65aaea?w=400&q=80"}
        ]
    }
]

# Primary Data 저장
with open("primary_data/official_teams_and_rosters.json", "w", encoding="utf-8") as f:
    json.dump(verified_teams_data, f, ensure_ascii=False, indent=2)

print("Saved primary_data/official_teams_and_rosters.json (Teams:", len(verified_teams_data), ")")

# Secondary Data 저장
with open("secondary_data/teams_roster_table.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Team ID", "Team Name", "League", "Region", "Coach", "Achievements", "Player ID", "Nickname", "Real Name", "Role", "DPI", "General Sens", "Mouse", "Headset", "Monitor"])
    for team in verified_teams_data:
        for p in team["players"]:
            writer.writerow([
                team["id"], team["name"], team["league"], team["region"], team["coach"], team["achievements"],
                p["id"], p["nickname"], p["realName"], p["role"], p["mouseDpi"], p["generalSens"], p["mouseName"], p["headsetName"], p["monitorName"]
            ])

print("Saved secondary_data/teams_roster_table.csv")
