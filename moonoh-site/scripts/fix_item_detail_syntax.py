import re

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace any malformed title.replace in onclick handlers with clean JSON.stringify or safe escape
code = code.replace(
    'item_name:\'${title.replace(/\'/g, \\"\\\'\\")}\'',
    'item_name:${JSON.stringify(title)}'
)
code = code.replace(
    'item_name:\'${title.replace(/\'/g, "\\\'")}\'',
    'item_name:${JSON.stringify(title)}'
)
code = code.replace(
    'item_name:\'${title.replace(/\'/g, "\\\\\'")}\'',
    'item_name:${JSON.stringify(title)}'
)
code = re.sub(
    r'item_name:\'\$\{title\.replace\([^\}]+\)\}\'',
    'item_name:${JSON.stringify(title)}',
    code
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Fixed quote syntax in item-detail.mjs")
