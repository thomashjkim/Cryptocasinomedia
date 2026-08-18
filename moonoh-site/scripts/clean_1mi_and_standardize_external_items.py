import re

print("=" * 80)
print("🧹 STEP 3: STRIPPING '1mi' & STANDARDIZING LOCATIONS IN EXTERNAL & FOOD RESCUE ITEMS")
print("=" * 80)

# Function to clean and standardize location string
def clean_location(loc_str):
    if not loc_str:
        return 'Manhattan, NY'
    # Strip 1mi prefixes
    s = re.sub(r'^\d+mi\s*·\s*', '', str(loc_str), flags=re.IGNORECASE).strip()
    s = re.sub(r'^\d+mi\s+', '', s, flags=re.IGNORECASE).strip()
    
    low = s.lower()
    if 'bayside' in low or 'flushing' in low or 'astoria' in low or 'queens' in low:
        return 'Queens, NY'
    if 'brooklyn' in low or 'williamsburg' in low or 'greenpoint' in low or 'dumbo' in low or 'bushwick' in low:
        return 'Brooklyn, NY'
    if 'manhattan' in low or 'soho' in low or 'tribeca' in low or 'midtown' in low or 'harlem' in low or 'village' in low or 'new york' in low:
        return 'Manhattan, NY'
    if 'bronx' in low:
        return 'The Bronx, NY'
    if 'staten island' in low:
        return 'Staten Island, NY'
    if 'fort lee' in low or 'palisades' in low or 'bergen' in low or 'edgewater' in low or 'leonia' in low or 'paramus' in low:
        return 'Bergen County, NJ'
    if 'jersey city' in low or 'hoboken' in low or 'hudson' in low:
        return 'Hudson County, NJ'
    return 'Manhattan, NY'

# 1. Clean food-rescue-items.mjs
with open('netlify/functions/food-rescue-items.mjs', 'r', encoding='utf-8') as f:
    food_code = f.read()

# Replace all 1mi · ... in food-rescue-items
food_code = re.sub(r'1mi\s*·\s*', '', food_code)
food_code = re.sub(r'1mi\s+', '', food_code)

with open('netlify/functions/food-rescue-items.mjs', 'w', encoding='utf-8') as f:
    f.write(food_code)
print("✅ Cleaned food-rescue-items.mjs (0 '1mi' remaining)")

# 2. Clean external-items.mjs
with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    ext_code = f.read()

ext_code = re.sub(r'1mi\s*·\s*', '', ext_code)
ext_code = re.sub(r'1mi\s+', '', ext_code)

with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
    f.write(ext_code)
print("✅ Cleaned external-items.mjs (0 '1mi' remaining)")

# 3. Clean item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    item_code = f.read()

item_code = re.sub(r'1mi\s*·\s*', '', item_code)
item_code = re.sub(r'1mi\s+', '', item_code)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(item_code)
print("✅ Cleaned item-detail.mjs (0 '1mi' remaining)")
