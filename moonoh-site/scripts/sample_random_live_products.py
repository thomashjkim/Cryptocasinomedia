import urllib.request
import json
import random

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prods = data['products']
random.seed(42)
samples = random.sample(prods, 15)

print(f"Sampling 15 random products across 900 items on live moon-oh.com:")
all_ok = True
for p in samples:
    u = f"https://moon-oh.com/local-product/{p['shop_id']}/{p['slug']}"
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            if resp.status == 200 and 'Product Not Found' not in body and '<h1' in body:
                print(f"  ✓ [{p['shop_id']}] {p['title'][:35]} -> HTTP 200 OK")
            else:
                print(f"  ✗ [{p['shop_id']}] {p['title'][:35]} -> FAILED")
                all_ok = False
    except Exception as e:
        print(f"  ✗ [{p['shop_id']}] {p['title'][:35]} -> ERROR: {e}")
        all_ok = False

print(f"\nAll 15 Random Live Samples Passed: {all_ok}")
