import urllib.request
import json
import re
import html
import time
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("=" * 80)
print("🥕 HARVESTING 500 FRESH AUTHENTIC NYC/NJ KARROT ITEMS")
print("=" * 80)

def extract_remix_context(html_str):
    start_idx = html_str.find('window.__remixContext =')
    if start_idx == -1: return None
    json_start = html_str.find('{', start_idx)
    brace_count = 0
    in_string = False
    escape = False
    for i in range(json_start, len(html_str)):
        c = html_str[i]
        if escape: escape = False; continue
        if c == '\\': escape = True; continue
        if c == '"': in_string = not in_string; continue
        if not in_string:
            if c == '{': brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    try: return json.loads(html_str[json_start:i+1])
                    except: return None
    return None

def standardize_location(loc_str):
    if not loc_str: return 'Manhattan, NY', 40.7831, -73.9712
    l = str(loc_str).lower()
    # Brooklyn
    if any(k in l for k in ['brooklyn', 'williamsburg', 'greenpoint', 'dumbo', 'bushwick', 'bedford', 'crown heights', 'park slope', 'bay ridge', 'sheepshead', 'flatbush', 'canarsie', 'downtown brooklyn', 'prospect', 'cobble hill', 'carroll']):
        return 'Brooklyn, NY', 40.6782, -73.9442
    # Queens
    if any(k in l for k in ['queens', 'astoria', 'flushing', 'long island city', 'lic', 'bayside', 'forest hills', 'rego park', 'sunnyside', 'woodside', 'elmhurst', 'jackson heights', 'jamaica', 'whitestone', 'ridgewood', 'ozone park']):
        return 'Queens, NY', 40.7282, -73.7949
    # Manhattan
    if any(k in l for k in ['manhattan', 'upper west side', 'upper east side', 'midtown', 'harlem', 'east harlem', 'washington heights', 'inwood', 'hell\'s kitchen', 'chelsea', 'soho', 'tribeca', 'village', 'chinatown', 'lower east side', 'financial district', 'new york', 'seventh avenue']):
        return 'Manhattan, NY', 40.7831, -73.9712
    # Bronx
    if any(k in l for k in ['bronx', 'riverdale', 'fordham', 'pelham', 'university heights', 'mott haven', 'throggs neck']):
        return 'The Bronx, NY', 40.8448, -73.8648
    # Staten Island
    if any(k in l for k in ['staten island', 'todt hill', 'st. george', 'tottenville']):
        return 'Staten Island, NY', 40.5795, -74.1502
    # New Jersey
    if any(k in l for k in ['fort lee', 'palisades', 'edgewater', 'leonia', 'paramus', 'closter', 'englewood', 'hackensack', 'bergen']):
        return 'Bergen County, NJ', 40.8509, -73.9701
    if any(k in l for k in ['jersey city', 'hoboken', 'weehawken', 'secaucus', 'newport', 'journal square', 'hudson']):
        return 'Hudson County, NJ', 40.7178, -74.0431
    # Nassau County
    if any(k in l for k in ['great neck', 'manhasset', 'nassau', 'long island']):
        return 'Nassau County, NY', 40.7433, -73.5884
    return 'Manhattan, NY', 40.7831, -73.9712

def infer_category(title):
    t = (title or '').lower()
    if any(k in t for k in ['chair', 'table', 'desk', 'sofa', 'couch', 'bed', 'mattress', 'dresser', 'nightstand', 'shelf', 'bookcase', 'cabinet', 'stool', 'bench', 'lamp', 'furniture', 'mirror', 'rug', 'curtain']):
        return 'Furniture'
    if any(k in t for k in ['phone', 'iphone', 'ipad', 'laptop', 'macbook', 'tv', 'television', 'monitor', 'keyboard', 'mouse', 'headphone', 'airpods', 'camera', 'speaker', 'audio', 'printer', 'ps5', 'xbox', 'nintendo', 'switch', 'charger', 'electronics', 'watch', 'apple watch']):
        return 'Electronics & appliances'
    if any(k in t for k in ['dress', 'skirt', 'jacket', 'coat', 'sweater', 'hoodie', 'shirt', 't-shirt', 'pants', 'jeans', 'boots', 'shoes', 'sneakers', 'bag', 'purse', 'tote', 'backpack', 'wallet', 'necklace', 'earring', 'ring', 'perfume', 'cologne', 'sunglasses', 'hat']):
        return 'Women\'s & Men\'s Fashion'
    if any(k in t for k in ['pot', 'pan', 'cookware', 'dish', 'plate', 'bowl', 'mug', 'cup', 'glass', 'knife', 'blender', 'air fryer', 'toaster', 'microwave', 'vacuum', 'fan', 'heater', 'plant', 'vase', 'candle', 'kitchen', 'home']):
        return 'Home, garden & DIY'
    if any(k in t for k in ['baby', 'kid', 'child', 'stroller', 'crib', 'toy', 'doll', 'infant', 'car seat']):
        return 'Baby & kids'
    if any(k in t for k in ['dog', 'cat', 'pet', 'leash', 'crate', 'carrier', 'aquarium']):
        return 'Pet supplies'
    if any(k in t for k in ['bike', 'bicycle', 'fitness', 'dumbbell', 'treadmill', 'yoga', 'golf', 'tennis', 'racket', 'weights', 'sports', 'tent', 'camping']):
        return 'Sports & leisure'
    if any(k in t for k in ['book', 'novel', 'game', 'board game', 'art', 'painting', 'poster', 'stationery', 'craft']):
        return 'Books, tickets & stationery'
    if any(k in t for k in ['cream', 'lotion', 'shampoo', 'serum', 'skincare', 'makeup', 'lipstick', 'beauty', 'cosmetics']):
        return 'Health & beauty'
    return 'Used Items'

