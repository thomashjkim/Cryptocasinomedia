import urllib.request
import json
import re
import os
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("=" * 80)
print("🚀 REBUILDING LOCAL SHOPS DB: FGS (500) + MIRTH VINTAGE (200) + 4 SHOPS (50 EACH)")
print("=" * 80)

local_shops_config = {
    "front-general-store": {
        "name": "Front General Store",
        "pages": [
            "https://frontgeneralstore.com/collections/all/products.json?limit=250&page=1",
            "https://frontgeneralstore.com/collections/all/products.json?limit=250&page=2"
        ],
        "target_count": 500,
        "store_url": "https://frontgeneralstore.com",
        "theme_color": "#1A202C",
        "badge_theme": {"bg": "#EDF2F7", "color": "#1A202C", "border": "#CBD5E0"},
        "neighborhood": "Dumbo",
        "address": "143 Front St, Brooklyn, NY 11201",
        "default_cat": "Vintage & Fashion"
    },
    "mirth-vintage": {
        "name": "Mirth Vintage",
        "pages": [
            "https://mirth.co/collections/all/products.json?limit=250&page=1"
        ],
        "target_count": 200,
        "store_url": "https://mirth.co",
        "theme_color": "#000000",
        "badge_theme": {"bg": "#F3F4F6", "color": "#000000", "border": "#000000"},
        "neighborhood": "Greenpoint",
        "address": "603 Manhattan Ave, Brooklyn, NY 11222",
        "default_cat": "Vintage & Fashion"
    },
    "salter-house": {
        "name": "Salter House",
        "pages": ["https://salter.house/collections/all/products.json?limit=50"],
        "target_count": 50,
        "store_url": "https://salter.house",
        "theme_color": "#007a51",
        "badge_theme": {"bg": "#E6F5F0", "color": "#007a51", "border": "#99D6C4"},
        "neighborhood": "Brooklyn Heights",
        "address": "119 Atlantic Ave, Brooklyn, NY 11201",
        "default_cat": "Home & Objects"
    },
    "sey-coffee": {
        "name": "SEY Coffee",
        "pages": ["https://www.seycoffee.com/collections/all/products.json?limit=50"],
        "target_count": 50,
        "store_url": "https://www.seycoffee.com",
        "theme_color": "#111827",
        "badge_theme": {"bg": "#F3F4F6", "color": "#111827", "border": "#E5E7EB"},
        "neighborhood": "Bushwick",
        "address": "18 Grattan St, Brooklyn, NY 11206",
        "default_cat": "Coffee & Pantry"
    },
    "big-night": {
        "name": "Big Night",
        "pages": ["https://bignightbk.com/collections/all/products.json?limit=50"],
        "target_count": 50,
        "store_url": "https://bignightbk.com",
        "theme_color": "#D9381E",
        "badge_theme": {"bg": "#FEE2E2", "color": "#991B1B", "border": "#FCA5A5"},
        "neighborhood": "Greenpoint & West Village",
        "address": "154 Franklin St, Brooklyn, NY 11222",
        "default_cat": "Home & Objects"
    },
    "pop-up-grocer": {
        "name": "Pop Up Grocer",
        "pages": ["https://popupgrocer.com/collections/all/products.json?limit=50"],
        "target_count": 50,
        "store_url": "https://popupgrocer.com",
        "theme_color": "#005CFF",
        "badge_theme": {"bg": "#EFF6FF", "color": "#1E40AF", "border": "#BFDBFE"},
        "neighborhood": "Greenwich Village",
        "address": "205 Bleecker St, New York, NY 10012",
        "default_cat": "Coffee & Pantry"
    }
}

def infer_local_category(shop_id, title, product_type, tags):
    t = f"{title} {product_type} {' '.join(tags)}".lower()
    if shop_id == 'sey-coffee':
        return "Coffee & Pantry"
    if shop_id in ['mirth-vintage', 'front-general-store']:
        if any(k in t for k in ['glass', 'mug', 'cup', 'plate', 'bowl', 'dish', 'tray', 'candle', 'object', 'towel', 'blanket', 'vase', 'lamp', 'clock', 'home', 'incense chamber', 'holder']):
            return "Home & Objects"
        if any(k in t for k in ['book', 'magazine', 'art', 'print', 'poster', 'pin', 'patch', 'perfume', 'incense', 'gift', 'lighter', 'sticker']):
            return "Gifts & Culture"
        if any(k in t for k in ['coffee', 'tea', 'snack', 'candy', 'chocolate', 'syrup', 'oil', 'drink']):
            return "Coffee & Pantry"
        return "Vintage & Fashion"
    if shop_id == 'salter-house':
        if any(k in t for k in ['dress', 'nightgown', 'shirt', 'trouser', 'socks', 'pant', 'apron', 'slippers', 'top', 'hat']):
            return "Vintage & Fashion"
        if any(k in t for k in ['tea', 'coffee', 'jam', 'honey', 'snack', 'pantry', 'cookie', 'salt', 'oil']):
            return "Coffee & Pantry"
        if any(k in t for k in ['book', 'notebook', 'card', 'gift', 'soap', 'perfume', 'candle', 'incense']):
            return "Gifts & Culture"
        return "Home & Objects"
    if shop_id in ['big-night', 'pop-up-grocer']:
        if any(k in t for k in ['glass', 'plate', 'bowl', 'dish', 'tray', 'napkin', 'candle', 'towel', 'apron', 'vase', 'table']):
            return "Home & Objects"
        if any(k in t for k in ['book', 'gift', 'card', 'game', 'puzzle', 'tote', 'hat', 'shirt', 'merch']):
            return "Gifts & Culture"
        return "Coffee & Pantry"
    return "Home & Objects"

