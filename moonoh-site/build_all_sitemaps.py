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

# =========================================================================
# 1. sitemap-pages.xml (Static + Hub / Category / Region Landing Pages)
# =========================================================================
xml_pages = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

static_pages = [
    ('/', '1.0', 'daily'),
    ('/explore', '0.9', 'daily'),
    ('/explore/food-rescue', '0.9', 'daily'),
    ('/explore/marketplaces', '0.8', 'daily'),
    ('/explore/local-shops', '0.8', 'daily'),
    ('/about', '0.5', 'monthly'),
    ('/press', '0.5', 'monthly'),
    ('/contact', '0.5', 'monthly'),
    ('/terms', '0.3', 'monthly'),
    ('/privacy', '0.3', 'monthly'),
    ('/return-policy', '0.3', 'monthly'),
    ('/fraud-prevention', '0.3', 'monthly'),
    ('/disclaimer', '0.3', 'monthly'),
]

for path, priority, freq in static_pages:
    xml_pages.append('  <url>')
    xml_pages.append(f'    <loc>https://moon-oh.com{path}</loc>')
    xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
    xml_pages.append(f'    <changefreq>{freq}</changefreq>')
    xml_pages.append(f'    <priority>{priority}</priority>')
    xml_pages.append('  </url>')

regions = ['manhattan', 'queens', 'brooklyn', 'flushing', 'bayside', 'astoria', 'fort-lee-nj', 'bergen-county-nj']
categories = ['electronics', 'furniture', 'womens-fashion', 'mens-fashion', 'shoes', 'home-garden', 'health-beauty', 'pet-supplies', 'baby-kids', 'sports-leisure', 'food-groceries', 'arts-books-music', 'antiques']

for reg in regions:
    xml_pages.append('  <url>')
    xml_pages.append(f'    <loc>https://moon-oh.com/explore/{reg}</loc>')
    xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
    xml_pages.append('    <changefreq>daily</changefreq>')
    xml_pages.append('    <priority>0.8</priority>')
    xml_pages.append('  </url>')

for cat in categories:
    xml_pages.append('  <url>')
    xml_pages.append(f'    <loc>https://moon-oh.com/explore/{cat}</loc>')
    xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
    xml_pages.append('    <changefreq>daily</changefreq>')
    xml_pages.append('    <priority>0.8</priority>')
    xml_pages.append('  </url>')

for reg in regions:
    for cat in categories:
        xml_pages.append('  <url>')
        xml_pages.append(f'    <loc>https://moon-oh.com/explore/{reg}/{cat}</loc>')
        xml_pages.append(f'    <lastmod>{today_str}</lastmod>')
        xml_pages.append('    <changefreq>daily</changefreq>')
        xml_pages.append('    <priority>0.7</priority>')
        xml_pages.append('  </url>')

