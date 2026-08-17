import re

print("=" * 80)
print("🔧 APPLYING UNIFIED CHRONOLOGICAL SORT ACROSS ALL PAGES & FUNCTIONS")
print("=" * 80)

js_timestamp_fn = """    function getItemTimestamp(item) {
      if (!item) return 0;
      if (item.postedAt) {
        const t = typeof item.postedAt === 'number' ? item.postedAt : new Date(item.postedAt).getTime();
        if (!isNaN(t) && t > 0) return t;
      }
      if (item.source_published_at) {
        const t = new Date(item.source_published_at).getTime();
        if (!isNaN(t) && t > 0) return t;
      }
      if (item.source_created_at) {
        const t = new Date(item.source_created_at).getTime();
        if (!isNaN(t) && t > 0) return t;
      }
      if (item.createdAt) {
        const t = typeof item.createdAt === 'number' ? item.createdAt : new Date(item.createdAt).getTime();
        if (!isNaN(t) && t > 0) return t;
      }
      const img = item.photo || item.image || item.image_source_url || '';
      const mTemp = String(img).match(/\\/temp\\/(\\d{13})\\//);
      if (mTemp) {
        const t = parseInt(mTemp[1], 10);
        if (!isNaN(t) && t > 0) return t;
      }
      const numStr = String(item.no || item.id || '').replace(/\\D/g, '');
      const num = parseInt(numStr, 10) || 0;
      if (num > 0) {
        return 1700000000000 + num * 100000;
      }
      return 0;
    }"""

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    explore_html = f.read()

if 'function getItemTimestamp' not in explore_html:
    explore_html = explore_html.replace('function calculateRelevanceScore', f'{js_timestamp_fn}\n\n    function calculateRelevanceScore')

new_newest_block = """      } else if (effectiveSort === 'newest') {
        filtered.sort((a, b) => {
          const tA = getItemTimestamp(a);
          const tB = getItemTimestamp(b);
          if (tB !== tA) return tB - tA;
          const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
          const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
          return numB - numA;
        });
      }"""

explore_html = re.sub(
    r'\}\s*else if \(effectiveSort === \'newest\'\)\s*\{[\s\S]*?\}\s*else if \(effectiveSort === \'price-asc\'\)',
    lambda m: f"{new_newest_block} else if (effectiveSort === 'price-asc')",
    explore_html
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(explore_html)
print("✅ Updated explore.html with unified chronological sort")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

if 'function getItemTimestamp' not in index_html:
    index_html = index_html.replace('function filterAndRender', f'{js_timestamp_fn}\n\n      function filterAndRender')

old_filter_sort = 'currentFilteredPool = filtered;'
new_filter_sort = """filtered.sort((a, b) => {
          const tA = getItemTimestamp(a);
          const tB = getItemTimestamp(b);
          if (tB !== tA) return tB - tA;
          const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
          const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
          return numB - numA;
        });
        currentFilteredPool = filtered;"""

if old_filter_sort in index_html and 'filtered.sort((a, b) => {' not in index_html:
    index_html = index_html.replace(old_filter_sort, new_filter_sort)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated index.html with unified chronological sort")

# 3. Update netlify/functions/explore.mjs
with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    explore_mjs = f.read()

if 'function getItemTimestamp' not in explore_mjs:
    explore_mjs = explore_mjs.replace('function inferCategoryFromText', f'''function getItemTimestamp(item) {{
  if (!item) return 0;
  if (item.postedAt) {{
    const t = typeof item.postedAt === 'number' ? item.postedAt : new Date(item.postedAt).getTime();
    if (!isNaN(t) && t > 0) return t;
  }}
  if (item.source_published_at) {{
    const t = new Date(item.source_published_at).getTime();
    if (!isNaN(t) && t > 0) return t;
  }}
  const img = item.photo || item.image || item.image_source_url || '';
  const mTemp = String(img).match(/\\/temp\\/(\\d{{13}})\\//);
  if (mTemp) {{
    const t = parseInt(mTemp[1], 10);
    if (!isNaN(t) && t > 0) return t;
  }}
  const numStr = String(item.no || item.id || '').replace(/\\D/g, '');
  const num = parseInt(numStr, 10) || 0;
  if (num > 0) {{
    return 1700000000000 + num * 100000;
  }}
  return 0;
}}

function inferCategoryFromText''')

explore_mjs = explore_mjs.replace(
    'cachedCombinedItems.sort((a, b) => (b.postedAt || 0) - (a.postedAt || 0));',
    '''cachedCombinedItems.sort((a, b) => {
      const tA = getItemTimestamp(a);
      const tB = getItemTimestamp(b);
      if (tB !== tA) return tB - tA;
      const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
      const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
      return numB - numA;
    });'''
)

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(explore_mjs)
print("✅ Updated netlify/functions/explore.mjs with unified chronological sort")

print("\n" + "=" * 80)
print("🎉 ALL FILES UPDATED WITH UNIFIED CHRONOLOGICAL SORT!")
print("=" * 80)
