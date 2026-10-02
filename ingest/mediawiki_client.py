"""
리퀴피디아 MediaWiki API 클라이언트 (api.php).

LPDB v3(`liquipedia_client.py`)와 달리 **API 키가 필요 없다.** 현재 PWS 팀 데이터가
이 경로로 수집됐다(scripts/59·63·65).

약관(https://liquipedia.net/api-terms-of-use)에서 이 파일이 지키는 것:
  - 연락처가 포함된 User-Agent (없으면 403 이 돌아온다)
  - gzip 수락
  - 응답 캐싱 — 같은 요청을 두 번 보내지 않는다
  - 호출 간 지연

콘텐츠는 CC-BY-SA 3.0 이다. 화면에 쓸 때 출처를 표기해야 한다
(`LeagueTeamGrid.jsx` 의 SourceAttribution).

환경변수
  LIQUIPEDIA_CONTACT   User-Agent 에 넣을 연락처. 없으면 레포 URL 을 쓴다.
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

API_URL = "https://liquipedia.net/pubg/api.php"

# 약관상 연락처가 필요하다. 개인 이메일 대신 프로젝트 URL 을 기본값으로 쓴다.
DEFAULT_CONTACT = "https://github.com/LWC000316/pubgesports"

# 리퀴피디아 약관의 호출 간격. action=parse 는 무거워서 따로 더 길게 둔다.
# 2초로 parse 를 때리면 429 가 돌아온다(실측). 줄이지 말 것.
MIN_SECONDS_BETWEEN_CALLS = 2.0
MIN_SECONDS_BETWEEN_PARSE = 30.0

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "intermediate_results" / "liquipedia_cache"


def use_utf8_output():
    """윈도우 콘솔 기본 코드페이지(cp949)에서 한글이 깨지지 않게 한다."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass


class MediaWikiClient:
    def __init__(self, cache_dir=CACHE_DIR, offline=False):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.offline = offline
        self.contact = os.environ.get("LIQUIPEDIA_CONTACT") or DEFAULT_CONTACT
        self._last_call = 0.0

    def _cache_path(self, url):
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
        return self.cache_dir / ("mw_%s.json" % digest)

    def _throttle(self, action=None):
        gap = (MIN_SECONDS_BETWEEN_PARSE if action == "parse"
               else MIN_SECONDS_BETWEEN_CALLS)
        elapsed = time.time() - self._last_call
        if elapsed < gap:
            time.sleep(gap - elapsed)

    def get(self, params, refresh=False):
        """api.php 를 호출하고 JSON 을 돌려준다. 응답은 캐시된다."""
        params = dict(params)
        params.setdefault("format", "json")
        url = "%s?%s" % (API_URL, urllib.parse.urlencode(params))

        cache_file = self._cache_path(url)
        if cache_file.exists() and not refresh:
            return json.loads(cache_file.read_text(encoding="utf-8"))["body"]

        if self.offline:
            raise SystemExit(
                "offline 모드인데 캐시에 없는 요청입니다:\n  %s" % url)

        self._throttle(params.get("action"))
        req = urllib.request.Request(url, headers={
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
            if e.code == 429:
                # 간격을 늘려 한 번만 더 시도한다. 그래도 막히면 사람이 볼 일이다.
                self._last_call = time.time()
                time.sleep(MIN_SECONDS_BETWEEN_PARSE)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    raw = resp.read()
                    if resp.info().get("Content-Encoding") == "gzip":
                        raw = gzip.decompress(raw)
                    body = json.loads(raw.decode("utf-8"))
            else:
                raw = e.read()
                if e.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                detail = raw.decode("utf-8", "replace")[:400]
                raise SystemExit(
                    "리퀴피디아 %s 응답: %s\n요청: %s\n"
                    "403 이면 User-Agent 의 연락처를 확인하세요." % (e.code, detail, url))
        finally:
            self._last_call = time.time()

        cache_file.write_text(
            json.dumps({"url": url, "fetched_at": time.time(), "body": body},
                       ensure_ascii=False, indent=2),
            encoding="utf-8")
        return body

    # ---------- 자주 쓰는 호출 ----------

    def wikitext(self, page, refresh=False):
        """문서의 위키 원문."""
        body = self.get({"action": "parse", "page": page, "prop": "wikitext"}, refresh)
        if "error" in body:
            raise SystemExit("문서를 찾지 못했습니다: %s\n%s" % (page, body["error"]))
        return body["parse"]["wikitext"]["*"]

    def page_images(self, page, refresh=False):
        """문서에 들어 있는 File: 이름 목록."""
        body = self.get({"action": "parse", "page": page, "prop": "images"}, refresh)
        if "error" in body:
            raise SystemExit("문서를 찾지 못했습니다: %s\n%s" % (page, body["error"]))
        return body["parse"]["images"]

    def image_urls(self, filenames, refresh=False):
        """File 이름 → 실제 URL. titles 한도가 있어 50개씩 나눠 보낸다."""
        urls = {}
        for i in range(0, len(filenames), 50):
            chunk = filenames[i:i + 50]
            body = self.get({
                "action": "query",
                "titles": "|".join("File:%s" % f for f in chunk),
                "prop": "imageinfo",
                "iiprop": "url",
            }, refresh)
            for page in body.get("query", {}).get("pages", {}).values():
                info = page.get("imageinfo")
                if info:
                    urls[page["title"].replace("File:", "")] = info[0]["url"]
        return urls

    def search(self, term, limit=5, refresh=False):
        """문서 제목 검색. 표기가 다를 때 실제 문서명을 찾는 용도."""
        body = self.get({"action": "opensearch", "search": term, "limit": limit}, refresh)
        return body[1] if len(body) > 1 else []


def main():
    """매핑을 짜기 전에 응답 원문을 눈으로 보기 위한 덤프."""
    import argparse
    use_utf8_output()
    ap = argparse.ArgumentParser(description="리퀴피디아 MediaWiki 응답 덤프")
    ap.add_argument("page", help="문서명 (예: PUBG_Champions_League/2026/Autumn)")
    ap.add_argument("--what", default="wikitext",
                    choices=["wikitext", "images", "search"])
    ap.add_argument("--chars", type=int, default=6000, help="wikitext 출력 길이")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    client = MediaWikiClient(offline=args.offline)

    if args.what == "wikitext":
        text = client.wikitext(args.page)
        print("=== 전체 %d자 / %d~%d 구간 ===" %
              (len(text), args.offset, args.offset + args.chars))
        print(text[args.offset:args.offset + args.chars])
    elif args.what == "images":
        images = client.page_images(args.page)
        print("=== File %d개 ===" % len(images))
        for f in images:
            print(" ", f)
    else:
        for title in client.search(args.page):
            print(" ", title)


if __name__ == "__main__":
    main()
