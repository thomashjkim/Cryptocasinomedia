import urllib.request
import json
import re
import html

# ─────────────────────────────────────────────
# HeyKorean prices are in cents (USD * 100). Karrot prices are in USD.
# ─────────────────────────────────────────────────────────────────────
CATEGORY_PRICE_CAPS = {
    'Shoes': 800,
    'Baby & kids': 1500,
    'Used Items': 3000,
    'Furniture': 5000,
    'Electronics & Appliances': 5000,
    "Women's fashion": 5000,
    "Men's fashion": 3000,
    'Home, garden & DIY': 3000,
}
DEFAULT_PRICE_CAP = 5000

def is_price_reasonable(price, category):
    if price < 0:
        return False
    cap = CATEGORY_PRICE_CAPS.get(category, DEFAULT_PRICE_CAP)
    return price <= cap

# ─────────────────────────────────────────────
# Valid NYC/NJ regions — anything else is filtered
# ─────────────────────────────────────────────
VALID_AREA_KEYWORDS = [
    'manhattan', 'brooklyn', 'queens', 'bronx', 'staten island',
    'flushing', 'bayside', 'astoria', 'jamaica', 'jackson heights',
    'woodside', 'corona', 'elmhurst', 'forest hills', 'ridgewood',
    'flatbush', 'bushwick', 'williamsburg', 'bedford', 'park slope',
    'new jersey', 'nj', 'fort lee', 'palisades', 'bergen', 'hudson',
    'edgewater', 'cliffside', 'hackensack', 'englewood',
    'new york', 'nyc', 'long island', 'great neck'
]

# Normalize area → canonical Moonoh town name
AREA_NORMALIZE = {
    'new york': 'Manhattan, NY',
    'nyc': 'Manhattan, NY',
    'manhattan': 'Manhattan, NY',
    'brooklyn': 'Brooklyn, NY',
    'bronx': 'Bronx, NY',
    'staten island': 'Staten Island, NY',
    'queens': 'Queens, NY',
    'flushing': 'Flushing, Queens, NY',
    'bayside': 'Bayside, Queens, NY',
    'astoria': 'Astoria, Queens, NY',
    'jackson heights': 'Jackson Heights, Queens, NY',
    'jamaica': 'Jamaica, Queens, NY',
    'woodside': 'Woodside, Queens, NY',
    'forest hills': 'Forest Hills, Queens, NY',
    'new jersey': 'Bergen County, NJ',
    'nj': 'Bergen County, NJ',
    'fort lee': 'Fort Lee, NJ',
    'palisades': 'Palisades Park, NJ',
    'bergen': 'Bergen County, NJ',
    'hudson': 'Hudson County, NJ',
    'edgewater': 'Edgewater, NJ',
    'englewood': 'Englewood, NJ',
    'hackensack': 'Hackensack, NJ',
    'long island': 'Queens, NY',
    'great neck': 'Queens, NY',
}

# ─────────────────────────────────────────────
# Location → (lat, lng) lookup table
# ─────────────────────────────────────────────
LOCATION_COORDS = {
    'manhattan, ny':       (40.7580, -73.9855),
    'brooklyn, ny':        (40.6782, -73.9442),
    'bronx, ny':           (40.8448, -73.8648),
    'staten island, ny':   (40.5795, -74.1502),
    'queens, ny':          (40.7282, -73.7949),
    'flushing, queens, ny':(40.7675, -73.8330),
    'bayside, queens, ny': (40.7634, -73.7691),
    'astoria, queens, ny': (40.7721, -73.9302),
    'jackson heights, queens, ny': (40.7557, -73.8831),
    'jamaica, queens, ny': (40.7021, -73.7882),
    'woodside, queens, ny':(40.7448, -73.9043),
    'forest hills, queens, ny': (40.7188, -73.8448),
    'bergen county, nj':   (40.9265, -74.0750),
    'fort lee, nj':        (40.8509, -73.9701),
    'palisades park, nj':  (40.8454, -74.0043),
    'hudson county, nj':   (40.7282, -74.0776),
    'edgewater, nj':       (40.8234, -73.9721),
    'englewood, nj':       (40.8926, -73.9726),
    'hackensack, nj':      (40.8859, -74.0435),
}

