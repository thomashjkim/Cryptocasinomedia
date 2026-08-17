import json
import re

# 1. Moonoh
with open('netlify/functions/moonoh-items-data.mjs', 'r', encoding='utf-8') as f:
    m_moon = re.search(r'export const realMoonohItems = (\[.*?\]);', f.read(), re.DOTALL)
moonoh_items = json.loads(m_moon.group(1))

# 2. Marketplaces
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
    m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', code, re.DOTALL)
    m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', code, re.DOTALL)
karrot_items = json.loads(m_karrot.group(1))
hey_items = json.loads(m_hey.group(1))

# 3. Local Shops
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_data = json.load(f)
local_prods = local_data.get('products', [])
shops_info = local_data.get('shops', {})

# 4. Food Rescue
with open('netlify/functions/food-rescue-items.mjs', 'r', encoding='utf-8') as f:
    m_fr = re.search(r'export const realFoodRescueItems = (\[.*?\]);', f.read(), re.DOTALL)
fr_items = json.loads(m_fr.group(1))

total_products = len(moonoh_items) + len(karrot_items) + len(hey_items) + len(local_prods) + len(fr_items)

print(f"Total Products: {total_products}")
print(f"  • Moonoh 자체 중고: {len(moonoh_items)}개")
print(f"  • Karrot NYC: {len(karrot_items)}개")
print(f"  • HeyKorean NYC/NJ: {len(hey_items)}개 (오늘 매물 포함)")
print(f"  • 로컬 숍 6곳 상품: {len(local_prods)}개")
for s_id, s_data in shops_info.items():
    if s_data.get('products_count', 0) > 0:
        print(f"      - {s_data.get('name')}: {s_data.get('products_count')}개")
print(f"  • Food Rescue (Kim'C Market): {len(fr_items)}개")
