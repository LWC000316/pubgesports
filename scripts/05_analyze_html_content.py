with open("primary_data/pubgesports_tournament_2024.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
# PWS, PGS, PGC, PCL 등 검색
keywords = ["PWS", "PGS", "PGC", "PCL", "PEC", "PAS", "KWANGDONG", "Gen.G", "Danawa"]
for kw in keywords:
    count = len(re.findall(kw, html, re.IGNORECASE))
    print(f"Keyword '{kw}': {count} occurrences")

# tournament 링크 형태 파악
links = re.findall(r'href="([^"]+)"', html)
tournament_links = [l for l in links if 'tournament' in l or 'team' in l or 'schedule' in l]
print("\nSample tournament/team links found:")
for l in list(set(tournament_links))[:10]:
    print(" -", l)