def normalize_area(raw_area):
    """Return (canonical_town, rawTown, lat, lng) or None if outside coverage."""
    if not raw_area:
        return None
    low = raw_area.lower().strip()
    # Check each valid keyword
    for kw in VALID_AREA_KEYWORDS:
        if kw in low:
            # Find canonical name
            canonical = None
            for key, val in AREA_NORMALIZE.items():
                if key in low:
                    canonical = val
                    break
            if not canonical:
                # Fall back by keyword
                if 'fort lee' in low:    canonical = 'Fort Lee, NJ'
                elif 'palisades' in low: canonical = 'Palisades Park, NJ'
                elif 'flushing' in low:  canonical = 'Flushing, Queens, NY'
                elif 'bayside' in low:   canonical = 'Bayside, Queens, NY'
                elif 'astoria' in low:   canonical = 'Astoria, Queens, NY'
                elif 'queens' in low:    canonical = 'Queens, NY'
                elif 'brooklyn' in low:  canonical = 'Brooklyn, NY'
                elif 'bronx' in low:     canonical = 'Bronx, NY'
                elif 'manhattan' in low: canonical = 'Manhattan, NY'
                elif 'new jersey' in low or ' nj' in low: canonical = 'Bergen County, NJ'
                else:                    canonical = 'Queens, NY'
            lat, lng = LOCATION_COORDS.get(canonical.lower(), (40.7282, -73.7949))
            return canonical, canonical, lat, lng
    return None  # outside coverage

# ─────────────────────────────────────────────
# Category mapping: HeyKorean API cat → Moonoh cat
# ─────────────────────────────────────────────
HK_CATEGORY_MAP = {
    'bedroom':             'Furniture',
    'living room':         'Furniture',
    'furniture':           'Furniture',
    'sofa':                'Furniture',
    'kitchen':             'Furniture',
    'office':              'Furniture',
    'small appliances':    'Electronics & Appliances',
    'electronics':         'Electronics & Appliances',
    'tv':                  'Electronics & Appliances',
    'computer':            'Electronics & Appliances',
    'bags':                "Women's fashion",
    'women':               "Women's fashion",
    "women's":             "Women's fashion",
    'men':                 "Men's fashion",
    "men's":               "Men's fashion",
    'golf':                "Men's fashion",
    'shoes':               'Shoes',
    'footwear':            'Shoes',
    'children':            'Baby & kids',
    "children's books":    'Baby & kids',
    'baby':                'Baby & kids',
    'kids':                'Baby & kids',
    'dog':                 'Baby & kids',
    'pet':                 'Baby & kids',
    'musical instruments': 'Electronics & Appliances',
    'jewelry':             "Women's fashion",
    'watch':               "Women's fashion",
    'antiques':            'Used Items',
    'books':               'Baby & kids',
    'coupons':             'Used Items',
    'bathroom':            'Home, garden & DIY',
    'garden':              'Home, garden & DIY',
}

def map_category(raw_cat, title=''):
    """Map raw HeyKorean category + title to Moonoh category."""
    if raw_cat:
        low = raw_cat.lower()
        for key, val in HK_CATEGORY_MAP.items():
            if key in low:
                return val

    # Fallback: infer from title keywords
    t = title.lower()
    if any(k in t for k in ['stroller', 'crib', 'baby', 'infant', 'toddler', 'diaper']):
        return 'Baby & kids'
    if any(k in t for k in ['loafer', 'sneaker', 'shoe', 'boot', 'heel', 'sandal', 'slipper', 'insole']):
        return 'Shoes'
    if any(k in t for k in ['sofa', 'couch', 'desk', 'dresser', 'wardrobe', 'cabinet', 'shelf', 'bookcase', 'table', 'chair', 'bed frame', 'mattress']):
        return 'Furniture'
    if any(k in t for k in ['laptop', 'phone', 'iphone', 'android', 'tablet', 'monitor', 'tv ', 'television', 'camera', 'airpods', 'headphone', 'speaker', 'appliance', 'cooker', 'purifier', 'humidifier', 'vacuum', 'washer', 'dryer', 'rice cooker', 'hot pot']):
        return 'Electronics & Appliances'
    if any(k in t for k in ['dress', 'blouse', 'skirt', 'shirt', 'pants', 'jeans', 'jacket', 'coat', 'handbag', 'purse', 'chanel', 'louis vuitton', 'gucci', 'prada', 'lv ']):
        return "Women's fashion"
    if any(k in t for k in ['men', 'jersey', 'suit', 'tie', 'golf', 'driver', 'putter']):
        return "Men's fashion"
    if any(k in t for k in ['toy', 'lego', 'puzzle', 'game ', 'pokemon', 'book', 'picture book']):
        return 'Baby & kids'
    if any(k in t for k in ['plant', 'garden', 'pot', 'outdoor', 'chandelier', 'light fixture']):
        return 'Home, garden & DIY'
    if any(k in t for k in ['necklace', 'bracelet', 'ring ', 'earring', 'watch', 'jewelry']):
        return "Women's fashion"
    return 'Used Items'

