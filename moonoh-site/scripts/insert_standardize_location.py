with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

helper = '''function standardizeLocationName(locStr) {
  if (!locStr) return 'Manhattan, NY';
  let l = String(locStr).toLowerCase().trim();
  if (l.includes('manhattan') || l.includes('soho') || l.includes('tribeca') || l.includes('midtown') || l.includes('new york') || l.includes('ny, ny')) return 'Manhattan, NY';
  if (l.includes('queens') || l.includes('bayside') || l.includes('flushing') || l.includes('astoria') || l.includes('lic')) return 'Queens, NY';
  if (l.includes('brooklyn') || l.includes('greenpoint') || l.includes('williamsburg') || l.includes('bushwick') || l.includes('dumbo')) return 'Brooklyn, NY';
  if (l.includes('bronx')) return 'The Bronx, NY';
  if (l.includes('staten island')) return 'Staten Island, NY';
  if (l.includes('hudson') || l.includes('jersey city') || l.includes('hoboken')) return 'Hudson County, NJ';
  if (l.includes('bergen') || l.includes('fort lee') || l.includes('palisades') || l.includes('ridgefield') || l.includes('closter')) return 'Bergen County, NJ';
  if (l.includes('nassau') || l.includes('great neck') || l.includes('long island')) return 'Nassau County, NY';
  return locStr.replace(/^[0-9]+mi\s*·\s*/i, '').trim() || 'Manhattan, NY';
}
'''

if 'function standardizeLocationName' not in code:
    code = code.replace('import { realFoodRescueItems }', helper + '\nimport { realFoodRescueItems }')
    with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ Inserted standardizeLocationName in item-detail.mjs")
else:
    print("Already present")
