#!/usr/bin/env python3
"""
리퀴피디아 선수 문서에서 방송·SNS 링크를 모아 시드에 넣는다.

선수 문서의 `{{Infobox player}}` 에 youtube/afreeca/chzzk 필드가 있다.
**트위치는 다루지 않는다** — 링크는 많지만 정보란에 장비를 적는 선수가 없었다.
**검색으로 추측하지 않는다** — 닉네임이 겹치는 사람이 많아 엉뚱한 채널을 붙일
위험이 크다. 위키가 그 선수 문서에 직접 적어 둔 값만 쓴다.

선수 문서명은 대회 문서의 렌더 HTML 에서 얻는다 (`<a href="/pubg/PageName">`).
위키 원문의 `{{Person|Nick}}` 은 닉네임만 주고, 문서명이 다른 경우가 29건 있다.

    python ingest/collect_player_links.py --survey   # 어떤 필드가 얼마나 있는지만
    python ingest/collect_player_links.py --dry-run  # 무엇이 바뀌는지만
    python ingest/collect_player_links.py            # 시드에 기록

반영 뒤에는 SEED_MODE=always 로 한 번 기동해야 DB 에 들어간다.
"""

import argparse
import html as html_mod
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mediawiki_client import MediaWikiClient   # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES = PROJECT_ROOT / "primary_data" / "_sources.json"

# 인포박스 필드 -> 시드 키. 방송만 가져온다. 트위터·인스타는 방송국이 아니라 넣지 않는다.
LINK_FIELDS = {
    "youtube": ("youtube", "https://youtube.com/%s"),
    "afreeca": ("soop", "https://ch.sooplive.co.kr/%s"),
    "soop": ("soop", "https://ch.sooplive.co.kr/%s"),
    "chzzk": ("chzzk", "https://chzzk.naver.com/%s"),
}

BATCH = 50


def player_pages(client, page):
    """대회 문서의 렌더 HTML 에서 (닉네임, 선수 문서명) 을 뽑는다."""
    doc = html_mod.unescape(
        client.get({"action": "parse", "page": page, "prop": "text"})["parse"]["text"]["*"])
    m = re.search(r'id="Participants".*?(?=<h2)', doc, re.S)
    scope = m.group(0) if m else doc

    out = {}
    for mm in re.finditer(
            r'class="block-player[^"]*"[^>]*>.*?<a href="/pubg/([^"#?]+)"[^>]*>([^<]+)</a>',
            scope, re.S):
        title = mm.group(1).replace("_", " ").strip()
        nick = mm.group(2).strip()
        if nick and title:
            out.setdefault(nick, title)
    return out


def fetch_infoboxes(client, titles):
    """문서 여러 개의 원문을 한 번에 받는다. 문서명 -> 원문."""
    result = {}
    titles = sorted(set(titles))
    for i in range(0, len(titles), BATCH):
        chunk = titles[i:i + BATCH]
        data = client.get({
            "action": "query", "prop": "revisions", "rvprop": "content",
            "rvslots": "main", "titles": "|".join(chunk), "formatversion": "2",
        })
        for p in data.get("query", {}).get("pages", []):
            if p.get("missing"):
                continue
            revs = p.get("revisions") or []
            if not revs:
                continue
            result[p["title"]] = revs[0]["slots"]["main"]["content"]
        print("  원문 수신 %d/%d" % (min(i + BATCH, len(titles)), len(titles)))
    return result


def extract_links(wikitext):
    """인포박스에서 방송 링크만 뽑는다. 값이 비어 있으면 넣지 않는다."""
    m = re.search(r"\{\{Infobox player(.*?)\n\}\}", wikitext, re.S)
    if not m:
        return {}
    body = m.group(1)
    links = {}
    for field, (key, template) in LINK_FIELDS.items():
        fm = re.search(r"\|\s*" + field + r"\s*=\s*([^\n|]*)", body, re.I)
        if not fm:
            continue
        value = fm.group(1).strip()
        if not value or value in ("-",):
            continue
        # 이미 전체 URL 이면 그대로, 아이디만 있으면 템플릿에 끼운다.
        # 앞에 슬래시가 붙어 오는 값이 있다(youtube = '/channel/UC...'). 떼지 않으면
        # 'https://youtube.com//channel/...' 처럼 슬래시가 겹친다.
        links[key] = value if value.startswith("http") else template % value.lstrip("/")
    return links


def main():
    ap = argparse.ArgumentParser(description="리퀴피디아 선수 문서에서 방송 링크 수집")
    ap.add_argument("--survey", action="store_true", help="분포만 본다")
    ap.add_argument("--dry-run", action="store_true", help="파일을 쓰지 않는다")
    args = ap.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    client = MediaWikiClient()
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))["leagues"]

    # 1. 리그별로 닉네임 -> 선수 문서명
    nick_to_title = {}
    for league, meta in sources.items():
        pages = player_pages(client, meta["page"])
        print("[%s] 선수 문서 링크 %d개" % (league, len(pages)))
        for nick, title in pages.items():
            nick_to_title.setdefault((league, nick), title)

    # 2. 시드에 있는 선수만 남긴다
    seeds = {}
    wanted = {}
    for path in sorted(PROJECT_ROOT.glob("primary_data/*_teams_verified.json")):
        teams = json.loads(path.read_text(encoding="utf-8"))
        seeds[path] = teams
        for team in teams:
            for player in team.get("players", []):
                title = nick_to_title.get((team.get("league"), player["nickname"]))
                if title:
                    wanted[(path, team["name"], player["nickname"])] = title

    print("\n시드 선수 중 문서명을 찾은 사람: %d명" % len(wanted))

    # 3. 원문 일괄 수신
    texts = fetch_infoboxes(client, wanted.values())
    print("문서 %d개 수신" % len(texts))

    # 4. 링크 추출
    found = Counter()
    per_player = {}
    for key, title in wanted.items():
        wt = texts.get(title)
        if not wt:
            continue
        links = extract_links(wt)
        if links:
            per_player[key] = links
            for k in links:
                found[k] += 1

    print("\n방송 링크가 있는 선수: %d명" % len(per_player))
    print("플랫폼별:", dict(found))

    if args.survey:
        print("\n예시 10명:")
        for (path, team, nick), links in list(per_player.items())[:10]:
            print("  %-16s %-24s %s" % (nick, team, links))
        return 0

    # 5. 시드에 기록
    touched = set()
    for (path, team_name, nick), links in per_player.items():
        for team in seeds[path]:
            if team["name"] != team_name:
                continue
            for player in team["players"]:
                if player["nickname"] == nick:
                    player["streams"] = links
                    touched.add(path)

    if args.dry_run:
        print("\n--dry-run 이라 파일을 쓰지 않았습니다.")
        return 0

    for path in sorted(touched):
        path.write_text(json.dumps(seeds[path], ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print("기록: %s" % path.relative_to(PROJECT_ROOT))

    print("\n다음: cd backend && SEED_MODE=always ./gradlew bootRun")
    return 0


if __name__ == "__main__":
    sys.exit(main())