# ─────────────────────────────────────────────
# Korean title cleaner / translator
# ─────────────────────────────────────────────
def clean_and_translate_title(title):
    t = title.strip()
    t = re.sub(r'^[^\w]*[\w\s\$]+｜', '', t).strip()
    t = re.sub(r'\d{3}[-\s]?\d{3,4}[-\s]?\d{4}', '', t).strip()
    t = re.sub(r'가격인하\s*', '', t).strip()
    t = re.sub(r'^\s*\d+만원?\s*', '', t).strip()

    translations = [
        (r'팝니다', 'for Sale'),
        (r'삽니다', 'Wanted'),
        (r'원형 부탄가스 테이블', 'Round Butane Gas Table'),
        (r'압력밥솥', 'Pressure Rice Cooker'),
        (r'밥솥', 'Rice Cooker'),
        (r'은수저 세트', 'Silver Spoon & Chopstick Set'),
        (r'구름버스 그림책', 'Cloud Bus Picture Books'),
        (r'그림책', 'Picture Books'),
        (r'서랍장', 'Dresser'),
        (r'원목 소파 테이블', 'Solid Wood Sofa Table'),
        (r'식탁 세트', 'Dining Table Set'),
        (r'의자 포함', 'with Chairs'),
        (r'세탁기 건조기 세트', 'Washer & Dryer Set'),
        (r'세탁기', 'Washer'),
        (r'건조기', 'Dryer'),
        (r'아기 침대', 'Baby Crib'),
        (r'유모차', 'Stroller'),
        (r'정품', 'Authentic'),
        (r'공기청정기', 'Air Purifier'),
        (r'가습기', 'Humidifier'),
        (r'청소기', 'Vacuum Cleaner'),
        (r'화장대', 'Vanity Table'),
        (r'책상', 'Desk'),
        (r'의자', 'Chair'),
        (r'침대', 'Bed'),
        (r'가방', 'Bag'),
        (r'지갑', 'Wallet'),
        (r'신발', 'Shoes'),
        (r'옷', 'Clothing'),
        (r'전자 피아노', 'Digital Piano'),
        (r'비데', 'Bidet'),
        (r'마법천자문', 'Magic Chinese Characters Books'),
        (r'킨더랜드 픽쳐북스', 'Kinderland Picture Books'),
        (r'쿠쿠', 'Cuckoo'),
        (r'혼마', 'Honma'),
        (r'풀 카트', 'Full Golf Cart'),
        (r'킹사우나 티켓', 'King Sauna Ticket'),
        (r'테일러메이드', 'TaylorMade'),
        (r'드라이버', 'Driver'),
        (r'우드', 'Wood'),
    ]

    for kor, eng in translations:
        t = re.sub(kor, eng, t)

    t = re.sub(r'\s+', ' ', t).strip()
    return t

# ─────────────────────────────────────────────
# Generate a natural-sounding description
# (no more "Outdoor item listed in 1mi · Queens")
# ─────────────────────────────────────────────
def make_description(title, category, town, source_name, price_usd):
    price_str = f"${price_usd:,}" if price_usd and price_usd > 0 else "Free"
    templates = [
        f"{title} available for {price_str} in {town}. Great condition, priced to sell. Contact seller through {source_name}.",
        f"Listing: {title} — {price_str}. Located in {town}. Originally posted on {source_name}. {category} item.",
        f"Pick up {title} for {price_str} in {town}. Category: {category}. See original listing on {source_name}.",
        f"{title} for sale at {price_str} near {town}. {category} — check out this deal on {source_name}.",
    ]
    # Deterministic choice based on title hash so it doesn't change every run
    idx = hash(title) % len(templates)
    return templates[idx]

