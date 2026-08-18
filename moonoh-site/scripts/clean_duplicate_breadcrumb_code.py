with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

duplicate_block = '''        if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
      const shopDisplayName = shopInfo.name || sellerName || 'Local Shop';
      const shopProfileUrl = `/local-shops/${shopSlug}`;
      const regionLinkUrl = generateRegionSlugUrl(townName, 'localshops');
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'localshops');

      breadcrumbHtml = `
        <a href="/explore?source=localshops">Local Shops</a>
        <span class="sep">›</span>
        <a href="${shopProfileUrl}">${shopDisplayName}</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;
    } else if (isExternal) {
      if (externalSource === 'kimc') {
        currentSourceKey = 'foodrescue';
        fallbackExploreUrl = '/explore?source=foodrescue';
        const regionLinkUrl = generateRegionSlugUrl(townName, 'foodrescue');
        const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'foodrescue');
        breadcrumbHtml = `
          <a href="/explore?source=foodrescue">Food Rescue</a>
          <span class="sep">›</span>
          <a href="${regionLinkUrl}">${townName}</a>
          <span class="sep">›</span>
          <a href="${categoryLinkUrl}">${categoryName}</a>
          <span class="sep">›</span>
        `;
      } else {
        currentSourceKey = 'marketplaces';
        fallbackExploreUrl = '/explore?source=marketplaces';
        const regionLinkUrl = generateRegionSlugUrl(townName, 'marketplaces');
        const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'marketplaces');
        breadcrumbHtml = `
          <a href="/explore?source=marketplaces">Marketplaces</a>
          <span class="sep">›</span>
          <a href="${regionLinkUrl}">${townName}</a>
          <span class="sep">›</span>
          <a href="${categoryLinkUrl}">${categoryName}</a>
          <span class="sep">›</span>
        `;
      }
    } else {
      currentSourceKey = 'moonoh';
      fallbackExploreUrl = '/explore?source=moonoh';
      const regionLinkUrl = generateRegionSlugUrl(townName, 'moonoh');
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'moonoh');
      breadcrumbHtml = `
        <a href="/explore?source=moonoh">Explore</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;
    }'''

single_block = '''    // Determine exact source context and breadcrumb links
    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
      const shopDisplayName = shopInfo.name || sellerName || 'Local Shop';
      const shopProfileUrl = `/local-shops/${shopSlug}`;
      const regionLinkUrl = generateRegionSlugUrl(townName, 'localshops');
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'localshops');

      breadcrumbHtml = `
        <a href="/explore?source=localshops">Local Shops</a>
        <span class="sep">›</span>
        <a href="${shopProfileUrl}">${shopDisplayName}</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;
    } else if (isExternal) {
      if (externalSource === 'kimc') {
        currentSourceKey = 'foodrescue';
        fallbackExploreUrl = '/explore?source=foodrescue';
        const regionLinkUrl = generateRegionSlugUrl(townName, 'foodrescue');
        const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'foodrescue');
        breadcrumbHtml = `
          <a href="/explore?source=foodrescue">Food Rescue</a>
          <span class="sep">›</span>
          <a href="${regionLinkUrl}">${townName}</a>
          <span class="sep">›</span>
          <a href="${categoryLinkUrl}">${categoryName}</a>
          <span class="sep">›</span>
        `;
      } else {
        currentSourceKey = 'marketplaces';
        fallbackExploreUrl = '/explore?source=marketplaces';
        const regionLinkUrl = generateRegionSlugUrl(townName, 'marketplaces');
        const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'marketplaces');
        breadcrumbHtml = `
          <a href="/explore?source=marketplaces">Marketplaces</a>
          <span class="sep">›</span>
          <a href="${regionLinkUrl}">${townName}</a>
          <span class="sep">›</span>
          <a href="${categoryLinkUrl}">${categoryName}</a>
          <span class="sep">›</span>
        `;
      }
    } else {
      currentSourceKey = 'moonoh';
      fallbackExploreUrl = '/explore?source=moonoh';
      const regionLinkUrl = generateRegionSlugUrl(townName, 'moonoh');
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'moonoh');
      breadcrumbHtml = `
        <a href="/explore?source=moonoh">Explore</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;
    }'''

# Replace the duplicated occurrence
first_idx = code.find('        if (localProductMatch) {')
second_idx = code.find('    } else if (isExternal) {', first_idx + 100)
end_idx = code.find('    // Render HTML Page', second_idx)

if first_idx != -1 and end_idx != -1:
    code = code[:first_idx] + single_block + '\n\n' + code[end_idx:]
    print("✅ Cleaned duplicate breadcrumb block in item-detail.mjs")
else:
    print("Could not find exact slice")

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)
