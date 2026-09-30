import { apiGet } from './client';

/**
 * HOT 탭 목록. 이번 주 조회수가 많은 순이고, 조회수가 아직 없으면
 * 세계대회 성적으로 정한 초기 순위(hot_seeds)가 대신 나온다.
 *
 * 선수 정보(감도·마우스·소속)는 백엔드가 players 에서 가져와 채운다 —
 * HOT 탭이 자기 사본을 들고 있지 않는다.
 */
export function fetchHotPlayers(limit = 12) {
  return apiGet(`/api/players/hot?limit=${limit}`);
}

/**
 * 선수 상세를 열었다고 알린다. 실패해도 화면에 영향이 없어야 하므로
 * 호출부에서 에러를 삼킨다.
 */
export function recordPlayerView(id) {
  return fetch(`/api/players/${encodeURIComponent(id)}/view`, { method: 'POST' });
}
