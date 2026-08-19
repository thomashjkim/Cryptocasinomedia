import urllib.request
import json
import time
import re
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

print("=" * 80)
print("🛍️  FETCHING ALL PRODUCTS FROM ALL LOCAL SHOP WEBSITES (FULL CATALOG)")
print("=" * 80)

SHOP_CONFIGS = [
    {
        "shop_id": "sey-coffee",
        "name": "SEY Coffee",
        "base_url": "https://www.seycoffee.com",
        "default_cat": "Coffee & Pantry",
        "location": "Brooklyn, NY",
        "neighborhood": "Bushwick",
        "borough": "Brooklyn, NY",
        "address": "18 Grattan St, Brooklyn, NY 11206",
        "lat": 40.7071, "lng": -73.9370,
        "theme_color": "#1A1A1A",
    },
    {
        "shop_id": "salter-house",
        "name": "Salter House",
        "base_url": "https://salter.house",
        "default_cat": "Home & Objects",
        "location": "Brooklyn, NY",
        "neighborhood": "Brooklyn Heights",
        "borough": "Brooklyn, NY",
        "address": "119 Atlantic Ave, Brooklyn, NY 11201",
        "lat": 40.6892, "lng": -73.9957,
        "theme_color": "#4A4A4A",
    },
    {
        "shop_id": "mirth-vintage",
        "name": "Mirth Vintage",
        "base_url": "https://mirth.co",
        "default_cat": "Vintage & Fashion",
        "location": "Brooklyn, NY",
        "neighborhood": "Greenpoint",
        "borough": "Brooklyn, NY",
        "address": "603 Manhattan Ave, Brooklyn, NY 11222",
        "lat": 40.7244, "lng": -73.9508,
        "theme_color": "#8B6A4A",
    },
    {
        "shop_id": "big-night",
        "name": "Big Night",
        "base_url": "https://bignightbk.com",
        "default_cat": "Home & Objects",
        "location": "Brooklyn, NY",
        "neighborhood": "Greenpoint",
        "borough": "Brooklyn, NY",
        "address": "167 Driggs Ave, Brooklyn, NY 11222",
        "lat": 40.7247, "lng": -73.9512,
        "theme_color": "#2D4A6B",
    },
    {
        "shop_id": "pop-up-grocer",
        "name": "Pop Up Grocer",
        "base_url": "https://popupgrocer.com",
        "default_cat": "Coffee & Pantry",
        "location": "Manhattan, NY",
        "neighborhood": "Greenwich Village",
        "borough": "Manhattan, NY",
        "address": "205 Bleecker St, New York, NY 10012",
        "lat": 40.7291, "lng": -74.0016,
        "theme_color": "#005CFF",
    },
]

def make_slug(title):
    slug = re.sub(r'[^a-z0-9\s-]', '', title.lower()).strip()
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug[:80].rstrip('-') or 'product'

def infer_category(cfg, product):
    tags = [t.lower() for t in (product.get('tags') or [])]
    ptype = (product.get('product_type') or '').lower()
    title = (product.get('title') or '').lower()
    desc = re.sub(r'<[^>]+>', '', product.get('body_html') or '').lower()[:200]
    combined = f"{title} {ptype} {' '.join(tags)} {desc}"

    if any(w in combined for w in ['coffee', 'espresso', 'bean', 'roast', 'brew', 'tea', 'pantry', 'olive oil', 'syrup']):
        return 'Coffee & Pantry'
    if any(w in combined for w in ['vintage', 'jacket', 'coat', 'denim', 'dress', 'shirt', 'pant', 'skirt', 'knitwear', 'sweater', 'fashion', 'clothing', 'apparel']):
        return 'Vintage & Fashion'
    if any(w in combined for w in ['soap', 'lotion', 'candle', 'scent', 'perfume', 'beauty', 'skin', 'body', 'hair', 'wellness']):
        return 'Health & Beauty'
    if any(w in combined for w in ['glass', 'plate', 'bowl', 'dish', 'mug', 'cup', 'linen', 'towel', 'home', 'object', 'ceramic', 'tray', 'vase', 'decor']):
        return 'Home & Objects'
    if any(w in combined for w in ['book', 'print', 'poster', 'art', 'stationery', 'card', 'gift']):
        return 'Gifts & Culture'
    if any(w in combined for w in ['snack', 'food', 'grocer', 'drink', 'beverage', 'cookie', 'chip', 'sauce', 'oil', 'honey', 'jam']):
        return 'Coffee & Pantry'
    return cfg['default_cat']

def fetch_all_products(cfg):
    all_products = []
    page = 1
    while True:
        url = f"{cfg['base_url']}/products.json?limit=250&page={page}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode('utf-8'))
                prods = data.get('products', [])
                if not prods:
                    break
                all_products.extend(prods)
                print(f"  Page {page}: +{len(prods)} products (total so far: {len(all_products)})")
                if len(prods) < 250:
                    break
                page += 1
                time.sleep(0.4)
        except Exception as e:
            print(f"  Page {page} error: {e}")
            break
    return all_products

