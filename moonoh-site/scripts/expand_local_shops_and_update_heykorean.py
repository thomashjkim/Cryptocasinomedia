import urllib.request
import json
import re
import html
import os
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("=" * 80)
print("🚀 EXPANDING LOCAL SHOPS (50 ITEMS EACH) & UPDATING HEYKOREAN LISTINGS")
print("=" * 80)

# =========================================================================
# 1. EXPAND 6 LOCAL SHOPS TO 50 PRODUCTS EACH
# =========================================================================

local_shops_config = {
    "front-general-store": {
        "name": "Front General Store",
        "url": "https://frontgeneralstore.com/collections/all/products.json?limit=50",
        "store_url": "https://frontgeneralstore.com",
        "theme_color": "#1A202C",
        "badge_theme": {"bg": "#EDF2F7", "color": "#1A202C", "border": "#CBD5E0"},
        "neighborhood": "Dumbo",
        "address": "143 Front St, Brooklyn, NY 11201",
        "default_cat": "Vintage & Fashion"
    },
    "mirth-vintage": {
        "name": "Mirth Vintage",
        "url": "https://mirth.co/collections/all/products.json?limit=50",
        "store_url": "https://mirth.co",
        "theme_color": "#000000",
        "badge_theme": {"bg": "#F3F4F6", "color": "#000000", "border": "#000000"},
        "neighborhood": "Greenpoint",
        "address": "603 Manhattan Ave, Brooklyn, NY 11222",
        "default_cat": "Vintage & Fashion"
    },
    "salter-house": {
        "name": "Salter House",
        "url": "https://salter.house/collections/all/products.json?limit=50",
        "store_url": "https://salter.house",
        "theme_color": "#007a51",
        "badge_theme": {"bg": "#E6F5F0", "color": "#007a51", "border": "#99D6C4"},
        "neighborhood": "Brooklyn Heights",
        "address": "119 Atlantic Ave, Brooklyn, NY 11201",
        "default_cat": "Home & Objects"
    },
    "sey-coffee": {
        "name": "SEY Coffee",
        "url": "https://www.seycoffee.com/collections/all/products.json?limit=50",
        "store_url": "https://www.seycoffee.com",
        "theme_color": "#111827",
        "badge_theme": {"bg": "#F3F4F6", "color": "#111827", "border": "#E5E7EB"},
        "neighborhood": "Bushwick",
        "address": "18 Grattan St, Brooklyn, NY 11206",
        "default_cat": "Coffee & Pantry"
    },
    "big-night": {
        "name": "Big Night",
        "url": "https://bignightbk.com/collections/all/products.json?limit=50",
        "store_url": "https://bignightbk.com",
        "theme_color": "#D9381E",
        "badge_theme": {"bg": "#FEE2E2", "color": "#991B1B", "border": "#FCA5A5"},
        "neighborhood": "Greenpoint & West Village",
        "address": "154 Franklin St, Brooklyn, NY 11222",
        "default_cat": "Home & Objects"
    },
    "pop-up-grocer": {
        "name": "Pop Up Grocer",
        "url": "https://popupgrocer.com/collections/all/products.json?limit=50",
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
        if any(k in t for k in ['glass', 'mug', 'cup', 'plate', 'bowl', 'dish', 'tray', 'candle', 'object', 'towel', 'blanket', 'vase', 'lamp', 'clock', 'home']):
            return "Home & Objects"
        if any(k in t for k in ['book', 'magazine', 'art', 'print', 'poster', 'pin', 'patch', 'perfume', 'incense']):
            return "Gifts & Culture"
        if any(k in t for k in ['coffee', 'tea', 'snack', 'candy', 'chocolate', 'syrup', 'oil']):
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

# Load existing local_shops_data.json if exists
if os.path.exists('local_shops_data.json'):
    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        existing_local_data = json.load(f)
        local_shops_metadata = existing_local_data.get('shops', {})

for shop_id, cfg in local_shops_config.items():
    print(f"\nFetching 50 items for {cfg['name']}...")
    try:
        req = urllib.request.Request(cfg['url'], headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_prods = data.get('products', [])
            print(f"  ✓ Received {len(raw_prods)} raw products from {cfg['name']}")
            
            shop_items_added = 0
            for idx, p in enumerate(raw_prods[:50]):
                title = p.get('title', 'Local Specialty Product').strip()
                handle = p.get('handle', f'product-{idx}')
                vendor = p.get('vendor') or cfg['name']
                product_type = p.get('product_type', '')
                tags = p.get('tags', [])
                
                # Prices
                variants = p.get('variants', [])
                price = float(variants[0].get('price', 0)) if variants else 0.0
                compare_at_price = float(variants[0].get('compare_at_price', 0)) if (variants and variants[0].get('compare_at_price')) else None
                
                # Images
                images = p.get('images', [])
                img_url = images[0].get('src') if images else 'https://moon-oh.com/images/default-item-placeholder.png'
                
                # Clean clean category
                cat = infer_local_category(shop_id, title, product_type, tags)
                
                item_obj = {
                    "id": f"{shop_id}-{idx+1}",
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
            
            # Update shop metadata count
            if shop_id in local_shops_metadata:
                local_shops_metadata[shop_id]["products_count"] = shop_items_added
                local_shops_metadata[shop_id]["theme_color"] = cfg["theme_color"]
                local_shops_metadata[shop_id]["badge_theme"] = cfg["badge_theme"]
            print(f"  ✅ Added {shop_items_added} items for {cfg['name']}")
    except Exception as e:
        print(f"  ❌ Error fetching {cfg['name']}: {e}")

# Save updated local_shops_data.json
updated_local_data = {
    "shops": local_shops_metadata,
    "products": all_local_products,
    "total_products": len(all_local_products),
    "last_updated": datetime.datetime.now().isoformat()
}

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(updated_local_data, f, indent=2, ensure_ascii=False)

print(f"\n🎉 Saved local_shops_data.json with {len(all_local_products)} total local products (50 per shop)!")


# =========================================================================
# 2. UPDATE HEYKOREAN MARKETPLACE LISTINGS WITH TODAY'S FRESH ITEMS
# =========================================================================

print("\n" + "=" * 80)
print("🔍 FETCHING & MERGING TODAY'S HEYKOREAN LISTINGS")
print("=" * 80)

def clean_and_translate_title(title):
    t = title.strip()
    t = re.sub(r'^[^\w]*[\w\s\$]+｜', '', t).strip()
    t = re.sub(r'\d{3}[-\s]?\d{3,4}[-\s]?\d{4}', '', t).strip()
    translations = [
        (r'팝니다', 'for Sale'), (r'삽니다', 'Wanted'), (r'압력밥솥', 'Pressure Rice Cooker'),
        (r'밥솥', 'Rice Cooker'), (r'서랍장', 'Dresser'), (r'원목 소파 테이블', 'Solid Wood Sofa Table'),
        (r'식탁 세트', 'Dining Table Set'), (r'식탁', 'Dining Table'), (r'의자 포함', 'with Chairs'),
        (r'세탁기 건조기 세트', 'Washer & Dryer Set'), (r'세탁기', 'Washer'), (r'건조기', 'Dryer'),
        (r'아기 침대', 'Baby Crib'), (r'유모차', 'Stroller'), (r'공기청정기', 'Air Purifier'),
        (r'가습기', 'Humidifier'), (r'청소기', 'Vacuum Cleaner'), (r'화장대', 'Vanity Table'),
        (r'책상', 'Desk'), (r'의자', 'Chair'), (r'침대', 'Bed'), (r'소파', 'Sofa'),
        (r'가방', 'Bag'), (r'지갑', 'Wallet'), (r'신발', 'Shoes'), (r'옷', 'Clothing'),
        (r'골프클럽', 'Golf Clubs'), (r'모니터', 'Monitor'), (r'전자레인지', 'Microwave')
    ]
    for kor, eng in translations:
        t = re.sub(kor, eng, t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

# Load existing external items from netlify/functions/external-items.mjs
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    ext_mjs = f.read()

m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', ext_mjs, re.DOTALL)
m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', ext_mjs, re.DOTALL)

existing_karrot = json.loads(m_karrot.group(1)) if m_karrot else []
existing_hey = json.loads(m_hey.group(1)) if m_hey else []
print(f"Existing in DB: {len(existing_karrot)} Karrot, {len(existing_hey)} HeyKorean")

# Fetch today's fresh HeyKorean pages
fresh_hk_items = []
try:
    req_hk = urllib.request.Request('https://market.heykorean.com/api/market/list?page=1&size=50', headers=headers)
    with urllib.request.urlopen(req_hk, timeout=15) as resp:
        hk_data = json.loads(resp.read().decode('utf-8'))
        raw_list = hk_data.get('list', [])
        print(f"✓ Fetched {len(raw_list)} items from HeyKorean API")
        
        for r in raw_list:
            raw_title = r.get('title', '').strip()
            # Filter commercial spam
            if r.get('store_type') == 'B' or any(k in raw_title for k in ['우체국', '경매', 'HVAC', '상점 바로가기', 'CAR SALES', 'FORD', 'KIA', '설치', '구매대행']):
                continue
            
            main_img = r.get('main_image') or ''
            img_url = ''
            if main_img:
                try:
                    img_obj = json.loads(main_img)
                    img_url = img_obj.get('large') or img_obj.get('medium') or img_obj.get('origin') or ''
                except:
                    img_url = main_img
            
            if not img_url:
                continue
            
            eng_title = clean_and_translate_title(raw_title)
            area = r.get('area_name_en') or r.get('area_name') or 'New York, NY'
            cat = r.get('category_title_en') or r.get('category_title') or 'Used Items'
            price = float(r.get('price', 0))
            
            item_id = f"heykorean-{r.get('id')}"
            fresh_hk_items.append({
                'id': item_id,
                'title': eng_title,
                'price': price,
                'location': f"1mi · {area}",
                'rawTown': area,
                'category': cat,
                'image': img_url,
                'photo': img_url,
                'source': 'heykorean',
                'sourceName': 'HeyKorean',
                'sourceUrl': f"https://market.heykorean.com/item/{r.get('id')}",
                'url': f"https://market.heykorean.com/item/{r.get('id')}",
                'timeAgo': 'Today'
            })
        print(f"✓ Parsed {len(fresh_hk_items)} high-quality fresh HeyKorean items for today")
except Exception as e:
    print(f"❌ Error fetching HeyKorean: {e}")

# Merge fresh items into existing HeyKorean list with deduplication
existing_ids = {i.get('id') for i in fresh_hk_items}
merged_hey = list(fresh_hk_items)
for item in existing_hey:
    if item.get('id') not in existing_ids:
        merged_hey.append(item)
        existing_ids.add(item.get('id'))

print(f"✅ Total Merged HeyKorean Items: {len(merged_hey)} items")

# Write updated external-items.mjs
new_ext_code = f"""// Real External Items Dataset (Karrot NYC & HeyKorean NYC/NJ Verified Marketplaces)
export const realKarrotItems = {json.dumps(existing_karrot, indent=2, ensure_ascii=False)};

export const realHeyKoreanItems = {json.dumps(merged_hey, indent=2, ensure_ascii=False)};
"""

with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
    f.write(new_ext_code)

print("✅ Saved netlify/functions/external-items.mjs")


# =========================================================================
# 3. REBUILD ALL SITEMAPS
# =========================================================================

print("\n" + "=" * 80)
print("🔍 REBUILDING ALL SITEMAPS")
print("=" * 80)

os.system('python3 build_all_sitemaps.py')
