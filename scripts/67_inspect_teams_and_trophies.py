import urllib.request
import urllib.parse
import gzip
import json
import re

teams = [
    "Vex E-Sports", "Vex", "VEX",
    "SLASH DOOM LAB", "Doom Lab", "Star Balloon",
    "SQUAD X ACADEMY", "Squad X",
    "ISKRA", "The Crown", "samgukzee", "Samgukzee",
    "HESEDIAN", "Hesedian", "Qx",
    "CFiVE", "cfive",
    "GGWP", "Overwhelm",
    "SOOPers", "DN SOOPers", "Danawa e-sports",
    "Gen.G Esports", "Gen.G",
    "T1", "Baegopa", "FN Esports", "PENTAGRAM",
    "Divine", "PHANTOM HEARTS", "Game PT", "Sentinel",
    "SUPERFECT", "Geekay Esports", "Eagle Owls", "Crazy Raccoon"
]

headers = {
    "User-Agent": "PUBGEsportsPlatform/1.0 (contact@pubgproject.local)",
    "Accept-Encoding": "gzip"
}

print("=== 리퀴피디아 검색 시작 ===")
found_pages = {}
for t in teams:
    encoded = urllib.parse.quote(t)
    url = f"https://liquipedia.net/pubg/api.php?action=opensearch&search={encoded}&limit=3&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            if resp.info().get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            d = json.loads(raw.decode("utf-8"))
            if d[1]:
                found_pages[t] = d[1]
                print(f"{t} -> {d[1]}")
    except Exception as e:
        print(f"{t} 오류: {e}")

with open("intermediate_results/team_search_matches.json", "w", encoding="utf-8") as f:
    json.dump(found_pages, f, ensure_ascii=False, indent=2)

print("=== 검색 완료 ===")
