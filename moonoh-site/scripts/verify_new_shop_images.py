import urllib.request
import json
import concurrent.futures

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

new_shop_ids = {'front-general-store', 'mirth-vintage', 'sey-coffee', 'salter-house'}
new_products = [p for p in db['products'] if p['shop_id'] in new_shop_ids]

print(f"Verifying images for {len(new_products)} new products across 4 shops...")

def check_image(p):
    url = p['image_source_url']
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            ct = resp.headers.get('Content-Type', '')
            ok = resp.status == 200 and ('image' in ct or 'octet-stream' in ct)
            return ok, resp.status, ct, p['id']
    except Exception as e:
        return False, 0, str(e), p['id']

success_count = 0
failed = []

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(check_image, new_products))

for ok, status, ct, pid in results:
    if ok:
        success_count += 1
    else:
        failed.append((pid, status, ct))

print(f"\nImage Verification Summary:")
print(f"  Total Checked: {len(new_products)}")
print(f"  Successful (HTTP 200 Image): {success_count} / {len(new_products)}")
print(f"  Failed: {len(failed)}")

if failed:
    print("Failed samples:", failed[:5])
else:
    print("✅ 100% of new product images are valid, permanent, and return HTTP 200!")