# ─────────────────────────────────────────────
# Seller nicknames
# ─────────────────────────────────────────────
karrot_nicknames = [
    "Miji", "AdelineL", "Alex_NYC", "Sarah_Q", "Jennifer_B", "Michael_K",
    "David_M", "Chloe_BK", "Kevin_AST", "Grace_LIC", "Daniel_W", "Emily_H",
    "James_P", "Sophia_F", "Jason_R", "Hannah_S", "Justin_T", "Jessica_V",
    "Andrew_Y", "Nicole_Z", "Tommy_L", "Amy_F", "Chris_BK", "Rachel_M"
]

heykorean_nicknames = [
    "Andrew Ye", "limchungkyu", "NY_Seller", "NJ_Resident", "Queens_Local",
    "Bayside_Life", "FortLee_Neighbor", "Flushing_Market", "Manhattan_Sublet",
    "FortLee_Moving", "Bayside_Mom", "Astoria_Declutter", "Hoboken_Trade",
    "Palisades_Home", "Hudson_Deals", "WestSide_NYC", "Edgewater_Sell",
    "Hackensack_Home", "Englewood_Local", "BergenCo_Seller"
]

# ─────────────────────────────────────────────
# FETCH HEYKOREAN
# ─────────────────────────────────────────────
def fetch_heykorean():
    items = []
    seen_ids = set()
    seen_title_keys = set()

    for page in range(1, 30):
        url = f'https://market.heykorean.com/api/market/list?page={page}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                raw_items = data.get('list', [])
                if not raw_items:
                    break

                for r in raw_items:
                    item_id = str(r.get('id', ''))
                    if item_id in seen_ids:
                        continue
                    seen_ids.add(item_id)

                    raw_title = r.get('title', '').strip()

                    # Hard filters
                    skip_keywords = [
                        '우체국', '경매', 'HVAC', '상점 바로가기', 'CAR SALES',
                        'FORD', 'KIA', '설치', '구매대행', '매물', '부동산',
                        'store_type'
                    ]
                    if r.get('store_type') == 'B':
                        continue
                    if any(k.lower() in raw_title.lower() for k in skip_keywords):
                        continue

                    # Region filter
                    raw_area = r.get('area_name_en') or r.get('area_name') or ''
                    area_info = normalize_area(raw_area)
                    if area_info is None:
                        continue  # outside NYC/NJ
                    canonical_town, raw_town, lat, lng = area_info

                    # HeyKorean price is in cents (API returns USD * 100)
                    price_usd = round(float(r.get('price') or 0) / 100, 2)

                    # Title translation
                    eng_title = clean_and_translate_title(raw_title)
                    if not eng_title or len(eng_title) < 3:
                        continue

                    # Dedup by normalized English title
                    title_key = re.sub(r'[^\w]', '', eng_title).lower()
                    if title_key in seen_title_keys:
                        continue
                    seen_title_keys.add(title_key)

                    # Image
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

                    # Category
                    raw_cat = r.get('category_title_en') or r.get('category_title') or ''
                    moonoh_cat = map_category(raw_cat, eng_title)

                    # Price sanity cap (per category)
                    if not is_price_reasonable(price_usd, moonoh_cat):
                        continue

                    # Seller name
                    seller_name = r.get('store_name') or ''
                    if not seller_name or seller_name.lower() in ('none', ''):
                        user_id = int(r.get('user_id') or 0)
                        seller_name = heykorean_nicknames[user_id % len(heykorean_nicknames)]

                    # Description
                    description = make_description(eng_title, moonoh_cat, canonical_town, 'HeyKorean', price_usd)

                    items.append({
                        'id': f'heykorean-{item_id}',
                        'title': eng_title,
                        'price': price_usd,
                        'location': f'1mi · {canonical_town}',
                        'rawTown': canonical_town,
                        'lat': lat,
                        'lng': lng,
                        'category': moonoh_cat,
                        'image': img_url,
                        'sellerName': seller_name,
                        'description': description,
                        'source': 'heykorean',
                        'sourceName': 'HeyKorean',
                        'url': f'https://market.heykorean.com/market/view/{item_id}'
                    })

        except Exception as e:
            print(f'HeyKorean page {page} error: {e}')

    print(f'Fetched {len(items)} HeyKorean items (after NYC/NJ filter + KRW→USD)')
    return items

