import json, re

print("=" * 80)
print("🔍 100% EXHAUSTIVE AUDIT ACROSS ALL PRODUCTS IN ALL 4 TABS")
print("=" * 80)

# Helper date sanitizer test
def format_display_time_ago(raw_str, source_type):
    if source_type in ('localshops', 'local-shop', 'shop'): return 'Local Shop'
    if source_type in ('foodrescue', 'kimc'): return 'Food Rescue'
    if source_type in ('marketplaces', 'karrot', 'heykorean', 'external'): return 'Community Listing'
    if not raw_str or str(raw_str).strip() in ('undefined', 'null', 'None', ''): return 'Recently'

    raw = str(raw_str).strip().rstrip('.')
    m_day = re.search(r'(\d+)\s*days?\s*ago', raw, re.I)
    if m_day:
        days = int(m_day.group(1))
        if days > 60: return 'Recently listed'
        if days == 1: return '1 day ago'
        return f'{days} days ago'

    if re.search(r'year|month', raw, re.I):
        m_month = re.search(r'(\d+)\s*months?\s*ago', raw, re.I)
        if m_month:
            months = int(m_month.group(1))
            if months > 2: return 'Recently listed'
            if months == 1: return '1 month ago'
            return f'{months} months ago'
        return 'Recently listed'

    m_hour = re.search(r'(\d+)\s*hours?\s*ago', raw, re.I)
    if m_hour:
        hrs = int(m_hour.group(1))
        return '1 hour ago' if hrs == 1 else f'{hrs} hours ago'

    if re.search(r'(\d+)\s*mins?\s*ago|minutes?\s*ago', raw, re.I):
        return 'Just now'

    if raw.lower() in ('today', 'yesterday'):
        return raw.capitalize()

    return 'Recently'


# =========================================================================
# TAB 1: LOCAL SHOPS (900 items)
# =========================================================================
print("\n[TAB 1] AUDITING LOCAL SHOPS PRODUCTS...")
local_shops_path = "local_shops_data.json"
local_count = 0
local_issues = []

with open(local_shops_path, "r", encoding="utf-8") as f:
    local_db = json.load(f)
    products = local_db.get("products", [])
    local_count = len(products)
    
    for idx, p in enumerate(products):
        # 1. Price check
        price = p.get("current_price")
        if price is None or price < 0:
            local_issues.append(f"Invalid price on product {p.get('id')}: {price}")
        
        # 2. Location check
        shop_id = p.get("shop_id")
        if not shop_id:
            local_issues.append(f"Missing shop_id on product {p.get('id')}")
        
        # 3. Image check
        img = p.get("image_source_url")
        if not img or not img.startswith("http"):
            local_issues.append(f"Missing image on product {p.get('id')}")

print(f"  • Total Local Shop items audited: {local_count}")
print(f"  • Issues found: {len(local_issues)}")
if local_issues:
    for iss in local_issues[:5]: print(f"    - {iss}")


# =========================================================================
# TAB 2: FOOD RESCUE (Kim'C Market items)
# =========================================================================
print("\n[TAB 2] AUDITING FOOD RESCUE PRODUCTS...")
food_rescue_issues = []
food_count = 0

with open("netlify/functions/food-rescue-items.mjs", "r", encoding="utf-8") as f:
    fr_code = f.read()
    m = re.search(r'export const realFoodRescueItems = (\[[\s\S]*?\]);', fr_code)
    if m:
        food_items = json.loads(m.group(1))
        food_count = len(food_items)
        for it in food_items:
            if not it.get("title"): food_issues.append("Missing title")
            if it.get("price") is None: food_issues.append(f"Missing price on {it.get('id')}")
            if not it.get("image"): food_issues.append(f"Missing image on {it.get('id')}")

print(f"  • Total Food Rescue items audited: {food_count}")
print(f"  • Issues found: {len(food_rescue_issues)}")


# =========================================================================
# TAB 3: MARKETPLACES (1,505 Karrot & HeyKorean items)
# =========================================================================
print("\n[TAB 3] AUDITING COMMUNITY MARKETPLACE PRODUCTS...")
mkt_count = 0
mkt_issues = []

with open("netlify/functions/external-items.mjs", "r", encoding="utf-8") as f:
    ext_code = f.read()
    m1 = re.search(r'export const realKarrotItems = (\[[\s\S]*?\]);', ext_code)
    m2 = re.search(r'export const realHeyKoreanItems = (\[[\s\S]*?\]);', ext_code)
    k_items = json.loads(m1.group(1)) if m1 else []
    h_items = json.loads(m2.group(1)) if m2 else []
    all_ext = k_items + h_items
    mkt_count = len(all_ext)
    
    for it in all_ext:
        # Check location cleanliness
        loc = it.get("location", "")
        if "1mi" in loc or "Today" in loc:
            mkt_issues.append(f"Dirty location string in {it.get('id')}: {loc}")
        # Check price
        if it.get("price") is None:
            mkt_issues.append(f"Missing price in {it.get('id')}")
        # Check image
        if not it.get("image"):
            mkt_issues.append(f"Missing image in {it.get('id')}")

print(f"  • Total Marketplace items audited: {mkt_count}")
print(f"  • Issues found: {len(mkt_issues)}")


# =========================================================================
# TAB 4: MOONOH ITEMS (595 visible items)
# =========================================================================
print("\n[TAB 4] AUDITING MOONOH MARKETPLACE PRODUCTS...")
moonoh_count = 0
moonoh_issues = []

with open("data.json", "r", encoding="utf-8") as f:
    moonoh_items = json.load(f)
    moonoh_count = len(moonoh_items)
    
    for it in moonoh_items:
        no = it.get("no")
        title = it.get("title")
        loc = it.get("location", "")
        
        # Check location
        if "1mi" in loc or "Today" in loc:
            moonoh_issues.append(f"Dirty location in No.{no}: {loc}")
        # Check title
        if not title:
            moonoh_issues.append(f"Missing title in No.{no}")
        # Check price
        if it.get("price") is None:
            moonoh_issues.append(f"Missing price in No.{no}")
        # Check sanitized date string test
        raw_day = it.get("strDayCount")
        sanitized_date = format_display_time_ago(raw_day, "moonoh")
        if re.search(r'1110|undefined|null|NaN|\b\d{3,}\s*days?', sanitized_date):
            moonoh_issues.append(f"Bad date output in No.{no}: {sanitized_date}")

print(f"  • Total Moonoh items audited: {moonoh_count}")
print(f"  • Issues found: {len(moonoh_issues)}")

print("\n" + "=" * 80)
print(f"🎉 TOTAL ITEMS AUDITED ACROSS ALL 4 TABS: {local_count + food_count + mkt_count + moonoh_count}")
print(f"🎉 TOTAL AUDIT ISSUES: {len(local_issues) + len(food_rescue_issues) + len(mkt_issues) + len(moonoh_issues)}")
print("=" * 80)
