import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import re

def fetch(url, headers=None, timeout=15):
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode('utf-8', errors='ignore'), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='ignore'), dict(e.headers)
    except Exception as e:
        return 0, str(e), {}

def run_suite():
    print("=== 1. REPRESENTATIVE SCREENS VERIFICATION ===")
    screens = [
        ("Explore Hub", "https://moon-oh.com/explore"),
        ("Explore Local Shops", "https://moon-oh.com/explore/local-shops"),
        ("Happier Detail 1", "https://moon-oh.com/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups"),
        ("Happier Detail 2", "https://moon-oh.com/local-product/happier-grocery/if-you-care-baking-pan-loaf"),
        ("Happier Detail 3", "https://moon-oh.com/local-product/happier-grocery/marak-sage-3-4oz-candle"),
        ("Kim'C Market Detail", "https://moon-oh.com/item/premium-artisan-korean-rice-kimc-101"),
        ("Big Night Detail", "https://moon-oh.com/local-product/big-night/fishwife-smoked-salmon-with-sweet-and-spicy-chili-crisp"),
        ("Moonoh P2P Detail", "https://moon-oh.com/item/mr-potato-head-mug-manhattan-ny-209")
    ]

    for name, url in screens:
        status, html, headers = fetch(url)
        print(f"  [{name}] {url} => HTTP {status}")
        if status == 200:
            canon = re.search(r'rel="canonical" [^>]*href="([^"]+)"', html) or re.search(r'href="([^"]+)" [^>]*rel="canonical"', html)
            h1 = re.search(r'<h1[^>]*>([\s\S]*?)<\/h1>', html)
            img = re.search(r'<img [^>]*src="([^"]+)"', html)
            print(f"    Canonical: {canon.group(1) if canon else 'N/A'}")
            print(f"    H1: {h1.group(1).strip() if h1 else 'N/A'}")
            print(f"    Image: {img.group(1)[:60] if img else 'N/A'}...")

    print("\n=== 2. SITEMAPS AUDIT & COUNTS ===")
    sitemaps = [
        ("sitemap-index.xml", "https://moon-oh.com/sitemap-index.xml", None),
        ("sitemap-pages.xml", "https://moon-oh.com/sitemap-pages.xml", 139),
        ("sitemap-moonoh.xml", "https://moon-oh.com/sitemap-moonoh.xml", 592),
        ("sitemap-marketplace.xml", "https://moon-oh.com/sitemap-marketplace.xml", 1401),
        ("sitemap-food-rescue.xml", "https://moon-oh.com/sitemap-food-rescue.xml", 15),
        ("sitemap-local-products.xml", "https://moon-oh.com/sitemap-local-products.xml", 90),
        ("sitemap-shops.xml", "https://moon-oh.com/sitemap-shops.xml", 3),
    ]

    total_urls = 0
    for name, url, exp_count in sitemaps:
        status, xml_text, _ = fetch(url)
        count = xml_text.count('<loc>')
        if name == "sitemap-index.xml":
            print(f"  [Index] {name} => HTTP {status}, Child Sitemaps: {count}")
        else:
            total_urls += count
            match_str = "MATCH" if (exp_count is None or count == exp_count) else f"MISMATCH (Expected {exp_count})"
            print(f"  [Child] {name} => HTTP {status}, URLs: {count} ({match_str})")

    print(f"  Total URLs across child sitemaps: {total_urls} (Expected 2240: {'MATCH' if total_urls == 2240 else 'MISMATCH'})")

    print("\n=== 3. PHASE 2 REGRESSION PROTECTION ===")
    # 1. Root & Explore
    s_root, _, _ = fetch("https://moon-oh.com/")
    s_exp, _, _ = fetch("https://moon-oh.com/explore")
    print(f"  Root / : HTTP {s_root}, /explore : HTTP {s_exp}")

    # 2. Legacy 1-hop 301
    s_leg, _, h_leg = fetch("https://moon-oh.com/item/mr-potato-head-mug-downtown-manhattan-209")
    loc = h_leg.get('Location') or h_leg.get('location')
    print(f"  Legacy 301 => HTTP {s_leg}, Dest: {loc}")

    # 3. Chanel 669111
    s_chanel, _, h_chanel = fetch("https://moon-oh.com/item/chanel-woc-wallet-on-chain-1mi-queens-ny-ext-heykorean-669111")
    noindex_c = h_chanel.get('X-Robots-Tag') or h_chanel.get('x-robots-tag')
    print(f"  Chanel 669111 => HTTP {s_chanel} (Expected 404), X-Robots-Tag: {noindex_c}")

    # 4. Old Happier Placeholder slug
    s_matcha, _, h_matcha = fetch("https://moon-oh.com/local-product/happier-grocery/happier-organic-ceremonial-matcha-100g")
    noindex_m = h_matcha.get('X-Robots-Tag') or h_matcha.get('x-robots-tag')
    print(f"  Old Placeholder Matcha => HTTP {s_matcha} (Expected 404), X-Robots-Tag: {noindex_m}")

    # 5. Merchant feed
    s_feed, feed_xml, _ = fetch("https://moon-oh.com/merchant-feed.xml")
    feed_items = feed_xml.count('<item>')
    print(f"  Merchant Feed => HTTP {s_feed}, Items: {feed_items} (Expected 0)")

    # 6. P2P vs External CTAs & Schema
    _, p2p_html, _ = fetch("https://moon-oh.com/item/mr-potato-head-mug-manhattan-ny-209")
    has_p2p_cta = "Buy & Chat" in p2p_html or "Chat on App" in p2p_html or "Buy on App" in p2p_html or "Download Moonoh" in p2p_html
    print(f"  P2P Detail Page CTA check => {'PASS' if has_p2p_cta else 'CHECK'}")

    _, ext_html, _ = fetch("https://moon-oh.com/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups")
    has_view_cta = "View on Happier Grocery" in ext_html or "View at Happier Grocery" in ext_html
    no_fake_schema = "shippingDetails" not in ext_html and "hasMerchantReturnPolicy" not in ext_html
    print(f"  External Detail CTA: {'PASS' if has_view_cta else 'FAIL'}, No fake shipping/return schema: {'PASS' if no_fake_schema else 'FAIL'}")

if __name__ == '__main__':
    run_suite()
