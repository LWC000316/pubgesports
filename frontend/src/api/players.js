import { apiGet } from './client';

/**
 * 선수 한 명의 전체 정보. 감도 13개 항목과 장비 목록이 여기에만 들어 있다.
 *
 * 팀 카드(/api/teams/cards)의 roster 에는 dpi·sens·mouse 세 개만 실린다 —
 * 146팀 전부에 전체 세팅을 실으면 응답이 과하게 커지기 때문이다.
 * 그래서 모달을 열 때 이 엔드포인트로 나머지를 받아 온다.
 */
export function fetchPlayerDetail(id) {
  return apiGet(`/api/players/${encodeURIComponent(id)}`);
}
