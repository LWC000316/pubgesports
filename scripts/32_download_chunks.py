import re
import urllib.request
import os

with open("intermediate_results/index-BVrWBIgE.js", "r", encoding="utf-8") as f:
    text = f.read()

# 추가로 로드되는 청크들 검색
chunks = re.findall(r'["\'](/assets/[a-zA-Z0-9_-]+\.js)["\']', text)
chunks += re.findall(r'["\'](assets/[a-zA-Z0-9_-]+\.js)["\']', text)
chunks = list(set(chunks))

print(f"발견된 추가 청크 수: {len(chunks)}")
base_url = "https://wwcd.lol"

for c in chunks:
    if not c.startswith("/"):
        c = "/" + c
    url = base_url + c
    fname = os.path.basename(c)
    local_path = "intermediate_results/" + fname
    if not os.path.exists(local_path):
        try:
            urllib.request.urlretrieve(url, local_path)
            print(f"다운로드 성공: {fname}")
        except Exception as e:
            print(f"실패 {fname}: {e}")
