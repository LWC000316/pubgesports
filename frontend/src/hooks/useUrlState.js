import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * 화면에서 고른 것을 **주소창에 적어 둔다.**
 *
 * 그 전에는 대회·경기·맵을 아무리 골라도 주소가 `/` 그대로였다. 그래서
 * 남에게 "이 경기 봐" 하고 링크를 보낼 수 없었고, 새로고침하면 처음 화면으로
 * 돌아갔다. 주소에 적어 두면 그 링크 하나로 남이 같은 화면을 본다.
 *
 *   useUrlState('st', null)   ->  ?st=as-pgs9gf
 *
 * **기록(history)은 쌓지 않는다.** `replaceState` 를 쓴다 — 칩을 누를 때마다
 * 기록이 쌓이면 뒤로가기를 열 번 눌러야 사이트를 벗어나게 된다. 공유와
 * 새로고침이 목적이지 탐색 기록이 아니다.
 *
 * 값이 기본값과 같으면 주소에서 뺀다. 주소를 짧게 두려는 것이다.
 */
export function useUrlState(key, initial, { parse, serialize } = {}) {
  const read = useCallback(() => {
    const raw = new URLSearchParams(window.location.search).get(key);
    if (raw == null) return initial;
    return parse ? parse(raw) : raw;
  }, [key, initial, parse]);

  const [value, setValue] = useState(read);
  // 첫 그림에서는 주소를 건드리지 않는다. 사용자가 연 링크를 그대로 둔다.
  const mounted = useRef(false);

  useEffect(() => {
    if (!mounted.current) {
      mounted.current = true;
      return;
    }
    const params = new URLSearchParams(window.location.search);
    const out = value == null ? null
      : (serialize ? serialize(value) : String(value));
    if (out == null || out === '' || out === String(initial)) params.delete(key);
    else params.set(key, out);
    const q = params.toString();
    window.history.replaceState(
      null, '', q ? `${window.location.pathname}?${q}` : window.location.pathname);
  }, [key, value, initial, serialize]);

  return [value, setValue];
}

/** 지금 주소를 클립보드로. 복사됐는지 알려 주려고 true/false 를 돌려준다. */
export async function copyCurrentUrl() {
  try {
    await navigator.clipboard.writeText(window.location.href);
    return true;
  } catch (e) {
    // 권한이 없거나 http 가 아닌 환경. 사용자가 직접 복사하도록 둔다.
    return false;
  }
}
