with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if (!d || !d.title) {',
    "if (!d || !d.title || d.isShow !== 'Y') {"
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Added isShow !== 'Y' check to item-detail.mjs (hidden products return 404)")
