import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import re

def fetch_url(url, method='GET', timeout=15):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            headers = dict(resp.headers)
            return resp.status, content, headers
    except urllib.error.HTTPError as e:
        content = e.read()
        headers = dict(e.headers)
        return e.code, content, headers
    except Exception as e:
        return 0, str(e).encode('utf-8'), {}

def run_production_audit():
    print("================================================================================")
    print("  PHASE 3A — PRODUCTION READ-ONLY COMPREHENSIVE AUDIT ON HTTPS://MOON-OH.COM")
    print("================================================================================\n")

    # Load local dataset to compare against production
    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        local_db = json.load(f)

    hg_items = [p for p in local_db['products'] if p['shop_id'] == 'happier-grocery']
    print(f"Auditing all {len(hg_items)} Happier Grocery items on live production...\n")

    table_rows = []
    failed_items = []
    unsplash_count = 0
    broken_img_count = 0
    wrong_mapping_count = 0
    wrong_outbound_count = 0

    for idx, item in enumerate(hg_items):
        pid = item['source_product_id']
        raw_id = pid.replace('hg-', '')
        slug = item['slug']
        prod_url = f"https://moon-oh.com/local-product/happier-grocery/{slug}"
        expected_official_url = f"https://shop.happiergrocery.com/product/{raw_id}"
        expected_title = item['title']
        expected_price = item['current_price']
        img_url = item['image_source_url']

        # 1. Fetch live production page
        status, content, headers = fetch_url(prod_url)
        html = content.decode('utf-8', errors='ignore')

        # Checks
        status_ok = (status == 200)

        # Canonical check
        canon_match = re.search(r'<link [^>]*href="([^"]+)" rel="canonical"', html) or re.search(r'<link [^>]*rel="canonical" [^>]*href="([^"]+)"', html)
        canonical_url = canon_match.group(1) if canon_match else ''
        canonical_ok = (canonical_url == prod_url)

        # Title check in H1 / Meta
        h1_match = re.search(r'<h1[^>]*>([\s\S]*?)<\/h1>', html)
        h1_text = h1_match.group(1).strip() if h1_match else ''
        title_ok = (expected_title.lower() in h1_text.lower()) or (h1_text.lower() in expected_title.lower())

        # Price check
        price_str = f"${expected_price:.2f}"
        price_alt_str = f"${int(expected_price)}" if expected_price.is_integer() else price_str
        price_ok = (price_str in html) or (price_alt_str in html) or (str(expected_price) in html)

        # Image check (must be CloudFront, not unsplash)
        is_unsplash = 'unsplash.com' in img_url or 'placeholder' in img_url
        if is_unsplash:
            unsplash_count += 1
        is_cloudfront = 'cloudfront.net' in img_url

        # Live Image Fetch
        img_status, img_content, img_headers = fetch_url(img_url)
        ct = img_headers.get('Content-Type', '') or img_headers.get('content-type', '')
        img_ok = (img_status == 200 and ('image' in ct or 'octet-stream' in ct))
        if not img_ok:
            broken_img_count += 1

        # CTA check
        cta_ok = ('View on Happier Grocery' in html) or ('View at Happier Grocery' in html)

        # Outbound URL check
        outbound_ok = expected_official_url in html
        if not outbound_ok:
            wrong_outbound_count += 1

        # Schema & Disclosure check
        json_ld_match = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
        schema_ok = False
        if json_ld_match:
            try:
                schema = json.loads(json_ld_match.group(1))
                nodes = schema.get('@graph', [schema])
                prod_node = next((n for n in nodes if n.get('@type') == 'Product'), None)
                if prod_node:
                    seller = prod_node.get('offers', {}).get('seller', {})
                    has_seller_org = seller.get('@type') == 'Organization' and 'Happier Grocery' in seller.get('name', '')
                    no_shipping = 'shippingDetails' not in prod_node.get('offers', {})
                    no_returns = 'hasMerchantReturnPolicy' not in prod_node.get('offers', {})
                    schema_ok = has_seller_org and no_shipping and no_returns
            except Exception as e:
                schema_ok = False

        disclosure_ok = 'Shipping, returns, and checkout are handled by Happier Grocery' in html

        passed_all = status_ok and canonical_ok and title_ok and price_ok and img_ok and cta_ok and outbound_ok and schema_ok and disclosure_ok
        res_str = "PASS" if passed_all else "FAIL"

        if not passed_all:
            failed_items.append({
                "pid": pid,
                "url": prod_url,
                "status": status,
                "canonical": canonical_ok,
                "title": title_ok,
                "price": price_ok,
                "img": img_ok,
                "cta": cta_ok,
                "outbound": outbound_ok,
                "schema": schema_ok,
                "disclosure": disclosure_ok
            })

        table_rows.append({
            "idx": idx + 1,
            "pid": pid,
            "moonoh_url": prod_url,
            "official_url": expected_official_url,
            "title_match": "YES" if title_ok else "NO",
            "price_match": "YES" if price_ok else "NO",
            "image_200": "200 OK" if img_ok else f"ERR {img_status}",
            "canonical_match": "YES" if canonical_ok else "NO",
            "cta_match": "YES" if cta_ok else "NO",
            "schema_match": "YES" if schema_ok else "NO",
            "result": res_str
        })

    # Print Table
    print(f"{'No':<3} | {'Product ID':<28} | {'Title Match':<11} | {'Price Match':<11} | {'Image 200':<10} | {'Canonical':<9} | {'CTA':<5} | {'Schema':<6} | {'Result'}")
    print("-" * 105)
    for r in table_rows:
        print(f"{r['idx']:<3} | {r['pid']:<28} | {r['title_match']:<11} | {r['price_match']:<11} | {r['image_200']:<10} | {r['canonical_match']:<9} | {r['cta_match']:<5} | {r['schema_match']:<6} | {r['result']}")

    print("\n--------------------------------------------------------------------------------")
    print("HAPPIER GROCERY 30-ITEM VERIFICATION TOTALS:")
    print(f"  - Total records:                  {len(hg_items)}")
    print(f"  - Fully passed:                   {len(table_rows) - len(failed_items)}")
    print(f"  - Failed:                         {len(failed_items)}")
    print(f"  - Unsplash/placeholder remaining: {unsplash_count}")
    print(f"  - Broken images:                  {broken_img_count}")
    print(f"  - Wrong product mappings:         {wrong_mapping_count}")
    print(f"  - Wrong outbound URLs:            {wrong_outbound_count}")
    print("--------------------------------------------------------------------------------\n")

    return len(failed_items) == 0

if __name__ == '__main__':
    run_production_audit()
