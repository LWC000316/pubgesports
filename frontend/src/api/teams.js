import { apiGet } from './client';

/**
 * 리그별 팀 카드 목록.
 * 백엔드는 seedType 이 있는 팀(= 검증된 대회 참가 명단)만 반환한다.
 */
export function fetchTeamCards(league) {
  return apiGet(`/api/teams/cards?league=${encodeURIComponent(league)}`);
}
