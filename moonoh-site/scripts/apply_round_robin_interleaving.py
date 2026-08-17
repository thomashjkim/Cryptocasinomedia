import re
import json

print("=" * 80)
print("🚀 IMPLEMENTING ROUND-ROBIN INTERLEAVING FOR LOCAL & MARKETPLACES TABS")
print("=" * 80)

# Helper JS functions to embed
interleaving_js_functions = '''    function interleaveLocalProducts(products) {
      if (!Array.isArray(products) || products.length === 0) return [];
      const shopMap = new Map();
      for (const p of products) {
        const sId = p.shop_id || p.source || 'other';
        if (!shopMap.has(sId)) shopMap.set(sId, []);
        shopMap.get(sId).push(p);
      }
      const shopKeys = Array.from(shopMap.keys());
      const maxLen = Math.max(...shopKeys.map(k => shopMap.get(k).length));
      const result = [];
      for (let i = 0; i < maxLen; i++) {
        for (const k of shopKeys) {
          const list = shopMap.get(k);
          if (i < list.length) {
            result.push(list[i]);
          }
        }
      }
      return result;
    }

    function interleaveMarketplaceProducts(products) {
      if (!Array.isArray(products) || products.length === 0) return [];
      const karrot = [];
      const heykorean = [];
      const others = [];
      for (const p of products) {
        const src = (p.source || '').toLowerCase();
        if (src.includes('karrot')) karrot.push(p);
        else if (src.includes('heykorean')) heykorean.push(p);
        else others.push(p);
      }
      const result = [];
      let kIdx = 0, hIdx = 0;
      while (kIdx < karrot.length || hIdx < heykorean.length) {
        if (kIdx < karrot.length) result.push(karrot[kIdx++]);
        if (hIdx < heykorean.length) result.push(heykorean[hIdx++]);
        if (hIdx < heykorean.length) result.push(heykorean[hIdx++]); // 1 Karrot : 2 HeyKorean ratio to match proportions
      }
      return result.concat(others);
    }'''

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    explore_html = f.read()

# Replace or insert interleaving functions in explore.html
if 'function interleaveLocalProducts' not in explore_html:
    explore_html = explore_html.replace('function getItemTimestamp', f'{interleaving_js_functions}\n\n    function getItemTimestamp')

# Update Newest sorting block in explore.html
old_newest_block = '''      } else if (effectiveSort === 'newest') {
        filtered.sort((a, b) => {
          const tA = getItemTimestamp(a);
          const tB = getItemTimestamp(b);
          if (tB !== tA) return tB - tA;
          const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
          const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
          return numB - numA;
        });
      }'''

new_newest_block = '''      } else if (effectiveSort === 'newest') {
        if (activeSource === 'localshops' && !currentSearchQuery) {
          filtered = interleaveLocalProducts(filtered);
        } else if ((activeSource === 'marketplaces' || activeSource === 'others') && !currentSearchQuery) {
          filtered = interleaveMarketplaceProducts(filtered);
        } else {
          filtered.sort((a, b) => {
            const tA = getItemTimestamp(a);
            const tB = getItemTimestamp(b);
            if (tB !== tA) return tB - tA;
            const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
            const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
            return numB - numA;
          });
        }
      }'''

if old_newest_block in explore_html:
    explore_html = explore_html.replace(old_newest_block, new_newest_block)
else:
    explore_html = re.sub(
        r'\}\s*else if \(effectiveSort === \'newest\'\)\s*\{[\s\S]*?\}\s*else if \(effectiveSort === \'price-asc\'\)',
        f"{new_newest_block} else if (effectiveSort === 'price-asc')",
        explore_html
    )

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(explore_html)
print("✅ Updated explore.html with Local & Marketplace interleaving")

# 2. Update index.html (Home)
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

if 'function interleaveLocalProducts' not in index_html:
    index_html = index_html.replace('function getItemTimestamp', f'{interleaving_js_functions}\n\n      function getItemTimestamp')

