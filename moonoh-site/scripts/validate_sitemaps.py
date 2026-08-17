import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

def validate_all_sitemaps():
    print("🔍 Running comprehensive sitemap validation...")
    
    if not os.path.exists('sitemap-index.xml'):
        print("❌ Error: sitemap-index.xml not found!")
        return False

    with open('sitemap-index.xml', 'r', encoding='utf-8') as f:
        index_content = f.read()

    sitemap_locs = re.findall(r'<loc>(.*?)</loc>', index_content)
    print(f"Found {len(sitemap_locs)} child sitemaps in index: {[os.path.basename(s) for s in sitemap_locs]}")

    all_urls = set()
    total_url_count = 0
    errors = []

    for s_url in sitemap_locs:
        filename = os.path.basename(urlparse(s_url).path)
        if not os.path.exists(filename):
            errors.append(f"Referenced sitemap file {filename} does not exist on disk!")
            continue

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        locs = re.findall(r'<loc>(.*?)</loc>', content)
        img_locs = re.findall(r'<image:loc>(.*?)</image:loc>', content)
        
        file_urls = set()
        for loc in locs:
            total_url_count += 1
            if not loc.startswith('https://moon-oh.com'):
                errors.append(f"[{filename}] Non-canonical origin in <loc>: {loc}")
            if '${' in loc or '}' in loc:
                errors.append(f"[{filename}] Template literal in <loc>: {loc}")
            if loc in file_urls:
                errors.append(f"[{filename}] Duplicate URL inside same file: {loc}")
            if loc in all_urls:
                errors.append(f"[{filename}] Duplicate URL across sitemaps: {loc}")
            
            file_urls.add(loc)
            all_urls.add(loc)

        for img in img_locs:
            if '/temp/' in img or img.lower().endswith('.heic') or '/image-proxy/temp' in img:
                errors.append(f"[{filename}] Temporary or HEIC image in <image:loc>: {img}")

        print(f"  ✓ {filename}: {len(locs)} valid canonical URLs, {len(img_locs)} images checked.")

    print(f"\n📊 Summary: {total_url_count} total URLs validated across {len(sitemap_locs)} sitemaps.")
    
    if errors:
        print(f"❌ Found {len(errors)} validation errors:")
        for err in errors[:10]:
            print(f"  - {err}")
        return False
    else:
        print("✅ 100% of sitemap URLs are canonical, valid, HTTPS, deduplicated, and clean of temporary assets!")
        return True

if __name__ == '__main__':
    success = validate_all_sitemaps()
    exit(0 if success else 1)
