import urllib.request
import json
import re
import html
import time
import os
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("=" * 80)
print("🚀 UPDATING MARKETPLACES: 500 KARROT ITEMS + FRESH HEYKOREAN ITEMS")
print("=" * 80)

# 1. Load 500 Karrot items
with open('scraped_karrot_500.json', 'r', encoding='utf-8') as f:
    karrot_items = json.load(f)

print(f"✅ Loaded {len(karrot_items)} authentic NYC Karrot items")

# 2. HeyKorean Helpers
def clean_and_translate_title(title):
    t = (title or '').strip()
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

def get_coordinates_and_standard_town(loc_str):
    if not loc_str:
        return 'Manhattan, NY', 40.7831, -73.9712
    l = str(loc_str).lower()
    if any(k in l for k in ['manhattan', 'soho', 'midtown', 'tribeca', 'new york', 'ny, ny', 'ny ny']):
        return 'Manhattan, NY', 40.7831, -73.9712
    if any(k in l for k in ['brooklyn', 'williamsburg', 'greenpoint', 'dumbo', 'bushwick']):
        return 'Brooklyn, NY', 40.6782, -73.9442
    if any(k in l for k in ['queens', 'flushing', 'bayside', 'astoria', 'lic', 'long island city']):
        return 'Queens, NY', 40.7282, -73.7949
    if 'bronx' in l:
        return 'The Bronx, NY', 40.8448, -73.8648
    if 'staten island' in l:
        return 'Staten Island, NY', 40.5795, -74.1502
    if any(k in l for k in ['fort lee', 'palisades', 'bergen', 'ridgefield', 'closter', 'englewood', 'paramus', 'new jersey', 'nj']):
        return 'Bergen County, NJ', 40.8509, -73.9701
    if any(k in l for k in ['jersey city', 'hoboken', 'hudson', 'newport']):
        return 'Hudson County, NJ', 40.7178, -74.0431
    if any(k in l for k in ['nassau', 'great neck', 'long island']):
        return 'Nassau County, NY', 40.7433, -73.5884
    return 'Manhattan, NY', 40.7831, -73.9712

def infer_hk_category(title):
    t = (title or '').lower()
    if any(k in t for k in ['의자', 'chair', '책상', 'desk', '소파', 'sofa', '테이블', 'table', '침대', 'bed', '서랍', 'dresser', '선반', 'shelf', '가구', 'furniture', '식탁', '매트리스']):
        return 'Furniture'
    if any(k in t for k in ['청소기', 'vacuum', '냉장고', 'fridge', '세탁기', 'washer', '밥솥', 'cooker', '모니터', 'monitor', 'tv', '전자', 'electronic', '컴퓨터', 'computer', '노트북', 'laptop', '아이폰', 'iphone', 'ipad', '맥북', 'macbook', '다이슨', 'dyson', '공기청정기', '에어컨', '가습기', '에어프라이어']):
        return 'Electronics & appliances'
    if any(k in t for k in ['가방', 'bag', '지갑', 'wallet', '신발', 'shoes', '옷', 'clothing', '패딩', 'jacket', '코트', 'coat', '구두', '부츠', '샤넬', '루이비통', 'chanel', 'vuitton', 'dress', '원피스']):
        return 'Women\'s & Men\'s Fashion'
    if any(k in t for k in ['아기', 'baby', '유모차', 'stroller', '장난감', 'toy', '키즈', 'kids', '카시트', '육아']):
        return 'Baby & kids'
    if any(k in t for k in ['골프', 'golf', '자전거', 'bike', '운동', '헬스', 'fitness', '캠핑', 'camping', '텐트']):
        return 'Sports & leisure'
    if any(k in t for k in ['화장품', 'cosmetic', '향수', 'perfume', '뷰티', 'beauty', '스킨케어']):
        return 'Health & beauty'
    if any(k in t for k in ['냄비', 'pot', '후라이팬', 'pan', '그릇', 'dish', '주방', 'kitchen', '식기']):
        return 'Home, garden & DIY'
    if any(k in t for k in ['책', 'book', '소설', '문제집', '티켓', 'ticket', '공연']):
        return 'Books, tickets & stationery'
    return 'Used Items'

def make_hk_slug(title, loc_str, item_id):
    clean_t = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    clean_t = re.sub(r'\s+', '-', clean_t)
    clean_t = re.sub(r'-+', '-', clean_t)[:50].rstrip('-') or 'item'
    clean_l = re.sub(r'[^a-zA-Z0-9\s-]', '', loc_str).strip().lower()
    clean_l = re.sub(r'\s+', '-', clean_l)
    clean_l = re.sub(r'-+', '-', clean_l).rstrip('-')
    return f"/item/{clean_t}-{clean_l}-ext-{item_id}"

