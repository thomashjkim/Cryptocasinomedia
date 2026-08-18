import urllib.request
import json
import time
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

stores = [
    {"id": "front-general-store", "name": "Front General Store", "base_url": "https://frontgeneralstore.com", "cat": "Vintage & Fashion", "loc": "Dumbo, Brooklyn, NY"},
    {"id": "mirth-vintage", "name": "Mirth Vintage", "base_url": "https://mirth.co", "cat": "Vintage & Fashion", "loc": "Greenpoint, Brooklyn, NY"},
    {"id": "salter-house", "name": "Salter House", "base_url": "https://salter.house", "cat": "Home & Objects", "loc": "Brooklyn Heights, Brooklyn, NY"},
    {"id": "sey-coffee", "name": "SEY Coffee", "base_url": "https://www.seycoffee.com", "cat": "Coffee & Pantry", "loc": "Bushwick, Brooklyn, NY"},
    {"id": "big-night", "name": "Big Night", "base_url": "https://bignightbk.com", "cat": "Home & Objects", "loc": "Greenpoint, Brooklyn, NY"},
    {"id": "pop-up-grocer", "name": "Pop Up Grocer", "base_url": "https://popupgrocer.com", "cat": "Coffee & Pantry", "loc": "West Village, Manhattan, NY"}
]

print("=" * 80)
print("🧪 SIMULATION: FULL LOCAL STORE INGESTION & QUALITY FILTERING")
print("=" * 80)

summary = {}
total_valid_products = 0

for store in stores:
    page = 1
    has_more = True
    store_valid = 0
    store_total = 0
    
    print(f"\nProbing & filtering {store['name']}...")
    while has_more and page <= 15:
        url = f"{store['base_url']}/products.json?limit=250&page={page}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                products = data.get('products', [])
                if not products:
                    has_more = False
                else:
                    store_total += len(products)
                    for p in products:
                        title = p.get('title', '').strip()
                        # Exclude gift cards and test items
                        if not title or 'gift card' in title.lower() or 'tip' in title.lower():
                            continue
                        images = p.get('images', [])
                        if not images:
                            continue
                        variants = p.get('variants', [])
                        if not variants:
                            continue
                        price = float(variants[0].get('price', 0))
                        if price <= 0:
                            continue
                        
                        store_valid += 1
                    
                    if len(products) < 250:
                        has_more = False
                    else:
                        page += 1
            time.sleep(0.2)
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            has_more = False
            
    print(f"  ➔ {store['name']}: {store_valid:,} valid products (out of {store_total:,} scanned)")
    summary[store['name']] = {"valid": store_valid, "total": store_total}
    total_valid_products += store_valid

print("\n" + "=" * 80)
print(f"🎉 TOTAL HIGH-QUALITY INGESTIBLE LOCAL PRODUCTS: {total_valid_products:,} items")
print("=" * 80)
for sname, sdata in summary.items():
    print(f"• {sname:<25} : {sdata['valid']:>5,} 개 (전체 {sdata['total']:>5,} 개 중 유효)")