def transform_product(cfg, raw, idx):
    variant = raw.get('variants', [{}])[0]
    price_str = variant.get('price', '0')
    try:
        price = float(price_str)
    except:
        price = 0.0

    images = raw.get('images', [])
    img_url = images[0].get('src', '') if images else ''
    # Remove query params from image URL
    img_url = img_url.split('?')[0] if img_url else ''

    title = raw.get('title', 'Product')
    slug = make_slug(title)
    shop_slug = cfg['shop_id']
    product_handle = raw.get('handle', slug)
    
    category = infer_category(cfg, raw)
    
    source_url = f"{cfg['base_url']}/products/{product_handle}?utm_source=moonoh&utm_medium=referral&utm_campaign=local-shops"
    canonical_source_url = f"{cfg['base_url']}/products/{product_handle}"
    
    avail = variant.get('available', True)
    
    published_at = raw.get('published_at') or raw.get('created_at') or ''
    updated_at = raw.get('updated_at') or ''

    desc_html = raw.get('body_html', '') or ''
    desc_clean = re.sub(r'<[^>]+>', '', desc_html).strip()[:500]
    
    return {
        "id": f"{shop_slug}-{product_handle}",
        "shop_id": shop_slug,
        "slug": product_handle,
        "handle": product_handle,
        "source_url": source_url,
        "canonical_source_url": canonical_source_url,
        "title": title,
        "brand": cfg['name'],
        "source_category": raw.get('product_type', ''),
        "moonoh_category": category,
        "primary_category": category,
        "current_price": str(price),
        "price": str(price),
        "original_price": str(variant.get('compare_at_price') or '0'),
        "discount_percentage": "0",
        "currency": "USD",
        "availability": "in_stock" if avail else "out_of_stock",
        "in_stock": str(avail),
        "availability_context": f"Available in store at {cfg['name']} ({cfg['neighborhood']}, {cfg['borough'].split(',')[0]})",
        "image_source_url": img_url,
        "image_alt": f"{title} available at {cfg['name']}",
        "moonoh_summary": f"Discover {title} from {cfg['name']} at {cfg['address']}",
        "description": desc_clean,
        "cta_text": f"View on {cfg['name']} ↗",
        "verified_physical_location": cfg['address'],
        "store_name": cfg['name'],
        "store_url": cfg['base_url'],
        "theme_color": cfg['theme_color'],
        "detailUrl": f"/local-product/{shop_slug}/{product_handle}",
        "url": f"/local-product/{shop_slug}/{product_handle}",
        "canonical_url": f"https://moon-oh.com/local-product/{shop_slug}/{product_handle}",
        "location": cfg['borough'],
        "rawTown": cfg['borough'],
        "townName": cfg['borough'],
        "location_neighborhood": f"{cfg['neighborhood']}, {cfg['borough']}",
        "store_city": "New York" if "NY" in cfg['borough'] else "Brooklyn",
        "store_state": "NY" if "NY" in cfg['borough'] else "NJ",
        "lat": str(cfg['lat']),
        "lng": str(cfg['lng']),
        "badgeName": cfg['name'],
        "source": shop_slug,
        "source_published_at": published_at,
        "last_checked_at": datetime.datetime.utcnow().isoformat() + "+00:00",
    }

# Load existing data
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    existing_db = json.load(f)

existing_shops = existing_db.get('shops', {})

# Keep front-general-store as-is (500 items already, their API 500s)
existing_front = [p for p in existing_db.get('products', []) if p.get('shop_id') == 'front-general-store']
print(f"\nℹ️  front-general-store API returns HTTP 500 - keeping existing {len(existing_front)} items")

all_new_products = list(existing_front)

# Fetch all products from each working shop
for cfg in SHOP_CONFIGS:
    print(f"\n{'='*60}")
    print(f"🛍️  Fetching ALL products from {cfg['name']} ({cfg['base_url']})")
    print(f"{'='*60}")
    
    raw_products = fetch_all_products(cfg)
    print(f"  ✅ Total fetched: {len(raw_products)} products")
    
    # Filter to in-stock only
    in_stock = [p for p in raw_products if p.get('variants', [{}])[0].get('available', True)]
    print(f"  ✅ In-stock: {len(in_stock)} products")
    
    transformed = [transform_product(cfg, p, idx) for idx, p in enumerate(in_stock)]
    
    # Quality check
    with_img = sum(1 for p in transformed if p.get('image_source_url'))
    with_price = sum(1 for p in transformed if float(p.get('current_price', 0)) > 0)
    print(f"  ✅ With image: {with_img}/{len(transformed)} | With price: {with_price}/{len(transformed)}")
    
    all_new_products.extend(transformed)

print(f"\n{'='*80}")
print(f"📦 TOTAL PRODUCTS COLLECTED: {len(all_new_products)}")
print(f"{'='*80}")

# Breakdown by shop
from collections import Counter
by_shop = Counter(p['shop_id'] for p in all_new_products)
for shop, count in sorted(by_shop.items(), key=lambda x: -x[1]):
    print(f"  {shop}: {count} items")

# Save
new_db = {
    "shops": existing_shops,
    "products": all_new_products
}

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(new_db, f, ensure_ascii=False, indent=2)

print(f"\n✅ Saved local_shops_data.json with {len(all_new_products)} total products")
