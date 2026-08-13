#!/usr/bin/env python3
"""
generate_aggregate_pages.py
Generates static SEO aggregate pages for:
  - /explore/{region}              (e.g. /explore/queens)
  - /explore/{category}            (e.g. /explore/furniture)
  - /explore/{region}/{category}   (e.g. /explore/queens/furniture)
Each page:
  1. Has unique SEO title/meta description/H1
  2. Shows a JS snippet that pre-selects the right filter in explore.html
  3. Has proper canonical, breadcrumb schema, and sitemap entry
"""

import os
import sys
import json
import re

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

# 0. Validate JS script syntax across all core HTML files before generating pages
ret = os.system("node validate_scripts.js")
if ret != 0:
    print("❌ JS Syntax Validation Failed! Aborting page generation.")
    sys.exit(1)

REGIONS = [
    {'slug': 'new-york-area',    'name': 'New York Area',              'borough': None},
    {'slug': 'manhattan',        'name': 'Manhattan, NY',              'borough': 'Manhattan'},
    {'slug': 'queens',           'name': 'Queens, NY',                 'borough': 'Queens'},
    {'slug': 'brooklyn',         'name': 'Brooklyn, NY',               'borough': 'Brooklyn'},
    {'slug': 'bronx',            'name': 'Bronx, NY',                  'borough': 'Bronx'},
    {'slug': 'flushing',         'name': 'Flushing, Queens, NY',       'borough': 'Queens'},
    {'slug': 'bayside',          'name': 'Bayside, Queens, NY',        'borough': 'Queens'},
    {'slug': 'astoria',          'name': 'Astoria, Queens, NY',        'borough': 'Queens'},
    {'slug': 'fort-lee-nj',      'name': 'Fort Lee, NJ',               'borough': 'Bergen County'},
    {'slug': 'bergen-county-nj', 'name': 'Bergen County, NJ',          'borough': 'Bergen County'},
]

CATEGORIES = [
    {'slug': 'food-groceries', 'name': 'Food & Groceries',         'filter': 'Food & Groceries'},
    {'slug': 'furniture',      'name': 'Furniture',                'filter': 'Furniture'},
    {'slug': 'electronics',    'name': 'Electronics & Appliances', 'filter': 'Electronics & Appliances'},
    {'slug': 'fashion',        'name': "Women's & Men's Fashion",  'filter': "Women's fashion"},
    {'slug': 'shoes',          'name': 'Shoes',                    'filter': 'Shoes'},
    {'slug': 'baby-kids',      'name': 'Baby & Kids',              'filter': 'Baby & kids'},
    {'slug': 'health-beauty',  'name': 'Health & Beauty',          'filter': 'Health & beauty'},
    {'slug': 'home-garden',    'name': 'Home & Garden',            'filter': 'Home, garden & DIY'},
    {'slug': 'sports-leisure', 'name': 'Sports & Leisure',         'filter': 'Sports & leisure'},
    {'slug': 'luggages-bags',  'name': 'Luggages & Bags',          'filter': 'Luggages & bags'},
    {'slug': 'free',           'name': 'Free Items',               'filter': 'Free'},
]

SITE_DOMAIN = 'https://moon-oh.com'


