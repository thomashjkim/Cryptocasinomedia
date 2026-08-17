import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

shops = {
    'mirth-vintage': 'https://mirth.co/collections/all/products.json?limit=50',
    'pop-up-grocer': 'https://popupgrocer.com/collections/all/products.json?limit=50',
    'salter-house': 'https://salter.house/collections/all/products.json?limit=50',
    'sey-coffee': 'https://www.seycoffee.com/collections/all/products.json?limit=50',
    'big-night': 'https://bignightbk.com/collections/all/products.json?limit=50',
    'front-general-store': 'https://frontgeneralstore.com/collections/all/products.json?limit=50'
}

print("--- 1. Testing Local Shops Live Product Endpoints ---")
for shop_id, url in shops.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            products = data.get('products', [])
            print(f"  ✓ {shop_id:<22}: {len(products)} products available")
    except Exception as e:
        print(f"  ❌ {shop_id:<22}: Error: {e}")

print("\n--- 2. Testing HeyKorean Live Market API ---")
try:
    req_hk = urllib.request.Request('https://market.heykorean.com/api/market/list?page=1&size=50', headers=headers)
    with urllib.request.urlopen(req_hk, timeout=10) as resp:
        hk_data = json.loads(resp.read().decode('utf-8'))
        hk_list = hk_data.get('list', [])
        print(f"  ✓ HeyKorean Live API: {len(hk_list)} fresh listings retrieved for today")
except Exception as e:
    print(f"  ❌ HeyKorean Live API Error: {e}")
