#!/usr/bin/env python3
"""
경쟁전(랭크) 경기에서 **자기장만** 모은다.

  python ingest/collect_ranked_zones.py --target 1000 --max-minutes 200
  python ingest/collect_ranked_zones.py --status        # 받지 않고 현황만

## 왜 필요한가

히트엔딩은 "이 맵은 자기장이 어디에 걸리는가"를 센다. 그런데 **2026-06-17
업데이트 42.1 에서 자기장이 개편**됐고(경쟁전·이스포츠의 "안전 구역 위치
보정 강도 완화"), 그 전후는 서로 다른 게임이다. 개편 뒤 이스포츠 경기는
맵당 142~281 판뿐이라 표본이 얇다.

**경쟁전은 이스포츠와 자기장 설정이 같다** (개발일지 "블루존 개편",
pubg.com/ko/news/10280). 일반전은 다르다 — 일반전만 경고·축소 시간이 따로
조정됐고 위치 보정은 그대로다. 그래서 `matchType == "competitive"` 만 받고
`official` 은 버린다. **섞으면 측정하려는 값 자체가 오염된다.**

## 어떻게 찾나

경기 목록을 얻는 것은 사실상 공짜다. 경쟁전 경기 하나에서 선수 이름을 얻고
그 선수의 최근 경기 목록을 받으면 **한 번 호출에 수백 개**가 나온다(실측
732개). 랭크를 도는 선수라 적중률도 높다 — 실측 14/14 가 경쟁전이었다.

**병목은 경기당 API 1회**다. 텔레메트리 주소를 받으려면 반드시 거쳐야 하고
분당 10회 제한이 걸린다. 내려받기 자체는 제한에 안 걸린다.

## 남기는 것

경기당 **자기장 페이즈만** 남긴다. 2KB 안쪽이다. 매치로그(300KB)처럼 동선과
킬까지 담지 않는다 — 히트맵에 필요 없고, 맵당 1,000판이면 1.2GB가 된다.

## 규칙

- 공식 API 는 **최근 14일**치만 보관한다. 과거로는 못 간다
- 맵마다 목표를 채우면 그 맵은 건너뛴다. 랭크는 맵 순환이 있어 쏠린다
- 중간에 멈춰도 이어서 한다. 받아 본 경기 id 를 적어 두고 다시 받지 않는다
- **장부를 자주 적는다.** 이 저장소에서 "마지막에 한 번 저장"으로 네 번
  데이터를 잃었다. 여기서는 기본 25경기마다 적는다
"""

import argparse
import gzip
import importlib.util
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "primary_data" / "ranked_zones"
SEEN = OUT_DIR / "_seen.json"
POOL = OUT_DIR / "_players.json"

SHARD = "steam"
API = "https://api.pubg.com/shards/%s" % SHARD
# 분당 10회. 넘기면 429 가 돌아온다 — 돈이 드는 게 아니라 거절당한다.
GAP = 6.2

_spec = importlib.util.spec_from_file_location(
    "bml", Path(__file__).with_name("build_match_log.py"))
bml = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bml)

# 지금 프로 경기에 쓰이는 맵만 모은다. 나머지는 이스포츠 표본이 0 이라
# 짝을 맞출 수 없다.
TARGET_MAPS = ["Baltic_Main", "Desert_Main", "Tiger_Main", "Neon_Main"]