def make_page(canonical_path, title, h1, meta_desc, location_filter, category_filter, breadcrumbs):
    """Generate an HTML aggregate page that pre-filters explore.html."""
    location_js = f"'{location_filter}'" if location_filter else 'null'
    category_js = f"'{category_filter}'" if category_filter else 'null'

    breadcrumb_items_html = ''
    for i, bc in enumerate(breadcrumbs):
        if bc.get('url'):
            breadcrumb_items_html += f'<li><a href="{bc["url"]}">{bc["label"]}</a></li>'
        else:
            breadcrumb_items_html += f'<li>{bc["label"]}</li>'

    # Build JSON-LD breadcrumb schema
    schema_items = []
    for i, bc in enumerate(breadcrumbs):
        schema_items.append({
            "@type": "ListItem",
            "position": i + 1,
            "name": bc['label'],
            "item": SITE_DOMAIN + bc.get('url', canonical_path)
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": schema_items
    }

    # Build URL params for explore redirect
    params = []
    if location_filter:
        params.append(f'location={location_filter.replace(" ", "+")}')
    if category_filter:
        params.append(f'category={category_filter.replace(" ", "+")}')
    redirect_url = '/explore' + ('?' + '&'.join(params) if params else '')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} | Moonoh</title>
  <meta name="description" content="{meta_desc}"/>
  <link rel="canonical" href="{SITE_DOMAIN}{canonical_path}"/>
  <meta property="og:title" content="{title} | Moonoh"/>
  <meta property="og:description" content="{meta_desc}"/>
  <meta property="og:url" content="{SITE_DOMAIN}{canonical_path}"/>
  <meta property="og:type" content="website"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet"/>
  <script type="application/ld+json">
  {json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; background: #FAFAFA; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
    .redirect-box {{ text-align: center; padding: 40px 24px; max-width: 480px; }}
    .redirect-box h1 {{ font-size: 24px; font-weight: 800; color: #111827; margin-bottom: 12px; }}
    .redirect-box p {{ font-size: 15px; color: #6B7280; margin-bottom: 28px; line-height: 1.6; }}
    .redirect-btn {{ display: inline-block; background: #4F46E5; color: white; font-weight: 700; font-size: 15px; padding: 14px 32px; border-radius: 999px; text-decoration: none; transition: background 0.2s; }}
    .redirect-btn:hover {{ background: #4338CA; }}
    .breadcrumb {{ font-size: 13px; color: #9CA3AF; margin-bottom: 20px; }}
    .breadcrumb a {{ color: #6B7280; text-decoration: none; }}
    .breadcrumb li {{ display: inline; }}
    .breadcrumb li + li::before {{ content: " › "; }}
  </style>
</head>
<body>
  <div class="redirect-box">
    <nav aria-label="breadcrumb">
      <ul class="breadcrumb">
        {breadcrumb_items_html}
      </ul>
    </nav>
    <h1>{h1}</h1>
    <p>{meta_desc}</p>
    <a class="redirect-btn" href="{redirect_url}" id="explore-link">Browse Listings →</a>
  </div>
  <script>
    // Auto-redirect to filtered explore page after brief moment
    (function() {{
      var target = {json.dumps(redirect_url)};
      window.location.replace(target);
    }})();
  </script>
</body>
</html>"""
    return html


def write_page(rel_path, html_content):
    """Write page to disk, creating dirs as needed."""
    full_path = os.path.join(SITE_DIR, rel_path.lstrip('/'))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f'  Written: /{rel_path}')


pages = []  # list of canonical paths for sitemap

# ─────────────────────────────────────────────
# Region-only pages: /explore/queens
# ─────────────────────────────────────────────
for region in REGIONS:
    path = f"/explore/{region['slug']}/index.html"
    canonical = f"/explore/{region['slug']}"
    title = f"Used Items for Sale in {region['name']}"
    h1 = f"{region['name']} Secondhand Marketplace"
    meta_desc = (f"Browse used items, furniture, electronics, clothing and more "
                 f"for sale in {region['name']}. Local Korean-American community marketplace on Moonoh.")
    breadcrumbs = [
        {'label': 'Home', 'url': '/'},
        {'label': 'Explore', 'url': '/explore'},
        {'label': region['name']},
    ]
    html = make_page(canonical, title, h1, meta_desc,
                     location_filter=region['borough'], category_filter=None, breadcrumbs=breadcrumbs)
    write_page(path, html)
    pages.append(canonical)

# ─────────────────────────────────────────────
# Category-only pages: /explore/furniture
# ─────────────────────────────────────────────
for cat in CATEGORIES:
    path = f"/explore/{cat['slug']}/index.html"
    canonical = f"/explore/{cat['slug']}"
    title = f"Used {cat['name']} for Sale Near NYC & NJ"
    h1 = f"{cat['name']} for Sale — NYC & NJ"
    meta_desc = (f"Find used {cat['name'].lower()} listings in the New York City and New Jersey area. "
                 f"Local deals on Moonoh — the Korean-American community marketplace.")
    breadcrumbs = [
        {'label': 'Home', 'url': '/'},
        {'label': 'Explore', 'url': '/explore'},
        {'label': cat['name']},
    ]
    html = make_page(canonical, title, h1, meta_desc,
                     location_filter=None, category_filter=cat['filter'], breadcrumbs=breadcrumbs)
    write_page(path, html)
    pages.append(canonical)

# ─────────────────────────────────────────────
# Region + Category combo pages: /explore/queens/furniture
# ─────────────────────────────────────────────
for region in REGIONS:
    for cat in CATEGORIES:
        path = f"/explore/{region['slug']}/{cat['slug']}/index.html"
        canonical = f"/explore/{region['slug']}/{cat['slug']}"
        title = f"Used {cat['name']} for Sale in {region['name']}"
        h1 = f"{cat['name']} in {region['name']}"
        meta_desc = (f"Buy used {cat['name'].lower()} in {region['name']}. "
                     f"Local listings from Korean-American community on Moonoh.")
        breadcrumbs = [
            {'label': 'Home', 'url': '/'},
            {'label': 'Explore', 'url': '/explore'},
            {'label': region['name'], 'url': f"/explore/{region['slug']}"},
            {'label': cat['name']},
        ]
        html = make_page(canonical, title, h1, meta_desc,
                         location_filter=region['borough'], category_filter=cat['filter'],
                         breadcrumbs=breadcrumbs)
        write_page(path, html)
        pages.append(canonical)

# ─────────────────────────────────────────────
# Update sitemap.xml with new pages
# ─────────────────────────────────────────────
sitemap_path = os.path.join(SITE_DIR, 'sitemap.xml')
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap_content = f.read()

# Build new URL entries
new_entries = ''
for canonical in pages:
    new_entries += f"""  <url>
    <loc>{SITE_DOMAIN}{canonical}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>\n"""

# Insert before closing </urlset>
if new_entries and '</urlset>' in sitemap_content:
    # Remove any previously generated aggregate entries first
    sitemap_content = re.sub(
        r'  <!-- AGGREGATE PAGES START -->.*?<!-- AGGREGATE PAGES END -->\n',
        '', sitemap_content, flags=re.DOTALL
    )
    import re
    insert_marker = '</urlset>'
    aggregate_block = f'  <!-- AGGREGATE PAGES START -->\n{new_entries}  <!-- AGGREGATE PAGES END -->\n'
    sitemap_content = sitemap_content.replace(insert_marker, aggregate_block + insert_marker)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f'\n✅ sitemap.xml updated with {len(pages)} aggregate page URLs')

print(f'\n✅ Generated {len(pages)} aggregate pages total:')
print(f'   - {len(REGIONS)} region pages (/explore/queens etc.)')
print(f'   - {len(CATEGORIES)} category pages (/explore/furniture etc.)')
print(f'   - {len(REGIONS) * len(CATEGORIES)} combo pages (/explore/queens/furniture etc.)')
