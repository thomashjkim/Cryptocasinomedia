import json
import re
import urllib.parse

with open('scripts/scraped_happier_raw.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

products_by_id = {}

for item in items:
    href = item.get('href', '')
    id_match = re.search(r'/product/([a-f0-9]+)', href)
    if not id_match:
        continue
    prod_id = id_match.group(1)
    
    if prod_id not in products_by_id:
        products_by_id[prod_id] = {
            'id': prod_id,
            'url': href,
            'image_url': '',
            'text': '',
            'alt': ''
        }
        
    img_src = item.get('imgSrc', '')
    if img_src:
        m = re.search(r'url=([^&]+)', img_src)
        if m:
            cdn_url = urllib.parse.unquote(m.group(1))
            products_by_id[prod_id]['image_url'] = cdn_url
            products_by_id[prod_id]['alt'] = item.get('imgAlt', '')
            
    text = item.get('text', '').strip()
    if text:
        products_by_id[prod_id]['text'] = text

print(f'Total uniquely parsed products: {len(products_by_id)}')
parsed_list = []
for p_id, p in products_by_id.items():
    lines = [l.strip() for l in p['text'].split('\n') if l.strip()]
    brand = lines[0] if len(lines) > 0 else 'Happier Grocery'
    title = lines[1] if len(lines) > 1 else lines[0] if len(lines) > 0 else 'Happier Grocery Item'
    
    price_val = 0.0
    pkg_size = 'Standard'
    for l in lines[2:]:
        if '$' in l:
            pm = re.search(r'\$([0-9.]+)', l)
            if pm:
                price_val = float(pm.group(1))
        elif any(c in l.lower() for c in ['oz', 'ct', 'ea', 'lb', 'g', 'ml', 'fl oz']):
            pkg_size = l
            
    parsed_list.append({
        'id': p_id,
        'title': title,
        'brand': brand,
        'price': price_val,
        'package_size': pkg_size,
        'url': p['url'],
        'image_url': p['image_url'],
        'alt': p['alt'] or title
    })

valid = [p for p in parsed_list if p['image_url'] and p['title'] and p['price'] > 0]
print(f'Products with valid title, price & image: {len(valid)}')

for i, p in enumerate(valid[:20]):
    print(f"{i+1}. [{p['brand']}] {p['title']} | ${p['price']} | Size: {p['package_size']}")
    print(f"   URL: {p['url']}")
    print(f"   IMG: {p['image_url'][:75]}...")

with open('scripts/happier_clean_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(valid, f, indent=2)
print("Saved scripts/happier_clean_parsed.json")
