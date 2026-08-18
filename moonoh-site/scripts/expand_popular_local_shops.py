import urllib.request
import json
import time
import re
import os
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

print("=" * 80)
print("🚀 METHOD B: PHASED EXPANSION OF POPULAR LOCAL SHOPS")
print("=" * 80)

# Shop Configurations and Expansion Targets
expansion_config = [
    {
        "shop_id": "front-general-store",
        "name": "Front General Store",
        "base_url": "https://frontgeneralstore.com",
        "target_count": 500,
        "default_cat": "Vintage & Fashion",
        "location": "Dumbo, Brooklyn, NYC",
        "neighborhood": "Dumbo",
        "address": "143 Front St, Brooklyn, NY 11201"
    },
    {
        "shop_id": "sey-coffee",
        "name": "SEY Coffee",
        "base_url": "https://www.seycoffee.com",
        "target_count": 300,
        "default_cat": "Coffee & Pantry",
        "location": "Bushwick, Brooklyn, NYC",
        "neighborhood": "Bushwick",
        "address": "18 Grattan St, Brooklyn, NY 11206"
    },
    {
        "shop_id": "salter-house",
        "name": "Salter House",
        "base_url": "https://salter.house",
        "target_count": 200,
        "default_cat": "Home & Objects",
        "location": "Brooklyn Heights, Brooklyn, NYC",
        "neighborhood": "Brooklyn Heights",
        "address": "119 Atlantic Ave, Brooklyn, NY 11201"
    },
    {
        "shop_id": "mirth-vintage",
        "name": "Mirth Vintage",
        "base_url": "https://mirth.co",
        "target_count": 200,
        "default_cat": "Vintage & Fashion",
        "location": "Greenpoint, Brooklyn, NYC",
        "neighborhood": "Greenpoint",
        "address": "603 Manhattan Ave, Brooklyn, NY 11222"
    },
    {
        "shop_id": "big-night",
        "name": "Big Night",
        "base_url": "https://bignightbk.com",
        "target_count": 200,
        "default_cat": "Home & Objects",
        "location": "Greenpoint, Brooklyn, NYC",
        "neighborhood": "Greenpoint",
        "address": "154 Franklin St, Brooklyn, NY 11222"
    }
]

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    return re.sub(r'[-\s]+', '-', text)

def infer_moonoh_category(title, product_type, default_cat):
    t = (title + ' ' + (product_type or '')).lower()
    if any(k in t for k in ['coffee', 'bean', 'roast', 'espresso', 'pantry', 'tea', 'syrup', 'olive oil', 'jam', 'snack', 'chocolate', 'preserve']):
        return 'Coffee & Pantry'
    if any(k in t for k in ['ring', 'necklace', 'earring', 'bracelet', 'silver', 'gold', 'jewelry', 'cuff', 'pendant']):
        return 'Jewelry & watches'
    if any(k in t for k in ['vintage', 'jacket', 'coat', 'denim', 'pant', 'dress', 'shirt', 'sweater', 'leather', 'tee', 'vest', 'cardigan', 'trousers', 'belt']):
        return 'Vintage & Fashion'
    if any(k in t for k in ['soap', 'lotion', 'balm', 'perfume', 'fragrance', 'candle', 'incense', 'cream', 'bath']):
        return 'Health & beauty'
    if any(k in t for k in ['glass', 'cup', 'mug', 'plate', 'bowl', 'dish', 'tray', 'ceramic', 'towel', 'linen', 'apron', 'vase', 'pillow', 'brush']):
        return 'Home & Objects'
    if any(k in t for k in ['book', 'magazine', 'art', 'print', 'poster', 'stationery', 'card', 'notebook']):
        return 'Gifts & Culture'
    return default_cat

# Load existing local shops data to preserve Pop Up Grocer and Happier Grocery
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

existing_products = local_db.get('products', [])
preserved_products = [p for p in existing_products if p.get('shop_id') in ['pop-up-grocer', 'happier-grocery']]
print(f"Preserved {len(preserved_products)} curated products from Pop Up Grocer & Happier Grocery")

all_expanded_products = list(preserved_products)
today_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

for cfg in expansion_config:
    shop_id = cfg['shop_id']
    shop_name = cfg['name']
    base_url = cfg['base_url']
    target = cfg['target_count']
    default_cat = cfg['default_cat']
    
    print(f"\nHarvesting {shop_name} (Target: {target} items)...")
    shop_products = []
    page = 1
    has_more = True
    seen_handles = set()
    
    while has_more and len(shop_products) < target and page <= 10:
        url = f"{base_url}/products.json?limit=250&page={page}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                raw_products = data.get('products', [])
                if not raw_products:
                    has_more = False
                else:
                    for p in raw_products:
                        handle = p.get('handle', '')
                        if not handle or handle in seen_handles:
                            continue
                        
                        title = p.get('title', '').strip()
                        if not title or 'gift card' in title.lower() or 'tip' in title.lower():
                            continue
                        
                        images = p.get('images', [])
                        if not images:
                            continue
                        img_url = images[0].get('src', '')
                        if not img_url:
                            continue
                        
                        variants = p.get('variants', [])
                        if not variants:
                            continue
                        
                        price = float(variants[0].get('price', 0))
                        if price <= 0:
                            continue
                        
                        compare_at = variants[0].get('compare_at_price')
                        orig_price = float(compare_at) if compare_at else 0.0
                        discount_pct = round((orig_price - price) / orig_price * 100) if orig_price > price else 0
                        
                        seen_handles.add(handle)
                        prod_slug = handle
                        prod_id = f"{shop_id}-{prod_slug}"
                        vendor = p.get('vendor') or shop_name
                        product_type = p.get('product_type') or default_cat
                        moonoh_cat = infer_moonoh_category(title, product_type, default_cat)
                        
                        shop_products.append({
                            "id": prod_id,
                            "shop_id": shop_id,
                            "slug": prod_slug,
                            "source_url": f"{base_url}/products/{handle}",
                            "canonical_source_url": f"{base_url}/products/{handle}",
                            "title": title,
                            "brand": vendor,
                            "source_category": product_type,
                            "moonoh_category": moonoh_cat,
                            "current_price": price,
                            "original_price": orig_price,
                            "discount_percentage": discount_pct,
                            "availability": "in_stock",
                            "availability_context": f"Available in store at {shop_name} ({cfg['neighborhood']}, Brooklyn)",
                            "image_source_url": img_url,
                            "image_alt": f"{title} available at {shop_name}",
                            "moonoh_summary": f"Discover {title} from {vendor} at {shop_name} in {cfg['neighborhood']}, Brooklyn. Curated local item available at {shop_name}.",
                            "cta_text": f"View on {shop_name} ↗",
                            "last_checked_at": today_iso
                        })
                        
                        if len(shop_products) >= target:
                            break
                    
                    if len(raw_products) < 250:
                        has_more = False
                    else:
                        page += 1
            time.sleep(0.2)
        except Exception as e:
            print(f"  Error on page {page}: {e}")
            has_more = False
            
    print(f"✓ Extracted {len(shop_products)} high-quality products for {shop_name}")
    all_expanded_products.extend(shop_products)

# Update local_shops_data.json
local_db['products'] = all_expanded_products
with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(local_db, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"🎉 TOTAL EXPANDED LOCAL SHOP PRODUCTS: {len(all_expanded_products)} items")
print("=" * 80)

# Rebuild sitemaps
print("\nRebuilding XML Sitemaps...")
os.system("python3 build_all_sitemaps.py")
