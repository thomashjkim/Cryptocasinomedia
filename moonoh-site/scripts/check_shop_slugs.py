import json

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

prods = data['products']

print("Sample slugs per shop:")
shops = {}
for p in prods:
    s = p['shop_id']
    if s not in shops:
        shops[s] = []
    shops[s].append(p['slug'])

for s, slugs in shops.items():
    print(f"\nShop: {s} (Total {len(slugs)})")
    print(f"  First 3 slugs: {slugs[:3]}")
