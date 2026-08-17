import urllib.request
import json
import re
import time

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

def clean_slug(title, handle, shop_slug, existing_slugs):
    base = handle if handle else re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    slug = base
    suffix = 1
    while slug in existing_slugs:
        slug = f"{base}-{suffix}"
        suffix += 1
    existing_slugs.add(slug)
    return slug

def infer_category(title, product_type, tags, shop_slug):
    text = f"{title} {product_type} {' '.join(tags)}".lower()
    
    if shop_slug == 'sey-coffee':
        return "Coffee & Pantry"
    
    # Coffee & Pantry
    if any(k in text for k in ['coffee', 'tea', 'matcha', 'latte', 'espresso', 'pantry', 'sauce', 'olive oil', 'jam', 'snack', 'chocolate', 'syrup', 'cider', 'mustard', 'conserva', 'cracker', 'cookie', 'salt', 'honey', 'granola', 'spice', 'food', 'beverage', 'drink', 'soda', 'bean']):
        return "Coffee & Pantry"
    
    # Vintage & Fashion
    if any(k in text for k in ['jacket', 'coat', 'pant', 'denim', 'jean', 'dress', 'shirt', 'tee', 't-shirt', 'sweater', 'vest', 'cardigan', 'skirt', 'blouse', 'trouser', 'shoe', 'boot', 'sandal', 'clog', 'sneaker', 'hat', 'cap', 'bag', 'tote', 'necklace', 'ring', 'earring', 'bracelet', 'jewelry', 'scarf', 'belt', 'vintage', 'apparel', 'clothing', 'sunglasses', 'kimono', 'sweatshirt']):
        return "Vintage & Fashion"
    
    # Gifts & Culture
    if any(k in text for k in ['book', 'magazine', 'journal', 'pen', 'paper', 'stationery', 'notebook', 'perfume', 'eau de parfum', 'incense', 'fragrance', 'card', 'gift', 'art', 'print', 'poster', 'record', 'vinyl']):
        return "Gifts & Culture"
    
    # Home & Objects
    return "Home & Objects"