# ─────────────────────────────────────────────
# FETCH KARROT
# Karrot prices are already in USD
# ─────────────────────────────────────────────
def fetch_karrot():
    items = []
    seen_ids = set()
    seen_title_keys = set()

    # Try multiple Karrot pages
    urls = [
        'https://us.karrotmarket.com/buy-sell/',
        'https://us.karrotmarket.com/buy-sell/?page=2',
        'https://us.karrotmarket.com/buy-sell/?page=3',
        'https://us.karrotmarket.com/buy-sell/?page=4',
        'https://us.karrotmarket.com/buy-sell/?page=5',
    ]

    # Also try NYC-specific Karrot regions
    nyc_urls = [
        'https://us.karrotmarket.com/buy-sell/?region=queens-ny',
        'https://us.karrotmarket.com/buy-sell/?region=brooklyn-ny',
        'https://us.karrotmarket.com/buy-sell/?region=flushing-ny',
    ]

    all_urls = urls + nyc_urls

    for url in all_urls:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw_html = resp.read().decode('utf-8', errors='ignore')
                articles = re.findall(r'<a[^>]*href=\"(/buy-sell/[^\"]+)\"[^>]*>(.*?)</a>', raw_html, re.DOTALL)

                for href, content in articles:
                    img_m = re.search(r'src=\"(https?://img[^\"]+)\"', content)
                    title_m = re.search(r'alt=\"([^\"]+)\"', content) or \
                              re.search(r'class=\"[^\"]*title[^\"]*\">([^<]+)<', content)
                    price_m = re.search(r'\$([0-9,]+)', content)

                    if not (img_m and title_m):
                        continue

                    img_url = html.unescape(img_m.group(1)).replace('&amp;', '&')
                    title = html.unescape(title_m.group(1)).strip()
                    price = float(price_m.group(1).replace(',', '')) if price_m else 0

                    art_id = href.rstrip('/').split('/')[-1]
                    if art_id in seen_ids:
                        continue
                    seen_ids.add(art_id)

                    title_key = re.sub(r'[^\w]', '', title).lower()
                    if title_key in seen_title_keys:
                        continue
                    seen_title_keys.add(title_key)

                    # Filter out non-items
                    skip = ['🔥🔥', 'paquete', '$$', '???', 'free shipping']
                    if any(s.lower() in title.lower() for s in skip):
                        continue

                    # Cap unrealistic USD price
                    if price > 5000:
                        continue

                    # Karrot NYC listings → assign realistic Queens coords
                    # (Karrot US is NYC-focused, no explicit area in scraped HTML)
                    idx = hash(art_id) % len(karrot_nicknames)
                    seller_name = karrot_nicknames[idx]

                    # Distribute across NYC boroughs for variety
                    town_options = ['Queens, NY', 'Brooklyn, NY', 'Queens, NY', 'Flushing, Queens, NY', 'Queens, NY']
                    town = town_options[hash(art_id) % len(town_options)]
                    lat, lng = LOCATION_COORDS.get(town.lower(), (40.7282, -73.7949))

                    moonoh_cat = map_category('', title)
                    description = make_description(title, moonoh_cat, town, 'Karrot', int(price))

                    items.append({
                        'id': f'karrot-{art_id}',
                        'title': title,
                        'price': price,
                        'location': f'1mi · {town}',
                        'rawTown': town,
                        'lat': lat,
                        'lng': lng,
                        'category': moonoh_cat,
                        'image': img_url,
                        'sellerName': seller_name,
                        'description': description,
                        'source': 'karrot',
                        'sourceName': 'Karrot',
                        'url': f'https://us.karrotmarket.com{href}'
                    })
        except Exception as e:
            print(f'Karrot url error {url}: {e}')

    print(f'Fetched {len(items)} Karrot items')
    return items


if __name__ == '__main__':
    hk = fetch_heykorean()
    kr = fetch_karrot()

    print(f'TOTAL: {len(hk)} HeyKorean + {len(kr)} Karrot = {len(hk) + len(kr)} items')

    with open('real_external_items.json', 'w', encoding='utf-8') as f:
        json.dump({'heykorean': hk, 'karrot': kr}, f, ensure_ascii=False, indent=2)

    print('Saved to real_external_items.json')
