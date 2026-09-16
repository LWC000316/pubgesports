import json

with open("intermediate_results/latest_pws_matches_summary.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

player_stats = {}

for m in matches:
    for roster in m.get("rosters", []):
        tag = roster.get("teamTag")
        for p in roster.get("players", []):
            name = p.get("name")
            kills = p.get("kills", 0)
            damage = p.get("damage", 0.0)
            
            if name not in player_stats:
                player_stats[name] = {
                    "playerName": name,
                    "teamTag": tag,
                    "kills": 0,
                    "damage": 0.0,
                    "matches": 0
                }
            player_stats[name]["kills"] += kills
            player_stats[name]["damage"] += damage
            player_stats[name]["matches"] += 1

player_rankings = list(player_stats.values())
for p in player_rankings:
    p["damage"] = round(p["damage"], 1)

player_rankings.sort(key=lambda x: (x["kills"], x["damage"]), reverse=True)

for idx, p in enumerate(player_rankings, start=1):
    p["rank"] = idx

with open("intermediate_results/latest_pws_player_stats.json", "w", encoding="utf-8") as f:
    json.dump(player_rankings, f, ensure_ascii=False, indent=2)

print("=== 2026 PWS Phase 2 Series 1 1일차 개인 킬 TOP 10 ===")
print(f"{'순위':<4} {'선수명':<20} {'팀':<8} {'킬':<5} {'총데미지':<10}")
for p in player_rankings[:10]:
    print(f"{p['rank']:<4} {p['playerName']:<20} {p['teamTag']:<8} {p['kills']:<5} {p['damage']:<10}")
