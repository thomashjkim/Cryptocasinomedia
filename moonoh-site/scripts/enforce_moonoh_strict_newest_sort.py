import re

print("=" * 80)
print("🔧 ENFORCING STRICT NEWEST (ITEM NO DESCENDING) SORT FOR MOONOH TAB")
print("=" * 80)

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

target_sort_block = '''      } else if (effectiveSort === 'newest') {
        if (activeSource === 'localshops' && !currentSearchQuery) {
          filtered = interleaveLocalProducts(filtered);
        } else if ((activeSource === 'marketplaces' || activeSource === 'others') && !currentSearchQuery) {
          filtered = interleaveMarketplaceProducts(filtered);
        } else {
          filtered.sort((a, b) => {
            const tA = getItemTimestamp(a);
            const tB = getItemTimestamp(b);
            if (tB !== tA) return tB - tA;
            const numA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
            const numB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
            return numB - numA;
          });
        }
      }'''

replacement_sort_block = '''      } else if (effectiveSort === 'newest') {
        if (activeSource === 'localshops' && !currentSearchQuery) {
          filtered = interleaveLocalProducts(filtered);
        } else if ((activeSource === 'marketplaces' || activeSource === 'others') && !currentSearchQuery) {
          filtered = interleaveMarketplaceProducts(filtered);
        } else {
          filtered.sort((a, b) => {
            // Strict Moonoh auto-increment ID sorting (highest No = most recently posted)
            if (activeSource === 'moonoh' || (isStrictMoonoh(a) && isStrictMoonoh(b))) {
              const noA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
              const noB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
              if (noA > 0 && noB > 0 && noA !== noB) return noB - noA;
            }
            const tA = getItemTimestamp(a);
            const tB = getItemTimestamp(b);
            if (tB !== tA) return tB - tA;
            const numA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
            const numB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
            return numB - numA;
          });
        }
      }'''

if target_sort_block in exp_html:
    exp_html = exp_html.replace(target_sort_block, replacement_sort_block)
    with open('explore.html', 'w', encoding='utf-8') as f:
        f.write(exp_html)
    print("✅ explore.html: Enforced strict No. descending sort for Moonoh items")
else:
    print("⚠️ Could not find exact sort block in explore.html")

# 2. Update explore.mjs
with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    exp_mjs = f.read()

target_mjs_sort = '''    cachedCombinedItems.sort((a, b) => {
      const tA = getItemTimestamp(a);
      const tB = getItemTimestamp(b);
      if (tB !== tA) return tB - tA;
      const numA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
      const numB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
      return numB - numA;
    });'''

replacement_mjs_sort = '''    cachedCombinedItems.sort((a, b) => {
      if (a.source === 'moonoh' && b.source === 'moonoh') {
        const noA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
        const noB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
        if (noA > 0 && noB > 0 && noA !== noB) return noB - noA;
      }
      const tA = getItemTimestamp(a);
      const tB = getItemTimestamp(b);
      if (tB !== tA) return tB - tA;
      const numA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
      const numB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
      return numB - numA;
    });'''

if target_mjs_sort in exp_mjs:
    exp_mjs = exp_mjs.replace(target_mjs_sort, replacement_mjs_sort)
    with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
        f.write(exp_mjs)
    print("✅ explore.mjs: Enforced strict No. descending sort for Moonoh items")
else:
    print("⚠️ Could not find exact sort block in explore.mjs")
