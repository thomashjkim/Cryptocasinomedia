import json

print("=" * 80)
print("📍 UPDATING LOCAL SHOPS EXACT PHYSICAL ADDRESSES, MAP COORDS & REGIONS")
print("=" * 80)

# Exact verified shop metadata
SHOPS_METADATA = {
    "sey-coffee": {
        "name": "SEY Coffee",
        "region": "Brooklyn, NY",
        "neighborhood": "Bushwick",
        "address": "18 Grattan St, Brooklyn, NY 11206",
        "city": "Brooklyn",
        "state": "NY",
        "zip": "11206",
        "lat": 40.7051,
        "lng": -73.9324,
        "theme_color": "#111827",
        "category": "Coffee & Pantry"
    },
    "front-general-store": {
        "name": "Front General Store",
        "region": "Brooklyn, NY",
        "neighborhood": "DUMBO",
        "address": "143 Front St, Brooklyn, NY 11201",
        "city": "Brooklyn",
        "state": "NY",
        "zip": "11201",
        "lat": 40.7025,
        "lng": -73.9877,
        "theme_color": "#2C3E50",
        "category": "Vintage & Fashion"
    },
    "mirth-vintage": {
        "name": "Mirth Vintage",
        "region": "Brooklyn, NY",
        "neighborhood": "Greenpoint",
        "address": "603 Manhattan Ave, Brooklyn, NY 11222",
        "city": "Brooklyn",
        "state": "NY",
        "zip": "11222",
        "lat": 40.7246,
        "lng": -73.9514,
        "theme_color": "#000000",
        "category": "Vintage & Fashion"
    },
    "salter-house": {
        "name": "Salter House",
        "region": "Brooklyn, NY",
        "neighborhood": "Brooklyn Heights",
        "address": "119 Atlantic Ave, Brooklyn, NY 11201",
        "city": "Brooklyn",
        "state": "NY",
        "zip": "11201",
        "lat": 40.6917,
        "lng": -73.9972,
        "theme_color": "#007A4B",
        "category": "Home & Objects"
    },
    "big-night": {
        "name": "Big Night",
        "region": "Brooklyn, NY",
        "neighborhood": "Greenpoint",
        "address": "154 Franklin St, Brooklyn, NY 11222",
        "city": "Brooklyn",
        "state": "NY",
        "zip": "11222",
        "lat": 40.7297,
        "lng": -73.9582,
        "theme_color": "#F63616",
        "category": "Home & Objects"
    },
    "happier-grocery": {
        "name": "Happier Grocery",
        "region": "Manhattan, NY",
        "neighborhood": "SoHo",
        "address": "365 Canal St, New York, NY 10013",
        "city": "New York",
        "state": "NY",
        "zip": "10013",
        "lat": 40.7208,
        "lng": -74.0042,
        "theme_color": "#1DAA4A",
        "category": "Coffee & Pantry"
    },
    "pop-up-grocer": {
        "name": "Pop Up Grocer",
        "region": "Manhattan, NY",
        "neighborhood": "Greenwich Village",
        "address": "205 Bleecker St, New York, NY 10012",
        "city": "New York",
        "state": "NY",
        "zip": "10012",
        "lat": 40.7291,
        "lng": -74.0016,
        "theme_color": "#005CFF",
        "category": "Coffee & Pantry"
    }
}

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

# Update shops dict
for s_id, s_meta in SHOPS_METADATA.items():
    if s_id in local_db.get('shops', {}):
        s = local_db['shops'][s_id]
        s['name'] = s_meta['name']
        s['region'] = s_meta['region']
        s['neighborhood'] = s_meta['neighborhood']
        s['address_line_1'] = s_meta['address']
        s['city'] = s_meta['city']
        s['state'] = s_meta['state']
        s['postal_code'] = s_meta['zip']
        s['theme_color'] = s_meta['theme_color']
        s['lat'] = s_meta['lat']
        s['lng'] = s_meta['lng']

# Update all 900 products
for p in local_db.get('products', []):
    s_id = p.get('shop_id')
    if s_id in SHOPS_METADATA:
        meta = SHOPS_METADATA[s_id]
        p['location'] = meta['region']
        p['rawTown'] = meta['region']
        p['townName'] = meta['region']
        p['location_neighborhood'] = f"{meta['neighborhood']}, {meta['region']}"
        p['store_city'] = meta['city']
        p['store_state'] = meta['state']
        p['verified_physical_location'] = meta['address']
        p['lat'] = meta['lat']
        p['lng'] = meta['lng']
        p['theme_color'] = meta['theme_color']

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(local_db, f, indent=2, ensure_ascii=False)

print("✅ Updated local_shops_data.json with exact physical addresses and standardized regions (Brooklyn, NY / Manhattan, NY)")
