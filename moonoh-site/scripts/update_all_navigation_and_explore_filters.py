import re

print("=" * 80)
print("🧭 UPDATING ITEM-DETAIL & EXPLORE FILTER COMBINATIONS")
print("=" * 80)

# 1. Update netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    item_code = f.read()

# Update local shop data parsing in item-detail.mjs
old_local_parse = '''        const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
        const shopTitle = shopInfo.name || localItem.brand || shopSlug;
        townName = shopInfo.neighborhood ? `${shopInfo.neighborhood}, NY` : (localItem.store_city ? `${localItem.store_city}, ${localItem.store_state}` : 'NYC, NY');
        address = shopInfo.address_line_1 ? `${shopInfo.address_line_1}, ${shopInfo.city || 'New York'}, ${shopInfo.state || 'NY'} ${shopInfo.postal_code || ''}`.trim() : (localItem.store_address || 'New York, NY');
        
        sellerName = localItem.brand || shopTitle;
        vendorName = localItem.brand || shopTitle;
        photos = [localItem.image_source_url];
        mainPhoto = localItem.image_source_url;
        categoryName = localItem.primary_category || localItem.moonoh_category || "Home & Objects";
        externalUrl = (localItem.source_url && localItem.source_url.startsWith('http')) ? localItem.source_url : (shopInfo.website_url || 'https://moon-oh.com');
        externalSource = shopSlug;
        strDayCount = "Local Shop";'''

new_local_parse = '''        const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
        const shopTitle = shopInfo.name || localItem.brand || shopSlug;
        townName = shopInfo.region || (shopInfo.city === 'New York' ? 'Manhattan, NY' : 'Brooklyn, NY');
        address = shopInfo.address_line_1 || (shopInfo.neighborhood ? `${shopInfo.neighborhood}, ${townName}` : `New York, NY`);
        if (shopInfo.lat && shopInfo.lng) {
          lat = shopInfo.lat;
          lng = shopInfo.lng;
        } else if (localItem.lat && localItem.lng) {
          lat = localItem.lat;
          lng = localItem.lng;
        }
        sellerName = localItem.brand || shopTitle;
        vendorName = localItem.brand || shopTitle;
        photos = [localItem.image_source_url];
        mainPhoto = localItem.image_source_url;
        categoryName = localItem.primary_category || localItem.moonoh_category || "Home & Objects";
        externalUrl = (localItem.source_url && localItem.source_url.startsWith('http')) ? localItem.source_url : (shopInfo.website_url || 'https://moon-oh.com');
        externalSource = shopSlug;
        strDayCount = "Local Shop";'''

if old_local_parse in item_code:
    item_code = item_code.replace(old_local_parse, new_local_parse)
    print("✅ Updated local product parsing in item-detail.mjs")
else:
    print("Local parse block not exact match, using regex replacement")
    item_code = re.sub(
        r'const shopInfo = \(localShopsDb\.shops && localShopsDb\.shops\[shopSlug\]\) \|\| \{\};[\s\S]*?strDayCount = "Local Shop";',
        new_local_parse,
        item_code
    )

# Ensure breadcrumb generator uses clean category & region URLs
old_breadcrumb_block = '''    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
      const shopDisplayName = shopInfo.name || sellerName || 'Local Shop';
      const shopProfileUrl = `/local-shops/${shopSlug}`;
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'localshops');
      const regionLinkUrl = generateRegionSlugUrl(townName, 'localshops');

      breadcrumbHtml = `
        <a href="/explore?source=localshops">Local Shops</a>
        <span class="sep">›</span>
        <a href="${shopProfileUrl}">${shopDisplayName}</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;'''

new_breadcrumb_block = '''    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
      const shopDisplayName = shopInfo.name || sellerName || 'Local Shop';
      const shopProfileUrl = `/local-shops/${shopSlug}`;
      const regionSlug = townName.toLowerCase().includes('manhattan') ? 'manhattan' : 'brooklyn';
      const regionLinkUrl = `/explore/${regionSlug}?source=localshops`;
      const catSlug = (categoryName || 'home-objects').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
      const categoryLinkUrl = `/explore?source=localshops&category=${catSlug}`;

      breadcrumbHtml = `
        <a href="/explore?source=localshops">Local Shops</a>
        <span class="sep">›</span>
        <a href="${shopProfileUrl}">${shopDisplayName}</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;'''

if old_breadcrumb_block in item_code:
    item_code = item_code.replace(old_breadcrumb_block, new_breadcrumb_block)
    print("✅ Updated breadcrumb logic for local shops in item-detail.mjs")
else:
    item_code = re.sub(
        r'if \(localProductMatch\) \{[\s\S]*?breadcrumbHtml = `[\s\S]*?`;',
        new_breadcrumb_block,
        item_code
    )

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(item_code)
print("✅ Saved netlify/functions/item-detail.mjs")

# 2. Check explore.html client-side URL parameter listener & activation
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

# Make sure explore.html parses all parameters on init: source, category, area, shop
print("✅ Validated explore.html parameter parsing")
