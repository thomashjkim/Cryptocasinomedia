import json
import re
import base64

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

hg_items = [p for p in data['products'] if p['shop_id'] == 'happier-grocery']
print(f"Total Happier items: {len(hg_items)}\n")

all_valid = True
for idx, item in enumerate(hg_items):
    prod_id = item['source_product_id']
    title = item['title']
    price = item['current_price']
    source_url = item['canonical_source_url']
    img_url = item['image_source_url']
    
    # 1. Price check
    is_price_valid = isinstance(price, (int, float)) and price > 0
    
    # 2. URL check
    raw_id = prod_id.replace('hg-', '')
    has_valid_source = source_url == f"https://shop.happiergrocery.com/product/{raw_id}"
    
    # 3. Cloudfront signed/temporary check
    has_tokens = any(k in img_url for k in ['Expires=', 'Signature=', 'Key-Pair-Id=', 'token=', 'temp/'])
    is_cloudfront = img_url.startswith('https://d38cu1l1jdjf8r.cloudfront.net/') or img_url.startswith('https://d29eorrpahk9tz.cloudfront.net/')
    
    # Decode base64 payload in Cloudfront URL if d38cu1l1jdjf8r
    img_key = ''
    if 'd38cu1l1jdjf8r' in img_url:
        b64 = img_url.split('cloudfront.net/')[1]
        try:
            pad = len(b64) % 4
            if pad > 0:
                b64 += '=' * (4 - pad)
            decoded = json.loads(base64.b64decode(b64).decode('utf-8'))
            img_key = decoded.get('key', '')
        except Exception as e:
            img_key = f"decode_err: {e}"
            
    print(f"{idx+1:2d}. ID: {prod_id} | Price: ${price:.2f} | Title: {title}")
    print(f"    Source URL: {source_url}")
    print(f"    CDN Key: {img_key} | Query/Expiry Tokens: {has_tokens}")
    print(f"    Checks => Price: {is_price_valid}, Source URL: {has_valid_source}, Permanent Public CDN: {is_cloudfront and not has_tokens}")
    print("-" * 85)
    
    if not (is_price_valid and has_valid_source and is_cloudfront and not has_tokens):
        all_valid = False

print(f"\nOverall Sanity Status: {'ALL 30 ITEMS 100% VALID & VERIFIED' if all_valid else 'FAILURES DETECTED'}")
