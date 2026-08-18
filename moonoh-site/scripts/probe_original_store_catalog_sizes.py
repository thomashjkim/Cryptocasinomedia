import urllib.request
import json
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

stores = [
    {"id": "front-general-store", "name": "Front General Store", "base_url": "https://frontgeneralstore.com"},
    {"id": "mirth-vintage", "name": "Mirth Vintage", "base_url": "https://mirth.co"},
    {"id": "salter-house", "name": "Salter House", "base_url": "https://salter.house"},
    {"id": "sey-coffee", "name": "SEY Coffee", "base_url": "https://www.seycoffee.com"},
    {"id": "big-night", "name": "Big Night", "base_url": "https://bignightbk.com"},
    {"id": "pop-up-grocer", "name": "Pop Up Grocer", "base_url": "https://popupgrocer.com"},
    {"id": "happier-grocery", "name": "Happier Grocery", "base_url": "https://www.happiergrocery.com"}
]

print("=" * 80)
print("🔍 PROBING ORIGINAL LOCAL STORE INVENTORY SIZES (OFFICIAL SHOPIFY CATALOGS)")
print("=" * 80)

results = []

for store in stores:
    total_products = 0
    page = 1
    has_more = True
    
    print(f"\nChecking {store['name']} ({store['base_url']})...")
    while has_more and page <= 20:  # up to 5,000 items
        url = f"{store['base_url']}/products.json?limit=250&page={page}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                products = data.get('products', [])
                if not products:
                    has_more = False
                else:
                    total_products += len(products)
                    if len(products) < 250:
                        has_more = False
                    else:
                        page += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            has_more = False
    
    print(f"  ➔ Total Original Products in {store['name']}: {total_products} items (scanned {page} pages)")
    results.append({
        "name": store['name'],
        "url": store['base_url'],
        "total_original": total_products
    })

# Sort by total products descending
results.sort(key=lambda x: x['total_original'], reverse=True)

print("\n" + "=" * 80)
print("🏆 RANKING: ORIGINAL LOCAL STORE INVENTORY SIZES")
print("=" * 80)
for idx, r in enumerate(results):
    print(f"[{idx+1}] {r['name']:<25} | {r['total_original']:>6,} items | {r['url']}")
print("=" * 80)
