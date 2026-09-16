import urllib.request
import gzip
import json
import re

url = "https://liquipedia.net/pubg/api.php?action=parse&page=PUBG_WEEKLY_SERIES/2026/Phase_2&prop=wikitext&format=json"
req = urllib.request.Request(url, headers={
    "User-Agent": "PUBGEsportsPlatform/1.0 (contact@pubgproject.local)",
    "Accept-Encoding": "gzip"
})

with urllib.request.urlopen(req) as resp:
    raw = resp.read()
    if resp.info().get("Content-Encoding") == "gzip":
        raw = gzip.decompress(raw)
    data = json.loads(raw.decode("utf-8"))

wt = data.get("parse", {}).get("wikitext", {}).get("*", "")

matches = re.findall(r'\{\{Opponent\|([^|\n\r]+)([\s\S]*?)(?=\{\{Opponent|\n==)', wt)
results = []
for name, body in matches:
    name = name.strip()
    persons = re.findall(r'\{\{Person\|([^|}]+)(?:\|([^}]+))?\}\}', body)
    players = [p[0].strip() for p in persons if "staff" not in p[1] and "coach" not in p[1]]
    if players:
        results.append({
            "team": name,
            "players": players
        })

print(f"총 {len(results)}개 팀 추출 완료")
for idx, r in enumerate(results, 1):
    t_name = r["team"]
    plist = ", ".join(r["players"])
    print(f"{idx}. {t_name} -> {plist}")

with open("intermediate_results/liquipedia_24_teams_perfect.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
