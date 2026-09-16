import json

with open("intermediate_results/latest_pws_matches_summary.json", "r", encoding="utf-8") as f:
    matches = json.load(f)

# 배틀그라운드 e스포츠 슈퍼 룰 순위 포인트
# 1등: 10, 2등: 6, 3등: 5, 4등: 4, 5등: 3, 6등: 2, 7등: 1, 8등: 1, 9등 이하: 0
rank_points_table = {
    1: 10,
    2: 6,
    3: 5,
    4: 4,
    5: 3,
    6: 2,
    7: 1,
    8: 1
}

team_stats = {}

for m in matches:
    for roster in m.get("rosters", []):
        tag = roster.get("teamTag")
        rank = roster.get("rank")
        players = roster.get("players", [])
        
        match_kills = sum(p.get("kills", 0) for p in players)
        match_damage = sum(p.get("damage", 0.0) for p in players)
        rank_pts = rank_points_table.get(rank, 0)
        chicken = 1 if rank == 1 else 0
        
        if tag not in team_stats:
            team_stats[tag] = {
                "teamTag": tag,
                "totalPoints": 0,
                "rankPoints": 0,
                "killPoints": 0,
                "damage": 0.0,
                "chickens": 0,
                "matchesPlayed": 0,
                "players": set()
            }
            
        team_stats[tag]["matchesPlayed"] += 1
        team_stats[tag]["killPoints"] += match_kills
        team_stats[tag]["rankPoints"] += rank_pts
        team_stats[tag]["totalPoints"] += (match_kills + rank_pts)
        team_stats[tag]["damage"] += match_damage
        team_stats[tag]["chickens"] += chicken
        for p in players:
            team_stats[tag]["players"].add(p.get("name"))

leaderboard = []
for tag, data in team_stats.items():
    leaderboard.append({
        "teamTag": tag,
        "totalPoints": data["totalPoints"],
        "killPoints": data["killPoints"],
        "rankPoints": data["rankPoints"],
        "chickens": data["chickens"],
        "damage": round(data["damage"], 1),
        "players": sorted(list(data["players"]))
    })

# 정렬 기준: 총점 내림차순, 킬포인트 내림차순, 데미지 내림차순
leaderboard.sort(key=lambda x: (x["totalPoints"], x["killPoints"], x["damage"]), reverse=True)

for idx, item in enumerate(leaderboard, start=1):
    item["rank"] = idx

with open("intermediate_results/latest_pws_leaderboard.json", "w", encoding="utf-8") as f:
    json.dump(leaderboard, f, ensure_ascii=False, indent=2)

print("=== 2026 PWS Phase 2 Series 1 1일차 공식 리더보드 결과 ===")
print(f"{'순위':<4} {'팀태그':<8} {'총점':<6} {'순위P':<6} {'킬P':<6} {'치킨':<5} {'총데미지':<10}")
for row in leaderboard:
    print(f"{row['rank']:<4} {row['teamTag']:<8} {row['totalPoints']:<6} {row['rankPoints']:<6} {row['killPoints']:<6} {row['chickens']:<5} {row['damage']:<10}")