class Api:
    """분당 10회를 지키는 호출기. 호출 수를 세어 보고한다."""

    def __init__(self, key):
        self.key = key
        self.last = 0.0
        self.calls = 0

    def get(self, url):
        wait = GAP - (time.time() - self.last)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(url, headers={
            "Authorization": "Bearer %s" % self.key,
            "Accept": "application/vnd.api+json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # 분당 제한. 한 박자 쉬고 한 번만 다시 시도한다.
                time.sleep(GAP * 3)
                with urllib.request.urlopen(req, timeout=30) as r:
                    return json.loads(r.read().decode("utf-8"))
            raise
        finally:
            self.last = time.time()
            self.calls += 1


def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + chr(10),
        encoding="utf-8")


def fetch_telemetry(url):
    """텔레메트리를 받아 그대로 돌려준다. **파일로 남기지 않는다.**

    `build_match_log.fetch_telemetry` 는 캐시 파일을 쓰는데, 거기에
    `os.devnull` 을 넘겼더니 그 경로가 "이미 있는 캐시"로 인식돼 빈 내용을
    읽었다. 실측으로 55회 호출에 0건을 모았다. 여기서는 캐시가 필요 없다 —
    자기장만 뽑고 버리기 때문이다.

    약관상 gzip 을 받아야 한다. 33MB 가 약 3MB 로 줄어든다.
    """
    req = urllib.request.Request(url, headers={
        "Accept-Encoding": "gzip",
        "User-Agent": "PUBGProVault/1.0 (https://github.com/LWC000316/pubgesports)",
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    return json.loads(raw.decode("utf-8"))


def have_counts():
    out = {}
    for m in TARGET_MAPS:
        d = OUT_DIR / m
        out[m] = len(list(d.glob("*.json"))) if d.is_dir() else 0
    return out


def phases_of(events):
    """자기장 페이즈. 반경이 줄다 멈추는 순간이 다음 구역 예고다
    (매치로그 화면의 derivePhases 와 같은 규칙)."""
    circles = []
    for e in events:
        if e.get("_T") != "LogGameStatePeriodic":
            continue
        g = e.get("gameState") or {}
        if not g.get("safetyZoneRadius"):
            continue
        pos = g.get("safetyZonePosition") or {}
        circles.append({"t": int(g.get("elapsedTime") or 0),
                        "x": pos.get("x", 0), "y": pos.get("y", 0),
                        "r": g.get("safetyZoneRadius")})
    if not circles:
        return []
    out = [circles[0]]
    shrinking = False
    for a, b in zip(circles, circles[1:]):
        if b["r"] < a["r"] - 1e-9:
            shrinking = True
        elif shrinking:
            out.append(b)
            shrinking = False
    return out


def main():
    ap = argparse.ArgumentParser(description="경쟁전 자기장 수집")
    ap.add_argument("--target", type=int, default=1000, help="맵마다 모을 경기 수")
    ap.add_argument("--max-minutes", type=float, default=200.0)
    ap.add_argument("--save-every", type=int, default=25,
                    help="이만큼 모을 때마다 장부를 적는다")
    ap.add_argument("--status", action="store_true", help="받지 않고 현황만")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    counts = have_counts()
    print("맵별 현황 (목표 %d)" % args.target)
    for m, n in counts.items():
        print("   %-14s %4d %s" % (m, n, "완료" if n >= args.target else ""))
    if args.status:
        return 0

    key = os.environ.get("PUBG_API_KEY")
    if not key:
        print("PUBG_API_KEY 가 없습니다.", file=sys.stderr)
        return 1

    api = Api(key)
    seen = set(load(SEEN, []))
    players = list(load(POOL, []))
    start = time.time()
    added = 0

    def budget_left():
        return (time.time() - start) / 60 < args.max_minutes

    def flush():
        # 순서를 고정해 둔다. 안 그러면 내용이 같아도 파일이 매번 달라져
        # 빈 커밋이 쌓인다 (히트 집계에서 실제로 겪었다).
        save_json(SEEN, sorted(seen))
        save_json(POOL, sorted(set(players))[:400])

    # 선수 풀이 비어 있으면 표본 창구에서 씨앗을 얻는다.
    if not players and budget_left():
        print("\n선수 풀이 비었습니다. 표본에서 씨앗을 찾습니다.")
        try:
            doc = api.get("%s/samples" % API)
            ids = [r["id"] for r in doc["data"]["relationships"]["matches"]["data"]]
        except Exception as e:
            print("표본을 받지 못했습니다: %s" % e, file=sys.stderr)
            ids = []
        for mid in ids:
            if not budget_left() or len(set(players)) >= 24:
                break
            try:
                d = api.get("%s/matches/%s" % (API, mid))
            except Exception:
                continue
            seen.add(mid)
            if d["data"]["attributes"].get("matchType") != "competitive":
                continue
            players += [i["attributes"]["stats"]["name"]
                        for i in d.get("included", [])
                        if i.get("type") == "participant"][:24]
        flush()
        print("   씨앗 선수 %d명" % len(set(players)))

    pool = sorted(set(players))
    queue = []
    pi = 0

    while budget_left():
        need = [m for m in TARGET_MAPS if counts[m] < args.target]
        if not need:
            print("\n모든 맵이 목표를 채웠습니다.")
            break

        if not queue:
            if pi >= len(pool):
                print("\n선수 풀을 다 돌았습니다. 한 번 더 실행하면 이어서 넓힙니다.")
                break
            chunk = pool[pi:pi + 6]
            pi += 6
            try:
                d = api.get("%s/players?filter[playerNames]=%s"
                            % (API, ",".join(chunk)))
            except Exception as e:
                print("   선수 조회 실패: %s" % e)
                continue
            for pl in d.get("data", []):
                for m in pl["relationships"]["matches"]["data"]:
                    if m["id"] not in seen:
                        queue.append(m["id"])
            print("   선수 %d명 -> 후보 %d개" % (len(chunk), len(queue)))
            continue

        mid = queue.pop()
        if mid in seen:
            continue
        seen.add(mid)
        try:
            d = api.get("%s/matches/%s" % (API, mid))
        except Exception:
            continue
        attrs = d["data"]["attributes"]
        mp = attrs.get("mapName")
        if attrs.get("matchType") != "competitive" or mp not in need:
            continue

        # 이 경기에 뛴 선수를 풀에 보탠다. 풀이 마르지 않게 한다.
        fresh = [i["attributes"]["stats"]["name"] for i in d.get("included", [])
                 if i.get("type") == "participant"]
        for n in fresh[:8]:
            if n not in pool:
                pool.append(n)
                players.append(n)

        assets = [x for x in d.get("included", []) if x.get("type") == "asset"]
        url = assets[0]["attributes"]["URL"] if assets else None
        if not url:
            continue
        try:
            events = fetch_telemetry(url)
        except Exception as e:
            print("   텔레메트리 실패 %s: %s" % (mid[:8], e))
            continue

        size = bml.MAP_SIZE.get(mp)
        ph = phases_of(events)
        if not size or len(ph) < 3:
            continue

        def ratio(v):
            return round(max(0.0, min(1.0, v / size)), 4)

        doc = {
            "matchId": mid,
            "map": mp,
            "mapLabel": bml.MAP_LABEL.get(mp, mp),
            "createdAt": attrs.get("createdAt"),
            "source": "competitive",
            "gameMode": attrs.get("gameMode"),
            "phases": [{"phase": i + 1, "t": c["t"],
                        "x": ratio(c["x"]), "y": ratio(c["y"]),
                        "r": round(c["r"] / size, 5)}
                       for i, c in enumerate(ph)],
        }
        save_json(OUT_DIR / mp / ("%s.json" % mid), doc)
        counts[mp] += 1
        added += 1
        if added % args.save_every == 0:
            flush()
            print("   모은 경기 %d · 호출 %d · 경과 %.0f분 · %s"
                  % (added, api.calls, (time.time() - start) / 60,
                     " ".join("%s %d" % (m[:6], counts[m]) for m in TARGET_MAPS)))

    flush()
    print("\n새로 모은 경기 %d · API 호출 %d · 경과 %.0f분"
          % (added, api.calls, (time.time() - start) / 60))
    for m, n in have_counts().items():
        print("   %-14s %4d / %d" % (m, n, args.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