def make_slug(title, loc_str, item_id):
    clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    clean_t = re.sub(r'\s+', '-', clean_t)
    clean_t = re.sub(r'-+', '-', clean_t)[:50].rstrip('-') or 'item'
    clean_l = re.sub(r'[^a-zA-Z0-9\s-]', '', loc_str).strip().lower()
    clean_l = re.sub(r'\s+', '-', clean_l)
    clean_l = re.sub(r'-+', '-', clean_l).rstrip('-')
    return f"/item/{clean_t}-{clean_l}-ext-{item_id}"

# Harvest keywords
search_keywords = [
    'furniture', 'sofa', 'table', 'chair', 'bed', 'desk', 'lamp', 'dresser', 'shelf', 'mirror', 'rug',
    'electronics', 'tv', 'phone', 'laptop', 'monitor', 'keyboard', 'camera', 'airpods', 'ipad', 'speaker', 'audio', 'ps5', 'switch', 'game',
    'dress', 'jacket', 'coat', 'shoes', 'sneakers', 'boots', 'bag', 'purse', 'tote', 'backpack', 'sweater', 'jeans', 'watch',
    'kitchen', 'cookware', 'pot', 'pan', 'dish', 'plate', 'mug', 'plant', 'vase', 'candle', 'vacuum', 'fan', 'heater', 'blender',
    'baby', 'kids', 'toy', 'stroller', 'crib',
    'pet', 'dog', 'cat', 'carrier', 'crate',
    'bike', 'bicycle', 'fitness', 'dumbbell', 'weights', 'yoga', 'book', 'art', 'painting'
]

harvested_items = {}

print("Harvesting from Karrot US...")
# 1. Main listing
try:
    req = urllib.request.Request('https://us.karrotmarket.com/buy-sell/', headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        ctx = extract_remix_context(resp.read().decode('utf-8'))
        routes = ctx.get('state', {}).get('loaderData', {}) if ctx else {}
        for k, v in routes.items():
            if isinstance(v, dict) and 'articles' in v:
                for a in v.get('articles', []):
                    if a.get('thumbnail') and a.get('nodeId'):
                        harvested_items[a['nodeId']] = a
except Exception as e:
    print('Main page error:', e)

print(f"Main page: {len(harvested_items)} items")

# 2. Search queries
for kw in search_keywords:
    if len(harvested_items) >= 550:
        break
    url = f"https://us.karrotmarket.com/buy-sell/all/?search={kw}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            ctx = extract_remix_context(resp.read().decode('utf-8'))
            routes = ctx.get('state', {}).get('loaderData', {}) if ctx else {}
            for k, v in routes.items():
                if isinstance(v, dict) and 'articles' in v:
                    for a in v.get('articles', []):
                        if a.get('thumbnail') and a.get('nodeId'):
                            harvested_items[a['nodeId']] = a
        print(f"  Keyword '{kw}': total collected so far = {len(harvested_items)}")
    except Exception as e:
        print(f"  Error on '{kw}':", e)
    time.sleep(0.15)

print(f"\n✅ Total unique Karrot articles harvested: {len(harvested_items)}")

# Convert to Moonoh Marketplace item format
final_karrot_items = []
now_ms = int(datetime.datetime.now().timestamp() * 1000)

for idx, (node_id, a) in enumerate(harvested_items.items()):
    title = a.get('title', 'Item').strip()
    price_str = str(a.get('price', '0')).replace('$', '').replace(',', '').strip()
    try: price = float(price_str)
    except: price = 0.0
    
    img_url = a.get('thumbnail', '')
    if not img_url or not img_url.startswith('http'):
        continue
    
    display_loc = a.get('displayLocationName', 'Manhattan, NY')
    town_name, lat, lng = standardize_location(display_loc)
    category = infer_category(title)
    item_id = f"karrot-{node_id}"
    
    slug = make_slug(title, town_name, item_id)
    posted_at = now_ms - (idx * 300000 + 60000) # Distributed recent timestamps
    
    karrot_obj = {
        "id": item_id,
        "no": item_id,
        "title": title,
        "price": price,
        "location": town_name,
        "rawTown": display_loc,
        "townName": town_name,
        "lat": lat,
        "lng": lng,
        "image": img_url,
        "photo": img_url,
        "category": category,
        "categoryName": category,
        "url": slug,
        "detailUrl": slug,
        "canonical_url": f"https://moon-oh.com{slug}",
        "source": "karrot",
        "badgeName": "Karrot",
        "external_url": f"https://us.karrotmarket.com/articles/{a.get('id') or node_id}",
        "sellerName": "Karrot Neighbor",
        "description": f"Verified secondhand listing: {title}. Originally posted by a local neighbor in {display_loc} on Karrot. Discover and browse neighborhood secondhand deals on Moonoh.",
        "postedAt": posted_at,
        "status": "ongoing"
    }
    final_karrot_items.append(karrot_obj)
    if len(final_karrot_items) >= 500:
        break

print(f"✅ Formatted {len(final_karrot_items)} top Karrot items for NY/NJ area")

# Save to scraped_karrot_500.json
with open('scraped_karrot_500.json', 'w', encoding='utf-8') as f:
    json.dump(final_karrot_items, f, ensure_ascii=False, indent=2)
print("Saved scraped_karrot_500.json")
