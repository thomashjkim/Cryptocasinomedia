import re

print("=" * 80)
print("🧭 ENFORCING ACCURATE BREADCRUMB CATEGORIES & TAB + REGION + CATEGORY COMBINATIONS")
print("=" * 80)

# =========================================================================
# 1. Update netlify/functions/item-detail.mjs
# =========================================================================
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    item_code = f.read()

# Helper to generate category slug
category_helper_code = '''
function getCategorySlug(catStr) {
  if (!catStr) return 'other';
  let c = String(catStr).toLowerCase().trim();
  if (c.includes('vintage') || c.includes('fashion') && (c.includes('vintage') || c.includes('clothing'))) return 'vintage-fashion';
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

# Replace helper definitions
item_code = re.sub(
    r'function generateRegionSlugUrl[\s\S]*?return `/explore\$\{qStr\}`;[\s\S]*?function generateCategorySlugUrl[\s\S]*?return `/explore\$\{qStr\}`;[\s\S]*?\}',
    category_helper_code.strip(),
    item_code
)

# Update breadcrumb generation in item-detail.mjs
new_breadcrumb_generation = '''    if (localProductMatch) {
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

item_code = re.sub(
    r'if \(localProductMatch\) \{[\s\S]*?breadcrumbHtml = `[\s\S]*?`;\s*\}',
    new_breadcrumb_generation,
    item_code
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(item_code)
print("✅ Updated breadcrumb URL generation in item-detail.mjs")


# =========================================================================
# 2. Update explore.html
# =========================================================================
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

# Enhance parameter parsing in explore.html
new_param_parser = '''    // Parse initial URL parameters on page load (Tab, Region, Category, Shop)
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
      
      // Region selection
      if (initialParams.has('area') || initialParams.has('town') || initialParams.has('region')) {
        const targetArea = (initialParams.get('area') || initialParams.get('town') || initialParams.get('region') || '').trim();
        const locSelect = document.getElementById('location-select');
        if (locSelect && targetArea) {
          for (let opt of locSelect.options) {
            if (opt.value && (opt.value.toLowerCase() === targetArea.toLowerCase() || 
                targetArea.toLowerCase().includes(opt.value.toLowerCase()) || 
                opt.value.toLowerCase().includes(targetArea.toLowerCase()))) {
              locSelect.value = opt.value;
              activeTown = opt.value;
              break;
            }
          }
        }
      }
      
      // Category selection across ALL tabs
      if (initialParams.has('category') || initialParams.has('cat')) {
        const rawCat = (initialParams.get('category') || initialParams.get('cat') || '').toLowerCase().replace(/[^a-z0-9]/g, '');
        
        if (activeSource === 'localshops') {
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
        } else {
          // General categories for Moonoh, Marketplaces, Food Rescue
          const generalCatSlugMap = {
            'foodgroceries': 'food-groceries',
            'food': 'food-groceries',
            'groceries': 'food-groceries',
            'furniture': 'furniture',
            'electronics': 'electronics',
            'appliances': 'electronics',
            'electronicsappliances': 'electronics',
            'healthbeauty': 'health-beauty',
            'womensfashion': 'womens-fashion',
            'mensfashion': 'mens-fashion',
            'shoes': 'shoes',
            'babykids': 'baby-kids',
            'sportsleisure': 'sports-leisure',
            'toysgames': 'toys-games',
            'jewelrywatches': 'jewelry-watches',
            'luggagesbags': 'luggages-bags',
            'homegarden': 'home-garden',
            'antiques': 'antiques',
            'artsbooksmusic': 'arts-books-music',
            'free': 'free',
            'petsupplies': 'pet-supplies'
          };
          const matchedSlug = generalCatSlugMap[rawCat] || rawCat;
          const targetLabel = pillSlugToLabel[matchedSlug];
          
          if (targetLabel) {
            document.querySelectorAll('#category-filter-container .filter-pill').forEach(btn => {
              const bLabel = btn.textContent.trim();
              if (bLabel.toLowerCase() === targetLabel.toLowerCase() || (pillLabelToSlug[bLabel] || '').toLowerCase() === matchedSlug) {
                btn.classList.add('active');
              } else {
                btn.classList.remove('active');
              }
            });
          }
        }
      }
      
      updateSearchUI();
    } catch (err) {}'''

exp_html = re.sub(
    r'// Parse initial URL parameters on page load[\s\S]*?updateSearchUI\(\);\s*\}\s*catch\s*\(err\)\s*\{\}',
    new_param_parser.strip(),
    exp_html
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp_html)
print("✅ Updated explore.html parameter parsing & simultaneous Tab + Region + Category activation")


# =========================================================================
# 3. Update netlify/functions/explore.mjs (SSR)
# =========================================================================
with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    exp_mjs = f.read()

# Make sure query parsing supports area, category, source
exp_mjs = exp_mjs.replace(
    "const qTownName = q.get('townName') || q.get('town');",
    "const qTownName = q.get('area') || q.get('townName') || q.get('town') || q.get('region');"
)

exp_mjs = exp_mjs.replace(
    "const qSource = (q.get('source') || q.get('tab') || '').toLowerCase().trim();",
    "const qSource = (q.get('source') || q.get('tab') || '').toLowerCase().trim();"
)

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(exp_mjs)
print("✅ Updated explore.mjs SSR parameter support")
