import json
import re

with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    ext_code = f.read()

m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', ext_code, re.DOTALL)
karrot_items = json.loads(m_karrot.group(1)) if m_karrot else []

print(f"Total Karrot items in external-items.mjs: {len(karrot_items)}")

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    detail_code = f.read()

# We can import realKarrotItems, realHeyKoreanItems or populate allRealExternalItems from them dynamically!
# Let's inspect where allRealExternalItems ends in item-detail.mjs
m_all = re.search(r'const allRealExternalItems = (\{[\s\S]*?\n\};)', detail_code)
if m_all:
    # Build dictionary
    ext_dict = {}
    for item in karrot_items:
        ext_dict[item['id']] = item
    
    # Also load hey korean items
    m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', ext_code, re.DOTALL)
    hey_items = json.loads(m_hey.group(1)) if m_hey else []
    for item in hey_items:
        ext_dict[item['id']] = item
        
    print(f"Constructed allRealExternalItems with {len(ext_dict)} items ({len(karrot_items)} Karrot + {len(hey_items)} HeyKorean)")
    
    new_db_str = f"const allRealExternalItems = {json.dumps(ext_dict, ensure_ascii=False, indent=2)};"
    detail_code = detail_code[:m_all.start()] + new_db_str + detail_code[m_all.end():]
    
    with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
        f.write(detail_code)
    print("✅ Successfully updated allRealExternalItems in netlify/functions/item-detail.mjs")
else:
    print("⚠️ Could not match allRealExternalItems pattern")
