// 2026 PUBG WEEKLY SERIES: KOREA Phase 2 공식 검증 마스터 데이터셋 (리퀴피디아 팀 업적 전수 일치)

export const TOURNAMENT_LOGOS = {
  PWS: "/logos/tournaments/pws.png",
  PCL: "/logos/tournaments/pcl.png",
  EMEA: "/logos/tournaments/emea.png",
  AMER: "/logos/tournaments/amer.png",
  PTS: "/logos/tournaments/pts.png",
  PVS: "/logos/tournaments/pvs.png"
};

// LATEST_PWS2_TEAMS 는 이 파일에서 제거되었다.
// 검증된 PWS 팀 데이터의 원본은 primary_data/pws2_teams_verified.json 이고
// 백엔드 DataInitializer 가 직접 읽는다. 프론트엔드는 /api/teams/cards 로 받는다.


export const TOURNAMENTS_DATA = [
  {
    id: 'pgs4',
    name: 'PUBG Global Series 4 (PGS 4)',
    tier: 'Global S-Tier',
    location: '상하이, 중국',
    period: '2024.06.03 ~ 2024.06.09',
    status: '종료',
    prizePool: '$300,000',
    totalMatches: 18,
    champion: 'Twisted Minds'
  },
  {
    id: 'pws2024_s1',
    name: '2024 PUBG WEEKLY SERIES: KOREA Phase 1',
    tier: 'Regional Tier 1',
    location: '서울, 대한민국',
    period: '2024.03.23 ~ 2024.04.14',
    status: '종료',
    prizePool: '₩80,000,000',
    totalMatches: 30,
    champion: 'Kwangdong Freecs'
  }
];

export const LEADERBOARD_PGS4 = [
  { rank: 1, team: 'Twisted Minds', tag: 'TWIS', region: 'EMEA', wwcd: 3, killPoints: 89, rankPoints: 48, total: 137, prize: '$100,000' },
  { rank: 2, team: 'CERBERUS Esports', tag: 'CES', region: 'APAC', wwcd: 2, killPoints: 81, rankPoints: 44, total: 125, prize: '$40,000' },
  { rank: 3, team: 'Soniqs', tag: 'SQ', region: 'AMER', wwcd: 2, killPoints: 72, rankPoints: 41, total: 113, prize: '$20,000' },
  { rank: 4, team: 'Gen.G Esports', tag: 'GEN', region: 'KR', wwcd: 2, killPoints: 68, rankPoints: 37, total: 105, prize: '$14,000' }
];