xml_pages.append('</urlset>')
with open('sitemap-pages.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_pages))
print('✅ Saved sitemap-pages.xml')


# =========================================================================
# 2. sitemap-moonoh.xml (Moonoh User Secondhand Items + Images)
# =========================================================================
xml_moonoh = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for item in moonoh_items:
    slug = clean_slug(item.get('title', 'item'))
    loc = clean_slug(item.get('rawTown', item.get('location', 'nyc-ny')))
    no = item.get('no', item.get('id', ''))
    url = f"https://moon-oh.com/item/{slug}-{loc}-{no}"
    img = to_web_jpg(item.get('image', item.get('photo', '')))
    title = item.get('title', '')
    
    xml_moonoh.append('  <url>')
    xml_moonoh.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_moonoh.append(f'    <lastmod>{today_str}</lastmod>')
    xml_moonoh.append('    <changefreq>daily</changefreq>')
    xml_moonoh.append('    <priority>0.8</priority>')
    if img:
        abs_img = img if img.startswith('http') else f"https://moon-oh.com{img}"
        xml_moonoh.append('    <image:image>')
        xml_moonoh.append(f'      <image:loc>{escape_xml(abs_img)}</image:loc>')
        xml_moonoh.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_moonoh.append('    </image:image>')
    xml_moonoh.append('  </url>')

xml_moonoh.append('</urlset>')
with open('sitemap-moonoh.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_moonoh))
print('✅ Saved sitemap-moonoh.xml')


# =========================================================================
# 3. sitemap-marketplace.xml (Karrot & HeyKorean Items + Images)
# =========================================================================
xml_market = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for item in karrot_items + heykorean_items:
    slug = clean_slug(item.get('title', 'item'))
    loc = clean_slug(item.get('location', 'nyc-ny'))
    item_id = item.get('id', '')
    url = f"https://moon-oh.com/item/{slug}-{loc}-ext-{item_id}"
    img = to_web_jpg(item.get('image', ''))
    title = item.get('title', '')
    
    xml_market.append('  <url>')
    xml_market.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_market.append(f'    <lastmod>{today_str}</lastmod>')
    xml_market.append('    <changefreq>daily</changefreq>')
    xml_market.append('    <priority>0.7</priority>')
    if img and img.startswith('http'):
        xml_market.append('    <image:image>')
        xml_market.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        xml_market.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_market.append('    </image:image>')
    xml_market.append('  </url>')

xml_market.append('</urlset>')
with open('sitemap-marketplace.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_market))
print('✅ Saved sitemap-marketplace.xml')


# =========================================================================
# 4. sitemap-food-rescue.xml (Kim'C Market Fight Food Waste Items + Images)
# =========================================================================
xml_fr = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

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
print('✅ Saved sitemap-food-rescue.xml')


# =========================================================================
# 5. sitemap-local-products.xml (Curated Local Shop Products + Images)
# =========================================================================
xml_local_prod = ['<?xml version="1.0" encoding="UTF-8"?>',
                  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

for prod in local_shops_data.get('products', []):
    shop_id = prod.get('shop_id', '')
    slug = prod.get('slug', '')
    url = f"https://moon-oh.com/local-product/{shop_id}/{slug}"
    img = prod.get('image_source_url', '')
    title = prod.get('title', '')
    
    xml_local_prod.append('  <url>')
    xml_local_prod.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_local_prod.append(f'    <lastmod>{today_str}</lastmod>')
    xml_local_prod.append('    <changefreq>daily</changefreq>')
    xml_local_prod.append('    <priority>0.7</priority>')
    if img and img.startswith('http'):
        xml_local_prod.append('    <image:image>')
        xml_local_prod.append(f'      <image:loc>{escape_xml(img)}</image:loc>')
        xml_local_prod.append(f'      <image:title>{escape_xml(title)}</image:title>')
        xml_local_prod.append('    </image:image>')
    xml_local_prod.append('  </url>')

xml_local_prod.append('</urlset>')
with open('sitemap-local-products.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_local_prod))
print('✅ Saved sitemap-local-products.xml')


# =========================================================================
# 6. sitemap-shops.xml (Local Shop Brand / Directory Hub Pages)
# =========================================================================
xml_shops = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for shop_id, shop_info in local_shops_data.get('shops', {}).items():
    url = f"https://moon-oh.com/local-shops/{shop_id}"
    xml_shops.append('  <url>')
    xml_shops.append(f'    <loc>{escape_xml(url)}</loc>')
    xml_shops.append(f'    <lastmod>{today_str}</lastmod>')
    xml_shops.append('    <changefreq>weekly</changefreq>')
    xml_shops.append('    <priority>0.8</priority>')
    xml_shops.append('  </url>')

xml_shops.append('</urlset>')
with open('sitemap-shops.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_shops))
print('✅ Saved sitemap-shops.xml')


# =========================================================================
# 7. sitemap-index.xml (Master Index) & sitemap.xml fallback
# =========================================================================
sub_sitemaps = [
    'https://moon-oh.com/sitemap-pages.xml',
    'https://moon-oh.com/sitemap-moonoh.xml',
    'https://moon-oh.com/sitemap-marketplace.xml',
    'https://moon-oh.com/sitemap-food-rescue.xml',
    'https://moon-oh.com/sitemap-local-products.xml',
    'https://moon-oh.com/sitemap-shops.xml'
]

xml_idx = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for sm_url in sub_sitemaps:
    xml_idx.append('  <sitemap>')
    xml_idx.append(f'    <loc>{sm_url}</loc>')
    xml_idx.append(f'    <lastmod>{today_str}</lastmod>')
    xml_idx.append('  </sitemap>')

xml_idx.append('</sitemapindex>')
sitemap_index_content = '\n'.join(xml_idx)

with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_index_content)

# Keep sitemap.xml identical to sitemap-index.xml so both /sitemap.xml and /sitemap-index.xml work seamlessly
with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_index_content)

print('✅ Saved sitemap-index.xml and sitemap.xml (Master Index)')
