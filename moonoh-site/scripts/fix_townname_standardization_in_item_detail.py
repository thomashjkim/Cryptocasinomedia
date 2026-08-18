import re

print("=" * 80)
print("🏙️ STANDARDIZING TOWN NAME IN ITEM-DETAIL (NO 'NYC', NO '1mi')")
print("=" * 80)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Helper function definition in item-detail.mjs
standardize_loc_helper = '''
function standardizeLocationName(rawLoc) {
  if (!rawLoc) return 'Manhattan, NY';
  let s = String(rawLoc).trim().replace(/^\\d+mi\\s*·\\s*/i, '').replace(/^\\d+mi\\s+/i, '');
  let low = s.toLowerCase();
  if (low.includes('bayside') || low.includes('flushing') || low.includes('astoria') || low.includes('queens')) return 'Queens, NY';
  if (low.includes('brooklyn') || low.includes('williamsburg') || low.includes('greenpoint') || low.includes('dumbo') || low.includes('bushwick')) return 'Brooklyn, NY';
  if (low.includes('manhattan') || low.includes('soho') || low.includes('tribeca') || low.includes('midtown') || low.includes('harlem') || low.includes('village') || low === 'nyc' || low === 'new york') return 'Manhattan, NY';
  if (low.includes('bronx')) return 'The Bronx, NY';
  if (low.includes('staten')) return 'Staten Island, NY';
  if (low.includes('fort lee') || low.includes('palisades') || low.includes('bergen') || low.includes('edgewater') || low.includes('leonia') || low.includes('paramus')) return 'Bergen County, NJ';
  if (low.includes('jersey city') || low.includes('hoboken') || low.includes('hudson')) return 'Hudson County, NJ';
  return 'Manhattan, NY';
}
'''

if 'function standardizeLocationName' not in code:
    code = code.replace('function inferCategoryFromText', f'{standardize_loc_helper}\nfunction inferCategoryFromText')

# Standardize townName in Moonoh item parsing
code = code.replace(
    'townName = d.productTownName || "NYC";',
    'townName = standardizeLocationName(d.productTownName || d.address || "Manhattan, NY");'
)

# Standardize townName in external item parsing
code = code.replace(
    "townName = extItem.location || 'Brooklyn, NY';",
    "townName = standardizeLocationName(extItem.location || extItem.rawTown || 'Brooklyn, NY');"
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Standardized location helper and townName assignment in item-detail.mjs")
