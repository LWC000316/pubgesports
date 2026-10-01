import { apiGet } from './client';

/**
 * 대회 아카이브 목록. category 는 global / regional / scrim.
 * 비우면 전부 가져온다.
 */
export function fetchTournaments(category) {
  const q = category ? `?category=${encodeURIComponent(category)}` : '';
  return apiGet(`/api/tournaments/archive${q}`);
}

/** 대회 하나의 순위표와 선수 기록. */
export function fetchTournament(id) {
  return apiGet(`/api/tournaments/archive/${encodeURIComponent(id)}`);
}
