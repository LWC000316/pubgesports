import { useState, useEffect, useCallback } from 'react';

/**
 * API 호출 상태를 다루는 공용 훅.
 *
 *   const { data, loading, error, reload } = useApi(() => fetchTeamCards(league), [league]);
 *
 * fetcher 는 deps 가 바뀔 때마다 다시 실행된다.
 * 실패 시 data 는 fallback 값으로 되돌아간다 — 이전 리그의 데이터가 남지 않게 하기 위함.
 */
export function useApi(fetcher, deps = [], fallback = null) {
  const [data, setData] = useState(fallback);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // fetcher 는 매 렌더마다 새 함수라 deps 로 쓸 수 없다. 호출자가 준 deps 를 쓴다.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const run = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await fetcher());
    } catch (e) {
      setError(e.message || '알 수 없는 오류');
      setData(fallback);
    } finally {
      setLoading(false);
    }
  }, deps);

  useEffect(() => {
    run();
  }, [run]);

  return { data, loading, error, reload: run };
}
