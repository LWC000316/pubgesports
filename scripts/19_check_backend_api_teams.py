import urllib.request
import json

try:
    with urllib.request.urlopen("http://localhost:8080/api/teams") as res:
        teams = json.loads(res.read().decode("utf-8"))
        print(f"Backend /api/teams count: {len(teams)}")
        for t in teams[:5]:
            print(f" - Team: {t.get('name')}, League: {t.get('league')}, Players: {[p.get('nickname') for p in t.get('players', [])]}")
except Exception as e:
    print(f"Error fetching /api/teams: {e}")
