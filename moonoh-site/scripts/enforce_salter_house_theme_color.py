import json
import re

print("=" * 80)
print("🌲 ENFORCING SALTER HOUSE THEME COLOR #007A4B ACROSS ALL FILES")
print("=" * 80)

# 1. Update local_shops_data.json
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'salter-house' in data.get('shops', {}):
    data['shops']['salter-house']['theme_color'] = '#007A4B'

for p in data.get('products', []):
    if p.get('shop_id') == 'salter-house':
        p['theme_color'] = '#007A4B'

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("✅ Updated local_shops_data.json with theme_color #007A4B for Salter House")

# 2. Update netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Update Salter House styling in item-detail.mjs
salter_block_pattern = r'\}\s*else if \(externalSource === "salter-house"\)\s*\{[\s\S]*?btnBgColor = "[^"]+";'
new_salter_block = '''} else if (externalSource === "salter-house") {
      bannerBg = "#E6F5F0";
      bannerBorder = "#99D6C4";
      bannerColor = "#007A4B";
      btnBgColor = "#007A4B";
      btnTextColor = "#FFFFFF";'''

code = re.sub(salter_block_pattern, new_salter_block, code)

# Ensure any #007a51 or #3B5A40 for salter is replaced with #007A4B
code = code.replace('"#007a51"', '"#007A4B"').replace('"#3B5A40"', '"#007A4B"')

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ Updated netlify/functions/item-detail.mjs with Salter House button color #007A4B")

# 3. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    explore_html = f.read()

explore_html = re.sub(
    r'\.badge-salter\s*\{[\s\S]*?\}',
    '''.badge-salter {
      background-color: #E6F5F0;
      color: #007A4B;
      border: 1px solid #99D6C4;
    }''',
    explore_html
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(explore_html)
print("✅ Updated explore.html with .badge-salter color #007A4B")

# 4. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

index_html = re.sub(
    r'\.badge-salter\s*\{[\s\S]*?\}',
    '''.badge-salter {
      background-color: #E6F5F0;
      color: #007A4B;
      border: 1px solid #99D6C4;
    }''',
    index_html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated index.html with .badge-salter color #007A4B")

print("\n" + "=" * 80)
print("🎉 SALTER HOUSE THEME COLOR #007A4B STRICTLY ENFORCED ACROSS ALL FILES!")
print("=" * 80)
