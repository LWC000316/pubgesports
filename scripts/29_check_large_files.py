import os

large_files = []
for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root or "build" in root or ".gradle" in root:
        continue
    for f in files:
        p = os.path.join(root, f)
        try:
            sz = os.path.getsize(p)
            if sz > 5 * 1024 * 1024:  # 5MB 이상
                large_files.append((p, sz / (1024 * 1024)))
        except:
            pass

print("5MB 이상 파일 목록:")
for p, sz in large_files:
    print(f" - {p}: {sz:.2f} MB")
