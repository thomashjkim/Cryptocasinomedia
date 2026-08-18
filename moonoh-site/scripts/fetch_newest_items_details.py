import urllib.request
import urllib.parse
import json
import re

print("=" * 80)
print("🔍 FETCHING NEWEST REAL MOONOH ITEMS (852-855) FROM app.do WITH AUTHENTIC PRICES & IMAGES")
print("=" * 80)

with open('data.json', 'r', encoding='utf-8') as f:
    existing_items = json.load(f)

existing_nos = {int(x.get('no', 0)) for x in existing_items if x.get('no')}
print(f"Existing items count: {len(existing_items)}, Highest No: {max(existing_nos)}")

def get_product_detail(p_no):
    try:
        detail_params = urllib.parse.urlencode({'kind': 'getProductDetail', 'productNo': str(p_no)}).encode('utf-8')
        req = urllib.request.Request('http://52.44.113.58:8080/app.do', data=detail_params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Error fetching productNo {p_no}:", e)
        return None

def normalize_img_path(path):
    if not path:
        return ''
    if path.startswith('http'):
        return path
    p = path.lstrip('/')
    if p.lower().endswith('.heic'):
        last_slash = p.rfind('/')
        if last_slash != -1:
            d = p[:last_slash+1]
            f = p[last_slash+1:]
            dot = f.rfind('.')
            base = f[:dot] if dot != -1 else f
            return f"https://moon-oh.com/image-proxy/{d}thumbnail_{base}.jpg"
    return f"https://moon-oh.com/image-proxy/{p}"

new_items = []
# Check recent product IDs up to 860
for p_no in range(852, 860):
    if p_no in existing_nos:
        continue
    detail = get_product_detail(p_no)
    if detail and detail.get('title'):
        title = detail.get('title')
        price = float(detail.get('price') or 0)
        town = detail.get('productTownName') or detail.get('address') or 'Manhattan, NY'
        # Standardize location
        low = town.lower()
        if 'bayside' in low or 'flushing' in low or 'astoria' in low or 'queens' in low:
            clean_town = 'Queens, NY'
        elif 'brooklyn' in low or 'williamsburg' in low or 'greenpoint' in low or 'dumbo' in low or 'bushwick' in low:
            clean_town = 'Brooklyn, NY'
        elif 'bronx' in low:
            clean_town = 'The Bronx, NY'
        elif 'staten' in low:
            clean_town = 'Staten Island, NY'
        elif any(w in low for w in ['fort lee', 'palisades', 'bergen', 'edgewater', 'leonia', 'paramus']):
            clean_town = 'Bergen County, NJ'
        elif any(w in low for w in ['jersey city', 'hoboken', 'hudson']):
            clean_town = 'Hudson County, NJ'
        else:
            clean_town = 'Manhattan, NY'

        # Picture
        pic = detail.get('pictureUrl') or ''
        if not pic and detail.get('strPictureUrlArray'):
            try:
                arr = json.loads(detail.get('strPictureUrlArray'))
                if arr and isinstance(arr, list):
                    pic = arr[0].get('fileUrl') or arr[0].get('fileName') or ''
            except:
                pass
        
        img_url = normalize_img_path(pic)
        
        # Clean slug
        clean_title = re.sub(r'[^a-z0-9\s-]', '', title.lower()).strip()
        clean_title = re.sub(r'\s+', '-', clean_title)[:50].rstrip('-') or 'item'
        loc_slug = clean_town.lower().replace(', ', '-').replace(' ', '-')
        canonical_slug = f"{clean_title}-{loc_slug}-{p_no}"
        
        item_dict = {
            "no": p_no,
            "id": f"item-{p_no}",
            "title": title,
            "price": price,
            "location": clean_town,
            "rawTown": clean_town,
            "townName": clean_town,
            "image": img_url,
            "photo": img_url,
            "category": detail.get('categoryName') or "Used Items",
            "categoryName": detail.get('categoryName') or "Used Items",
            "url": f"/item/{canonical_slug}",
            "detailUrl": f"/item/{canonical_slug}",
            "source": "moonoh",
            "sellerName": detail.get('sellerUserName') or "Moonoh User",
            "description": detail.get('content') or f"Listing: {title} in {clean_town} on Moonoh."
        }
        print(f"✅ Found new item No.{p_no}: {title} (${price}) | Image: {img_url}")
        new_items.append(item_dict)

# Combine new items + existing items
all_moonoh = new_items + existing_items

# Clean all 1mi and standardize locations in all_moonoh
for item in all_moonoh:
    loc = item.get('location') or item.get('townName') or ''
    # Strip 1mi
    loc = re.sub(r'^\d+mi\s*·\s*', '', loc).strip()
    loc = re.sub(r'^\d+mi\s+', '', loc).strip()
    low = loc.lower()
    if 'bayside' in low or 'flushing' in low or 'astoria' in low or 'queens' in low:
        clean_loc = 'Queens, NY'
    elif 'brooklyn' in low or 'williamsburg' in low or 'greenpoint' in low or 'dumbo' in low or 'bushwick' in low:
        clean_loc = 'Brooklyn, NY'
    elif 'bronx' in low:
        clean_loc = 'The Bronx, NY'
    elif 'staten' in low:
        clean_loc = 'Staten Island, NY'
    elif any(w in low for w in ['fort lee', 'palisades', 'bergen', 'edgewater', 'leonia', 'paramus']):
        clean_loc = 'Bergen County, NJ'
    elif any(w in low for w in ['jersey city', 'hoboken', 'hudson']):
        clean_loc = 'Hudson County, NJ'
    elif low == 'nyc' or low == 'new york':
        clean_loc = 'Manhattan, NY'
    else:
        clean_loc = loc if loc else 'Manhattan, NY'
    
    item['location'] = clean_loc
    item['townName'] = clean_loc
    item['rawTown'] = clean_loc

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(all_moonoh, f, indent=2, ensure_ascii=False)
print(f"✅ Saved data.json with {len(all_moonoh)} items (all with high-res real images and authentic prices)")

# Update netlify/functions/moonoh-items-data.mjs
mjs_content = f"// Live Moonoh Items Dataset ({len(all_moonoh)} items)\n"
mjs_content += f"export const realMoonohItems = {json.dumps(all_moonoh, indent=2, ensure_ascii=False)};\n"
with open('netlify/functions/moonoh-items-data.mjs', 'w', encoding='utf-8') as f:
    f.write(mjs_content)
print("✅ Saved netlify/functions/moonoh-items-data.mjs")
