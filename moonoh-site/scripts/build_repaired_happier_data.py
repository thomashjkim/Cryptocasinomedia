import json
import re
import urllib.parse
import urllib.request

# 1. Load clean parsed products
with open('scripts/happier_clean_parsed.json', 'r', encoding='utf-8') as f:
    parsed = json.load(f)

# Also add sample product 69f4b7f336470545e58ee629 (Lasso Watermelon Lime Gelatin Cups)
sample_prod = {
    'id': '69f4b7f336470545e58ee629',
    'title': 'Lasso Watermelon Lime Gelatin Cups',
    'brand': 'Lasso',
    'price': 5.34,
    'package_size': 'Standard',
    'url': 'https://shop.happiergrocery.com/product/69f4b7f336470545e58ee629',
    'image_url': 'https://d38cu1l1jdjf8r.cloudfront.net/eyJidWNrZXQiOiJqYWxkaXByb2R1Y3RpbWFnZWJ1Y2tldCIsImtleSI6InZmdC04MTAyMTcxMzAwNDUtMTc4Njc0NjQ3NDIxMS5wbmciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjUwMCwiaGVpZ2h0Ijo1MDAsImZpdCI6ImNvbnRhaW4iLCJiYWNrZ3JvdW5kIjp7InIiOjIzNCwiZyI6MjM2LCJiIjoyMzEsImFscGhhIjowfX0sImZsYXR0ZW4iOnsiYmFja2dyb3VuZCI6eyJyIjoyMzQsImciOjIzNiwiYiI6MjMxLCJhbHBoYSI6MH19fX0=',
    'alt': 'Lasso Watermelon Lime Gelatin Cups at Happier Grocery Soho'
}

all_available = [sample_prod] + [p for p in parsed if p['id'] != sample_prod['id']]
print(f"Total available authentic Happier Grocery items: {len(all_available)}")

# Load existing local_shops_data.json
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_data = json.load(f)

existing_hg = [p for p in local_data['products'] if p.get('shop_id') == 'happier-grocery']
other_products = [p for p in local_data['products'] if p.get('shop_id') != 'happier-grocery']

repaired_hg = []
for i, orig in enumerate(existing_hg):
    auth = all_available[i]
    slug = orig['slug']
    item_id = orig['id']
    
    title = auth['title']
    brand = auth['brand']
    price = auth['price']
    pkg = auth['package_size']
    img_url = auth['image_url']
    prod_id = auth['id']
    
    t_lower = (title + ' ' + brand).lower()
    if any(k in t_lower for k in ['candle', 'facial', 'tissue', 'soap', 'lotion', 'balm']):
        moonoh_cat = "Health & beauty"
    elif any(k in t_lower for k in ['pan', 'bag', 'clean', 'towel', 'agitator']):
        moonoh_cat = "Home, garden & DIY"
    else:
        moonoh_cat = "Food & Groceries"
        
    summary = f"Curated {moonoh_cat.lower()} product from Happier Grocery flagship market in Soho, NYC. Sourced directly from independent, organic, and artisanal producers."
    
    repaired_item = {
        "id": item_id,
        "source_product_id": f"hg-{prod_id}",
        "shop_id": "happier-grocery",
        "slug": slug,
        "source_url": f"https://shop.happiergrocery.com/product/{prod_id}?utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops",
        "canonical_source_url": f"https://shop.happiergrocery.com/product/{prod_id}",
        "title": title,
        "brand": brand,
        "source_category": moonoh_cat,
        "moonoh_category": moonoh_cat,
        "package_size": pkg,
        "currency": "USD",
        "current_price": price,
        "original_price": 0.0,
        "discount_percentage": 0,
        "sell_by_date": None,
        "availability": "in_stock",
        "availability_context": "Available in store & local delivery at Happier Grocery (Soho, NYC)",
        "image_source_url": img_url,
        "image_alt": f"{title} by {brand} at Happier Grocery Soho",
        "moonoh_summary": summary,
        "cta_text": "View on Happier Grocery \u2197",
        "last_checked_at": "2026-08-17T12:00:00Z"
    }
    repaired_hg.append(repaired_item)

print(f"✅ Generated {len(repaired_hg)} repaired Happier Grocery items.")

# Update local_shops_data.json
local_data['products'] = other_products + repaired_hg
# Sort by shop_id and id
local_data['products'].sort(key=lambda x: (x['shop_id'], int(re.search(r'\d+', x['id']).group(0)) if re.search(r'\d+', x['id']) else x['id']))

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(local_data, f, indent=2, ensure_ascii=False)
print(f"🎉 Successfully updated local_shops_data.json with total {len(local_data['products'])} products!")
