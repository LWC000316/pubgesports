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

/**
 * 그 대회에서 매치로그를 가진 경기 목록 — {id, startedAt, map, duration, kills, winner}.
 * 경기 순서대로 온다. startedAt 이 비면 그 단계는 순서를 모른다는 뜻이다.
 */
export function fetchMatchList(tournamentId) {
  return apiGet(`/api/tournaments/archive/${encodeURIComponent(tournamentId)}/matches`);
}

/** 경기 하나의 매치로그 — 이동 경로·자기장·킬 지점. */
export function fetchMatchLog(tournamentId, matchId) {
  return apiGet(
    `/api/tournaments/archive/${encodeURIComponent(tournamentId)}/matches/${encodeURIComponent(matchId)}`
  );
}

/** 히트엔딩 — 집계된 맵 목록. */
export function fetchHeatMaps() {
  return apiGet('/api/heat');
}

/** 맵 하나의 히트 집계 (격자별 착지·사망·최종 자기장 횟수). */
export function fetchHeat(map) {
  return apiGet(`/api/heat/${encodeURIComponent(map)}`);
}
