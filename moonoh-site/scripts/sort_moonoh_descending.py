import json

with open('data.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Sort strictly by product number descending
items.sort(key=lambda x: int(x.get('no', 0)), reverse=True)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

mjs_content = f"// Live Moonoh Items Dataset ({len(items)} items)\n"
mjs_content += f"export const realMoonohItems = {json.dumps(items, indent=2, ensure_ascii=False)};\n"

with open('netlify/functions/moonoh-items-data.mjs', 'w', encoding='utf-8') as f:
    f.write(mjs_content)

print(f"✅ Sorted {len(items)} items. Highest No: {items[0]['no']} ({items[0]['title']})")
