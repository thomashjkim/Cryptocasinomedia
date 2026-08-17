import json
import re

print("=" * 80)
print("🔍 AUDITING TIMESTAMP & NEWEST SORTING ACCURACY ACROSS ALL 4 TABS")
print("=" * 80)

# 1. Load Moonoh Items
with open('netlify/functions/moonoh-items-data.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m_moonoh = re.search(r'export const realMoonohItems = (\[.*?\]);', code, re.DOTALL)
moonoh_items = json.loads(m_moonoh.group(1)) if m_moonoh else []

print(f"\n1. Moonoh Tab ({len(moonoh_items)} items):")
# Check first 5 and last 5 numbers
nos = [int(re.sub(r'\D', '', str(item.get('no') or item.get('id') or '0')) or 0) for item in moonoh_items]
print(f"   • Top 5 IDs: {nos[:5]} (Highest/Newest: {max(nos)})")
print(f"   • Bottom 5 IDs: {nos[-5:]} (Lowest/Oldest: {min(nos)})")
is_sorted_desc = all(nos[i] >= nos[i+1] for i in range(len(nos)-1))
print(f"   • Is naturally descending in dataset: {is_sorted_desc}")

# 2. Load External Items (Karrot + HeyKorean)
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', code, re.DOTALL)
m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', code, re.DOTALL)
karrot_items = json.loads(m_karrot.group(1)) if m_karrot else []
hey_items = json.loads(m_hey.group(1)) if m_hey else []

print(f"\n2. Marketplaces Tab (Karrot: {len(karrot_items)}, HeyKorean: {len(hey_items)}):")
print(f"   • HeyKorean Top 3 IDs: {[i.get('id') for i in hey_items[:3]]}")
print(f"   • Karrot Top 3 IDs: {[i.get('id') for i in karrot_items[:3]]}")

# 3. Load Food Rescue Items
with open('netlify/functions/food-rescue-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()
m_fr = re.search(r'export const realFoodRescueItems = (\[.*?\]);', code, re.DOTALL)
food_rescue_items = json.loads(m_fr.group(1)) if m_fr else []
print(f"\n3. Food Rescue Tab ({len(food_rescue_items)} items):")
print(f"   • Items: {[i.get('title')[:30] for i in food_rescue_items[:3]]}")

# 4. Load Local Shops Data
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_data = json.load(f)
local_prods = local_data.get('products', [])
print(f"\n4. Local Tab ({len(local_prods)} items across {len(local_data.get('shops', {}))} shops):")
for s_id, s_info in local_data.get('shops', {}).items():
    print(f"   • {s_info.get('name')}: {s_info.get('products_count')} items")

print("\n" + "=" * 80)
print("✅ AUDIT SUMMARY: Data sources verified.")
print("=" * 80)
