"""Run this once to download the robot image into assets/"""
import urllib.request, os, sys

os.makedirs("assets", exist_ok=True)

# Multiple fallback URLs — tries each until one works
urls = [
    "https://cdn-icons-png.flaticon.com/512/8649/8649595.png",
    "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
    "https://cdn-icons-png.flaticon.com/512/6134/6134346.png",
]

for url in urls:
    try:
        print(f"Trying: {url}")
        urllib.request.urlretrieve(url, "assets/robot.png")
        size = os.path.getsize("assets/robot.png")
        if size > 5000:
            print(f"✓ Saved assets/robot.png ({size} bytes)")
            sys.exit(0)
    except Exception as e:
        print(f"  Failed: {e}")

print("✗ All downloads failed — will use emoji fallback")
