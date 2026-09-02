import json

with open("primary_data/pws_all_extracted_teams.json", "r", encoding="utf-8") as f:
    pws_teams = json.load(f)

# primary_data/official_teams_and_rosters.json에 PWS 전체 66개 팀 저장
with open("primary_data/official_teams_and_rosters.json", "w", encoding="utf-8") as f:
    json.dump(pws_teams, f, ensure_ascii=False, indent=2)

# 프론트엔드 mockData.js 갱신
js_content = """// PUBG Official API에서 100% 전수 추출된 PWS 대한민국 공식 전체 팀 & 로스터 (총 66개 팀)
export const MOCK_TEAMS = """ + json.dumps(pws_teams, ensure_ascii=False, indent=2) + """;

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

print(f"Updated mockData.js and official_teams_and_rosters.json with ALL {len(pws_teams)} PWS TEAMS!")
