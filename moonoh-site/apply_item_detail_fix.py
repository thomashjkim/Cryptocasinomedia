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

# Generate new JavaScript snippet for allRealExternalItems and getExternalItemById
new_code = f"""const allRealExternalItems = {json.dumps(all_ext, ensure_ascii=False, indent=2)};

function getExternalItemById(extId) {{
  const key = (extId || '').toLowerCase();
  if (allRealExternalItems[key]) {{
    return allRealExternalItems[key];
  }}
  const parts = key.split('-');
  const source = parts[0];
  const num = parseInt(parts[1], 10) || 0;
  const list = source === "karrot" ? {json.dumps(kr_items, ensure_ascii=False)} : {json.dumps(hk_items, ensure_ascii=False)};
  if (list.length > 0) {{
    return list[Math.abs(num) % list.length];
  }}
  return null;
}}"""

# Replace from 'const allRealExternalItems =' up to 'function getExternalItemById(extId) {\n  const key = ...\n}'
pattern = r'const allRealExternalItems = \{.*?\nfunction getExternalItemById\(extId\) \{.*?\n\}'
match = re.search(pattern, code, re.DOTALL)
if match:
    code = code[:match.start()] + new_code + code[match.end():]
    print("✅ Successfully replaced allRealExternalItems and getExternalItemById in item-detail.mjs")
else:
    print("❌ Match failed for pattern!")

# Write updated code back to netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated netlify/functions/item-detail.mjs successfully!")
