import re

print("=" * 80)
print("❤️ ➔ ❌ STEP 5: REMOVING ALL FAVORITE 'HEART' ICONS")
print("=" * 80)

# 1. Update netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Remove like-badge CSS
code = re.sub(r'\.like-badge\s*\{[\s\S]*?\}', '', code)
code = re.sub(r'\.like-badge\s*svg\s*\{[\s\S]*?\}', '', code)

# Remove like-badge HTML
code = re.sub(
    r'<div class="like-badge">[\s\S]*?<\/div>',
    '',
    code
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ Removed like-badge CSS & HTML from netlify/functions/item-detail.mjs")

# 2. Update item.html
with open('item.html', 'r', encoding='utf-8') as f:
    item_html = f.read()

item_html = re.sub(r'\.like-badge\s*\{[\s\S]*?\}', '', item_html)
item_html = re.sub(r'\.like-badge\s*svg\s*\{[\s\S]*?\}', '', item_html)
item_html = re.sub(
    r'<div class="like-badge">[\s\S]*?<\/div>',
    '',
    item_html
)

with open('item.html', 'w', encoding='utf-8') as f:
    f.write(item_html)
print("✅ Removed like-badge CSS & HTML from item.html")
