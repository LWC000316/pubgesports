#!/usr/bin/env python3
"""
텔레메트리에서 매치로그(선수 이동 경로·자기장·킬)를 뽑는다.

  python ingest/build_match_log.py as-pgs9gf              # 대회의 모든 경기
  python ingest/build_match_log.py as-pgs9gf --match <id> # 한 경기만

결과: primary_data/matchlogs/<대회id>/<경기id>.json

## 왜 따로 뽑는가

텔레메트리 원본은 **경기당 33MB, 이벤트 5만 4천 건**이다. 그대로 화면에 보낼 수
없다. 필요한 네 가지만 남기면 수백 KB 로 줄어든다.

  LogMatchStart         맵 이름, 참가자 목록
  LogPlayerPosition     선수 이동 경로 (약 11,000건 = 64명 x 170지점)
  LogGameStatePeriodic  자기장 중심·반경
  LogPlayerKillV2       킬 발생 위치

좌표는 센티미터 단위이고 맵 크기로 나눠 0~1 비율로 저장한다. 그래야 화면에서
맵 이미지 크기와 무관하게 쓸 수 있다.
"""

import argparse
import gzip
import io
import json
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "intermediate_results" / "tournaments"
CACHE_DIR = PROJECT_ROOT / "intermediate_results" / "telemetry"
OUT_DIR = PROJECT_ROOT / "primary_data" / "matchlogs"

# 맵 한 변의 길이(cm). 좌표를 0~1 로 정규화하는 데 쓴다.
# 공식 문서와 커뮤니티에서 확인된 값이다.
MAP_SIZE = {
    "Baltic_Main": 816000,      # Erangel 8km
    "Erangel_Main": 816000,     # 2019~2020년 대회의 에란겔. 같은 8km 맵이다
    "Desert_Main": 816000,      # Miramar 8km
    "Tiger_Main": 816000,       # Taego 8km
    "Neon_Main": 816000,        # Rondo 8km
    "Kiki_Main": 816000,        # Deston 8km
    "DihorOtok_Main": 612000,   # Vikendi 6km
    "Savage_Main": 408000,      # Sanhok 4km
    "Summerland_Main": 204000,  # Karakin 2km
    "Chimera_Main": 306000,     # Paramo 3km
    "Heaven_Main": 102000,      # Haven 1km
    "Range_Main": 204000,
}

MAP_LABEL = {
    "Baltic_Main": "Erangel", "Erangel_Main": "Erangel", "Desert_Main": "Miramar", "Tiger_Main": "Taego",
    "Neon_Main": "Rondo", "Kiki_Main": "Deston", "DihorOtok_Main": "Vikendi",
    "Savage_Main": "Sanhok", "Summerland_Main": "Karakin",
    "Chimera_Main": "Paramo", "Heaven_Main": "Haven",
}


