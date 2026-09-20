// 백엔드 호출 공통 래퍼.
// 개발 환경에서는 vite.config.js 의 프록시가 /api 를 localhost:8080 으로 넘긴다.

export async function apiGet(path) {
  let res;
  try {
    res = await fetch(path);
  } catch (e) {
    // 네트워크 자체가 실패한 경우 (백엔드 미기동 등)
    throw new Error('백엔드 서버에 연결하지 못했습니다.');
  }

  if (!res.ok) {
    throw new Error(`서버가 ${res.status} ${res.statusText} 로 응답했습니다.`);
  }

  return res.json();
}
