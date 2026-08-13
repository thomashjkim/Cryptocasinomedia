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
    return clean

# 1. Load Moonoh Items
with open('netlify/functions/moonoh-items-data.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m = re.search(r'export const realMoonohItems = (\[.*?\]);', code, re.DOTALL)
moonoh_items = json.loads(m.group(1)) if m else []

# 2. Load Food Rescue Items
with open('netlify/functions/food-rescue-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m = re.search(r'export const realFoodRescueItems = (\[.*?\]);', code, re.DOTALL)
food_rescue_items = json.loads(m.group(1)) if m else []

# 3. Load External Items
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', code, re.DOTALL)
m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', code, re.DOTALL)
karrot_items = json.loads(m_karrot.group(1)) if m_karrot else []
heykorean_items = json.loads(m_hey.group(1)) if m_hey else []

# 4. Load Local Shops
local_shops_data = {}
if os.path.exists('local_shops_data.json'):
    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        local_shops_data = json.load(f)

print(f'Loaded: {len(moonoh_items)} Moonoh, {len(food_rescue_items)} KimC, {len(karrot_items)} Karrot, {len(heykorean_items)} HeyKorean, {len(local_shops_data.get("products", []))} Local Shop items')

# --- Build sitemap-food-rescue.xml ---
xml_fr = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
          '  <url>',
          '    <loc>https://moon-oh.com/explore/food-rescue</loc>',
          f'    <lastmod>{today_str}</lastmod>',
          '    <changefreq>daily</changefreq>',
          '    <priority>0.9</priority>',
          '  </url>']

for item in food_rescue_items:
    slug = clean_slug(item.get('title', 'item'))
    item_id = item.get('id', '')
    url = f"https://moon-oh.com/item/{slug}-brooklyn-ny-ext-{item_id}"
    img = item.get('image', '')
    title = item.get('title', '')
    
    xml_fr.append('  <url>')
    xml_fr.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_fr.append(f'    <lastmod>{today_str}</lastmod>')
    xml_fr.append('    <changefreq>daily</changefreq>')
    xml_fr.append('    <priority>0.8</priority>')
    if img:
        xml_fr.append('    <image:image>')
        xml_fr.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        xml_fr.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_fr.append('    </image:image>')
    xml_fr.append('  </url>')

xml_fr.append('</urlset>')
with open('sitemap-food-rescue.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_fr))
print('Saved sitemap-food-rescue.xml')

# --- Build sitemap-external.xml ---
xml_ext = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
           '  <url>',
           '    <loc>https://moon-oh.com/explore/marketplaces</loc>',
           f'    <lastmod>{today_str}</lastmod>',
           '    <changefreq>daily</changefreq>',
           '    <priority>0.8</priority>',
           '  </url>']

for item in karrot_items + heykorean_items:
    slug = clean_slug(item.get('title', 'item'))
    loc = clean_slug(item.get('location', 'nyc-ny'))
    item_id = item.get('id', '')
    url = f"https://moon-oh.com/item/{slug}-{loc}-ext-{item_id}"
    img = to_web_jpg(item.get('image', ''))
    title = item.get('title', '')
    
    xml_ext.append('  <url>')
    xml_ext.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_ext.append(f'    <lastmod>{today_str}</lastmod>')
    xml_ext.append('    <changefreq>daily</changefreq>')
    xml_ext.append('    <priority>0.7</priority>')
    if img and img.startswith('http'):
        xml_ext.append('    <image:image>')
        xml_ext.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        xml_ext.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_ext.append('    </image:image>')
    xml_ext.append('  </url>')

xml_ext.append('</urlset>')
with open('sitemap-external.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_ext))
print('Saved sitemap-external.xml')

# --- Build sitemap-local-shops.xml ---
xml_local = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
             '  <url>',
             '    <loc>https://moon-oh.com/explore/local-shops</loc>',
             f'    <lastmod>{today_str}</lastmod>',
             '    <changefreq>daily</changefreq>',
             '    <priority>0.8</priority>',
             '  </url>']

for prod in local_shops_data.get('products', []):
    shop_id = prod.get('shop_id', '')
    slug = prod.get('slug', '')
    url = f"https://moon-oh.com/local-product/{shop_id}/{slug}"
    img = prod.get('image_source_url', '')
    title = prod.get('title', '')
    
    xml_local.append('  <url>')
    xml_local.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_local.append(f'    <lastmod>{today_str}</lastmod>')
    xml_local.append('    <changefreq>daily</changefreq>')
    xml_local.append('    <priority>0.7</priority>')
    if img and img.startswith('http'):
        xml_local.append('    <image:image>')
        xml_local.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        xml_local.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_local.append('    </image:image>')
    xml_local.append('  </url>')

xml_local.append('</urlset>')
with open('sitemap-local-shops.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_local))
print('Saved sitemap-local-shops.xml')

# --- Build main sitemap.xml (Static + Categories/Regions + Moonoh Items) ---
xml_main = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
            '  <url>',
            '    <loc>https://moon-oh.com/</loc>',
            f'    <lastmod>{today_str}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>1.0</priority>',
            '  </url>',
            '  <url>',
            '    <loc>https://moon-oh.com/explore</loc>',
            f'    <lastmod>{today_str}</lastmod>',
            '    <changefreq>daily</changefreq>',
            '    <priority>0.9</priority>',
            '  </url>']

# Add Category & Region aggregated explore pages
regions = ['manhattan', 'queens', 'brooklyn', 'flushing', 'bayside', 'astoria', 'fort-lee-nj', 'bergen-county-nj']
categories = ['electronics', 'furniture', 'womens-fashion', 'mens-fashion', 'shoes', 'home-garden', 'health-beauty', 'pet-supplies', 'baby-kids', 'sports-leisure', 'food-groceries']

for reg in regions:
    xml_main.append('  <url>')
    xml_main.append(f'    <loc>https://moon-oh.com/explore/{reg}</loc>')
    xml_main.append(f'    <lastmod>{today_str}</lastmod>')
    xml_main.append('    <changefreq>daily</changefreq>')
    xml_main.append('    <priority>0.8</priority>')
    xml_main.append('  </url>')

for cat in categories:
    xml_main.append('  <url>')
    xml_main.append(f'    <loc>https://moon-oh.com/explore/{cat}</loc>')
    xml_main.append(f'    <lastmod>{today_str}</lastmod>')
    xml_main.append('    <changefreq>daily</changefreq>')
    xml_main.append('    <priority>0.8</priority>')
    xml_main.append('  </url>')

for reg in regions:
    for cat in categories:
        xml_main.append('  <url>')
        xml_main.append(f'    <loc>https://moon-oh.com/explore/{reg}/{cat}</loc>')
        xml_main.append(f'    <lastmod>{today_str}</lastmod>')
        xml_main.append('    <changefreq>daily</changefreq>')
        xml_main.append('    <priority>0.7</priority>')
        xml_main.append('  </url>')

# Add Moonoh Items
for item in moonoh_items:
    slug = clean_slug(item.get('title', 'item'))
    loc = clean_slug(item.get('rawTown', item.get('location', 'nyc-ny')))
    no = item.get('no', item.get('id', ''))
    url = f"https://moon-oh.com/item/{slug}-{loc}-{no}"
    img = to_web_jpg(item.get('image', item.get('photo', '')))
    title = item.get('title', '')
    
    xml_main.append('  <url>')
    xml_main.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_main.append(f'    <lastmod>{today_str}</lastmod>')
    xml_main.append('    <changefreq>daily</changefreq>')
    xml_main.append('    <priority>0.8</priority>')
    if img:
        abs_img = img if img.startswith('http') else f"https://moon-oh.com{img}"
        xml_main.append('    <image:image>')
        xml_main.append(f'      <image:loc>{escape_xml(abs_img)}</image:loc>')
        xml_main.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_main.append('    </image:image>')
    xml_main.append('  </url>')

xml_main.append('</urlset>')
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_main))
print('Saved sitemap.xml')

# --- Build sitemap-index.xml ---
xml_idx = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
           '  <sitemap>',
           '    <loc>https://moon-oh.com/sitemap.xml</loc>',
           f'    <lastmod>{today_str}</lastmod>',
           '  </sitemap>',
           '  <sitemap>',
           '    <loc>https://moon-oh.com/sitemap-food-rescue.xml</loc>',
           f'    <lastmod>{today_str}</lastmod>',
           '  </sitemap>',
           '  <sitemap>',
           '    <loc>https://moon-oh.com/sitemap-external.xml</loc>',
           f'    <lastmod>{today_str}</lastmod>',
           '  </sitemap>',
           '  <sitemap>',
           '    <loc>https://moon-oh.com/sitemap-local-shops.xml</loc>',
           f'    <lastmod>{today_str}</lastmod>',
           '  </sitemap>',
           '</sitemapindex>']

with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_idx))
print('Saved sitemap-index.xml')
