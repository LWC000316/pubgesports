import urllib.request
import gzip
import json

# 1. 2026 PWS Phase 2에 포함된 전체 이미지 목록 가져오기
url = 'https://liquipedia.net/pubg/api.php?action=parse&page=PUBG_WEEKLY_SERIES/2026/Phase_2&prop=images&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'PUBGEsportsPlatform/1.0 (contact@pubgproject.local)', 'Accept-Encoding': 'gzip'})
with urllib.request.urlopen(req) as resp:
    raw = resp.read()
    if resp.info().get('Content-Encoding') == 'gzip':
        raw = gzip.decompress(raw)
    data = json.loads(raw.decode('utf-8'))

all_images = data.get('parse', {}).get('images', [])

# 이미지 URL 일괄 조회 (한 번에 최대 50개까지 가능)
titles = '|'.join(['File:' + f for f in all_images])
query_url = f'https://liquipedia.net/pubg/api.php?action=query&titles={titles}&prop=imageinfo&iiprop=url&format=json'
q_req = urllib.request.Request(query_url, headers={'User-Agent': 'PUBGEsportsPlatform/1.0 (contact@pubgproject.local)', 'Accept-Encoding': 'gzip'})

with urllib.request.urlopen(q_req) as resp:
    raw = resp.read()
    if resp.info().get('Content-Encoding') == 'gzip':
        raw = gzip.decompress(raw)
    q_data = json.loads(raw.decode('utf-8'))

url_map = {}
for k, v in q_data.get('query', {}).get('pages', {}).items():
    t = v.get('title', '').replace('File:', '')
    ii = v.get('imageinfo', [{}])[0]
    u = ii.get('url')
    if u:
        url_map[t] = u

print(f'조회된 이미지 URL 총 개수: {len(url_map)}')
with open('intermediate_results/liquipedia_image_urls.json', 'w', encoding='utf-8') as f:
    json.dump(url_map, f, ensure_ascii=False, indent=2)