def harvest_shopify_shop(shop_config, limit, existing_slugs):
    shop_id = shop_config['id']
    shop_url = shop_config['website_url'].rstrip('/')
    print(f"Harvesting {shop_id} (target: {limit})...")
    
    collected = []
    page = 1
    
    while len(collected) < limit:
        url = f"{shop_url}/products.json?limit=250&page={page}"
        try:
            data = fetch_json(url)
            products = data.get('products', [])
            if not products:
                break
            
            for p in products:
                if len(collected) >= limit:
                    break
                
                # Check variants availability and price
                variants = p.get('variants', [])
                avail_variants = [v for v in variants if v.get('available', True)]
                if not avail_variants:
                    continue  # Skip sold out
                
                v0 = avail_variants[0]
                price = float(v0.get('price', 0))
                if price <= 0:
                    continue
                
                # Check image
                images = p.get('images', [])
                if not images:
                    continue
                
                img_src = images[0].get('src', '')
                if not img_src:
                    continue
                if img_src.startswith('//'):
                    img_src = f"https:{img_src}"
                
                title = p.get('title', '').strip()
                handle = p.get('handle', '').strip()
                brand = p.get('vendor', '').strip() or shop_config['name']
                product_type = p.get('product_type', '').strip()
                tags = p.get('tags', [])
                
                slug = clean_slug(title, handle, shop_id, existing_slugs)
                cat = infer_category(title, product_type, tags, shop_id)
                
                item_id = f"{shop_id}-{len(collected) + 1}"
                prod_id = f"{shop_id[:3]}-{p['id']}"
                source_prod_url = f"{shop_url}/products/{handle}"
                canonical_source_url = source_prod_url
                
                source_pub = p.get('published_at')
                source_created = p.get('created_at')
                source_updated = p.get('updated_at')
                
                summary = f"Curated {cat.lower()} item from {shop_config['name']} in {shop_config['neighborhood']}, NYC. {p.get('body_html', '')[:120].replace('<p>', '').replace('</p>', '').replace('<br>', ' ').strip()}"
                summary = re.sub(r'<[^>]+>', '', summary).strip()
                if len(summary) > 200:
                    summary = summary[:197] + '...'
                
                record = {
                    "id": item_id,
                    "source_product_id": prod_id,
                    "shop_id": shop_id,
                    "slug": slug,
                    "source_url": f"{source_prod_url}?utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops",
                    "canonical_source_url": canonical_source_url,
                    "title": title,
                    "brand": brand,
                    "source_category": product_type or cat,
                    "moonoh_category": cat,
                    "primary_category": cat,
                    "package_size": v0.get('title') if v0.get('title') != 'Default Title' else 'Standard',
                    "currency": "USD",
                    "current_price": price,
                    "original_price": float(v0.get('compare_at_price')) if v0.get('compare_at_price') else 0.0,
                    "discount_percentage": round(((float(v0.get('compare_at_price')) - price) / float(v0.get('compare_at_price'))) * 100) if v0.get('compare_at_price') and float(v0.get('compare_at_price')) > price else 0,
                    "sell_by_date": None,
                    "availability": "in_stock",
                    "availability_context": f"Available in store & online at {shop_config['name']} ({shop_config['neighborhood']}, NYC)",
                    "image_source_url": img_src,
                    "image_alt": f"{title} by {brand} at {shop_config['name']} {shop_config['neighborhood']}",
                    "moonoh_summary": summary,
                    "cta_text": f"View at {shop_config['name']} \u2197",
                    "source_published_at": source_pub,
                    "source_created_at": source_created,
                    "source_updated_at": source_updated,
                    "source_order": len(collected) + 1,
                    "last_checked_at": "2026-08-17T12:00:00Z",
                    "store_address": shop_config['address_line_1'],
                    "store_city": shop_config['city'],
                    "store_state": shop_config['state'],
                    "store_postal_code": shop_config['postal_code'],
                    "store_location_source": shop_config.get('location_source', 'official website')
                }
                collected.append(record)
            
            page += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"Error fetching {shop_id} page {page}: {e}")
            break
            
    print(f"  -> Collected {len(collected)} items for {shop_id}")
    return collected

