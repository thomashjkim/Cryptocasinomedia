import re

print("=" * 80)
print("🚀 UPGRADING ITEM DETAIL BREADCRUMBS, BACK NAVIGATION & EXPLORE PARAM RESTORATION")
print("=" * 80)

# 1. Update explore.html to handle all source/category/shop URL params on load
with open('explore.html', 'r', encoding='utf-8') as f:
    explore_html = f.read()

# Enhance initCategoryFromUrl and initialParams in explore.html
old_init_params = '''    // Parse initial URL parameters on page load
    try {
      const initialParams = new URLSearchParams(window.location.search);
      if (initialParams.has('tab')) {
        const t = initialParams.get('tab');
        activeSource = (t === 'local') ? 'localshops' : t;
      }
      if (initialParams.has('q')) {
        currentSearchQuery = initialParams.get('q') || '';
      }
      if (initialParams.has('sort')) {
        currentSortOption = initialParams.get('sort');
        userHasExplicitSort = true;
      } else {
        currentSortOption = currentSearchQuery ? 'relevance' : 'newest';
        userHasExplicitSort = false;
      }
      if (initialParams.has('area')) {
        activeTown = initialParams.get('area') || '';
        const locSelect = document.getElementById('location-select');
        if (locSelect) locSelect.value = activeTown;
      }
      updateSearchUI();
    } catch (err) {}'''

new_init_params = '''    // Parse initial URL parameters on page load
    try {
      const initialParams = new URLSearchParams(window.location.search);
      if (initialParams.has('tab') || initialParams.has('source')) {
        const t = (initialParams.get('tab') || initialParams.get('source') || '').toLowerCase();
        if (t === 'local' || t === 'localshops' || t === 'local-shops') activeSource = 'localshops';
        else if (t === 'marketplaces' || t === 'marketplace' || t === 'others') activeSource = 'marketplaces';
        else if (t === 'foodrescue' || t === 'food-rescue') activeSource = 'foodrescue';
        else if (t === 'moonoh') activeSource = 'moonoh';
        else activeSource = t;
      }
      if (initialParams.has('q')) {
        currentSearchQuery = initialParams.get('q') || '';
      }
      if (initialParams.has('shop')) {
        currentSearchQuery = initialParams.get('shop') || '';
      }
      if (initialParams.has('sort')) {
        currentSortOption = initialParams.get('sort');
        userHasExplicitSort = true;
      } else {
        currentSortOption = currentSearchQuery ? 'relevance' : 'newest';
        userHasExplicitSort = false;
      }
      if (initialParams.has('area')) {
        activeTown = initialParams.get('area') || '';
        const locSelect = document.getElementById('location-select');
        if (locSelect) locSelect.value = activeTown;
      }
      
      // Handle local category parameter (e.g. ?category=vintage-fashion or ?category=Coffee & Pantry)
      if (initialParams.has('category') || initialParams.has('cat')) {
        const rawCat = (initialParams.get('category') || initialParams.get('cat') || '').toLowerCase().replace(/[^a-z0-9]/g, '');
        const localCatMap = {
          'vintagefashion': 'Vintage & Fashion',
          'vintage': 'Vintage & Fashion',
          'fashion': 'Vintage & Fashion',
          'homeobjects': 'Home & Objects',
          'home': 'Home & Objects',
          'objects': 'Home & Objects',
          'coffeepantry': 'Coffee & Pantry',
          'coffee': 'Coffee & Pantry',
          'pantry': 'Coffee & Pantry',
          'giftsculture': 'Gifts & Culture',
          'gifts': 'Gifts & Culture',
          'culture': 'Gifts & Culture',
          'all': 'All'
        };
        if (localCatMap[rawCat]) {
          activeLocalCategory = localCatMap[rawCat];
          document.querySelectorAll('#local-filter-container .filter-pill').forEach(btn => {
            if ((btn.getAttribute('data-local-cat') || '').toLowerCase() === activeLocalCategory.toLowerCase()) {
              btn.classList.add('active');
            } else {
              btn.classList.remove('active');
            }
          });
        }
      }
      updateSearchUI();
    } catch (err) {}'''

