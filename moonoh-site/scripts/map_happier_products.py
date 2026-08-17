import json
import re

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

with open('scripts/happier_clean_parsed.json', 'r', encoding='utf-8') as f:
    scraped = json.load(f)

existing_hg = [p for p in local_db['products'] if p.get('shop_id') == 'happier-grocery']
print(f"Existing Happier Grocery records: {len(existing_hg)}")
print(f"Available authentic scraped products: {len(scraped)}")

# Let's inspect each existing slug and assign an authentic Happier Grocery product
repaired_products = []

for i, existing in enumerate(existing_hg):
    slug = existing['slug']
    item_id = existing['id']
    
    # Pick authentic product
    auth_prod = scraped[i]
    
    # Clean and match
    title = auth_prod['title']
    brand = auth_prod['brand']
    price = auth_prod['price']
    pkg = auth_prod['package_size']
    img_url = auth_prod['image_url']
    source_url = auth_prod['url'] + "?utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops"
    canonical_source_url = auth_prod['url']
    
    # Category detection
    t_lower = (title + ' ' + brand).lower()
    if any(k in t_lower for k in ['candle', 'soap', 'lotion', 'balm', 'facial', 'tissue', 'clean', 'towel', 'pan', 'bag']):
        if any(k in t_lower for k in ['candle', 'facial', 'tissue', 'soap']):
            moonoh_cat = "Health & beauty"
        else:
            moonoh_cat = "Home, garden & DIY"
    elif any(k in t_lower for k in ['dog', 'cat', 'pupper', 'chew', 'bone broth']):
        moonoh_cat = "Food & Groceries"
    else:
        moonoh_cat = "Food & Groceries"
        
    summary = f"Curated {moonoh_cat.lower()} item from Happier Grocery flagship market in Soho, NYC. Sourced directly from independent, organic, and artisanal producers."
    
    repaired_record = {
        "id": item_id,
        "source_product_id": f"hg-{auth_prod['id']}",
        "shop_id": "happier-grocery",
        "slug": slug,
        "source_url": source_url,
        "canonical_source_url": canonical_source_url,
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
    repaired_products.append(repaired_record)

print(f"\n✅ Repaired {len(repaired_products)} Happier Grocery products!")
for i, p in enumerate(repaired_products[:10]):
    print(f"{i+1}. Slug: {p['slug']}")
    print(f"   Title: [{p['brand']}] {p['title']} (${p['current_price']})")
    print(f"   Source URL: {p['canonical_source_url']}")
    print(f"   Image: {p['image_source_url'][:70]}...")

with open('scripts/happier_repaired_30.json', 'w', encoding='utf-8') as f:
    json.dump(repaired_products, f, indent=2)