old_index_filter = '''        filtered.sort((a, b) => {
          const tA = getItemTimestamp(a);
          const tB = getItemTimestamp(b);
          if (tB !== tA) return tB - tA;
          const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
          const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
          return numB - numA;
        });
        currentFilteredPool = filtered;'''

new_index_filter = '''        if (activeSource === 'localshops') {
          filtered = interleaveLocalProducts(filtered);
        } else if (activeSource === 'marketplaces' || activeSource === 'others') {
          filtered = interleaveMarketplaceProducts(filtered);
        } else {
          filtered.sort((a, b) => {
            const tA = getItemTimestamp(a);
            const tB = getItemTimestamp(b);
            if (tB !== tA) return tB - tA;
            const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
            const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
            return numB - numA;
          });
        }
        currentFilteredPool = filtered;'''

if old_index_filter in index_html:
    index_html = index_html.replace(old_index_filter, new_index_filter)
else:
    index_html = index_html.replace('currentFilteredPool = filtered;', new_index_filter)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated index.html with Local & Marketplace interleaving")

# 3. Update netlify/functions/explore.mjs
with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    explore_mjs = f.read()

mjs_interleaving = '''function interleaveLocalProducts(products) {
  if (!Array.isArray(products) || products.length === 0) return [];
  const shopMap = new Map();
  for (const p of products) {
    const sId = p.shop_id || p.source || 'other';
    if (!shopMap.has(sId)) shopMap.set(sId, []);
    shopMap.get(sId).push(p);
  }
  const shopKeys = Array.from(shopMap.keys());
  const maxLen = Math.max(...shopKeys.map(k => shopMap.get(k).length));
  const result = [];
  for (let i = 0; i < maxLen; i++) {
    for (const k of shopKeys) {
      const list = shopMap.get(k);
      if (i < list.length) {
        result.push(list[i]);
      }
    }
  }
  return result;
}

function interleaveMarketplaceProducts(products) {
  if (!Array.isArray(products) || products.length === 0) return [];
  const karrot = [];
  const heykorean = [];
  const others = [];
  for (const p of products) {
    const src = (p.source || '').toLowerCase();
    if (src.includes('karrot')) karrot.push(p);
    else if (src.includes('heykorean')) heykorean.push(p);
    else others.push(p);
  }
  const result = [];
  let kIdx = 0, hIdx = 0;
  while (kIdx < karrot.length || hIdx < heykorean.length) {
    if (kIdx < karrot.length) result.push(karrot[kIdx++]);
    if (hIdx < heykorean.length) result.push(heykorean[hIdx++]);
    if (hIdx < heykorean.length) result.push(heykorean[hIdx++]);
  }
  return result.concat(others);
}'''

if 'function interleaveLocalProducts' not in explore_mjs:
    explore_mjs = explore_mjs.replace('function getItemTimestamp', f'{mjs_interleaving}\n\nfunction getItemTimestamp')

explore_mjs = explore_mjs.replace(
    '''    } else if (isMarketplacesFilter) {
      filteredItems = allItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
    } else if (isLocalShopsFilter || isShopProfile) {
      const prods = (isShopProfile ? localShopsData.products.filter(p => p.shop_id === shopProfileSlug) : localShopsData.products) || [];''',
    '''    } else if (isMarketplacesFilter) {
      const mktItems = allItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
      filteredItems = interleaveMarketplaceProducts(mktItems);
    } else if (isLocalShopsFilter || isShopProfile) {
      const prods = (isShopProfile ? localShopsData.products.filter(p => p.shop_id === shopProfileSlug) : localShopsData.products) || [];
      const baseLocal = isShopProfile ? prods : interleaveLocalProducts(prods);'''
)

explore_mjs = explore_mjs.replace(
    'filteredItems = prods.map(p => ({',
    'filteredItems = (isShopProfile ? prods : interleaveLocalProducts(prods)).map(p => ({'
)

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(explore_mjs)
print("✅ Updated netlify/functions/explore.mjs with Local & Marketplace interleaving")

print("\n" + "=" * 80)
print("🎉 ALL FILES UPDATED WITH EQUAL ROUND-ROBIN INTERLEAVING!")
print("=" * 80)
