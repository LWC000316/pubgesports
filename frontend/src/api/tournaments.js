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

/** 그 대회에서 매치로그(이동 경로)를 가진 경기 id 목록. */
export function fetchMatchIds(tournamentId) {
  return apiGet(`/api/tournaments/archive/${encodeURIComponent(tournamentId)}/matches`);
}

/** 경기 하나의 매치로그 — 이동 경로·자기장·킬 지점. */
export function fetchMatchLog(tournamentId, matchId) {
  return apiGet(
    `/api/tournaments/archive/${encodeURIComponent(tournamentId)}/matches/${encodeURIComponent(matchId)}`
  );
}
