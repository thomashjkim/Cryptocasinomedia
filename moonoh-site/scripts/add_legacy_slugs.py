import json

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

with open('scripts/happier_slug_audit.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

audit_map = {r['source_product_id']: r['old_slug'] for r in audit_data}

for p in local_db['products']:
    if p.get('shop_id') == 'happier-grocery':
        sp_id = p.get('source_product_id')
        if sp_id in audit_map:
            p['legacy_slug'] = audit_map[sp_id]

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(local_db, f, indent=2, ensure_ascii=False)

print("✅ Added legacy_slug to all 30 Happier Grocery products in local_shops_data.json")
