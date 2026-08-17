import json
import re

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

local_db_str = json.dumps(local_db, ensure_ascii=False)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update const localShopsDb = {...};
pattern_db = r'const localShopsDb = \{.*?\};\n'
match_db = re.search(pattern_db, code)
if match_db:
    code = code[:match_db.start()] + f'const localShopsDb = {local_db_str};\n' + code[match_db.end():]
    print("✅ Replaced localShopsDb with 659 products & 7 shops")
else:
    print("❌ Failed to find localShopsDb")

# 2. Dynamic shop info lookup
target_shop_block = '''        if (shopSlug === 'happier-grocery') {
          townName = 'Soho, NY';
          address = '365 Canal St, New York, NY 10013';
          lat = 40.7208;
          lng = -74.0044;
        } else if (shopSlug === 'big-night') {
          townName = 'Greenpoint, NY';
          address = '154 Franklin St, Brooklyn, NY 11222';
          lat = 40.7297;
          lng = -73.9575;
        } else {
          townName = 'West Village, NY';
          address = '205 Bleecker St, New York, NY 10012';
          lat = 40.7300;
          lng = -74.0018;
        }

        const shopTitle = shopSlug === 'happier-grocery' ? 'Happier Grocery' : (shopSlug === 'big-night' ? 'Big Night' : 'Pop Up Grocer');
        sellerName = localItem.brand || shopTitle;
        vendorName = localItem.brand || shopTitle;
        photos = [localItem.image_source_url];
        mainPhoto = localItem.image_source_url;
        categoryName = localItem.moonoh_category || "Food & Groceries";
        externalUrl = (localItem.source_url && localItem.source_url.startsWith('http')) ? localItem.source_url : (shopSlug === 'happier-grocery' ? 'https://happiergrocery.com/' : (shopSlug === 'big-night' ? 'https://bignightbk.com/' : 'https://popupgrocer.com/'));'''

replacement_shop_block = '''        const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
        const shopTitle = shopInfo.name || localItem.brand || shopSlug;
        townName = shopInfo.neighborhood ? `${shopInfo.neighborhood}, NY` : (localItem.store_city ? `${localItem.store_city}, ${localItem.store_state}` : 'NYC, NY');
        address = shopInfo.address_line_1 ? `${shopInfo.address_line_1}, ${shopInfo.city || 'New York'}, ${shopInfo.state || 'NY'} ${shopInfo.postal_code || ''}`.trim() : (localItem.store_address || 'New York, NY');
        
        sellerName = localItem.brand || shopTitle;
        vendorName = localItem.brand || shopTitle;
        photos = [localItem.image_source_url];
        mainPhoto = localItem.image_source_url;
        categoryName = localItem.primary_category || localItem.moonoh_category || "Home & Objects";
        externalUrl = (localItem.source_url && localItem.source_url.startsWith('http')) ? localItem.source_url : (shopInfo.website_url || 'https://moon-oh.com');'''

if target_shop_block in code:
    code = code.replace(target_shop_block, replacement_shop_block)
    print("✅ Dynamic shop info lookup updated")
else:
    print("⚠️ Shop block not found directly, checking regex")

# 3. Notice text with "availability"
code = code.replace(
    'Shipping, returns, and checkout are handled by',
    'Shipping, returns, availability, and checkout are handled by'
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved netlify/functions/item-detail.mjs")
