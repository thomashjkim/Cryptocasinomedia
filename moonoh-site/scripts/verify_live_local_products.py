import urllib.request
import re

test_urls = [
    'https://moon-oh.com/local-product/sey-coffee/oma-plot',
    'https://moon-oh.com/local-product/front-general-store/tory-repeated-stitch-leather-belt-2332-2333-2334',
    'https://moon-oh.com/local-product/mirth-vintage/60s-lace-skirt-set',
    'https://moon-oh.com/local-product/salter-house/gift-wrap',
    'https://moon-oh.com/local-product/big-night/24k-gold-plated-0-75-0-5-oz-jigger',
    'https://moon-oh.com/local-product/pop-up-grocer/prind'
]

print("================================================================================")
print("🔍 TESTING LIVE PRODUCTION LOCAL PRODUCT DETAIL URLS")
print("================================================================================")

for u in test_urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            has_h1 = '<h1' in body
            has_not_found = 'Product Not Found' in body
            title_m = re.search(r'<title>(.*?)</title>', body)
            title = title_m.group(1) if title_m else 'No title'
            print(f"URL: {u}")
            print(f"  • HTTP: {resp.status} | Found: {not has_not_found} | Title: {title}")
    except Exception as e:
        print(f"URL: {u} | ERROR: {e}")

print("================================================================================")
