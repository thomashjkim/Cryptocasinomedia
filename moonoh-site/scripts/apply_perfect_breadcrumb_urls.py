import re

print("=" * 80)
print("🎯 APPLYING PERFECT BREADCRUMB URLS & MAPPING (TAB + REGION + CATEGORY)")
print("=" * 80)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. New Helper Functions
new_helpers = '''
function getCategorySlug(catStr) {
  if (!catStr) return 'other';
  let c = String(catStr).toLowerCase().trim();
  if (c.includes('vintage') || (c.includes('fashion') && (c.includes('vintage') || c.includes('clothing')))) return 'vintage-fashion';
  if (c.includes('coffee') || c.includes('pantry')) return 'coffee-pantry';
  if (c.includes('home & objects') || c.includes('objects') || c.includes('tableware')) return 'home-objects';
  if (c.includes('gifts') || c.includes('culture')) return 'gifts-culture';
  if (c.includes('food') || c.includes('grocer') || c.includes('drink') || c.includes('snack')) return 'food-groceries';
  if (c.includes('furniture')) return 'furniture';
  if (c.includes('electronic') || c.includes('appliance')) return 'electronics';
  if (c.includes('health') || c.includes('beauty')) return 'health-beauty';
  if (c.includes('women')) return 'womens-fashion';
  if (c.includes('men')) return 'mens-fashion';
  if (c.includes('shoe')) return 'shoes';
  if (c.includes('baby') || c.includes('kid')) return 'baby-kids';
  if (c.includes('sports') || c.includes('leisure')) return 'sports-leisure';
  if (c.includes('toy') || c.includes('game')) return 'toys-games';
  if (c.includes('jewelry') || c.includes('watch')) return 'jewelry-watches';
  if (c.includes('luggage') || c.includes('bag')) return 'luggages-bags';
  if (c.includes('pet')) return 'pet-supplies';
  if (c.includes('antique')) return 'antiques';
  if (c.includes('art') || c.includes('book') || c.includes('music')) return 'arts-books-music';
  if (c.includes('free')) return 'free';
  return c.replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'other';
}

function generateCategorySlugUrl(catStr, regionStr, sourceParam) {
  const s = sourceParam || 'moonoh';
  const catSlug = getCategorySlug(catStr);
  const loc = regionStr || 'Manhattan, NY';
  return `/explore?source=${encodeURIComponent(s)}&area=${encodeURIComponent(loc)}&category=${encodeURIComponent(catSlug)}`;
}

function generateRegionSlugUrl(locStr, sourceParam) {
  const s = sourceParam || 'moonoh';
  const loc = locStr || 'Manhattan, NY';
  return `/explore?source=${encodeURIComponent(s)}&area=${encodeURIComponent(loc)}`;
}
'''

# Replace old generateRegionSlugUrl / generateCategorySlugUrl
code = re.sub(
    r'function generateRegionSlugUrl[\s\S]*?return `/explore\$\{qStr\}`;[\s\S]*?function generateCategorySlugUrl[\s\S]*?return `/explore\$\{qStr\}`;[\s\S]*?\}',
    new_helpers.strip(),
    code
)

# 2. Update the Breadcrumb HTML construction near the end of item-detail.mjs
old_breadcrumb_construct = '''    if (localProductMatch) {
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

new_breadcrumb_construct = '''    if (localProductMatch) {
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

code = code.replace(old_breadcrumb_construct, new_breadcrumb_construct)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Successfully updated item-detail.mjs breadcrumb URLs")
