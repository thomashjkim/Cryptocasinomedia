import urllib.request
import json
import re
import html
import os
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("=" * 80)
print("🚀 UPDATING TODAY'S FRESH KARROT & HEYKOREAN MARKETPLACE LISTINGS")
print("=" * 80)

# -------------------------------------------------------------------------
# 1. GEO-COORDINATE MAPPER
# -------------------------------------------------------------------------
def get_coordinates_and_standard_town(loc_str):
    if not loc_str:
        return 'Manhattan, NY', 40.7831, -73.9712
    l = str(loc_str).lower()
    if 'manhattan' in l or 'soho' in l or 'midtown' in l or 'tribeca' in l or 'new york' in l or 'ny, ny' in l or 'ny ny' in l:
        return 'Manhattan, NY', 40.7831, -73.9712
    if 'brooklyn' in l or 'williamsburg' in l or 'greenpoint' in l or 'dumbo' in l or 'bushwick' in l:
        return 'Brooklyn, NY', 40.6782, -73.9442
    if 'queens' in l or 'flushing' in l or 'bayside' in l or 'astoria' in l or 'lic' in l or 'long island city' in l:
        return 'Queens, NY', 40.7282, -73.7949
    if 'bronx' in l:
        return 'The Bronx, NY', 40.8448, -73.8648
    if 'staten island' in l:
        return 'Staten Island, NY', 40.5795, -74.1502
    if 'fort lee' in l or 'palisades' in l or 'bergen' in l or 'ridgefield' in l or 'closter' in l or 'englewood' in l or 'paramus' in l:
        return 'Bergen County, NJ', 40.8509, -73.9701
    if 'jersey city' in l or 'hoboken' in l or 'hudson' in l or 'newport' in l:
        return 'Hudson County, NJ', 40.7178, -74.0431
    if 'nassau' in l or 'great neck' in l or 'long island' in l:
        return 'Nassau County, NY', 40.7433, -73.5884
    if 'new jersey' in l or 'nj' in l:
        return 'Bergen County, NJ', 40.8509, -73.9701
    return 'Manhattan, NY', 40.7831, -73.9712

# -------------------------------------------------------------------------
# 2. TITLE CLEANER & TRANSLATOR
# -------------------------------------------------------------------------
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

# -------------------------------------------------------------------------
# 3. HARVEST KARROT LISTINGS
# -------------------------------------------------------------------------
print("\n[Step 1] Loading & Harvesting fresh Karrot listings...")
fresh_karrot_items = []
scraped_karrot_file = "scraped_karrot_raw.json"

if os.path.exists(scraped_karrot_file):
    try:
        with open(scraped_karrot_file, "r", encoding="utf-8") as f:
            raw_karrot_data = json.load(f)
            for a in raw_karrot_data:
                node_id = a.get('nodeId') or a.get('id')
                if not node_id: continue
                raw_title = a.get('title', '').strip()
                raw_price = a.get('price', 0)
                try: price = float(raw_price) if raw_price else 0.0
                except: price = 0.0
                
                photo_obj = a.get('photo', {})
                img_url = photo_obj.get('url') if isinstance(photo_obj, dict) else (str(photo_obj) if photo_obj else '')
                if not img_url: continue
                
                region = a.get('region', {})
                loc_name = region.get('name', 'Queens') if isinstance(region, dict) else 'Queens'
                town_name, lat, lng = get_coordinates_and_standard_town(loc_name)
                
                seller = a.get('user', {})
                seller_name = seller.get('nickname', 'Karrot Neighbor') if isinstance(seller, dict) else 'Karrot Neighbor'
                
                item_id = f"karrot-{node_id}"
                fresh_karrot_items.append({
                    'id': item_id,
                    'title': raw_title,
                    'price': price,
                    'location': town_name,
                    'rawTown': town_name,
                    'lat': lat,
                    'lng': lng,
                    'category': 'Used Items',
                    'image': img_url,
                    'photo': img_url,
                    'sellerName': seller_name,
                    'description': f"{raw_title} for sale in {town_name} on Karrot. Buy and sell locally with zero fees.",
                    'source': 'karrot',
                    'sourceName': 'Karrot',
                    'url': f"https://us.karrotmarket.com/buy-sell/{node_id}/",
                    'detailUrl': f"https://us.karrotmarket.com/buy-sell/{node_id}/",
                    'timeAgo': 'Community Listing'
                })
        print(f"✓ Loaded {len(fresh_karrot_items)} authentic Karrot items from scraped database")
    except Exception as e:
        print(f"Error loading scraped karrot: {e}")


