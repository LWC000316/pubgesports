#!/usr/bin/env python3
"""
새로 받은 초안의 **로스터만** 기존 시드에 합친다.

  python ingest/merge_league_seed.py \
      --draft intermediate_results/pws_seed_draft.json \
      --seed  primary_data/pws2_teams_verified.json
  python ingest/merge_league_seed.py ... --check    # 쓰지 않고 보여만 준다

## 왜 초안으로 덮어쓰면 안 되나

재수집 초안에는 **우리가 손으로 모은 것이 하나도 없다.** 수집기는 감도·장비를
절대 쓰지 않는다 (리퀴피디아에 없는 값이다). PWS 만 해도 감도 56건·장비 7건이
사람 손으로 들어간 것이라, 초안을 그대로 복사하면 그게 전부 사라진다.

**팀 이름도 바꾸지 않는다.** 두 가지가 팀 이름을 자연키로 쓴다:

  - `player_views` · `hot_seeds` — (리그, 팀, 닉네임). 이름이 바뀌면 쌓인
    조회수가 선수에게서 떨어져 나간다
  - 매치로그의 `resolve_team` — 공식 API 의 인게임 접두사를 우리 시드 팀명에
    맞춘다. 우리 이름(`DN SOOPers`)이 대회 데이터와 맞고, 위키의 짧은 이름
    (`SOOPers`)은 위키 쪽 표기다

실제로 PWS 6팀이 위키에서 스폰서 접두사 없이 렌더된다. 그 대응은
`primary_data/_sources.json` 의 `teamAliases` 가 이미 들고 있으므로, 합칠 때
그 표를 따라 같은 팀으로 본다.

## 그래서 무엇을 가져오고 무엇을 지키나

| | 어디서 |
|---|---|
| 로스터(선수 목록·본명·역할) | **새 초안** |
| 감도(`setting`)·장비(`gears`) | **기존 시드** — 남아 있는 선수만 |
| 팀 이름·태그·로고·seedType | **기존 시드** |

새로 들어온 팀은 `seedType` 을 정할 수 없어 **그대로 멈춘다.** 자동으로 정하면
`pro`/`amateur` 가 아닌 값이 들어가 팀이 화면에서 사라진다. 사람이
`--seed-type <팀명>=<pro|amateur>` 로 알려 줘야 한다.

떠난 선수의 감도는 버린다. 그 선수가 다른 팀에서 다시 나타나면 그때 다시
넣어야 한다 — 팀이 다르면 같은 사람이라도 우리 자연키로는 다른 행이다.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES = PROJECT_ROOT / "primary_data" / "_sources.json"

# 위키가 주는 필드. 이것만 초안 값으로 덮어쓰고 **나머지는 전부 기존 것을
# 지킨다.** 반대로(지킬 것을 목록으로) 짰다가 `streams`(방송 링크 79명분)를
# 조용히 날렸다 — 손으로 넣은 필드가 앞으로 또 늘 텐데, 그때마다 목록에
# 추가하는 것을 기억할 수 없다. 모르는 필드는 지키는 쪽이 안전하다.
FROM_WIKI = ("nickname", "realName", "role")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def aliases_for(league):
    """위키 표기 -> 우리 시드 표기. `_sources.json` 의 teamAliases 를 뒤집은 것."""
    try:
        doc = load(SOURCES)
    except (OSError, ValueError):
        return {}
    entry = (doc.get("leagues") or doc).get(league) or {}
    return {v: k for k, v in (entry.get("teamAliases") or {}).items()}


def main():
    ap = argparse.ArgumentParser(description="초안의 로스터만 기존 시드에 합친다")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--seed", required=True)
    ap.add_argument("--seed-type", action="append", default=[],
                    metavar="팀명=pro|amateur",
                    help="새로 들어온 팀의 seedType. 여러 번 줄 수 있다")
    ap.add_argument("--check", action="store_true", help="쓰지 않고 보여만 준다")
    args = ap.parse_args()
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    draft = load(args.draft)
    seed = load(args.seed)
    league = seed[0].get("league") if seed else None
    back = aliases_for(league)

    extra = {}
    for item in args.seed_type:
        if "=" not in item:
            print("--seed-type 은 팀명=pro 형식입니다: %r" % item, file=sys.stderr)
            return 1
        k, v = item.split("=", 1)
        if v not in ("pro", "amateur"):
            print("seedType 은 pro 나 amateur 만 됩니다: %r" % v, file=sys.stderr)
            return 1
        extra[k.strip()] = v

    by_seed = {t["name"]: t for t in seed}

    def match(name):
        """초안의 팀 이름을 우리 시드의 팀으로."""
        if name in by_seed:
            return name
        if name in back and back[name] in by_seed:
            return back[name]
        return None

    unknown = [t["name"] for t in draft if match(t["name"]) is None]
    if unknown:
        missing = [n for n in unknown if n not in extra]
        if missing:
            print("기존 시드에 없는 팀 %d개의 seedType 을 알 수 없습니다:" % len(missing))
            for n in missing:
                print("   %s" % n)
            print("\npro / amateur 중 무엇인지는 대회 구조를 보고 사람이 정합니다.")
            print("   --seed-type \"%s=pro\" 처럼 알려 주세요. 진행을 멈춥니다." % missing[0])
            return 1

    out = []
    carried_over = {}
    kept_setting = kept_gear = lost_setting = lost_gear = 0
    roster_changed = []
    for t in draft:
        key = match(t["name"])
        base = by_seed.get(key)
        old_players = {p["nickname"]: p for p in (base or {}).get("players") or []}

        players = []
        for p in t.get("players") or []:
            prev = old_players.get(p["nickname"])
            # 기존 선수에서 출발해 위키가 주는 필드만 덮어쓴다.
            row = dict(prev or {})
            for f in FROM_WIKI:
                if f in p:
                    row[f] = p[f]
            for f in p:
                row.setdefault(f, p[f])
            if prev:
                if prev.get("setting"):
                    kept_setting += 1
                if prev.get("gears"):
                    kept_gear += 1
                for f in prev:
                    if f not in row:
                        carried_over.setdefault(f, 0)
            players.append(row)

        gone = set(old_players) - {p["nickname"] for p in players}
        for n in gone:
            if old_players[n].get("setting"):
                lost_setting += 1
            if old_players[n].get("gears"):
                lost_gear += 1
        if gone or len(players) != len(old_players):
            roster_changed.append((key or t["name"], sorted(gone),
                                   sorted({p["nickname"] for p in players} - set(old_players))))

        if base:
            merged = dict(base)
            merged["players"] = players
        else:
            # 새 팀. 초안의 이름·태그·로고를 쓰되 seedType 만 사람이 준 값으로.
            merged = {k: v for k, v in t.items() if not k.startswith("_")}
            merged["players"] = players
            merged["seedType"] = extra[t["name"]]
        out.append(merged)

    dropped = [n for n in by_seed if n not in {match(t["name"]) for t in draft}]

    print("리그 %s · 팀 %d -> %d" % (league, len(seed), len(out)))
    if dropped:
        print("  시드에서 빠지는 팀: %s" % ", ".join(sorted(dropped)))
    print("  이어받은 감도 %d · 장비 %d" % (kept_setting, kept_gear))
    hand = sorted({f for t in out for p in t["players"] for f in p} - set(FROM_WIKI))
    if hand:
        counts = {f: sum(1 for t in out for p in t["players"] if p.get(f)) for f in hand}
        print("  초안에 없지만 지킨 필드: %s"
              % ", ".join("%s %d명" % (f, n) for f, n in counts.items() if n))
    if lost_setting or lost_gear:
        print("  떠난 선수와 함께 사라지는 감도 %d · 장비 %d" % (lost_setting, lost_gear))
    if roster_changed:
        print("\n  로스터가 달라진 팀 %d개:" % len(roster_changed))
        for name, gone, added in roster_changed:
            print("     %-22s 나감 %-28s 들어옴 %s"
                  % (name, ", ".join(gone) or "-", ", ".join(added) or "-"))

    total_players = sum(len(t["players"]) for t in out)
    print("\n  선수 %d -> %d" % (sum(len(t.get("players") or []) for t in seed), total_players))

    if args.check:
        print("\n--check 라 쓰지 않았습니다.")
        return 0
    Path(args.seed).write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n%s 를 갱신했습니다." % args.seed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