def fetch_telemetry(url, cache_path):
    """텔레메트리를 받아 캐시한다. 33MB 라 한 번 받으면 다시 받지 않는다."""
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    # 약관상 gzip 을 받아야 한다. 33MB 가 약 3MB 로 줄어든다.
    req = urllib.request.Request(url, headers={
        "Accept-Encoding": "gzip",
        "User-Agent": "PUBGProVault/1.0 (https://github.com/LWC000316/pubgesports)",
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    text = raw.decode("utf-8")
    cache_path.write_text(text, encoding="utf-8")
    return json.loads(text)


def load_team_names(tournament_id):
    """
    인게임 아이디 접두사(GEN·17)를 보기 좋은 팀 이름(Gen.G Esports)으로 바꿀 표를
    만든다. 집계 단계(build_tournament_seed.py)가 닉네임 다수결로 이미 팀을
    확정해 뒀으니 그 결과를 재사용한다 — 여기서 다시 추측하지 않는다.
    """
    f = PROJECT_ROOT / "primary_data" / "tournaments" / ("%s.json" % tournament_id)
    if not f.is_file():
        return {}
    doc = json.loads(f.read_text(encoding="utf-8"))
    return {p["nickname"]: p.get("team") for p in doc.get("players", [])
            if p.get("nickname") and p.get("team")}


def relabel(log, by_nickname):
    """트랙의 team 을 해석된 팀 이름으로 바꾸고 태그는 tag 에 남긴다."""
    if not by_nickname:
        return 0
    # 한 팀의 태그 -> 이름. 팀원 중 한 명만 맞아도 팀 전체에 적용된다.
    by_tag = {}
    for track in log.get("tracks", []):
        name = by_nickname.get(track.get("nickname"))
        if name and track.get("team"):
            by_tag.setdefault(track["team"], name)

    changed = 0
    for track in log.get("tracks", []):
        tag = track.get("team")
        name = by_nickname.get(track.get("nickname")) or by_tag.get(tag)
        if name and name != tag:
            track["tag"] = tag
            track["team"] = name
            changed += 1
    log["tracks"].sort(key=lambda r: (r["team"] or "", r["nickname"]))
    return changed


def split_ingame_id(name):
    if "_" in name:
        prefix, rest = name.split("_", 1)
        if rest:
            return prefix, rest
    return None, name


def build(events, match_id):
    map_name = None
    players = {}          # 이름 -> {team, nickname}
    tracks = defaultdict(list)
    circles = []
    kills = []

    for e in events:
        t = e.get("_T")

        if t == "LogMatchStart":
            map_name = e.get("mapName")
            for c in e.get("characters", []):
                ch = c.get("character", {})
                name = ch.get("name")
                if name:
                    prefix, nick = split_ingame_id(name)
                    players[name] = {"team": prefix, "nickname": nick,
                                     "teamId": ch.get("teamId")}

        elif t == "LogPlayerPosition":
            ch = e.get("character", {})
            name = ch.get("name")
            loc = ch.get("location") or {}
            if not name or "x" not in loc:
                continue
            tracks[name].append({
                "t": int(e.get("elapsedTime") or 0),
                "x": loc["x"], "y": loc["y"],
                "v": 1 if ch.get("isInVehicle") else 0,
                "d": 1 if ch.get("isDBNO") else 0,
            })

        elif t == "LogGameStatePeriodic":
            g = e.get("gameState", {})
            pos = g.get("safetyZonePosition") or {}
            if g.get("safetyZoneRadius"):
                circles.append({
                    "t": int(g.get("elapsedTime") or 0),
                    "x": pos.get("x", 0), "y": pos.get("y", 0),
                    "r": g.get("safetyZoneRadius"),
                    "alive": g.get("numAlivePlayers"),
                    "aliveTeams": g.get("numAliveTeams"),
                })

        elif t == "LogPlayerKillV2":
            victim = e.get("victim") or {}
            killer = e.get("killer") or {}
            vloc = victim.get("location") or {}
            if "x" not in vloc:
                continue
            kills.append({
                "t": None,
                "victim": victim.get("name"),
                "killer": killer.get("name"),
                "x": vloc["x"], "y": vloc["y"],
                "weapon": (e.get("killerDamageInfo") or {}).get("damageCauserName"),
            })

    size = MAP_SIZE.get(map_name)
    if not size:
        raise SystemExit(
            "맵 크기를 모릅니다: %r\n"
            "MAP_SIZE 에 추가해야 좌표를 정규화할 수 있습니다. 진행을 멈춥니다."
            % map_name)

    def norm(v):
        # 0~1 비율. 소수 5자리면 8km 맵에서 8cm 해상도라 충분하다.
        return round(max(0.0, min(1.0, v / size)), 5)

    out_tracks = []
    for name, pts in tracks.items():
        pts.sort(key=lambda p: p["t"])
        meta = players.get(name, {})
        out_tracks.append({
            "name": name,
            "nickname": meta.get("nickname") or name,
            "team": meta.get("team"),
            "teamId": meta.get("teamId"),
            "points": [[p["t"], norm(p["x"]), norm(p["y"]), p["v"], p["d"]] for p in pts],
        })
    out_tracks.sort(key=lambda r: (r["team"] or "", r["nickname"]))

    circles.sort(key=lambda c: c["t"])
    out_circles = [{"t": c["t"], "x": norm(c["x"]), "y": norm(c["y"]),
                    "r": round(c["r"] / size, 5), "alive": c["alive"],
                    "aliveTeams": c["aliveTeams"]} for c in circles]

    out_kills = [{"victim": k["victim"], "killer": k["killer"],
                  "x": norm(k["x"]), "y": norm(k["y"]), "weapon": k["weapon"]}
                 for k in kills]

    return {
        "matchId": match_id,
        "map": map_name,
        "mapLabel": MAP_LABEL.get(map_name, map_name),
        "mapSize": size,
        "note": "좌표는 맵 한 변을 1 로 둔 비율이다. points 는 [경과초, x, y, 차량여부, 기절여부].",
        "duration": max((c["t"] for c in out_circles), default=0),
        "tracks": out_tracks,
        "circles": out_circles,
        "kills": out_kills,
    }


def main():
    ap = argparse.ArgumentParser(description="텔레메트리 -> 매치로그")
    ap.add_argument("tournament_id")
    ap.add_argument("--match", default=None, help="경기 하나만")
    ap.add_argument("--limit", type=int, default=None, help="앞에서 N경기만")
    ap.add_argument("--relabel-only", action="store_true",
                    help="이미 뽑은 매치로그의 팀 이름만 다시 붙인다 (네트워크 없음)")
    ap.add_argument("--keep-telemetry", action="store_true",
                    help="원본 텔레메트리를 남긴다. 기본은 뽑은 뒤 지운다 "
                         "(경기당 33MB — 10개 대회면 4GB 다)")
    args = ap.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    raw = RAW_DIR / args.tournament_id
    if not raw.is_dir():
        raise SystemExit("원본이 없습니다: %s\n먼저 fetch_tournament.ps1 을 돌리세요." % raw)

    files = sorted(raw.glob("match_*.json"))
    if args.match:
        files = [f for f in files if args.match in f.name]
    if args.limit:
        files = files[:args.limit]
    if not files:
        raise SystemExit("대상 경기가 없습니다.")

    out_dir = OUT_DIR / args.tournament_id
    out_dir.mkdir(parents=True, exist_ok=True)

    team_names = load_team_names(args.tournament_id)
    if not team_names:
        print("주의: 대회 집계 파일이 없어 팀 이름을 인게임 태그로 둡니다.")

    if args.relabel_only:
        # 이미 뽑아 둔 매치로그의 팀 이름만 고친다. 네트워크를 쓰지 않는다.
        total = 0
        files = sorted(out_dir.glob("*.json"))
        for dest in files:
            log = json.loads(dest.read_text(encoding="utf-8"))
            n = relabel(log, team_names)
            body = json.dumps(log, ensure_ascii=False, separators=(",", ":"))
            dest.write_text(body + chr(10), encoding="utf-8")
            total += n
            print("  %s · 선수 %d명 팀명 교체" % (dest.stem[:8], n))
        print("")
        print("-> %d개 경기, 트랙 %d건" % (len(files), total))
        return 0

    for f in files:
        match_id = f.stem.replace("match_", "")
        dest = out_dir / ("%s.json" % match_id)
        if dest.exists():
            print("  이미 있음: %s" % match_id)
            continue

        doc = json.loads(f.read_text(encoding="utf-8-sig"))
        assets = [a for a in doc.get("included", []) if a.get("type") == "asset"]
        url = assets[0]["attributes"]["URL"] if assets else None
        if not url:
            print("  텔레메트리 없음: %s" % match_id)
            continue

        print("  받는 중: %s" % match_id)
        cache_path = CACHE_DIR / args.tournament_id / ("%s.json" % match_id)
        events = fetch_telemetry(url, cache_path)
        log = build(events, match_id)
        relabel(log, team_names)
        dest.write_text(json.dumps(log, ensure_ascii=False, separators=(",", ":")) + "\n",
                        encoding="utf-8")
        kb = dest.stat().st_size // 1024
        print("    %s · 선수 %d · 자기장 %d · 킬 %d · %dKB"
              % (log["mapLabel"], len(log["tracks"]), len(log["circles"]),
                 len(log["kills"]), kb))

        # 원본은 뽑고 나면 쓸 일이 없다. 자산 URL 은 match_*.json 에 남아 있어
        # 필요하면 다시 받을 수 있다.
        if not args.keep_telemetry:
            cache_path.unlink(missing_ok=True)

    print("\n-> %s" % out_dir.relative_to(PROJECT_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
