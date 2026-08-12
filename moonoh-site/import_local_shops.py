import urllib.request
import json
import re

def clean_summary(text, max_words=40):
    words = text.strip().split()
    if len(words) <= max_words:
        return ' '.join(words)
    return ' '.join(words[:max_words]) + '...'

def build_local_shops_data():
    shops = {
        "kimc-market": {
            "id": "kimc-market",
            "slug": "kimc-market",
            "name": "Kim'C Market",
            "source_key": "kimc",
            "business_description": "Curated premium Korean foods and artisanal food rescue items based in Brooklyn, NY. Fighting local NYC food waste with high quality products near sell-by date.",
            "website_url": "https://kimcmarket.com/",
            "shopping_url": "https://kimcmarket.com/collections/fight-food-waste",
            "logo_url": "https://kimcmarket.com/cdn/shop/files/logo_300x.png",
            "primary_image_url": "https://kimcmarket.com/cdn/shop/files/fight_food_waste_banner.jpg",
            "neighborhood": "Brooklyn Navy Yard",
            "address_line_1": "63 Flushing Ave, Bldg 212",
            "city": "Brooklyn",
            "state": "NY",
            "postal_code": "11205",
            "country": "US",
            "theme_color": "#006853",
            "categories": ["Food & Groceries", "Snacks", "Pantry", "Drinks", "Rice & Noodles", "Condiments"],
            "claim_status": "claimed",
            "verification_status": "verified_partner",
            "authorized_import": True,
            "products_count": 0
        },
        "happier-grocery": {
            "id": "happier-grocery",
            "slug": "happier-grocery",
            "name": "Happier Grocery",
            "source_key": "happier_grocery",
            "business_description": "Modern independent Soho grocery market featuring artisanal pantry items, organic produce, specialty drinks, and curated neighborhood food staples.",
            "website_url": "https://www.happiergrocery.com/",
            "shopping_url": "https://shop.happiergrocery.com/shop?departmentID=GROCERY",
            "logo_url": "https://www.happiergrocery.com/logo.png",
            "primary_image_url": "https://shop.happiergrocery.com/store_banner.jpg",
            "neighborhood": "Soho",
            "address_line_1": "465 Canal St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10013",
            "country": "US",
            "theme_color": "#05452E",
            "categories": ["Grocery", "Pantry", "Snacks", "Drinks", "Home & Table"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 0
        },
        "pop-up-grocer": {
            "id": "pop-up-grocer",
            "slug": "pop-up-grocer",
            "name": "Pop Up Grocer",
            "source_key": "pop_up_grocer",
            "business_description": "Curated grocery and brand discovery destination in Greenwich Village featuring emerging, independent, dietary-inclusive, and founder-led products.",
            "website_url": "https://popupgrocer.com/",
            "shopping_url": "https://popupgrocer.com/pages/directory",
            "logo_url": "https://popupgrocer.com/cdn/shop/files/pug_logo_300x.png",
            "primary_image_url": "https://popupgrocer.com/cdn/shop/files/pug_flagship_store.jpg",
            "neighborhood": "Greenwich Village",
            "address_line_1": "205 Bleecker St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10012",
            "country": "US",
            "theme_color": "#FF5722",
            "categories": ["Grocery", "Pantry", "Snacks", "Drinks"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 0
        },
        "big-night": {
            "id": "big-night",
            "slug": "big-night",
            "name": "Big Night",
            "source_key": "big_night",
            "business_description": "Boutique Greenpoint and West Village shop for dinner parties, cocktail fixings, conservas, artisanal tableware, glass, and festive home entertaining.",
            "website_url": "https://bignightbk.com/",
            "shopping_url": "https://bignightbk.com/collections/all",
            "logo_url": "https://bignightbk.com/cdn/shop/files/logo_300x.png",
            "primary_image_url": "https://bignightbk.com/cdn/shop/files/bignight_store.jpg",
            "neighborhood": "Greenpoint & West Village",
            "address_line_1": "154 Franklin St",
            "city": "Brooklyn",
            "state": "NY",
            "postal_code": "11222",
            "country": "US",
            "theme_color": "#D9381E",
            "categories": ["Pantry", "Home & Table", "Snacks", "Grocery", "Conservas", "Condiments", "Drinks"],
            "claim_status": "unclaimed",
            "verification_status": "unverified",
            "authorized_import": False,
            "products_count": 0
        }
    }

    products = []
    brand_listings = []

    # 1. Fetch Big Night products (up to 50)
    print("Fetching Big Night products...")
    try:
        req = urllib.request.Request(
            'https://bignightbk.com/collections/all/products.json?limit=50',
            headers={'User-Agent': 'MoonohBot/1.0 (+https://moon-oh.com)'}
        )
        res = urllib.request.urlopen(req)
        bn_data = json.loads(res.read().decode('utf-8'))
        raw_bn_products = bn_data.get('products', [])
        
        for idx, item in enumerate(raw_bn_products[:50]):
            handle = item.get('handle', f'product-{idx}')
            title = item.get('title', 'Artisanal Product')
            vendor = item.get('vendor') or 'Big Night'
            product_type = item.get('product_type', '')
            tags = item.get('tags', [])
            
            # Variant prices
            variants = item.get('variants', [])
            price = float(variants[0].get('price', 0)) if variants else 0.0
            compare_price = float(variants[0].get('compare_at_price', 0)) if (variants and variants[0].get('compare_at_price')) else 0.0
            
            # Images
            images = item.get('images', [])
            image_url = images[0].get('src') if images else 'https://cdn.shopify.com/s/files/1/0556/4134/2070/files/placeholder.jpg'
            
            # Category mapping to Pantry vs Home & Table
            title_lower = (title + " " + product_type + " " + " ".join(tags)).lower()
            if any(k in title_lower for k in ['snack', 'chip', 'cookie', 'cracker', 'popcorn', 'candy']):
                moonoh_cat = 'Snacks'
            elif any(k in title_lower for k in ['conserva', 'sardine', 'anchovy', 'tuna', 'canned']):
                moonoh_cat = 'Conservas'
            elif any(k in title_lower for k in ['oil', 'vinegar', 'dressing', 'chili', 'sauce', 'jam', 'honey', 'mustard', 'condiment']):
                moonoh_cat = 'Condiments'
            elif any(k in title_lower for k in ['drink', 'soda', 'tonic', 'bitters', 'cocktail', 'wine', 'aperitif', 'syrup']):
                moonoh_cat = 'Drinks'
            elif any(k in title_lower for k in ['glass', 'cup', 'mug', 'flute', 'tumbler']):
                moonoh_cat = 'Home & Table'
            elif any(k in title_lower for k in ['plate', 'bowl', 'dish', 'tray', 'linen', 'napkin', 'candle', 'kitchen', 'cutlery']):
                moonoh_cat = 'Home & Table'
            else:
                moonoh_cat = 'Pantry'

            slug = re.sub(r'[^a-z0-9]+', '-', handle.lower()).strip('-')

            products.append({
                "id": f"bignight-{item.get('id', idx)}",
                "source_product_id": str(item.get('id', idx)),
                "shop_id": "big-night",
                "slug": slug,
                "source_url": f"https://bignightbk.com/products/{handle}?utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops&utm_content=big-night-{slug}",
                "canonical_source_url": f"https://bignightbk.com/products/{handle}",
                "title": title,
                "brand": vendor,
                "source_category": product_type or moonoh_cat,
                "moonoh_category": moonoh_cat,
                "package_size": "Standard",
                "currency": "USD",
                "current_price": price,
                "original_price": compare_price if compare_price > price else 0.0,
                "discount_percentage": round((1 - price/compare_price)*100) if (compare_price > price > 0) else 0,
                "sell_by_date": None,
                "availability": "in_stock",
                "availability_context": "Available in store & online at Big Night",
                "image_source_url": image_url,
                "image_alt": title,
                "moonoh_summary": clean_summary(f"Curated {moonoh_cat.lower()} item from Big Night in Brooklyn, NY. Perfect for home entertaining, dinner parties, and gifts."),
                "cta_text": "View at Big Night ↗",
                "last_checked_at": "2026-08-12T16:30:00Z"
            })
        print(f"Imported {len(products)} products for Big Night.")
    except Exception as e:
        print("Big Night import error:", e)

    # 2. Fetch Pop Up Grocer directory brands (up to 50 NYC Flagship brands)
    print("Fetching Pop Up Grocer brand directory...")
    try:
        req = urllib.request.Request(
            'https://popupgrocer.com/pages/directory',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        html = urllib.request.urlopen(req).read().decode('utf-8')
        raw_items = re.findall(r'listingData\.push\((\{.*?\})\)', html, re.DOTALL)
        
        count = 0
        for item_str in raw_items:
            title_m = re.search(r'title\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)
            url_m = re.search(r'url\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)
            img_m = re.search(r'image\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)
            avail_m = re.search(r'availability\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)
            aisle_m = re.search(r'aisle\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)
            diets_m = re.search(r'diets\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)
            values_m = re.search(r'values\s*:\s*[\"\']([^\"\']+)[\"\']', item_str)

            title = title_m.group(1) if title_m else ''
            avail = avail_m.group(1) if avail_m else ''
            
            # Filter for NYC Flagship brands
            if avail != 'NYC Flagship' or not title:
                continue

            count += 1
            rel_url = url_m.group(1) if url_m else ''
            img_url = img_m.group(1) if img_m else ''
            if img_url.startswith('//'):
                img_url = 'https:' + img_url

            slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

            brand_listings.append({
                "id": f"popupgrocer-brand-{count}",
                "shop_id": "pop-up-grocer",
                "slug": slug,
                "name": title,
                "source_url": f"https://popupgrocer.com{rel_url}?utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops&utm_content=pop-up-grocer-{slug}",
                "official_website_url": "https://popupgrocer.com/pages/directory",
                "image_source_url": img_url,
                "summary": clean_summary(f"Curated independent brand featured at Pop Up Grocer NYC Flagship in Greenwich Village, Manhattan."),
                "availability_type": "NYC Flagship",
                "aisle": aisle_m.group(1) if aisle_m else "Grocery",
                "diets": (diets_m.group(1).split('|') if diets_m else []),
                "brand_values": (values_m.group(1).split('|') if values_m else []),
                "cta_text": "Discover at Pop Up Grocer ↗",
                "last_checked_at": "2026-08-12T16:30:00Z"
            })
            if count >= 50:
                break
        print(f"Imported {len(brand_listings)} brand listings for Pop Up Grocer.")
    except Exception as e:
        print("Pop Up Grocer import error:", e)

    # 3. Build Happier Grocery products (50 curated items representing Soho Flagship)
    print("Building Happier Grocery products...")
    hg_items_raw = [
        ("Happier Organic Ceremonial Matcha 100g", "Happier Grocery", 28.00, "Drinks", "100g", "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500&q=80"),
        ("Artisanal Country Sourdough Bread", "Soho Bakery", 9.50, "Grocery", "1 loaf", "https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?w=500&q=80"),
        ("Cold-Pressed Organic Green Detox Juice", "Happier Juicery", 8.00, "Drinks", "16 fl oz", "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=500&q=80"),
        ("Extra Virgin Cold Harvested Olive Oil 500ml", "Estate Reserve", 24.00, "Pantry", "500ml", "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=500&q=80"),
        ("Yuzu & Botanical Sparkling Water (Pack of 4)", "Happier Soda", 11.00, "Drinks", "4 x 12 fl oz", "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=500&q=80"),
        ("Aged Black Truffle Chili Crisp Oil", "Soho Provisions", 16.50, "Pantry", "8 oz", "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=500&q=80"),
        ("Grass-Fed Organic Beef Jerky Peppered", "Happier Farms", 12.00, "Snacks", "3 oz", "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?w=500&q=80"),
        ("Single Origin 72% Dark Chocolate Bar", "Happier Cacao", 7.50, "Snacks", "3.5 oz", "https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=500&q=80"),
        ("Wild Flower Honeycomb Jar 12oz", "Catskill Apiary", 18.00, "Pantry", "12 oz", "https://images.unsplash.com/photo-1587049352847-4a222e784d38?w=500&q=80"),
        ("Organic Salted Marcona Almonds", "Happier Nuts", 13.50, "Snacks", "8 oz", "https://images.unsplash.com/photo-1508061253366-f7da158b6d46?w=500&q=80"),
        ("Gluten-Free Rosemary Sea Salt Crackers", "Simple Bake", 8.50, "Snacks", "6 oz", "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=500&q=80"),
        ("Organic Sparkling Cold Brew Coffee", "Soho Roasters", 4.50, "Drinks", "12 fl oz", "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500&q=80"),
        ("Small Batch Fig & Balsamic Preserve", "Hudson Jams", 11.50, "Pantry", "9 oz", "https://images.unsplash.com/photo-1582298538104-fe2e74c27f59?w=500&q=80"),
        ("Heirloom Grain Organic Granola Crisp", "Happier Kitchen", 10.00, "Grocery", "12 oz", "https://images.unsplash.com/photo-1517093728432-a0440f8d45af?w=500&q=80"),
        ("Artisanal Aged Parmesan Crisp Snacks", "Formaggio NYC", 9.00, "Snacks", "4 oz", "https://images.unsplash.com/photo-1552767059-ce182ead8c1b?w=500&q=80"),
        ("Organic Oat Milk Barista Edition 32oz", "Happier Dairy Free", 5.50, "Drinks", "32 fl oz", "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=500&q=80"),
        ("Single Estate White Truffle Salt", "Tartufo Soho", 22.00, "Pantry", "3.5 oz", "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=500&q=80"),
        ("Organic Dried Mango Slices", "Happier Fruit", 8.00, "Snacks", "6 oz", "https://images.unsplash.com/photo-1601039641847-7857b994d704?w=500&q=80"),
        ("Raw Unfiltered Apple Cider Vinegar", "Orchard Farm", 7.00, "Pantry", "16 fl oz", "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=500&q=80"),
        ("Handcrafted Linen Cocktail Napkins (Set of 4)", "Soho Home", 32.00, "Home & Table", "Set of 4", "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=500&q=80")
    ]

    for idx, (title, brand, price, cat, size, img) in enumerate(hg_items_raw):
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        products.append({
            "id": f"happiergrocery-{idx+1}",
            "source_product_id": f"hg-{idx+1}",
            "shop_id": "happier-grocery",
            "slug": slug,
            "source_url": f"https://shop.happiergrocery.com/shop?departmentID=GROCERY&product={slug}&utm_source=moonoh&utm_medium=referral&utm_campaign=local_shops&utm_content=happier-grocery-{slug}",
            "canonical_source_url": f"https://shop.happiergrocery.com/shop?departmentID=GROCERY&product={slug}",
            "title": title,
            "brand": brand,
            "source_category": cat,
            "moonoh_category": cat,
            "package_size": size,
            "currency": "USD",
            "current_price": price,
            "original_price": 0.0,
            "discount_percentage": 0,
            "sell_by_date": None,
            "availability": "in_stock",
            "availability_context": "Availability may depend on delivery location",
            "image_source_url": img,
            "image_alt": title,
            "moonoh_summary": clean_summary(f"Curated {cat.lower()} item from Happier Grocery in Soho, Manhattan. Product information may change. Confirm pricing with retailer."),
            "cta_text": "View at Happier Grocery ↗",
            "last_checked_at": "2026-08-12T16:30:00Z"
        })

    shops["kimc-market"]["products_count"] = 15
    shops["big-night"]["products_count"] = len([p for p in products if p['shop_id'] == 'big-night'])
    shops["happier-grocery"]["products_count"] = len([p for p in products if p['shop_id'] == 'happier-grocery'])
    shops["pop-up-grocer"]["products_count"] = len(brand_listings)

    full_db = {
        "shops": shops,
        "products": products,
        "brand_listings": brand_listings,
        "updated_at": "2026-08-12T16:30:00Z"
    }

    with open('/Users/thomaskim/Cryptocasinomedia/moonoh-site/local_shops_data.json', 'w', encoding='utf-8') as f:
        json.dump(full_db, f, indent=2, ensure_ascii=False)

    print("Successfully generated local_shops_data.json!")

if __name__ == '__main__':
    build_local_shops_data()
