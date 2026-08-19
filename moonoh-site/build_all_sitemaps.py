import json
import re
import datetime
import os

today_str = datetime.date.today().isoformat()

def escape_xml(s):
    if not s:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def to_web_jpg(img_url):
    if not img_url:
        return ""
    if img_url.lower().endswith('.heic'):
        last_slash = img_url.rfind('/')
        if last_slash != -1:
            d = img_url[:last_slash+1]
            f = img_url[last_slash+1:]
            dot = f.rfind('.')
            base = f[:dot] if dot != -1 else f
            return f"{d}thumbnail_{base}.jpg"
    return img_url

def clean_slug(text):
    clean = re.sub(r'[^a-z0-9\s-]', '', (text or 'item').lower()).strip()
    clean = re.sub(r'\s+', '-', clean)
    clean = re.sub(r'-+', '-', clean)
    if len(clean) > 50:
        clean = clean[:50].rstrip('-')
    return clean or 'item'

# --- 1. Load Moonoh Items ---
with open('netlify/functions/moonoh-items-data.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m = re.search(r'export const realMoonohItems = (\[.*?\]);', code, re.DOTALL)
moonoh_items = json.loads(m.group(1)) if m else []

# --- 2. Load Food Rescue Items ---
with open('netlify/functions/food-rescue-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m = re.search(r'export const realFoodRescueItems = (\[.*?\]);', code, re.DOTALL)
food_rescue_items = json.loads(m.group(1)) if m else []

# --- 3. Load External Items ---
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', code, re.DOTALL)
m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', code, re.DOTALL)
karrot_items = json.loads(m_karrot.group(1)) if m_karrot else []
heykorean_items = json.loads(m_hey.group(1)) if m_hey else []

# --- 4. Load Local Shops Data ---
local_shops_data = {}
if os.path.exists('local_shops_data.json'):
    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        local_shops_data = json.load(f)

print(f"Data Loaded: {len(moonoh_items)} Moonoh, {len(food_rescue_items)} KimC, {len(karrot_items)} Karrot, {len(heykorean_items)} HeyKorean, {len(local_shops_data.get('products', []))} Local Products, {len(local_shops_data.get('shops', {}))} Shops")

def generate_canonical_url(title_str, loc_str, item_id, is_ext=False):
    clean_t = clean_slug(title_str)
    loc_slug = 'manhattan-ny'
    if loc_str:
        l = str(loc_str).lower()
        l = re.sub(r'^\d+mi\s*·\s*', '', l)
        l = re.sub(r'^\d+mi\s+', '', l)
        if 'bayside' in l: loc_slug = 'bayside-queens-ny'
        elif 'flushing' in l: loc_slug = 'flushing-queens-ny'
        elif 'astoria' in l: loc_slug = 'astoria-queens-ny'
        elif 'queens' in l: loc_slug = 'queens-ny'
        elif 'brooklyn' in l: loc_slug = 'brooklyn-ny'
        elif 'manhattan' in l: loc_slug = 'manhattan-ny'
        elif 'bronx' in l: loc_slug = 'bronx-ny'
        elif 'staten' in l: loc_slug = 'staten-island-ny'
        elif any(w in l for w in ['fort lee', 'palisades', 'bergen', 'edgewater', 'leonia', 'paramus']): loc_slug = 'bergen-county-nj'
        elif any(w in l for w in ['jersey city', 'hoboken', 'hudson']): loc_slug = 'hudson-county-nj'
        else:
            loc_slug = clean_slug(loc_str) or 'manhattan-ny'
            
    id_suffix = f"ext-{item_id}" if is_ext else str(item_id)
    return f"https://moon-oh.com/item/{clean_t}-{loc_slug}-{id_suffix}"

# =========================================================================
# 1. sitemap-pages.xml
# =========================================================================
xml_pages = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

main_pages = [
    ("https://moon-oh.com/", "1.0", "daily"),
    ("https://moon-oh.com/explore", "0.9", "daily"),
    ("https://moon-oh.com/about", "0.8", "monthly"),
    ("https://moon-oh.com/safety-trust", "0.8", "monthly"),
    ("https://moon-oh.com/terms", "0.5", "yearly"),
    ("https://moon-oh.com/privacy", "0.5", "yearly"),
]

for url, pri, freq in main_pages:
    xml_pages.append('  <url>')
    xml_pages.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
    xml_pages.append(f'    <changefreq>{freq}</changefreq>')
    xml_pages.append(f'    <priority>{pri}</priority>')
    xml_pages.append('  </url>')

# Programmatic SEO Location & Category Hubs
regions = ['manhattan', 'brooklyn', 'queens', 'bronx', 'staten-island', 'bergen-county-nj', 'hudson-county-nj']
categories = ['electronics', 'furniture', 'fashion', 'baby-kids', 'home-garden', 'food-groceries', 'health-beauty', 'pet-supplies']

for r in regions:
    xml_pages.append('  <url>')
    xml_pages.append(f'    <loc>https://moon-oh.com/explore/{r}</loc>')
    xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
    xml_pages.append('    <changefreq>daily</changefreq>')
    xml_pages.append('    <priority>0.8</priority>')
    xml_pages.append('  </url>')
    for c in categories:
        xml_pages.append('  <url>')
        xml_pages.append(f'    <loc>https://moon-oh.com/explore/{r}/{c}</loc>')
        xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
        xml_pages.append('    <changefreq>daily</changefreq>')
        xml_pages.append('    <priority>0.7</priority>')
        xml_pages.append('  </url>')

xml_pages.append('</urlset>')
with open('sitemap-pages.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_pages))

# =========================================================================
# 2. sitemap-moonoh.xml (Moonoh User Items + Images)
# =========================================================================
xml_moonoh = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for item in moonoh_items:
    no = item.get('no', item.get('id', ''))
    url = generate_canonical_url(item.get('title'), item.get('rawTown', item.get('location', '')), no, is_ext=False)
    img = to_web_jpg(item.get('image', item.get('photo', '')))
    title = item.get('title', '')
    
    xml_moonoh.append('  <url>')
    xml_moonoh.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_moonoh.append(f'    <lastmod>{today_str}</lastmod>')
    xml_moonoh.append('    <changefreq>weekly</changefreq>')
    xml_moonoh.append('    <priority>0.7</priority>')
    if img and img.startswith('http'):
        xml_moonoh.append('    <image:image>')
        xml_moonoh.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        if title:
            xml_moonoh.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_moonoh.append('    </image:image>')
    xml_moonoh.append('  </url>')

xml_moonoh.append('</urlset>')
with open('sitemap-moonoh.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_moonoh))

# =========================================================================
# 3. sitemap-marketplace.xml (Karrot + HeyKorean)
# =========================================================================
xml_marketplace = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

all_market = karrot_items + heykorean_items
for item in all_market:
    item_id = item.get('id', '')
    url = generate_canonical_url(item.get('title'), item.get('location', ''), item_id, is_ext=True)
    img = to_web_jpg(item.get('image', ''))
    title = item.get('title', '')
    
    xml_marketplace.append('  <url>')
    xml_marketplace.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_marketplace.append(f'    <lastmod>{today_str}</lastmod>')
    xml_marketplace.append('    <changefreq>daily</changefreq>')
    xml_marketplace.append('    <priority>0.6</priority>')
    if img and img.startswith('http'):
        xml_marketplace.append('    <image:image>')
        xml_marketplace.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        if title:
            xml_marketplace.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_marketplace.append('    </image:image>')
    xml_marketplace.append('  </url>')

xml_marketplace.append('</urlset>')
with open('sitemap-marketplace.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_marketplace))

# =========================================================================
# 4. sitemap-food-rescue.xml (Kim'C Market Items)
# =========================================================================
xml_food = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for item in food_rescue_items:
    item_id = item.get('id', '')
    url = generate_canonical_url(item.get('title'), item.get('location', ''), item_id, is_ext=True)
    img = to_web_jpg(item.get('image', ''))
    title = item.get('title', '')
    
    xml_food.append('  <url>')
    xml_food.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_food.append(f'    <lastmod>{today_str}</lastmod>')
    xml_food.append('    <changefreq>daily</changefreq>')
    xml_food.append('    <priority>0.7</priority>')
    if img and img.startswith('http'):
        xml_food.append('    <image:image>')
        xml_food.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        if title:
            xml_food.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_food.append('    </image:image>')
    xml_food.append('  </url>')

xml_food.append('</urlset>')
with open('sitemap-food-rescue.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_food))

# =========================================================================
# 5. sitemap-shops.xml (Local Shop Hubs)
# =========================================================================
xml_shops = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for s_id, s_info in local_shops_data.get('shops', {}).items():
    url = f"https://moon-oh.com/local-shops/{s_id}"
    img = s_info.get('primary_image_url') or s_info.get('logo_url') or ''
    name = s_info.get('name', '')
    
    xml_shops.append('  <url>')
    xml_shops.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_shops.append(f'    <lastmod>{today_str}</lastmod>')
    xml_shops.append('    <changefreq>weekly</changefreq>')
    xml_shops.append('    <priority>0.8</priority>')
    if img and img.startswith('http'):
        xml_shops.append('    <image:image>')
        xml_shops.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        if name:
            xml_shops.append(f'      <image:title>{escape_xml(name)}</image:title>')
        xml_shops.append('    </image:image>')
    xml_shops.append('  </url>')

xml_shops.append('</urlset>')
with open('sitemap-shops.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_shops))

# =========================================================================
# 6. sitemap-local-products.xml (900 Local Products + Images)
# =========================================================================
xml_local_prods = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for p in local_shops_data.get('products', []):
    shop_id = p.get('shop_id', '')
    slug = p.get('slug', '')
    url = f"https://moon-oh.com/local-product/{shop_id}/{slug}"
    img = p.get('image_source_url') or p.get('primary_image_url') or ''
    title = p.get('title', '')
    
    xml_local_prods.append('  <url>')
    xml_local_prods.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_local_prods.append(f'    <lastmod>{today_str}</lastmod>')
    xml_local_prods.append('    <changefreq>daily</changefreq>')
    xml_local_prods.append('    <priority>0.8</priority>')
    if img and img.startswith('http'):
        xml_local_prods.append('    <image:image>')
        xml_local_prods.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        if title:
            xml_local_prods.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_local_prods.append('    </image:image>')
    xml_local_prods.append('  </url>')

xml_local_prods.append('</urlset>')
with open('sitemap-local-products.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_local_prods))

# =========================================================================
# 7. sitemap-index.xml (Master Index)
# =========================================================================
xml_index = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             '  <sitemap><loc>https://moon-oh.com/sitemap-pages.xml</loc><lastmod>' + today_str + '</lastmod></sitemap>',
             '  <sitemap><loc>https://moon-oh.com/sitemap-moonoh.xml</loc><lastmod>' + today_str + '</lastmod></sitemap>',
             '  <sitemap><loc>https://moon-oh.com/sitemap-marketplace.xml</loc><lastmod>' + today_str + '</lastmod></sitemap>',
             '  <sitemap><loc>https://moon-oh.com/sitemap-food-rescue.xml</loc><lastmod>' + today_str + '</lastmod></sitemap>',
             '  <sitemap><loc>https://moon-oh.com/sitemap-shops.xml</loc><lastmod>' + today_str + '</lastmod></sitemap>',
             '  <sitemap><loc>https://moon-oh.com/sitemap-local-products.xml</loc><lastmod>' + today_str + '</lastmod></sitemap>',
             '</sitemapindex>']

with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_index))

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_index))

print("✅ All XML Sitemaps successfully regenerated!")
