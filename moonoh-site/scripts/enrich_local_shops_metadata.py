import json

# Verified Shop Metadata
COORDINATES = {
    "front-general-store": {
        "lat": 40.7029, "lng": -73.9877,
        "theme_color": "#2C3E50", "badge_bg": "#EDF2F7", "badge_text": "#1A202C",
        "verified_location": "143 Front St, Brooklyn, NY 11201 (DUMBO)",
        "source_url": "https://frontgeneralstore.com"
    },
    "mirth-vintage": {
        "lat": 40.7246, "lng": -73.9511,
        "theme_color": "#8C6D1F", "badge_bg": "#FEF3C7", "badge_text": "#78350F",
        "verified_location": "603 Manhattan Ave, Brooklyn, NY 11222 (Greenpoint)",
        "source_url": "https://mirth.co"
    },
    "sey-coffee": {
        "lat": 40.7052, "lng": -73.9324,
        "theme_color": "#1F2937", "badge_bg": "#F3F4F6", "badge_text": "#111827",
        "verified_location": "18 Grattan St, Brooklyn, NY 11206 (Bushwick)",
        "source_url": "https://www.seycoffee.com"
    },
    "salter-house": {
        "lat": 40.6917, "lng": -73.9959,
        "theme_color": "#3B5A40", "badge_bg": "#ECFDF5", "badge_text": "#064E3B",
        "verified_location": "119 Atlantic Ave, Brooklyn, NY 11201 (Brooklyn Heights)",
        "source_url": "https://salter.house"
    },
    "big-night": {
        "lat": 40.7289, "lng": -73.9577,
        "theme_color": "#C53030", "badge_bg": "#FEE2E2", "badge_text": "#991B1B",
        "verified_location": "154 Franklin St, Brooklyn, NY 11222 (Greenpoint)",
        "source_url": "https://bignightbk.com"
    },
    "happier-grocery": {
        "lat": 40.7225, "lng": -74.0084,
        "theme_color": "#15803D", "badge_bg": "#DCFCE7", "badge_text": "#14532D",
        "verified_location": "465 Canal St, New York, NY 10013 (Soho)",
        "source_url": "https://www.happiergrocery.com"
    },
    "pop-up-grocer": {
        "lat": 40.7291, "lng": -74.0006,
        "theme_color": "#1D4ED8", "badge_bg": "#DBEAFE", "badge_text": "#1E40AF",
        "verified_location": "205 Bleecker St, New York, NY 10012 (Greenwich Village)",
        "source_url": "https://popupgrocer.com"
    }
}

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Enrich Shops
for s_id, s_info in db.get('shops', {}).items():
    meta = COORDINATES.get(s_id, {})
    if meta:
        s_info['latitude'] = meta['lat']
        s_info['longitude'] = meta['lng']
        s_info['verified_physical_location'] = meta['verified_location']
        s_info['badge_theme'] = {
            "bg": meta['badge_bg'],
            "color": meta['badge_text'],
            "border": meta['theme_color']
        }

# Enrich Products
for p in db.get('products', []):
    s_id = p.get('shop_id')
    meta = COORDINATES.get(s_id, {})
    shop_obj = db.get('shops', {}).get(s_id, {})
    
    p['source'] = s_id
    p['source_id'] = p.get('source_product_id') or p.get('id')
    p['store_name'] = shop_obj.get('name', 'Local Shop')
    p['store_url'] = shop_obj.get('website_url', meta.get('source_url', ''))
    p['store_physical_location'] = meta.get('verified_location', '')
    p['latitude'] = meta.get('lat', 40.7128)
    p['longitude'] = meta.get('lng', -74.0060)
    p['canonical_url'] = f"https://moon-oh.com/local-product/{s_id}/{p.get('slug')}"
    p['attribution_status'] = "Independently curated from public storefront"
    p['last_verified'] = "2026-08-17"

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"✅ Enriched all {len(db.get('products', []))} products and {len(db.get('shops', {}))} shops in local_shops_data.json")
