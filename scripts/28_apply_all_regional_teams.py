import json

with open("primary_data/official_teams_and_rosters.json", "r", encoding="utf-8") as f:
    all_teams = json.load(f)

js_content = """// 권역별(PWS, PCL, EMEA, AMER, APAC) 최신 정규 대회 참가 모든 프로팀 (총 """ + str(len(all_teams)) + """개 팀)
export const MOCK_TEAMS = """ + json.dumps(all_teams, ensure_ascii=False, indent=2) + """;

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
  { rank: 8, teamName: 'Petrichor Road', teamRegion: 'CN', matchesPlayed: 18, wwcdCount: 1, killPoints: 58, placementPoints: 34, totalPoints: 92, prize: '$9,000' }
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

print(f"Updated mockData.js with ALL {len(all_teams)} REGIONAL TEAMS!")
