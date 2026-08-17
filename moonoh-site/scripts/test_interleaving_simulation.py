import json

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_data = json.load(f)

prods = local_data.get('products', [])

# Separate into queues by shop_id
shops_map = {}
for p in prods:
    s_id = p.get('shop_id') or p.get('source') or 'other'
    if s_id not in shops_map:
        shops_map[s_id] = []
    shops_map[s_id].append(p)

print(f"Loaded {len(prods)} products across {len(shops_map)} shops:")
for s_id, items in shops_map.items():
    print(f"  • {s_id}: {len(items)} items")

# Multi-way Interleaving (Round Robin)
shop_keys = list(shops_map.keys())
interleaved = []
max_len = max(len(items) for items in shops_map.values())

for round_idx in range(max_len):
    for s_id in shop_keys:
        if round_idx < len(shops_map[s_id]):
            interleaved.append(shops_map[s_id][round_idx])

print(f"\nTotal Interleaved Products: {len(interleaved)}")
print("\n--- FIRST 24 ITEMS IN FEED (Page 1) ---")
for idx, p in enumerate(interleaved[:24]):
    print(f"[{idx+1:02d}] Shop: {p['shop_id']:<20} | Title: {p['title'][:40]:<40} | ${p['current_price']}")
