import json
import re

# Load clean real_external_items.json
with open('real_external_items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

hk_items = data['heykorean']
kr_items = data['karrot']

# Build dictionary
all_ext = {}
for item in kr_items + hk_items:
    all_ext[item['id'].lower()] = item

print(f"Loaded {len(all_ext)} items from real_external_items.json")

# Read item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Generate only the new allRealExternalItems dict (NOT getExternalItemById — that stays in the file)
new_dict = f"const allRealExternalItems = {json.dumps(all_ext, ensure_ascii=False, indent=2)};"

# SAFE: Only replace from 'const allRealExternalItems = {' up to the closing '};'
# This stops BEFORE inferCategoryFromText or getExternalItemById
pattern = r'const allRealExternalItems = \{.*?\n\};'
match = re.search(pattern, code, re.DOTALL)
if match:
    code = code[:match.start()] + new_dict + code[match.end():]
    print("✅ Successfully replaced allRealExternalItems dict in item-detail.mjs")
else:
    print("❌ Match failed for pattern!")

# Write updated code back to netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated netlify/functions/item-detail.mjs successfully!")
