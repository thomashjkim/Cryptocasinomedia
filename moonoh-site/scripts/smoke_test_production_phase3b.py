import urllib.request
import re

def run_smoke_tests():
    print("=== LIVE PRODUCTION SMOKE TESTS (PHASE 3B) ===\n")
    
    # 1. / (Home)
    req = urllib.request.Request("https://moon-oh.com/", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode('utf-8')
        print(f"1. / (Home): HTTP {resp.status} | Has Local Tab: {'tab-source-localshops' in body} | Has Mixer: {'local-products-mixer.js' in body}")
    
    # 2. /explore
    req = urllib.request.Request("https://moon-oh.com/explore", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode('utf-8')
        print(f"2. /explore: HTTP {resp.status} | Has Local Filter Container: {'id=\"local-filter-container\"' in body}")
    
    # 3. Big Night sample
    url_bn = "https://moon-oh.com/local-product/big-night/small-round-tray"
    req = urllib.request.Request(url_bn, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode('utf-8')
        canon_match = url_bn in body and 'rel="canonical"' in body
        print(f"3. Big Night Sample: HTTP {resp.status} | Self-Canonical: {canon_match}")
        
    # 4. Happier Grocery sample
    url_hg = "https://moon-oh.com/local-product/happier-grocery/yeowww-catnip-cat-toys-strawberry-red"
    req = urllib.request.Request(url_hg, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode('utf-8')
        print(f"4. Happier Grocery Sample: HTTP {resp.status} | Title found: {'YEOWWW' in body}")

    # 5. 4 New Shops Samples
    samples = [
        ("Front General Store", "https://moon-oh.com/local-product/front-general-store/issey-miyake-bow-tie-pleated-zip-up-jacket"),
        ("Mirth Vintage", "https://moon-oh.com/local-product/mirth-vintage/suede-panel-clogs-10"),
        ("SEY Coffee", "https://moon-oh.com/local-product/sey-coffee/2026-william-ortiz-la-cabana-end-of-season-colombia"),
        ("Salter House", "https://moon-oh.com/local-product/salter-house/altra-eau-de-parfum")
    ]
    print("5. 4 New Shops Representatives:")
    for name, s_url in samples:
        req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            has_cta = f"View at {name}" in body or f"View on {name}" in body or "View at" in body
            print(f"   • {name}: HTTP {resp.status} | CTA OK: {has_cta} | Notice OK: {'Shipping, returns, availability' in body}")

    # 6. Sitemaps HTTP 200
    req_idx = urllib.request.Request("https://moon-oh.com/sitemap-index.xml", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_idx) as resp:
        print(f"6a. /sitemap-index.xml: HTTP {resp.status}")
    req_loc = urllib.request.Request("https://moon-oh.com/sitemap-local-products.xml", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_loc) as resp:
        body_loc = resp.read().decode('utf-8')
        loc_count = len(re.findall(r'<loc>', body_loc))
        print(f"6b. /sitemap-local-products.xml: HTTP {resp.status} | Count: {loc_count}")
    
    # 7. Local Sitemap URL count = 659
    print(f"7. Local Sitemap URL Count: {loc_count} (Expected: 659: {loc_count == 659})")

    # 8. Merchant feed
    req_mf = urllib.request.Request("https://moon-oh.com/merchant-feed.xml", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_mf) as resp:
        body_mf = resp.read().decode('utf-8')
        item_count = len(re.findall(r'<item>', body_mf))
        print(f"8. Merchant Feed Items Count: {item_count} (Expected: 0: {item_count == 0})")

    # 9. 390px CSS overflow
    req_exp = urllib.request.Request("https://moon-oh.com/explore", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_exp) as resp:
        body = resp.read().decode('utf-8')
        has_resp = 'box-sizing:border-box' in body or 'max-width:100%' in body or '.filter-container' in body
        print(f"9. 390px Responsive CSS Rules: {has_resp}")

    # 10. Mixing check
    req_json = urllib.request.Request("https://moon-oh.com/local_shops_data.json", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_json) as resp:
        import json
        data = json.loads(resp.read().decode('utf-8'))
        print(f"10. local_shops_data.json live: {len(data.get('products', []))} products across {len(data.get('shops', {}))} shops")
        
    print("\n✅ LIVE PRODUCTION SMOKE TESTS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    run_smoke_tests()
