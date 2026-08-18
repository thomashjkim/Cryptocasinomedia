import urllib.request
import urllib.parse
import json
import re

print("=" * 80)
print("📥 STEP 1: SYNCING LIVE MOONOH BACKEND DATABASE (640+ ITEMS)")
print("=" * 80)

def fetch_live_moonoh_items():
    login_data = urllib.parse.urlencode({'kind': 'login', 'id': 'admin', 'password': '1234'}).encode('utf-8')
    req_login = urllib.request.Request('http://52.44.113.58:8080/admin.do', data=login_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
    with urllib.request.urlopen(req_login, timeout=10) as resp:
        cookies = resp.headers.get('Set-Cookie', '')
        cookie = cookies.split(';')[0] if cookies else ''

    data_payload = urllib.parse.urlencode({'kind': 'getProductArray', 'page': '0', 'viewCount': '1000'}).encode('utf-8')
    req_data = urllib.request.Request('http://52.44.113.58:8080/admin.do', data=data_payload, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie})
    
    with urllib.request.urlopen(req_data, timeout=15) as d_resp:
        res_json = json.loads(d_resp.read().decode('utf-8'))
        products = res_json.get('productArray', []) if isinstance(res_json, dict) else res_json
        return products

def standardize_location(raw_loc):
    if not raw_loc:
        return 'Manhattan, NY'
    l = str(raw_loc).strip()
    # Strip 1mi prefixes
    l = re.sub(r'^\d+mi\s*·\s*', '', l, flags=re.IGNORECASE).strip()
    l = re.sub(r'^\d+mi\s+', '', l, flags=re.IGNORECASE).strip()
    
    low = l.lower()
    if 'bayside' in low or 'flushing' in low or 'astoria' in low or 'queens' in low or 'lic' in low or 'long island city' in low:
        return 'Queens, NY'
    if 'brooklyn' in low or 'williamsburg' in low or 'greenpoint' in low or 'dumbo' in low or 'bushwick' in low or 'park slope' in low:
        return 'Brooklyn, NY'
    if 'manhattan' in low or 'soho' in low or 'tribeca' in low or 'midtown' in low or 'harlem' in low or 'village' in low or 'new york' in low:
        return 'Manhattan, NY'
    if 'bronx' in low:
        return 'The Bronx, NY'
    if 'staten island' in low:
        return 'Staten Island, NY'
    if 'fort lee' in low or 'palisades' in low or 'bergen' in low or 'edgewater' in low or 'leonia' in low or 'paramus' in low:
        return 'Bergen County, NJ'
    if 'jersey city' in low or 'hoboken' in low or 'hudson' in low or 'weehawken' in low or 'secaucus' in low:
        return 'Hudson County, NJ'
    
    return 'Manhattan, NY'

def infer_category(title, desc, cat_name):
    txt = f"{title or ''} {desc or ''} {cat_name or ''}".lower()
    if any(w in txt for w in ['phone', 'laptop', 'camera', 'airpods', 'ipad', 'tv', 'headphone', 'audio', 'electronic', 'charger', 'speaker', 'keyboard', 'monitor', 'printer', 'ps5', 'nintendo', 'ring']):
        return 'Electronics & Appliances'
    if any(w in txt for w in ['sofa', 'table', 'chair', 'bed', 'desk', 'couch', 'dresser', 'mattress', 'shelf', 'nightstand', 'cabinet', 'stool', 'bench', '가구', '책상', '의자', '침대', '식탁']):
        return 'Furniture'
    if any(w in txt for w in ['dress', 'skirt', 'jacket', 'coat', 'pant', 'shirt', 'sweater', 'blouse', 'denim', 'jeans', 'women', 'fashion', 'boots', 'sneakers', 'bag', 'purse', 'tote', 'clutch', 'earring', 'necklace', 'perfume', 'cologne']):
        return "Women's & Men's Fashion"
    if any(w in txt for w in ['cookie', 'snack', 'food', 'tea', 'coffee', 'sauce', 'oil', 'grocery', 'chip', 'noodle', 'rice']):
        return 'Food & Groceries'
    if any(w in txt for w in ['cream', 'lotion', 'serum', 'shampoo', 'soap', 'cosmetic', 'beauty', 'skin', 'wellness', 'fragrance']):
        return 'Health & Beauty'
    if any(w in txt for w in ['baby', 'kid', 'stroller', 'toy', 'doll', 'crib', 'infant']):
        return 'Baby & Kids'
    if any(w in txt for w in ['dog', 'cat', 'pet', 'leash', 'crate', 'carrier']):
        return 'Pet Supplies'
    if any(w in txt for w in ['bowl', 'plate', 'vase', 'candle', 'cup', 'glass', 'dish', 'towel', 'tray', 'pot', 'pan', 'kitchen', 'home', 'decor']):
        return 'Home, garden & DIY'
    return 'Used Items'

