import sys
import time

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import fetch_images as f  # noqa: E402

for q in sys.argv[1:]:
    j = f.api({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": 8, "format": "json"})
    print(q, "=>")
    for h in j["query"]["search"]:
        print("   ", h["title"])
    time.sleep(2)
