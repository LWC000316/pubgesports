import json

with open("intermediate_results/loadPlayerRegistry-DAwZTWap.js", "r", encoding="utf-8") as f:
    text = f.read()

with open("intermediate_results/loadMatchStats-DMWuc7Rg.js", "r", encoding="utf-8") as f:
    text2 = f.read()

with open("intermediate_results/Admin-BgtPz-YP.js", "r", encoding="utf-8") as f:
    text3 = f.read()

out_data = {
    "loadPlayerRegistry": text[:3000],
    "loadMatchStats": text2[:3000],
    "Admin": text3[:3000]
}

with open("intermediate_results/loader_samples.json", "w", encoding="utf-8") as out:
    json.dump(out_data, out, ensure_ascii=False, indent=2)

print("샘플 추출 완료")
