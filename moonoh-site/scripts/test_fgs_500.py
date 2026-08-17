import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

fgs_products = []
for page in [1, 2, 3]:
    url = f"https://frontgeneralstore.com/collections/all/products.json?limit=250&page={page}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            prods = data.get('products', [])
            fgs_products.extend(prods)
            print(f"Page {page}: received {len(prods)} products (Total so far: {len(fgs_products)})")
            if len(prods) < 250:
                break
    except Exception as e:
        print(f"Error on page {page}: {e}")

print(f"\nTotal Front General Store Products Available: {len(fgs_products)}")
