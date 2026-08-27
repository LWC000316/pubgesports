export const MOCK_PLAYERS = [
  {
    id: 1,
    nickname: "Seoul",
    realName: "조기열 (Gi-yeol Cho)",
    role: "IGL / Main Attacker",
    country: "KR",
    profileImageUrl: "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=400&q=80",
    teamName: "Danawa e-sports",
    teamLogoUrl: "https://i.namu.wiki/i/7u4mC-7x68uG8X.png",
    mouseDpi: 800,
    generalSens: 28.0,
    mouseName: "Logitech G PRO X SUPERLIGHT 2",
    lastCrawledAt: "2024-06-10T04:00:00"
  },
  {
    id: 2,
    nickname: "Salute",
    realName: "우제현 (Je-hyeon Woo)",
    role: "Main Attacker",
    country: "KR",
    profileImageUrl: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80",
    teamName: "KWANGDONG FREECS",
    teamLogoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Kwangdong_Freecs_logo.svg/200px-Kwangdong_Freecs_logo.svg.png",
    mouseDpi: 800,
    generalSens: 33.0,
    mouseName: "Razer DeathAdder V3 Pro",
    lastCrawledAt: "2024-06-10T04:00:00"
  },
  {
    id: 3,
    nickname: "Inonix",
    realName: "나희주 (Hee-joo Na)",
    role: "All-Rounder / Attacker",
    country: "KR",
    profileImageUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",
    teamName: "Gen.G",
    teamLogoUrl: "https://upload.wikimedia.org/wikipedia/en/thumb/9/91/Gen.G_logo.svg/200px-Gen.G_logo.svg.png",
    mouseDpi: 400,
    generalSens: 50.0,
    mouseName: "Zowie EC2-CW",
    lastCrawledAt: "2024-06-10T04:00:00"
  },
  {
    id: 4,
    nickname: "Heaven",
    realName: "김태성 (Tae-sung Kim)",
    role: "Main Attacker",
    country: "KR",
    profileImageUrl: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80",
    teamName: "KWANGDONG FREECS",
    teamLogoUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Kwangdong_Freecs_logo.svg/200px-Kwangdong_Freecs_logo.svg.png",
    mouseDpi: 800,
    generalSens: 30.0,
    mouseName: "Logitech G PRO X SUPERLIGHT 2",
    lastCrawledAt: "2024-06-10T04:00:00"
  },
  {
    id: 5,
    nickname: "TGLTN",
    realName: "James Giezen",
    role: "Fragger",
    country: "AU",
    profileImageUrl: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80",
    teamName: "Soniqs",
    teamLogoUrl: "https://i.namu.wiki/i/Soniqs_Logo.png",
    mouseDpi: 800,
    generalSens: 24.0,
    mouseName: "Logitech G PRO X SUPERLIGHT",
    lastCrawledAt: "2024-06-10T04:00:00"
  }
];

export const MOCK_PLAYER_DETAILS = {
  1: {
    id: 1,
    nickname: "Seoul",
    realName: "조기열 (Gi-yeol Cho)",
    role: "IGL / Main Attacker",
    country: "KR",
    profileImageUrl: "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=400&q=80",
    chzzkUrl: "https://chzzk.naver.com/",
    youtubeUrl: "https://www.youtube.com/@seoul_pubg",
    soopUrl: "https://bj.afreecatv.com/seoul",
    isActive: true,
    lastCrawledAt: "2024-06-10T04:00:00",
    team: {
      id: 3,
      name: "Danawa e-sports",
      region: "KR",
      logoUrl: "https://i.namu.wiki/i/7u4mC-7x68uG8X.png"
    },
    setting: {
      mouseDpi: 800,
      generalSens: 28.0,
      aimingSens: 28.0,
      adsSens: 28.0,
      scope2xSens: 28.0,
      scope3xSens: 28.0,
      scope4xSens: 28.0,
      scope6xSens: 28.0,
      verticalMultiplier: 1.2,
      fov: 90,
      resolution: "1728x1080 (16:10)",
      screenMode: "전체 화면",
      renderScale: 100,
      edpi: 22400
    },
    gears: [
      { id: 1, category: "MOUSE", name: "Logitech G PRO X SUPERLIGHT 2", brand: "Logitech" },
      { id: 2, category: "MOUSEPAD", name: "Artisan Ninja FX Zero Soft", brand: "Artisan" },
      { id: 3, category: "KEYBOARD", name: "Wooting 60HE (Rapid Trigger)", brand: "Wooting" },
      { id: 4, category: "HEADSET", name: "Sennheiser IE 200", brand: "Sennheiser" },
      { id: 5, category: "MONITOR", name: "BenQ ZOWIE XL2566K (360Hz)", brand: "BenQ" }
    ],
    highlights: [
      { id: 1, title: "PGC 2023 그랜드 파이널 매드무비", videoUrl: "https://www.youtube.com/embed/dQw4w9WgXcQ", tournament: "PGC 2023" }
    ]
  }
};