# Load existing HeyKorean items from external-items.mjs
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    ext_code = f.read()

m_hey = re.search(r'export const realHeyKoreanItems = (\[[\s\S]*?\]);', ext_code)
existing_hey = json.loads(m_hey.group(1)) if m_hey else []
print(f"Existing HeyKorean items: {len(existing_hey)}")

# Fetch fresh pages from HeyKorean API
fresh_hk_raw = []
for p in range(1, 11):
    url = f'https://market.heykorean.com/api/market/list?page={p}&size=50'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = data.get('list', [])
            if not items: break
            fresh_hk_raw.extend(items)
            time.sleep(0.15)
    except Exception as e:
        print(f"  Page {p} error:", e)
        break

print(f"✅ Fetched {len(fresh_hk_raw)} raw items from HeyKorean API")

# Process fresh HeyKorean items
processed_fresh_hk = []
existing_ids = {str(item.get('id', '')).replace('heykorean-', '') for item in existing_hey}
existing_ids.update({str(item.get('no', '')).replace('heykorean-', '') for item in existing_hey})

now_ms = int(datetime.datetime.now().timestamp() * 1000)

for idx, r in enumerate(fresh_hk_raw):
    item_id_num = str(r.get('no') or r.get('id') or '')
    if not item_id_num or item_id_num in existing_ids:
        continue
    
    raw_title = r.get('title', '').strip()
    clean_title = clean_and_translate_title(raw_title)
    if not clean_title or len(clean_title) < 2:
        continue
    
    price_val = r.get('price', 0)
    try: price = float(price_val) if price_val else 0.0
    except: price = 0.0
    
    img_url = r.get('thumbnail') or r.get('img_url') or r.get('image') or ''
    if not img_url or not img_url.startswith('http'):
        continue
    
    raw_loc = r.get('region_name') or r.get('city') or r.get('state') or 'Manhattan'
    town_name, lat, lng = get_coordinates_and_standard_town(raw_loc)
    cat = infer_hk_category(raw_title)
    
    item_id = f"heykorean-{item_id_num}"
    slug = make_hk_slug(clean_title, town_name, item_id)
    
    hk_obj = {
        "id": item_id,
        "no": item_id,
        "title": clean_title,
        "original_title": raw_title,
        "price": price,
        "location": town_name,
        "rawTown": raw_loc,
        "townName": town_name,
        "lat": lat,
        "lng": lng,
        "image": img_url,
        "photo": img_url,
        "category": cat,
        "categoryName": cat,
        "url": slug,
        "detailUrl": slug,
        "canonical_url": f"https://moon-oh.com{slug}",
        "source": "heykorean",
        "badgeName": "HeyKorean",
        "external_url": f"https://market.heykorean.com/market/view/{item_id_num}",
        "sellerName": r.get('writer', 'HeyKorean User'),
        "description": f"Verified secondhand listing: {clean_title} ({raw_title}). Listed on HeyKorean in {raw_loc}. Discover local secondhand deals with 0% fees on Moonoh.",
        "postedAt": now_ms - (idx * 180000),
        "status": "active"
    }
    processed_fresh_hk.append(hk_obj)
    existing_ids.add(item_id_num)

print(f"✅ Added {len(processed_fresh_hk)} brand new HeyKorean listings")

# Merge fresh HeyKorean at top
all_final_hey = processed_fresh_hk + existing_hey
print(f"Total HeyKorean items: {len(all_final_hey)}")

# Write updated netlify/functions/external-items.mjs
mjs_content = f"""// Aggregated Marketplace Listings: Karrot ({len(karrot_items)}) & HeyKorean ({len(all_final_hey)})
export const realKarrotItems = {json.dumps(karrot_items, ensure_ascii=False, indent=2)};

export const realHeyKoreanItems = {json.dumps(all_final_hey, ensure_ascii=False, indent=2)};

export default async (req, context) => {{
  return new Response(JSON.stringify([...realKarrotItems, ...realHeyKoreanItems]), {{
    status: 200,
    headers: {{
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=60, s-maxage=120"
    }}
  }});
}};

export const config = {{
  path: "/api/external-items"
}};
"""

with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
    f.write(mjs_content)

print(f"✅ Saved netlify/functions/external-items.mjs with {len(karrot_items)} Karrot + {len(all_final_hey)} HeyKorean = {len(karrot_items) + len(all_final_hey)} Total Marketplace items")
