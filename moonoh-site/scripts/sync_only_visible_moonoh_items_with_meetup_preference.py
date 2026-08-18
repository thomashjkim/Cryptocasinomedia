import urllib.request
import urllib.parse
import json
import re
import time

print("=" * 80)
print("🛡️ SYNCING ONLY VISIBLE (isShow == 'Y') MOONOH ITEMS WITH MEETUP PREFERENCE")
print("=" * 80)

# Step 1: Login to admin.do and get all products with isShow status
login_data = urllib.parse.urlencode({'kind': 'login', 'id': 'admin', 'password': '1234'}).encode('utf-8')
req_login = urllib.request.Request('http://52.44.113.58:8080/admin.do', data=login_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

with urllib.request.urlopen(req_login, timeout=10) as resp:
    cookie = resp.headers.get('Set-Cookie', '').split(';')[0]
    data_payload = urllib.parse.urlencode({'kind': 'getProductArray', 'page': '0', 'viewCount': '1000'}).encode('utf-8')
    req_data = urllib.request.Request('http://52.44.113.58:8080/admin.do', data=data_payload, headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie})
    with urllib.request.urlopen(req_data, timeout=15) as d_resp:
        res_json = json.loads(d_resp.read().decode('utf-8'))
        all_admin_prods = res_json.get('productArray', [])

print(f"Total admin products found: {len(all_admin_prods)}")

# Filter only isShow == 'Y' and not title.lower().startswith('test')
visible_admin_prods = [
    p for p in all_admin_prods 
    if p.get('isShow') == 'Y' and not p.get('title', '').strip().lower().startswith('test')
]
print(f"Visible products (isShow == 'Y'): {len(visible_admin_prods)}")

# Step 2: Helper for meetup location standardization
def standardize_meetup_location(meetup_town, meetup_address):
    combined = f"{meetup_town or ''} {meetup_address or ''}".lower()
    # Strip 1mi
    combined = re.sub(r'^\d+mi\s*·\s*', '', combined).strip()
    
    if any(w in combined for w in ['bayside', 'flushing', 'astoria', 'long island city', 'lic', 'queens', 'sunnyside', 'woodside', 'forest hills', 'elmhurst']):
        return 'Queens, NY'
    if any(w in combined for w in ['brooklyn', 'williamsburg', 'greenpoint', 'dumbo', 'bushwick', 'park slope', 'bedford', 'crown heights']):
        return 'Brooklyn, NY'
    if any(w in combined for w in ['bronx', 'fordham', 'riverdale', 'pelham']):
        return 'The Bronx, NY'
    if any(w in combined for w in ['staten island', 'st. george', 'todt hill']):
        return 'Staten Island, NY'
    if any(w in combined for w in ['fort lee', 'palisades', 'bergen', 'edgewater', 'leonia', 'paramus', 'englewood', 'hackensack', 'cliffside']):
        return 'Bergen County, NJ'
    if any(w in combined for w in ['jersey city', 'hoboken', 'weehawken', 'hudson', 'newport', 'journal square']):
        return 'Hudson County, NJ'
    if any(w in combined for w in ['manhattan', 'soho', 'tribeca', 'midtown', 'village', 'harlem', 'chelsea', 'upper east', 'upper west', 'new york']):
        return 'Manhattan, NY'
    
    return 'Manhattan, NY'

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

# Step 3: Fetch detail for each visible item
final_items = []
print("Fetching details for visible items...")

for idx, p in enumerate(visible_admin_prods):
    p_no = p.get('no')
    try:
        detail_params = urllib.parse.urlencode({'kind': 'getProductDetail', 'productNo': str(p_no)}).encode('utf-8')
        req = urllib.request.Request('http://52.44.113.58:8080/app.do', data=detail_params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {p_no}: {e}")
        continue
    
    if not d or not d.get('title'):
        continue
    
    # Double check isShow in app.do
    if d.get('isShow') != 'Y':
        print(f"Skipping hidden item {p_no} (isShow != Y in app.do)")
        continue
        
    title = d.get('title', '').strip()
    if title.lower().startswith('test'):
        continue
        
    price = float(d.get('price') or 0)
    
    # Meetup Preference Location!
    meetup_town = d.get('productTownName') or ''
    meetup_address = d.get('address') or ''
    standard_loc = standardize_meetup_location(meetup_town, meetup_address)
    
    # Picture
    pic = d.get('pictureUrl') or ''
    if not pic and d.get('strPictureUrlArray'):
        try:
            arr = json.loads(d.get('strPictureUrlArray'))
            if arr and isinstance(arr, list):
                pic = arr[0].get('fileUrl') or arr[0].get('fileName') or ''
        except:
            pass
    img_url = normalize_img_path(pic) or 'https://moon-oh.com/images/default-item-placeholder.png'
    
    # Clean slug
    clean_title = re.sub(r'[^a-z0-9\s-]', '', title.lower()).strip()
    clean_title = re.sub(r'\s+', '-', clean_title)[:50].rstrip('-') or 'item'
    loc_slug = standard_loc.lower().replace(', ', '-').replace(' ', '-')
    canonical_slug = f"{clean_title}-{loc_slug}-{p_no}"
    
    item_dict = {
        "no": int(p_no),
        "id": f"item-{p_no}",
        "title": title,
        "price": price,
        "location": standard_loc,
        "rawTown": standard_loc,
        "townName": standard_loc,
        "meetupAddress": meetup_address,
        "meetupTownName": meetup_town,
        "lat": float(d.get('productY') or 40.7128),
        "lng": float(d.get('productX') or -74.0060),
        "image": img_url,
        "photo": img_url,
        "category": d.get('categoryName') or "Used Items",
        "categoryName": d.get('categoryName') or "Used Items",
        "url": f"/item/{canonical_slug}",
        "detailUrl": f"/item/{canonical_slug}",
        "source": "moonoh",
        "sellerName": d.get('sellerUserName') or "Moonoh User",
        "description": d.get('content') or f"Listing: {title} in {standard_loc} on Moonoh.",
        "postedAt": int(time.time() * 1000) - idx * 60000
    }
    final_items.append(item_dict)

# Sort strictly by product number descending
final_items.sort(key=lambda x: x['no'], reverse=True)

print(f"\n✅ Total visible Moonoh items processed: {len(final_items)}")
print(f"   Highest No: {final_items[0]['no']} ({final_items[0]['title']} - ${final_items[0]['price']} in {final_items[0]['location']})")

# Save to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(final_items, f, indent=2, ensure_ascii=False)
print("✅ Saved data.json")

# Save to netlify/functions/moonoh-items-data.mjs
mjs_content = f"// Live Moonoh Items Dataset ({len(final_items)} visible items, isShow == 'Y', Meetup Preference location)\n"
mjs_content += f"export const realMoonohItems = {json.dumps(final_items, indent=2, ensure_ascii=False)};\n"
with open('netlify/functions/moonoh-items-data.mjs', 'w', encoding='utf-8') as f:
    f.write(mjs_content)
print("✅ Saved netlify/functions/moonoh-items-data.mjs")
