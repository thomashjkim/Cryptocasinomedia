with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'export default async (req, context) => {\n  try {\n    const url = new URL(req.url);',
    'export default async (req, context) => {\n  try {\n    const url = new URL(req.url);\n    const localShopsDb = getLocalShopsDb();'
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Added localShopsDb at top of handler")
