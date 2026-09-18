"""
frontend/src/data/esportsData.js 의 LATEST_PWS2_TEAMS(검증 완료된 24개 PWS 팀)를
백엔드 DataInitializer 가 읽는 시드 JSON 으로 내보낸다.

로고·트로피·시드 구분은 26/27번 보고서에서 수작업 검증한 값이므로
손으로 옮겨 적지 않고 원본에서 직접 추출한다.

출력: primary_data/pws2_teams_verified.json
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "frontend" / "src" / "data" / "esportsData.js"
TARGET = ROOT / "primary_data" / "pws2_teams_verified.json"

MARKER = "export const LATEST_PWS2_TEAMS ="


def extract_array_literal(text, marker):
    """marker 뒤의 첫 '[' 부터 괄호 수를 세어 짝이 맞는 ']' 까지 잘라낸다."""
    start = text.index(marker)
    open_idx = text.index("[", start)

    depth = 0
    in_string = False
    quote = ""
    i = open_idx

    while i < len(text):
        ch = text[i]
        if in_string:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                in_string = False
        elif ch in ('"', "'"):
            in_string = True
            quote = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[open_idx:i + 1]
        i += 1

    raise ValueError("배열 리터럴의 닫는 괄호를 찾지 못했습니다.")


def main():
    if not SOURCE.exists():
        raise SystemExit(f"원본 파일이 없습니다: {SOURCE}")

    raw = SOURCE.read_text(encoding="utf-8")
    literal = extract_array_literal(raw, MARKER)
    teams = json.loads(literal)

    seed = []
    for team in teams:
        players = []
        for p in team.get("roster", []):
            players.append({
                "nickname": p.get("nickname"),
                "realName": p.get("realName") or p.get("nickname"),
                "role": p.get("role") or "Player",
                "mouseDpi": p.get("dpi"),
                "generalSens": float(p["sens"]) if p.get("sens") is not None else None,
                "mouseName": p.get("mouse"),
            })

        seed.append({
            "id": team.get("id"),
            "name": team.get("name"),
            "tag": team.get("tag"),
            "seedType": team.get("seedType"),
            "logoUrl": team.get("logo") or "",
            "league": team.get("league") or "PWS",
            "region": "KR",
            "trophies": [
                {"name": t.get("name"), "count": t.get("count")}
                for t in team.get("trophies", [])
            ],
            "players": players,
        })

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(
        json.dumps(seed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    pro = sum(1 for t in seed if t["seedType"] == "pro")
    amateur = sum(1 for t in seed if t["seedType"] == "amateur")
    with_trophy = sum(1 for t in seed if t["trophies"])
    roster_total = sum(len(t["players"]) for t in seed)

    print(f"출력 완료: {TARGET}")
    print(f"  전체 팀     : {len(seed)}개 (pro {pro} / amateur {amateur})")
    print(f"  트로피 보유 : {with_trophy}개 팀")
    print(f"  로스터 선수 : {roster_total}명")

    missing_logo = [t["name"] for t in seed if not t["logoUrl"]]
    if missing_logo:
        print(f"  로고 없음   : {len(missing_logo)}개 팀 -> {', '.join(missing_logo)}")


if __name__ == "__main__":
    main()
