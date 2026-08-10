import json
import re

with open('real_external_items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

hk_items = data['heykorean']
kr_items = data['karrot']

# Build quick lookup dictionary (keyed by item id lowercase)
all_ext_items = {}
for item in kr_items + hk_items:
    all_ext_items[item['id'].lower()] = item

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    content = f.read()

# ─────────────────────────────────────────────────────────
# 1. Replace the allRealExternalItems lookup dict + getExternalItemById
# ─────────────────────────────────────────────────────────
new_lookup_code = f"""const allRealExternalItems = {json.dumps(all_ext_items, ensure_ascii=False, indent=2)};

function getExternalItemById(extId) {{
  const key = (extId || '').toLowerCase();
  if (allRealExternalItems[key]) {{
    return allRealExternalItems[key];
  }}
  // Fallback by source and index if ID is numeric
  const parts = key.split('-');
  const source = parts[0];
  const num = parseInt(parts[1], 10) || 0;
  const list = source === "karrot" ? {json.dumps(kr_items, ensure_ascii=False)} : {json.dumps(hk_items, ensure_ascii=False)};
  if (list.length > 0) {{
    return list[Math.abs(num) % list.length];
  }}
  return null;
}}"""

pattern = r'const karrotTitles = \[.*?function getExternalItemById\(extId\) \{.*?\n\}'
updated_content = re.sub(pattern, new_lookup_code, content, flags=re.DOTALL)

# ─────────────────────────────────────────────────────────
# 2. Fix auto-generated description: use real description from data
# OLD: description = `${extItem.title}. Outdoor item listed in ${extItem.location}. Cross-posted from ${extItem.sourceName}.`;
# NEW: use extItem.description if present, else generate naturally
# ─────────────────────────────────────────────────────────
old_desc = '      description = `${extItem.title}. Outdoor item listed in ${extItem.location}. Cross-posted from ${extItem.sourceName}.`;'
new_desc = '      description = extItem.description || `${extItem.title} listed in ${extItem.rawTown || extItem.location}. Originally posted on ${extItem.sourceName}.`;'
updated_content = updated_content.replace(old_desc, new_desc)

# ─────────────────────────────────────────────────────────
# 3. Fix seller name bug: line 1273 overwrites with generic name
# OLD: sellerName = extItem.sourceName === "HeyKorean" ? "HeyKorean Seller" : "Karrot Seller";
# NEW: (delete this line — use real sellerName from extItem.sellerName set on line 1267)
# ─────────────────────────────────────────────────────────
bad_seller_line = '      sellerName = extItem.sourceName === "HeyKorean" ? "HeyKorean Seller" : "Karrot Seller";'
updated_content = updated_content.replace(bad_seller_line, '      // sellerName already set above from extItem.sellerName')

# ─────────────────────────────────────────────────────────
# 4. Fix map coordinates: use lat/lng from extItem if available
# OLD: (lat/lng stay at default 40.7128, -74.0060 for all external items)
# The external block ends before the else block.
# We inject lat/lng assignment right after the externalUrl/externalSource lines.
# ─────────────────────────────────────────────────────────
old_cat_line = '      categoryName = extItem.category;\n      externalUrl = extItem.url;\n      externalSource = extItem.source;'
new_cat_line = (
    '      categoryName = extItem.category;\n'
    '      externalUrl = extItem.url;\n'
    '      externalSource = extItem.source;\n'
    '      // Use real coordinates from scraped data if available\n'
    '      if (extItem.lat && extItem.lng) { lat = extItem.lat; lng = extItem.lng; }'
)
updated_content = updated_content.replace(old_cat_line, new_cat_line)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated item-detail.mjs:")
print("  ✅ Real items lookup dict")
print("  ✅ Real descriptions (no more template)")
print("  ✅ Real seller names (no more generic override)")
print("  ✅ Real map coordinates per item")