def run_all():
    # Load existing local shops DB
    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    existing_slugs = set(p['slug'] for p in db['products'])
    
    # 4 New Shop Configs
    new_shops = {
        "front-general-store": {
            "id": "front-general-store",
            "slug": "front-general-store",
            "name": "Front General Store",
            "source_key": "front_general_store",
            "business_description": "Curated vintage clothing, Japanese workwear, vintage jewelry, home goods, and unique lifestyle accessories in DUMBO, Brooklyn.",
            "website_url": "https://frontgeneralstore.com",
            "shopping_url": "https://frontgeneralstore.com/collections/all",
            "logo_url": "https://frontgeneralstore.com/cdn/shop/files/fgs_logo.png",
            "primary_image_url": "https://frontgeneralstore.com/cdn/shop/files/fgs_store.jpg",
            "neighborhood": "DUMBO",
            "address_line_1": "143 Front St",
            "city": "Brooklyn",
            "state": "NY",
            "postal_code": "11201",
            "country": "US",
            "theme_color": "#2C3E50",
            "categories": ["Vintage & Fashion", "Home & Objects", "Gifts & Culture"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 500,
            "location_source": "official website (https://frontgeneralstore.com/pages/about-us)"
        },
        "mirth-vintage": {
            "id": "mirth-vintage",
            "slug": "mirth-vintage",
            "name": "Mirth Vintage",
            "source_key": "mirth_vintage",
            "business_description": "Carefully selected contemporary vintage clothing, timeless silhouettes, footwear, and accessories in Greenpoint, Brooklyn.",
            "website_url": "https://mirth.co",
            "shopping_url": "https://mirth.co/collections/all",
            "logo_url": "https://mirth.co/cdn/shop/files/mirth_logo.png",
            "primary_image_url": "https://mirth.co/cdn/shop/files/mirth_store.jpg",
            "neighborhood": "Greenpoint",
            "address_line_1": "603 Manhattan Ave",
            "city": "Brooklyn",
            "state": "NY",
            "postal_code": "11222",
            "country": "US",
            "theme_color": "#B8860B",
            "categories": ["Vintage & Fashion", "Gifts & Culture"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 30,
            "location_source": "official website (https://mirth.co)"
        },
        "sey-coffee": {
            "id": "sey-coffee",
            "slug": "sey-coffee",
            "name": "SEY Coffee",
            "source_key": "sey_coffee",
            "business_description": "Internationally renowned micro-batch specialty coffee roastery and cafe sourcing single-origin coffees in Bushwick, Brooklyn.",
            "website_url": "https://www.seycoffee.com",
            "shopping_url": "https://www.seycoffee.com/collections/coffee",
            "logo_url": "https://www.seycoffee.com/cdn/shop/files/sey_logo.png",
            "primary_image_url": "https://www.seycoffee.com/cdn/shop/files/sey_store.jpg",
            "neighborhood": "Bushwick",
            "address_line_1": "18 Grattan St",
            "city": "Brooklyn",
            "state": "NY",
            "postal_code": "11206",
            "country": "US",
            "theme_color": "#222222",
            "categories": ["Coffee & Pantry", "Gifts & Culture"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 30,
            "location_source": "official website (https://www.seycoffee.com)"
        },
        "salter-house": {
            "id": "salter-house",
            "slug": "salter-house",
            "name": "Salter House",
            "source_key": "salter_house",
            "business_description": "Family-owned small-batch home goods, natural fiber nightwear, sustainable housewares, tea, and literature in Brooklyn Heights & East Village.",
            "website_url": "https://salter.house",
            "shopping_url": "https://salter.house/collections/all",
            "logo_url": "https://salter.house/cdn/shop/files/salter_logo.png",
            "primary_image_url": "https://salter.house/cdn/shop/files/salter_store.jpg",
            "neighborhood": "Brooklyn Heights",
            "address_line_1": "119 Atlantic Ave",
            "city": "Brooklyn",
            "state": "NY",
            "postal_code": "11201",
            "country": "US",
            "theme_color": "#4A6B53",
            "categories": ["Home & Objects", "Vintage & Fashion", "Coffee & Pantry", "Gifts & Culture"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 30,
            "location_source": "official website (https://salter.house)"
        }
    }
    
    # Collect items
    fgs_items = harvest_shopify_shop(new_shops['front-general-store'], 500, existing_slugs)
    new_shops['front-general-store']['products_count'] = len(fgs_items)
    
    mirth_items = harvest_shopify_shop(new_shops['mirth-vintage'], 30, existing_slugs)
    new_shops['mirth-vintage']['products_count'] = len(mirth_items)
    
    sey_items = harvest_shopify_shop(new_shops['sey-coffee'], 30, existing_slugs)
    new_shops['sey-coffee']['products_count'] = len(sey_items)
    
    salter_items = harvest_shopify_shop(new_shops['salter-house'], 30, existing_slugs)
    new_shops['salter-house']['products_count'] = len(salter_items)
    
    # Update existing shops with primary_category
    for p in db['products']:
        if not p.get('primary_category'):
            p['primary_category'] = infer_category(p['title'], p.get('source_category', ''), [], p['shop_id'])
            p['moonoh_category'] = p['primary_category']
    
    # Add new shops and products to DB
    for k, v in new_shops.items():
        db['shops'][k] = v
        
    all_new_products = fgs_items + mirth_items + sey_items + salter_items
    db['products'].extend(all_new_products)
    
    with open('local_shops_data.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
        
    print(f"\n🎉 Successfully added 4 new shops ({len(new_shops)}) and {len(all_new_products)} new products!")
    print(f"Total Local Products in local_shops_data.json: {len(db['products'])}")
    print(f"Total Local Shops in local_shops_data.json: {len(db['shops'])}")

if __name__ == '__main__':
    run_all()