# -------------------------------------------------------------------------
# 4. HARVEST TODAY'S HEYKOREAN LISTINGS
# -------------------------------------------------------------------------
print("\n[Step 2] Harvesting fresh HeyKorean listings...")
fresh_hk_items = []
for page in [1, 2, 3, 4, 5]:
    try:
        req_hk = urllib.request.Request(f'https://market.heykorean.com/api/market/list?page={page}&size=50', headers=headers)
        with urllib.request.urlopen(req_hk, timeout=12) as resp:
            hk_data = json.loads(resp.read().decode('utf-8'))
            raw_list = hk_data.get('list', [])
            for r in raw_list:
                raw_title = r.get('title', '').strip()
                if not raw_title or r.get('store_type') == 'B' or any(k in raw_title for k in ['우체국', '경매', 'HVAC', '상점 바로가기', 'CAR SALES', 'FORD', 'KIA', '설치', '구매대행', '정수기', '리스']):
                    continue
                
                main_img = r.get('main_image') or ''
                img_url = ''
                if main_img:
                    try:
                        img_obj = json.loads(main_img)
                        img_url = img_obj.get('large') or img_obj.get('medium') or img_obj.get('origin') or ''
                    except:
                        img_url = main_img
                if not img_url: continue
                
                eng_title = clean_and_translate_title(raw_title)
                area = r.get('area_name_en') or r.get('area_name') or 'New York, NY'
                cat = r.get('category_title_en') or r.get('category_title') or 'Used Items'
                
                # Raw price in HeyKorean API is cents (e.g. 1500 = $15.00)
                raw_price = float(r.get('price', 0))
                price = raw_price / 100.0 if raw_price >= 100 else raw_price
                
                town_name, lat, lng = get_coordinates_and_standard_town(area)
                item_id = f"heykorean-{r.get('id')}"
                
                fresh_hk_items.append({
                    'id': item_id,
                    'title': eng_title,
                    'price': price,
                    'location': town_name,
                    'rawTown': town_name,
                    'lat': lat,
                    'lng': lng,
                    'category': cat,
                    'image': img_url,
                    'photo': img_url,
                    'sellerName': 'HeyKorean Neighbor',
                    'description': f"{eng_title} listed in {town_name}. Verified community marketplace exchange on Moonoh.",
                    'source': 'heykorean',
                    'sourceName': 'HeyKorean',
                    'sourceUrl': f"https://market.heykorean.com/item/{r.get('id')}",
                    'url': f"https://market.heykorean.com/item/{r.get('id')}",
                    'detailUrl': f"https://market.heykorean.com/item/{r.get('id')}",
                    'timeAgo': 'Community Listing'
                })
    except Exception as e:
        print(f"  Error on page {page}: {e}")

print(f"✓ Built {len(fresh_hk_items)} validated fresh HeyKorean items for today")


# -------------------------------------------------------------------------
# 5. MERGE WITH EXISTING EXTERNAL ITEMS (DEDUPLICATE & UPDATE COORDINATES)
# -------------------------------------------------------------------------
print("\n[Step 3] Merging & Standardizing Coordinates across All External Items...")

with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    ext_mjs = f.read()

m_k = re.search(r'export const realKarrotItems = (\[[\s\S]*?\]);\n\nexport const realHeyKoreanItems', ext_mjs)
m_h = re.search(r'export const realHeyKoreanItems = (\[[\s\S]*?\]);', ext_mjs)

old_karrot = json.loads(m_k.group(1)) if m_k else []
old_hey = json.loads(m_h.group(1)) if m_h else []

# Merge Karrot
karrot_map = {}
for item in fresh_karrot_items:
    karrot_map[item['id']] = item

for item in old_karrot:
    iid = item.get('id')
    if iid not in karrot_map:
        town_name, lat, lng = get_coordinates_and_standard_town(item.get('location') or item.get('rawTown'))
        item['location'] = town_name
        item['rawTown'] = town_name
        item['lat'] = lat
        item['lng'] = lng
        item['timeAgo'] = 'Community Listing'
        karrot_map[iid] = item

merged_karrot = list(karrot_map.values())

# Merge HeyKorean
hey_map = {}
for item in fresh_hk_items:
    hey_map[item['id']] = item

for item in old_hey:
    iid = item.get('id')
    if iid not in hey_map:
        town_name, lat, lng = get_coordinates_and_standard_town(item.get('location') or item.get('rawTown'))
        item['location'] = town_name
        item['rawTown'] = town_name
        item['lat'] = lat
        item['lng'] = lng
        item['timeAgo'] = 'Community Listing'
        # Fix raw price if in cents
        raw_p = float(item.get('price', 0))
        if raw_p >= 1000 and raw_p % 100 == 0:
            item['price'] = raw_p / 100.0
        hey_map[iid] = item

merged_hey = list(hey_map.values())

print(f"✅ Total Merged Karrot Items: {len(merged_karrot)}")
print(f"✅ Total Merged HeyKorean Items: {len(merged_hey)}")

# Write updated external-items.mjs
new_ext_mjs = f'''// High-Performance Zero-Latency External Marketplaces (Karrot & HeyKorean) Dataset
export const realKarrotItems = {json.dumps(merged_karrot, indent=2)};

export const realHeyKoreanItems = {json.dumps(merged_hey, indent=2)};
'''

with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
    f.write(new_ext_mjs)

# Also update allRealExternalItems dictionary in item-detail.mjs using clean index slicing
all_ext_dict = {}
for it in (merged_karrot + merged_hey):
    all_ext_dict[it['id'].lower()] = it

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    item_detail_code = f.read()

start_marker = 'const allRealExternalItems = {'
end_marker = 'function getExternalItemById'

start_idx = item_detail_code.find(start_marker)
end_idx = item_detail_code.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_dict_code = f'const allRealExternalItems = {json.dumps(all_ext_dict, indent=2)};\n\n'
    item_detail_code = item_detail_code[:start_idx] + new_dict_code + item_detail_code[end_idx:]
    with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
        f.write(item_detail_code)
    print("✅ Updated netlify/functions/external-items.mjs and item-detail.mjs with 100% synchronized data")
else:
    print("❌ Could not find exact dictionary marker in item-detail.mjs")

# Re-run build sitemaps
print("\n[Step 4] Rebuilding XML Sitemaps for new listings...")
os.system("python3 build_all_sitemaps.py")
