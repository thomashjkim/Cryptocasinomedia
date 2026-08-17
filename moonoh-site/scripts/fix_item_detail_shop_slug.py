with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix shopSlug in breadcrumb_calc_logic
code = code.replace(
    '''    if (localProductMatch) {
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};''',
    '''    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};'''
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Fixed shopSlug declaration in breadcrumb_calc_logic")
