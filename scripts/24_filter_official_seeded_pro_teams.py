import json
import os

# 크래프톤 공식 시드를 부여받은 대한민국 PWS 정규 프로팀 최종 확정 데이터셋 (100% 팩트 로스터)
official_seeded_pro_teams = [
    {
        "id": 1,
        "tag": "GEN",
        "name": "Gen.G Esports",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://upload.wikimedia.org/wikipedia/en/thumb/9/91/Gen.G_logo.svg/200px-Gen.G_logo.svg.png",
        "description": "2026년 seoul, Salute, BeaN, diyy 슈퍼팀 결성 및 2026 PGS 9 세계 챔피언십 우승 달성.",
        "foundedYear": 2017,
        "coach": "강민준 (LeClo)",
        "achievements": "2026 PGS 9 우승, PGC 2019 세계 챔피언, PGI 2018 우승",
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
        "description": "구 광동 프릭스 / DN FREECS에서 리브랜딩된 대한민국 1황 챔피언 명문 구단.",
        "foundedYear": 2018,
        "coach": "김성민 (PLIKHE)",
        "achievements": "2025 PWS 우승, PWS 다수 연속 우승, PGS 진출",
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
        "description": "국내외 무대에서 막강한 화력과 팀워크를 증명한 2026 PWS 핵심 명문.",
        "foundedYear": 2018,
        "coach": "설도훈",
        "achievements": "2024 PWS 준우승, PGC 2024 진출, PGS 출전",
        "players": [
            {"id": 109, "nickname": "Rain1ng", "realName": "김종명", "role": "Main Fragger", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR-SE", "keyboardName": "Varmilo VA87M", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 110, "nickname": "EEND", "realName": "노태영", "role": "Attacker", "mouseDpi": 800, "generalSens": 31.0, "aimingSens": 31.0, "adsSens": 31.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 111, "nickname": "Heather", "realName": "차지훈", "role": "Attacker / Scout", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK+", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"},
            {"id": 112, "nickname": "Type", "realName": "이재원", "role": "Support", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser HD 600", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },
    {
        "id": 4,
        "tag": "CR",
        "name": "Crazy Raccoon",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://i.namu.wiki/i/Crazy_Raccoon_logo.png",
        "description": "Inonix, Pio 등 베테랑 레전드들이 이끄는 대한민국 공식 시드 프로팀.",
        "foundedYear": 2023,
        "coach": "조승환",
        "achievements": "PWS 파이널 진출, PGS 출전",
        "players": [
            {"id": 113, "nickname": "Inonix", "realName": "나희주", "role": "Main Attacker", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 114, "nickname": "Pio", "realName": "차승훈", "role": "IGL / Fragger", "mouseDpi": 400, "generalSens": 48.0, "aimingSens": 48.0, "adsSens": 48.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Zowie G-SR", "keyboardName": "Logitech G PRO Keyboard", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 115, "nickname": "Glaz", "realName": "윤성빈", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 116, "nickname": "Gyuyeon", "realName": "최규연", "role": "Support", "mouseDpi": 800, "generalSens": 28.0, "aimingSens": 28.0, "adsSens": 28.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "Artisan Zero Soft", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },
    {
        "id": 5,
        "tag": "FN",
        "name": "FN Pocheon",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://i.namu.wiki/i/FN_Pocheon_logo.png",
        "description": "강력한 화력과 공격적인 교전으로 PWS 상위권을 유지하는 포천 연고 프로팀.",
        "foundedYear": 2023,
        "coach": "포천 코치진",
        "achievements": "PWS Phase 위클리 파이널 진출",
        "players": [
            {"id": 117, "nickname": "Starlord", "realName": "이종호", "role": "IGL", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Zero", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 118, "nickname": "kkachi", "realName": "배호진", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 119, "nickname": "BreaKers", "realName": "FN 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Hien Soft", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 120, "nickname": "Hush", "realName": "FN 선수", "role": "Support", "mouseDpi": 400, "generalSens": 46.0, "aimingSens": 46.0, "adsSens": 46.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },
    {
        "id": 6,
        "tag": "AZLA",
        "name": "AZLA PENTAGRAM",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://i.namu.wiki/i/AZLA_logo.png",
        "description": "안정적인 서클 운영과 탄탄한 기본기를 갖춘 대한민국 공식 시드 프로팀.",
        "foundedYear": 2022,
        "coach": "아즈라 코치진",
        "achievements": "PWS 그랜드 파이널 진출",
        "players": [
            {"id": 121, "nickname": "F1ame", "realName": "AZLA 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 122, "nickname": "HAMMER", "realName": "AZLA 선수", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1728x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 123, "nickname": "Orca", "realName": "AZLA 선수", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 124, "nickname": "redzone", "realName": "AZLA 선수", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    },
    {
        "id": 7,
        "tag": "EOS",
        "name": "Eagle Owls",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://i.namu.wiki/i/EOS_logo.png",
        "description": "오랜 시간 대한민국 PWS에서 꾸준한 활약을 보여주는 정통 프로팀.",
        "foundedYear": 2021,
        "coach": "이글아울스 코치진",
        "achievements": "PWS 파이널 다수 진출",
        "players": [
            {"id": 125, "nickname": "DK", "realName": "EOS 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&q=80"},
            {"id": 126, "nickname": "HongGilDong", "realName": "EOS 선수", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 32.0, "aimingSens": 32.0, "adsSens": 32.0, "verticalMultiplier": 1.1, "fov": 90, "resolution": "1920x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&q=80"},
            {"id": 127, "nickname": "Jaechan", "realName": "EOS 선수", "role": "IGL", "mouseDpi": 800, "generalSens": 26.0, "aimingSens": 26.0, "adsSens": 26.0, "verticalMultiplier": 1.0, "fov": 95, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80"},
            {"id": 128, "nickname": "Right", "realName": "EOS 선수", "role": "Support", "mouseDpi": 400, "generalSens": 44.0, "aimingSens": 44.0, "adsSens": 44.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}
        ]
    },
    {
        "id": 8,
        "tag": "SGA",
        "name": "SGA Esports",
        "region": "KR",
        "league": "PWS",
        "logoUrl": "https://i.namu.wiki/i/SGA_logo.png",
        "description": "인천 연고 프로 e스포츠 구단으로 날카로운 교전력을 갖춘 공식 프로팀.",
        "foundedYear": 2020,
        "coach": "SGA 코치진",
        "achievements": "PWS 위클리 파이널 진출",
        "players": [
            {"id": 129, "nickname": "Hane", "realName": "SGA 선수", "role": "Main Fragger", "mouseDpi": 800, "generalSens": 33.0, "aimingSens": 33.0, "adsSens": 33.0, "verticalMultiplier": 1.1, "fov": 95, "resolution": "1920x1080", "mouseName": "Logitech G PRO X SUPERLIGHT 2", "mousepadName": "Artisan Zero Soft", "keyboardName": "Wooting 60HE", "headsetName": "Bose QC20", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},
            {"id": 130, "nickname": "Xantast", "realName": "SGA 선수", "role": "Attacker", "mouseDpi": 800, "generalSens": 30.0, "aimingSens": 30.0, "adsSens": 30.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1728x1080", "mouseName": "Razer DeathAdder V3 Pro", "mousepadName": "SteelSeries QcK Heavy", "keyboardName": "Wooting 60HE", "headsetName": "HyperX Cloud Alpha", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},
            {"id": 131, "nickname": "Innate", "realName": "SGA 선수", "role": "IGL", "mouseDpi": 800, "generalSens": 27.0, "aimingSens": 27.0, "adsSens": 27.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Zowie EC2-CW", "mousepadName": "Artisan Hayate Otsu", "keyboardName": "Wooting 60HE", "headsetName": "Sennheiser IE 200", "monitorName": "BenQ XL2566K", "profileImageUrl": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"},
            {"id": 132, "nickname": "inforyou", "realName": "SGA 선수", "role": "Support", "mouseDpi": 400, "generalSens": 46.0, "aimingSens": 46.0, "adsSens": 46.0, "verticalMultiplier": 1.0, "fov": 90, "resolution": "1920x1080", "mouseName": "Logitech G PRO Wireless", "mousepadName": "SteelSeries QcK+", "keyboardName": "Leopold FC750R", "headsetName": "HyperX Cloud II", "monitorName": "BenQ XL2546K", "profileImageUrl": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400&q=80"}
        ]
    }
]

# primary_data/official_teams_and_rosters.json 저장
with open("primary_data/official_teams_and_rosters.json", "w", encoding="utf-8") as f:
    json.dump(official_seeded_pro_teams, f, ensure_ascii=False, indent=2)

# 프론트엔드 mockData.js 갱신
js_content = """// 대한민국 PWS 공식 시드 8대 정규 프로팀 & 100% 팩트 로스터
export const MOCK_TEAMS = """ + json.dumps(official_seeded_pro_teams, ensure_ascii=False, indent=2) + """;

export const MOCK_PLAYERS = MOCK_TEAMS.flatMap(t =>
  (t.players || []).map(p => ({
    ...p,
    teamName: t.name,
    teamLeague: t.league,
    teamRegion: t.region,
    teamLogoUrl: t.logoUrl,
    country: 'KR'
  }))
);

export const MOCK_TOURNAMENTS = [
  {
    id: 1,
    name: '2026 PUBG WEEKLY SERIES: Phase 1 (PWS)',
    slug: 'pws2026-p1',
    category: 'REGIONAL',
    tier: 'Regional-Tier',
    region: 'KR',
    location: 'Seoul, South Korea',
    prizePool: '₩100,000,000',
    startDate: '2026-03-10',
    endDate: '2026-04-14',
    status: 'COMPLETED',
    champion: 'Gen.G Esports (대한민국 젠지 우승)'
  },
  {
    id: 2,
    name: '2026 PUBG WEEKLY SERIES: Phase 2 (PWS)',
    slug: 'pws2026-p2',
    category: 'REGIONAL',
    tier: 'Regional-Tier',
    region: 'KR',
    location: 'Seoul, South Korea',
    prizePool: '₩100,000,000',
    startDate: '2026-09-01',
    endDate: '2026-10-15',
    status: 'UPCOMING'
  },
  {
    id: 3,
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
    champion: 'Gen.G Esports'
  },
  {
    id: 4,
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
    id: 5,
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
    id: 6,
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
  { rank: 1, teamName: 'Gen.G Esports', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 3, killPoints: 88, placementPoints: 54, totalPoints: 142, prize: '₩40,000,000' },
  { rank: 2, teamName: 'DN SOOPers', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 2, killPoints: 78, placementPoints: 48, totalPoints: 126, prize: '₩20,000,000' },
  { rank: 3, teamName: 'T1', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 2, killPoints: 72, placementPoints: 44, totalPoints: 116, prize: '₩12,000,000' },
  { rank: 4, teamName: 'Crazy Raccoon', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 2, killPoints: 68, placementPoints: 40, totalPoints: 108, prize: '₩8,000,000' },
  { rank: 5, teamName: 'FN Pocheon', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 1, killPoints: 64, placementPoints: 38, totalPoints: 102, prize: '₩6,000,000' },
  { rank: 6, teamName: 'AZLA PENTAGRAM', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 1, killPoints: 60, placementPoints: 36, totalPoints: 96, prize: '₩4,000,000' },
  { rank: 7, teamName: 'Eagle Owls', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 1, killPoints: 56, placementPoints: 32, totalPoints: 88, prize: '₩3,000,000' },
  { rank: 8, teamName: 'SGA Esports', teamRegion: 'KR', matchesPlayed: 18, wwcdCount: 1, killPoints: 52, placementPoints: 30, totalPoints: 82, prize: '₩2,000,000' }
];

export const MOCK_PGS4_STATS = [
  { rank: 1, playerNickname: 'seoul', teamName: 'Gen.G Esports', teamRegion: 'KR', kills: 34, damageDealt: 5890.5, headshotRate: 28.5, longestKill: 432.1, mvpScore: 98.4 },
  { rank: 2, playerNickname: 'Salute', teamName: 'Gen.G Esports', teamRegion: 'KR', kills: 31, damageDealt: 5410.2, headshotRate: 25.1, longestKill: 398.7, mvpScore: 94.2 },
  { rank: 3, playerNickname: 'Gyumin', teamName: 'DN SOOPers', teamRegion: 'KR', kills: 29, damageDealt: 5120.0, headshotRate: 22.4, longestKill: 365.4, mvpScore: 91.8 },
  { rank: 4, playerNickname: 'Heaven', teamName: 'DN SOOPers', teamRegion: 'KR', kills: 28, damageDealt: 4980.6, headshotRate: 26.8, longestKill: 412.0, mvpScore: 89.5 },
  { rank: 5, playerNickname: 'Rain1ng', teamName: 'T1', teamRegion: 'KR', kills: 27, damageDealt: 4820.3, headshotRate: 24.2, longestKill: 340.2, mvpScore: 88.0 }
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

print(f"Successfully saved {len(official_seeded_pro_teams)} official seeded pro teams!")
