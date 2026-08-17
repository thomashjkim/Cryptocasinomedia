import json
import re

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)
local_db_str = json.dumps(local_db, ensure_ascii=False)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update const localShopsDb = {...};
pattern_db = r'const localShopsDb = \{.*?\};\n'
match_db = re.search(pattern_db, code)
if match_db:
    code = code[:match_db.start()] + f'const localShopsDb = {local_db_str};\n' + code[match_db.end():]
    print("✅ Replaced localShopsDb")
else:
    print("❌ Failed to find localShopsDb")

# 2. Update localItem find logic to support legacy_slug and 1-hop 301 redirect
pattern_find = r'localItem = localShopsDb\.products\.find\(p => p\.shop_id === shopSlug && \(p\.slug === prodSlug \|\| p\.id === prodSlug \|\| p\.source_product_id === prodSlug\)\);'
replacement_find = '''localItem = localShopsDb.products.find(p => p.shop_id === shopSlug && (p.slug === prodSlug || p.id === prodSlug || p.source_product_id === prodSlug || p.legacy_slug === prodSlug));
      if (localItem && prodSlug === localItem.legacy_slug && localItem.legacy_slug !== localItem.slug) {
        return new Response(null, {
          status: 301,
          headers: {
            "Location": `https://moon-oh.com/local-product/${shopSlug}/${localItem.slug}`,
            "Cache-Control": "public, max-age=86400"
          }
        });
      }'''

if pattern_find in code:
    code = code.replace(pattern_find, replacement_find)
    print("✅ Updated localItem find & legacy redirect")
else:
    # Try regex search
    pattern_regex = r'localItem = localShopsDb\.products\.find\(p => p\.shop_id === shopSlug && \(.*?\)\);'
    match_f = re.search(pattern_regex, code)
    if match_f:
        code = code[:match_f.start()] + replacement_find + code[match_f.end():]
        print("✅ Regex updated localItem find & legacy redirect")
    else:
        print("❌ Failed to find localItem search pattern")

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved netlify/functions/item-detail.mjs")