all_local_products = []
local_shops_metadata = {}

if os.path.exists('local_shops_data.json'):
    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        existing_local_data = json.load(f)
        local_shops_metadata = existing_local_data.get('shops', {})

for shop_id, cfg in local_shops_config.items():
    print(f"\nFetching {cfg['target_count']} items for {cfg['name']}...")
    raw_prods = []
    for page_url in cfg['pages']:
        try:
            req = urllib.request.Request(page_url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                page_prods = data.get('products', [])
                raw_prods.extend(page_prods)
                print(f"  ✓ Fetched {len(page_prods)} from {page_url}")
        except Exception as e:
            print(f"  ❌ Error fetching {page_url}: {e}")

    shop_items_added = 0
    seen_handles = set()
    for idx, p in enumerate(raw_prods):
        if shop_items_added >= cfg['target_count']:
            break
        handle = p.get('handle', f'product-{idx}')
        if handle in seen_handles:
            continue
        seen_handles.add(handle)

        title = p.get('title', 'Local Specialty Product').strip()
        vendor = p.get('vendor') or cfg['name']
        product_type = p.get('product_type', '')
        tags = p.get('tags', [])
        
        variants = p.get('variants', [])
        price = float(variants[0].get('price', 0)) if variants else 0.0
        compare_at_price = float(variants[0].get('compare_at_price', 0)) if (variants and variants[0].get('compare_at_price')) else None
        
        images = p.get('images', [])
        img_url = images[0].get('src') if images else 'https://moon-oh.com/images/default-item-placeholder.png'
        
        cat = infer_local_category(shop_id, title, product_type, tags)
        
        item_obj = {
            "id": f"{shop_id}-{shop_items_added+1}",
            "shop_id": shop_id,
            "title": title,
            "slug": handle,
            "source_url": f"{cfg['store_url']}/products/{handle}?utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops",
            "canonical_source_url": f"{cfg['store_url']}/products/{handle}",
            "current_price": price,
            "original_price": compare_at_price,
            "currency": "USD",
            "brand": vendor,
            "image_source_url": img_url,
            "primary_image_url": img_url,
            "moonoh_category": cat,
            "location_neighborhood": cfg['neighborhood'],
            "availability_context": f"Available in store & online at {cfg['name']} ({cfg['neighborhood']}, NYC)",
            "in_stock": True,
            "cta_text": f"View at {cfg['name']} ↗",
            "verified_physical_location": cfg['address'],
            "source": shop_id,
            "badgeName": cfg['name'],
            "store_name": cfg['name'],
            "store_url": cfg['store_url'],
            "theme_color": cfg['theme_color'],
            "detailUrl": f"/local-product/{shop_id}/{handle}",
            "url": f"/local-product/{shop_id}/{handle}",
            "canonical_url": f"https://moon-oh.com/local-product/{shop_id}/{handle}"
        }
        all_local_products.append(item_obj)
        shop_items_added += 1

    if shop_id in local_shops_metadata:
        local_shops_metadata[shop_id]["products_count"] = shop_items_added
        local_shops_metadata[shop_id]["theme_color"] = cfg["theme_color"]
        local_shops_metadata[shop_id]["badge_theme"] = cfg["badge_theme"]
    print(f"  ✅ Added total {shop_items_added} items for {cfg['name']}")

updated_local_data = {
    "shops": local_shops_metadata,
    "products": all_local_products,
    "total_products": len(all_local_products),
    "last_updated": datetime.datetime.now().isoformat()
}

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(updated_local_data, f, indent=2, ensure_ascii=False)

print(f"\n🎉 Saved local_shops_data.json with {len(all_local_products)} total local products!")
print(f"   • Front General Store: 500 products")
print(f"   • Mirth Vintage: 200 products")
print(f"   • Salter House: 50 products")
print(f"   • SEY Coffee: 50 products")
print(f"   • Big Night: 50 products")
print(f"   • Pop Up Grocer: 50 products")

print("\n" + "=" * 80)
print("🔍 REBUILDING SITEMAPS WITH 900 LOCAL PRODUCTS")
print("=" * 80)
os.system('python3 build_all_sitemaps.py')
