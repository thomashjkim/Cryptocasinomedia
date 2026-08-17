import json
import re

# 1. Load local_shops_data.json and happier_slug_audit.json
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

with open('scripts/happier_slug_audit.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

audit_map = {r['source_product_id']: r for r in audit_data}

# Update products in local_db
updated_products = []
for p in local_db['products']:
    if p.get('shop_id') == 'happier-grocery':
        sp_id = p.get('source_product_id')
        if sp_id in audit_map:
            aud = audit_map[sp_id]
            p['slug'] = aud['new_slug']
            p['title'] = aud['official_title']
            p['brand'] = aud['brand']
            p['current_price'] = aud['price']
            p['image_alt'] = f"{aud['official_title']} by {aud['brand']} at Happier Grocery Soho"
    updated_products.append(p)

local_db['products'] = updated_products

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(local_db, f, indent=2, ensure_ascii=False)
print("✅ Updated local_shops_data.json with authentic slugs")

# 2. Sync into netlify/functions/item-detail.mjs
local_db_str = json.dumps(local_db, ensure_ascii=False)
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'const localShopsDb = \{.*?\};\n'
match = re.search(pattern, code)
if match:
    new_code = code[:match.start()] + f'const localShopsDb = {local_db_str};\n' + code[match.end():]
    with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("✅ Synced updated localShopsDb into netlify/functions/item-detail.mjs")
else:
    print("❌ Pattern not matched in item-detail.mjs")