raw_products = fetch_live_moonoh_items()
print(f"✅ Fetched {len(raw_products)} raw items from Moonoh Backend")

sanitized_items = []
for p in raw_products:
    p_no = p.get('no') or p.get('id')
    if not p_no:
        continue
    
    # Check images
    img = p.get('photo') or p.get('image') or ''
    if img:
        if img.startswith('http://52.44.113.58:8080/'):
            # Convert to secure proxy URL
            path_part = img.replace('http://52.44.113.58:8080/', '')
            img = f"https://moon-oh.com/image-proxy/{path_part}"
        elif not img.startswith('http'):
            img = f"https://moon-oh.com/image-proxy/{img.lstrip('/')}"
    else:
        img = "https://moon-oh.com/images/default-item-placeholder.png"
    
    town = standardize_location(p.get('townName') or p.get('location'))
    cat = infer_category(p.get('title'), p.get('description'), p.get('categoryName'))
    
    price_val = 0.0
    try:
        price_val = float(p.get('price') or 0)
    except:
        price_val = 0.0
    
    # Generate canonical URL slug
    clean_title = re.sub(r'[^a-z0-9\s-]', '', (p.get('title') or 'item').lower()).strip()
    clean_title = re.sub(r'\s+', '-', clean_title)
    clean_title = re.sub(r'-+', '-', clean_title)[:50].rstrip('-') or 'item'
    loc_slug = re.sub(r'[^a-z0-9\s-]', '', town.lower()).strip().replace(' ', '-')
    canonical_slug = f"{clean_title}-{loc_slug}-{p_no}"
    
    item_obj = {
        "id": f"moonoh-{p_no}",
        "no": p_no,
        "title": p.get('title') or "Untitled Item",
        "price": price_val,
        "location": town,
        "rawTown": town,
        "townName": town,
        "lat": p.get('lat') or 40.7128,
        "lng": p.get('lng') or -74.0060,
        "category": cat,
        "categoryName": cat,
        "image": img,
        "photo": img,
        "sellerName": p.get('sellerName') or "Moonoh User",
        "description": p.get('description') or f"Listing: {p.get('title')} in {town} on Moonoh.",
        "source": "moonoh",
        "sourceName": "Moonoh",
        "url": f"/item/{canonical_slug}",
        "canonical_url": f"https://moon-oh.com/item/{canonical_slug}",
        "postedAt": p.get('postedAt') or (1700000000000 + int(p_no) * 100000),
        "createdAt": p.get('createdAt') or p.get('postedAt') or (1700000000000 + int(p_no) * 100000)
    }
    sanitized_items.append(item_obj)

# Sort strictly newest first (No: 855 > 854 > 853...)
sanitized_items.sort(key=lambda x: int(x['no']), reverse=True)

print(f"✅ Processed and standardized {len(sanitized_items)} Moonoh items")
top_titles = [f"No.{x['no']} - {x['title'][:20]}" for x in sanitized_items[:5]]
print(f"  • Top 5 latest items: {top_titles}")

# Write to netlify/functions/moonoh-items-data.mjs
mjs_content = f"// Live Moonoh Items Dataset (Synced from Moonoh Backend - Total {len(sanitized_items)} items)\n"
mjs_content += f"export const realMoonohItems = {json.dumps(sanitized_items, indent=2, ensure_ascii=False)};\n"

with open('netlify/functions/moonoh-items-data.mjs', 'w', encoding='utf-8') as f:
    f.write(mjs_content)
print("✅ Saved netlify/functions/moonoh-items-data.mjs")

# Also update data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(sanitized_items, f, indent=2, ensure_ascii=False)
print("✅ Saved data.json")
