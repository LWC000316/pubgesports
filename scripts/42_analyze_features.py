import json
import glob
import os

with open("intermediate_results/sample_match_data.json", "r", encoding="utf-8") as f:
    sample_match = json.load(f)

match_summary = {
    "matchId": sample_match.get("matchId"),
    "map": sample_match.get("map"),
    "duration": sample_match.get("duration"),
    "teams_count": len(sample_match.get("teams", [])),
    "players_count": len(sample_match.get("players", [])),
    "kills_count": len(sample_match.get("kills", [])),
    "frames_count": len(sample_match.get("frames", []))
}

print("샘플 매치 데이터 요약:")
print(json.dumps(match_summary, ensure_ascii=False, indent=2))