if old_init_params in explore_html:
    explore_html = explore_html.replace(old_init_params, new_init_params)
    with open('explore.html', 'w', encoding='utf-8') as f:
        f.write(explore_html)
    print("✅ Updated explore.html with enhanced parameter restoration")
else:
    print("⚠️ old_init_params not exact match in explore.html, checking alternative...")

# 2. Update netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    item_detail_mjs = f.read()

# Replace generateRegionSlugUrl and generateCategorySlugUrl and breadcrumb markup
helpers_replacement = '''function generateRegionSlugUrl(locStr, sourceParam) {
  if (!locStr) return sourceParam ? `/explore?source=${sourceParam}` : '/explore';
  let l = locStr.toLowerCase();
  const qStr = sourceParam ? `?source=${sourceParam}` : '';
  if (l.includes('manhattan') || l.includes('soho') || l.includes('tribeca') || l.includes('midtown') || l.includes('new york')) return `/explore/manhattan${qStr}`;
  if (l.includes('queens') || l.includes('bayside') || l.includes('flushing') || l.includes('astoria') || l.includes('lic')) return `/explore/queens${qStr}`;
  if (l.includes('brooklyn') || l.includes('greenpoint') || l.includes('williamsburg') || l.includes('bushwick') || l.includes('dumbo')) return `/explore/brooklyn${qStr}`;
  if (l.includes('bronx')) return `/explore/bronx${qStr}`;
  if (l.includes('staten island')) return `/explore/staten-island${qStr}`;
  if (l.includes('hudson') || l.includes('jersey city') || l.includes('hoboken')) return `/explore/hudson-county-nj${qStr}`;
  if (l.includes('bergen') || l.includes('fort lee') || l.includes('palisades')) return `/explore/bergen-county-nj${qStr}`;
  return `/explore${qStr}`;
}

function generateCategorySlugUrl(catStr, regionStr, sourceParam) {
  if (!catStr) return sourceParam ? `/explore?source=${sourceParam}` : '/explore';
  let c = catStr.toLowerCase();
  const qStr = sourceParam ? `?source=${sourceParam}` : '';

  // Local Category URLs
  if (c.includes('vintage') || c.includes('fashion') || c.includes('clothing')) {
    return sourceParam === 'localshops' ? `/explore?source=localshops&category=vintage-fashion` : `/explore/womens-fashion${qStr}`;
  }
  if (c.includes('coffee') || c.includes('pantry')) {
    return sourceParam === 'localshops' ? `/explore?source=localshops&category=coffee-pantry` : `/explore/food-groceries${qStr}`;
  }
  if (c.includes('home & objects') || c.includes('objects') || c.includes('tableware')) {
    return sourceParam === 'localshops' ? `/explore?source=localshops&category=home-objects` : `/explore/home-garden${qStr}`;
  }
  if (c.includes('gifts') || c.includes('culture')) {
    return sourceParam === 'localshops' ? `/explore?source=localshops&category=gifts-culture` : `/explore/arts-books-music${qStr}`;
  }

  // General Categories
  let catSlug = 'other';
  if (c.includes('food') || c.includes('grocery') || c.includes('drink')) catSlug = 'food-groceries';
  else if (c.includes('furniture')) catSlug = 'furniture';
  else if (c.includes('electronic')) catSlug = 'electronics';
  else if (c.includes('health') || c.includes('beauty')) catSlug = 'health-beauty';
  else if (c.includes('women')) catSlug = 'womens-fashion';
  else if (c.includes('men')) catSlug = 'mens-fashion';
  else if (c.includes('shoe')) catSlug = 'shoes';
  else if (c.includes('baby') || c.includes('kid')) catSlug = 'baby-kids';
  else if (c.includes('sport') || c.includes('leisure')) catSlug = 'sports-leisure';
  else if (c.includes('toy') || c.includes('game')) catSlug = 'toys-games';
  else if (c.includes('home') || c.includes('garden')) catSlug = 'home-garden';
  else if (c.includes('jewelry') || c.includes('watch')) catSlug = 'jewelry-watches';
  else if (c.includes('bag') || c.includes('luggage')) catSlug = 'luggages-bags';
  else if (c.includes('art') || c.includes('book') || c.includes('music')) catSlug = 'arts-books-music';
  else if (c.includes('pet')) catSlug = 'pet-supplies';
  else if (c.includes('antique')) catSlug = 'antiques';

  let regSlug = null;
  if (regionStr) {
    let l = regionStr.toLowerCase();
    if (l.includes('manhattan')) regSlug = 'manhattan';
    else if (l.includes('queens')) regSlug = 'queens';
    else if (l.includes('brooklyn')) regSlug = 'brooklyn';
    else if (l.includes('bronx')) regSlug = 'bronx';
    else if (l.includes('staten island')) regSlug = 'staten-island';
    else if (l.includes('fort lee')) regSlug = 'fort-lee-nj';
    else if (l.includes('bergen')) regSlug = 'bergen-county-nj';
    else if (l.includes('hudson')) regSlug = 'hudson-county-nj';
  }

  if (regSlug && catSlug !== 'other') {
    return `/explore/${regSlug}/${catSlug}${qStr}`;
  } else if (catSlug !== 'other') {
    return `/explore/${catSlug}${qStr}`;
  }
  return `/explore${qStr}`;
}'''

