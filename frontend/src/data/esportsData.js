// 아직 백엔드에 연결되지 않은 화면이 쓰는 정적 데이터. 지금은 리그 로고뿐이다.

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


// TOURNAMENTS_DATA 와 LEADERBOARD_PGS4 는 이 파일에서 제거되었다.
// 대회 목록·순위표·선수 기록은 공식 PUBG API 에서 받아 정리한
// primary_data/tournaments/*.json 이 원본이고, 백엔드가 /api/tournaments/archive
// 로 내보낸다. 손으로 적은 PGS 4 순위표는 그 경로로 대체됐다.