export const MOCK_TOURNAMENTS = [
  {
    id: 1,
    name: "PUBG Global Series 4 (PGS 4)",
    slug: "pgs-4-2024",
    tier: "S-Tier",
    region: "GLOBAL",
    startDate: "2024-06-03",
    endDate: "2024-06-09",
    prizePool: "$300,000",
    location: "Shanghai, China",
    logoUrl: "https://esports.pubg.com/assets/images/pgs4-logo.png",
    status: "COMPLETED",
    totalTeams: 16
  }
];

export const MOCK_PGS4_LEADERBOARD = [
  { rank: 1, teamName: "Twisted Minds", teamRegion: "EMEA", wwcdCount: 3, killPoints: 94, placementPoints: 58, totalPoints: 152, matchesPlayed: 18, prize: "$100,000" },
  { rank: 2, teamName: "KWANGDONG FREECS", teamRegion: "KR", wwcdCount: 2, killPoints: 86, placementPoints: 55, totalPoints: 141, matchesPlayed: 18, prize: "$40,000" },
  { rank: 3, teamName: "Soniqs", teamRegion: "AMER", wwcdCount: 2, killPoints: 81, placementPoints: 52, totalPoints: 133, matchesPlayed: 18, prize: "$25,000" },
  { rank: 4, teamName: "Danawa e-sports", teamRegion: "KR", wwcdCount: 1, killPoints: 78, placementPoints: 49, totalPoints: 127, matchesPlayed: 18, prize: "$18,000" },
  { rank: 5, teamName: "CERBERUS Esports", teamRegion: "APAC", wwcdCount: 1, killPoints: 73, placementPoints: 46, totalPoints: 119, matchesPlayed: 18, prize: "$15,000" },
  { rank: 6, teamName: "Gen.G", teamRegion: "KR", wwcdCount: 1, killPoints: 65, placementPoints: 43, totalPoints: 108, matchesPlayed: 18, prize: "$12,000" },
  { rank: 7, teamName: "17Gaming", teamRegion: "APAC", wwcdCount: 1, killPoints: 60, placementPoints: 39, totalPoints: 99, matchesPlayed: 18, prize: "$10,000" },
  { rank: 8, teamName: "Natus Vincere", teamRegion: "EMEA", wwcdCount: 0, killPoints: 55, placementPoints: 37, totalPoints: 92, matchesPlayed: 18, prize: "$8,000" }
];

export const MOCK_PGS4_STATS = [
  { rank: 1, playerNickname: "Heaven", teamName: "KWANGDONG FREECS", kills: 34, damage: 6120.5, knocks: 31, assists: 15, headshotRate: 24.5, survivalTimeAvg: 1280.0, twireRating: 1.38 },
  { rank: 2, playerNickname: "TGLTN", teamName: "Soniqs", kills: 31, damage: 5840.0, knocks: 28, assists: 12, headshotRate: 28.2, survivalTimeAvg: 1210.0, twireRating: 1.32 },
  { rank: 3, playerNickname: "Seoul", teamName: "Danawa e-sports", kills: 29, damage: 5410.2, knocks: 26, assists: 18, headshotRate: 31.0, survivalTimeAvg: 1190.0, twireRating: 1.29 },
  { rank: 4, playerNickname: "Salute", teamName: "KWANGDONG FREECS", kills: 27, damage: 5100.0, knocks: 24, assists: 14, headshotRate: 22.8, survivalTimeAvg: 1240.0, twireRating: 1.24 },
  { rank: 5, playerNickname: "Inonix", teamName: "Gen.G", kills: 23, damage: 4320.0, knocks: 20, assists: 11, headshotRate: 26.4, survivalTimeAvg: 1080.0, twireRating: 1.15 }
];
