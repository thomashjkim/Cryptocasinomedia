import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_DIR = os.path.join(PROJECT_ROOT, "index", "local")

# 1. Discover all local HTML files
all_files = []
for root, dirs, files in os.walk(LOCAL_DIR):
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.join(root, f))

# 2. Define whitelist of authoritative pages that MUST remain indexed (index, follow)
# - The master directory hub (/local/)
# - All 51 state hubs (/local/{state}/)
# - Top 5 high-value state regulatory guides (California, New York, Texas, Florida, Nevada)
top_5_guides = [
    os.path.join(LOCAL_DIR, 'california', 'crypto-gambling-and-advertising-legal-regulatory-guide-california-2026', 'index.html'),
    os.path.join(LOCAL_DIR, 'new-york', 'crypto-gambling-and-advertising-legal-regulatory-guide-new-york-2026', 'index.html'),
    os.path.join(LOCAL_DIR, 'texas', 'crypto-gambling-and-advertising-legal-regulatory-guide-texas-2026', 'index.html'),
    os.path.join(LOCAL_DIR, 'florida', 'crypto-gambling-and-advertising-legal-regulatory-guide-florida-2026', 'index.html'),
    os.path.join(LOCAL_DIR, 'nevada', 'crypto-gambling-and-advertising-legal-regulatory-guide-nevada-2026', 'index.html'),
]

keep_index = set()
keep_index.add(os.path.join(LOCAL_DIR, 'index.html'))

for p in all_files:
    rel_path = os.path.relpath(p, LOCAL_DIR)
    parts = rel_path.split(os.sep)
    # State hubs have depth 2: e.g. "california/index.html"
    if len(parts) == 2 and parts[1] == 'index.html':
        keep_index.add(p)

for p in top_5_guides:
    if os.path.exists(p):
        keep_index.add(p)

to_noindex = [p for p in all_files if p not in keep_index]

print(f"Total local HTML files: {len(all_files)}")
print(f"Authoritative pages to KEEP INDEXED: {len(keep_index)}")
print(f"Thin programmatic pages to set NOINDEX, FOLLOW: {len(to_noindex)}")

# 3. Apply noindex, follow to the 829 thin programmatic doorway pages
noindex_meta = (
    '<meta name="robots" content="noindex, follow">\n'
    '    <meta name="googlebot" content="noindex, follow">\n'
    '    <meta name="bingbot" content="noindex, follow">'
)

modified_count = 0
for file_path in to_noindex:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing robots/googlebot/bingbot tags
    cleaned = re.sub(r'<meta\s+name=["\'](robots|googlebot|bingbot)["\']\s+content=["\'][^"\']*["\']>\s*', '', content)
    
    # Insert the noindex, follow block right after <meta name="description" ...> or <head>
    if '<meta name="description"' in cleaned:
        desc_end = cleaned.find('>', cleaned.find('<meta name="description"'))
        if desc_end != -1:
            new_content = cleaned[:desc_end+1] + '\n    ' + noindex_meta + cleaned[desc_end+1:]
        else:
            new_content = cleaned.replace('<head>', '<head>\n    ' + noindex_meta)
    else:
        new_content = cleaned.replace('<head>', '<head>\n    ' + noindex_meta)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    modified_count += 1

print(f"SUCCESS: Updated {modified_count} local pages to 'noindex, follow'!")

# 4. Ensure the 57 whitelisted pages explicitly have 'index, follow'
index_meta = (
    '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n'
    '    <meta name="googlebot" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n'
    '    <meta name="bingbot" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
)

for file_path in keep_index:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = re.sub(r'<meta\s+name=["\'](robots|googlebot|bingbot)["\']\s+content=["\'][^"\']*["\']>\s*', '', content)
    if '<meta name="description"' in cleaned:
        desc_end = cleaned.find('>', cleaned.find('<meta name="description"'))
        if desc_end != -1:
            new_content = cleaned[:desc_end+1] + '\n    ' + index_meta + cleaned[desc_end+1:]
        else:
            new_content = cleaned.replace('<head>', '<head>\n    ' + index_meta)
    else:
        new_content = cleaned.replace('<head>', '<head>\n    ' + index_meta)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"SUCCESS: Verified {len(keep_index)} authoritative pages have 'index, follow'!")

# 5. Regenerate index/local-sitemap.xml with ONLY the 57 indexed URLs
# (Per Google Guidelines: never submit noindex URLs in XML sitemaps)
sitemap_path = os.path.join(PROJECT_ROOT, "index", "local-sitemap.xml")

sitemap_urls = []
# Root local hub
sitemap_urls.append(("https://cryptocasinomedia.com/local/", "0.9"))

# Sorted state hubs
state_urls = []
guide_urls = []

for file_path in sorted(keep_index):
    rel_path = os.path.relpath(file_path, os.path.join(PROJECT_ROOT, "index"))
    # Format to URL: e.g. local/california/index.html -> https://cryptocasinomedia.com/local/california/
    url_path = rel_path.replace(os.sep, '/')
    if url_path.endswith('index.html'):
        url_path = url_path[:-len('index.html')]
    if not url_path.endswith('/'):
        url_path += '/'
    full_url = f"https://cryptocasinomedia.com/{url_path}"
    
    if full_url == "https://cryptocasinomedia.com/local/":
        continue
    elif "guide" in full_url:
        guide_urls.append((full_url, "0.8"))
    else:
        state_urls.append((full_url, "0.8"))

sitemap_urls.extend(state_urls)
sitemap_urls.extend(guide_urls)

sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

today_str = "2026-10-06"
for loc, priority in sitemap_urls:
    sitemap_lines.append(
        f'  <url><loc>{loc}</loc><lastmod>{today_str}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>'
    )
sitemap_lines.append('</urlset>\n')

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sitemap_lines))

print(f"SUCCESS: Regenerated {sitemap_path} with exactly {len(sitemap_urls)} authoritative URLs (0 noindex URLs)!")
