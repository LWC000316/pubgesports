import { apiGet } from './client';

/**
 * 리그별 수집 출처. 어느 대회 문서에서 언제 가져온 데이터인지.
 * primary_data/_sources.json 을 백엔드가 그대로 내보낸다.
 *
 * 화면에 "언제 기준" 인지를 밝히기 위한 것이다. 이 표시가 없던 동안
 * PTS 가 5개월 지난 대회를 가리키고 있어도 보는 사람이 알 수 없었다.
 */
export function fetchLeagueSources() {
  return apiGet('/api/leagues/sources');
}
