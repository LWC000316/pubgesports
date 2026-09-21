"""
Liquipedia LPDB API v3 클라이언트.

약관(https://liquipedia.net/api-terms-of-use)에서 이 파일이 지키는 것:
  - 연락처가 포함된 User-Agent
  - gzip 수락
  - 시간당 60회 제한 (코드로 강제한다. 초과하면 예외를 던지고 멈춘다)
  - 응답 캐싱 (같은 요청을 두 번 보내지 않는다)

콘텐츠는 CC-BY-SA 3.0 이다. 수집한 데이터를 화면에 쓸 때 리퀴피디아 출처를 표기해야 한다.

환경변수
  LIQUIPEDIA_API_KEY   필수. 리퀴피디아에 신청해 승인받은 LPDB v3 키.
  LIQUIPEDIA_CONTACT   필수. User-Agent 에 넣을 연락처(이메일 또는 프로젝트 URL).
"""

import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

def use_utf8_output():
    """윈도우 콘솔 기본 코드페이지(cp949)에서 한글이 깨지지 않게 한다."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass


BASE_URL = "https://api.liquipedia.net/api/v3"

# 약관: LiquipediaDB API 는 시간당 60회.
RATE_LIMIT_PER_HOUR = 60
RATE_WINDOW_SECONDS = 3600

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "intermediate_results" / "liquipedia_cache"
CALL_LOG = CACHE_DIR / "_call_log.json"


class RateLimitExceeded(RuntimeError):
    """시간당 호출 한도를 넘었을 때. 재시도하지 말고 기다려야 한다."""


class LiquipediaClient:
    def __init__(self, wiki="pubg", cache_dir=CACHE_DIR, offline=False):
        self.wiki = wiki
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.offline = offline

        self.api_key = os.environ.get("LIQUIPEDIA_API_KEY")
        self.contact = os.environ.get("LIQUIPEDIA_CONTACT")
        if not offline:
            if not self.api_key:
                raise SystemExit(
                    "LIQUIPEDIA_API_KEY 가 없습니다. 승인받은 LPDB v3 키를 환경변수로 넣어 주세요.\n"
                    "  export LIQUIPEDIA_API_KEY=...\n"
                    "키가 아직 없다면 --offline 으로 캐시만 읽을 수 있습니다."
                )
            if not self.contact:
                raise SystemExit(
                    "LIQUIPEDIA_CONTACT 가 없습니다. 약관상 User-Agent 에 연락처를 넣어야 합니다.\n"
                    "  export LIQUIPEDIA_CONTACT=you@example.com"
                )

    # ---------- 호출 한도 ----------

    def _recent_calls(self):
        if not CALL_LOG.exists():
            return []
        try:
            stamps = json.loads(CALL_LOG.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        cutoff = time.time() - RATE_WINDOW_SECONDS
        return [t for t in stamps if t > cutoff]

    def _record_call(self):
        stamps = self._recent_calls()
        stamps.append(time.time())
        CALL_LOG.write_text(json.dumps(stamps), encoding="utf-8")

    def remaining_calls(self):
        """이번 시간 창에서 남은 호출 수."""
        return RATE_LIMIT_PER_HOUR - len(self._recent_calls())

    def _check_rate_limit(self):
        recent = self._recent_calls()
        if len(recent) >= RATE_LIMIT_PER_HOUR:
            wait = int(recent[0] + RATE_WINDOW_SECONDS - time.time())
            raise RateLimitExceeded(
                "시간당 %d회 한도에 도달했습니다. 약 %d분 뒤에 다시 실행하세요. "
                "이미 받은 응답은 캐시에 있으므로 --offline 으로 이어서 작업할 수 있습니다."
                % (RATE_LIMIT_PER_HOUR, max(1, wait // 60))
            )

    # ---------- 요청 ----------

    def _cache_path(self, url):
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
        return self.cache_dir / ("%s.json" % digest)

    def query(self, datapoint, conditions=None, query=None, limit=100,
              offset=0, order=None, refresh=False):
        """
        LPDB v3 데이터포인트 하나를 조회한다.

        datapoint   "team", "squadplayer", "tournament", "placement" 등
        conditions  LPDB 조건식. 예: "[[pagename::PUBG_Champions_League/2026]]"
        query       가져올 필드를 쉼표로. 생략하면 전체.
        """
        params = {"wiki": self.wiki, "limit": limit, "offset": offset}
        if conditions:
            params["conditions"] = conditions
        if query:
            params["query"] = query
        if order:
            params["order"] = order

        url = "%s/%s?%s" % (BASE_URL, datapoint, urllib.parse.urlencode(params))
        cache_file = self._cache_path(url)

        if cache_file.exists() and not refresh:
            payload = json.loads(cache_file.read_text(encoding="utf-8"))
            return payload["result"]

        if self.offline:
            raise SystemExit(
                "offline 모드인데 캐시에 없는 요청입니다:\n  %s\n"
                "키를 넣고 온라인으로 한 번 받아야 합니다." % url
            )

        self._check_rate_limit()
        req = urllib.request.Request(url, headers={
            "Authorization": "Apikey %s" % self.api_key,
            "User-Agent": "PUBGProVault/1.0 (%s)" % self.contact,
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
        })

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                if resp.info().get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                body = json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            raise SystemExit("리퀴피디아 %s 응답: %s\n요청: %s" % (e.code, detail, url))
        finally:
            self._record_call()

        result = body.get("result", body)
        cache_file.write_text(
            json.dumps({"url": url, "fetched_at": time.time(), "result": result},
                       ensure_ascii=False, indent=2),
            encoding="utf-8")
        return result


def main():
    """필드 이름을 눈으로 확인하기 위한 덤프. 매핑을 짜기 전에 이걸 먼저 돌린다."""
    import argparse
    use_utf8_output()
    ap = argparse.ArgumentParser(description="LPDB 응답 원본을 그대로 출력한다")
    ap.add_argument("datapoint", help="team / squadplayer / tournament / placement ...")
    ap.add_argument("--conditions", default=None)
    ap.add_argument("--query", default=None)
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--wiki", default="pubg")
    ap.add_argument("--offline", action="store_true", help="캐시만 읽는다")
    args = ap.parse_args()

    client = LiquipediaClient(wiki=args.wiki, offline=args.offline)
    rows = client.query(args.datapoint, conditions=args.conditions,
                        query=args.query, limit=args.limit)
    print(json.dumps(rows, ensure_ascii=False, indent=2)[:8000])
    print("\n--- %d건, 남은 호출 %d회 ---" % (len(rows), client.remaining_calls()))


if __name__ == "__main__":
    main()
