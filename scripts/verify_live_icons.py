import urllib.request

urls = [
    "/favicon.ico",
    "/icon.svg",
    "/icon.png",
    "/apple-icon.png",
]

base = "https://aegis-brain-alpha.vercel.app"

for path in urls:
    full = base + path
    try:
        req = urllib.request.Request(full, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            ct = resp.headers.get("Content-Type")
            print(f"  [OK] {path}: Status {resp.status}, Content-Type: {ct}, Size: {len(data):,} bytes")
    except Exception as e:
        print(f"  [FAIL] {path}: {e}")