# Replace helper functions in item-detail.mjs
item_detail_mjs = re.sub(
    r'function generateRegionSlugUrl[\s\S]*?function generateSlug',
    f"{helpers_replacement}\n\nfunction generateSlug",
    item_detail_mjs
)

# Now construct smart breadcrumbs and Back button in HTML template
new_header_and_breadcrumb = '''  <!-- Top Header -->
  <header class="header-nav">
    <div class="header-content">
      <a href="${fallbackExploreUrl}" class="header-back" onclick="handleBackNavigation(event, '${fallbackExploreUrl}')">
        ← <span class="back-text-full">Back to Explore</span><span class="back-text-short">Back</span>
      </a>
      <a href="/" class="header-logo">
        <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e51874e4a73ff20cb673ec_Logo.svg" alt="moonoh logo"/>
      </a>
      <button class="header-share-btn" onclick="openShareModal()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
        <span>Share</span>
      </button>
    </div>
  </header>

  <!-- Product Detail Container -->
  <main class="item-detail-container">

    <!-- Smart Filter-Linked Breadcrumbs -->
    <nav class="breadcrumb-bar" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="sep">›</span>
      ${breadcrumbHtml}
      <span class="current">${title}</span>
    </nav>'''

# Add fallbackExploreUrl and breadcrumbHtml computation in item-detail.mjs handler
breadcrumb_calc_logic = '''
    // Determine exact source context and fallback URLs
    let currentSourceKey = 'moonoh';
    let fallbackExploreUrl = '/explore?source=moonoh';
    let breadcrumbHtml = '';

    if (localProductMatch) {
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
    }
'''

# Insert breadcrumb_calc_logic right before return new Response(
item_detail_mjs = re.sub(
    r'(const html = `<!DOCTYPE html>)',
    f"{breadcrumb_calc_logic}\n    \\1",
    item_detail_mjs
)

# Replace the top header and breadcrumb section in HTML string
item_detail_mjs = re.sub(
    r'<!-- Top Header -->[\s\S]*?<nav class="breadcrumb-bar" aria-label="Breadcrumb">[\s\S]*?</nav>',
    new_header_and_breadcrumb,
    item_detail_mjs
)

# Add handleBackNavigation JS function right before </body>
back_nav_js = '''  <script>
    function handleBackNavigation(e, fallbackUrl) {
      e.preventDefault();
      if (window.history.length > 1 && document.referrer && (document.referrer.includes(window.location.host) || document.referrer.includes('moon-oh.com')) && !document.referrer.includes('/item/') && !document.referrer.includes('/local-product/')) {
        window.history.back();
      } else {
        window.location.href = fallbackUrl;
      }
    }
  </script>
</body>'''

if 'function handleBackNavigation' not in item_detail_mjs:
    item_detail_mjs = item_detail_mjs.replace('</body>', back_nav_js)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(item_detail_mjs)

print("✅ Saved netlify/functions/item-detail.mjs with smart breadcrumbs & back navigation")
