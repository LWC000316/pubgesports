import urllib.request
import os
import json

base_dir = "frontend/public/logos"
tourney_dir = os.path.join(base_dir, "tournaments")
team_dir = os.path.join(base_dir, "teams")

os.makedirs(tourney_dir, exist_ok=True)
os.makedirs(team_dir, exist_ok=True)

headers = {
    "User-Agent": "PUBGEsportsPlatform/1.0 (contact@pubgproject.local)"
}

def download_file(url, save_path):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            with open(save_path, "wb") as f:
                f.write(content)
        print(f"다운로드 성공: {save_path} ({len(content)} bytes)")
        return True
    except Exception as e:
        print(f"다운로드 실패 ({url}): {e}")
        return False

# 1. 대회 로고 다운로드
tourney_urls = {
    "pws.png": "https://liquipedia.net/commons/images/9/93/PUBG_WEEKLY_SERIES_KOREA_icon_darkmode.png",
    "pcl.png": "https://liquipedia.net/commons/images/d/d3/PUBG_Champions_League_darkmode.png",
    "emea.png": "https://liquipedia.net/commons/images/f/f3/Eu_hd.png",
    "amer.png": "https://liquipedia.net/commons/images/8/8a/PUBG_Americas_Series_darkmode.png",
    "apac.png": "https://liquipedia.net/commons/images/1/12/Asia-pacific_flag_hd.png"
}

for fname, url in tourney_urls.items():
    p = os.path.join(tourney_dir, fname)
    download_file(url, p)

# 2. 팀 로고 다운로드
with open("intermediate_results/liquipedia_image_urls.json", "r", encoding="utf-8") as f:
    img_urls = json.load(f)

team_logo_targets = {
    "dns.png": img_urls.get("DN SOOPers allmode.png"),
    "geng.png": img_urls.get("Gen.G Esports 2026 allmode.png"),
    "t1.png": img_urls.get("T1 2019 allmode.png"),
    "bgp.png": img_urls.get("Baegopa allmode.png"),
    "fn.png": img_urls.get("FN Esports allmode.png"),
    "azla.png": img_urls.get("PENTAGRAM 2023 darkmode.png"),
    "dn.png": img_urls.get("Divine KR allmode.png"),
    "phe.png": img_urls.get("PHANTOM HEARTS darkmode.png"),
    "dgp.png": img_urls.get("Game PT darkmode.png"),
    "sen.png": img_urls.get("Sentinel KR allmode.png"),
    "spf.png": img_urls.get("SUPERFECT Esports allmode.png"),
    "gk.png": img_urls.get("Geekay Esports 2024 allmode.png"),
    "eos.png": img_urls.get("Eagle Owls 22 allmode.png"),
    "cr.png": img_urls.get("Crazy Raccoon 2021 allmode.png"),
    "sl.png": img_urls.get("Star Balloon allmode.png"),
    "ggwp.png": "https://liquipedia.net/commons/images/8/8b/GGWP_darkmode.png",
    "om.png": img_urls.get("Overwhelm darkmode.png") or img_urls.get("Overwhelm allmode.png")
}

for fname, url in team_logo_targets.items():
    if url:
        p = os.path.join(team_dir, fname)
        download_file(url, p)

print("로고 다운로드 완료!")
