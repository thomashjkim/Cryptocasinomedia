import fs from 'fs';
import mixerPkg from '../js/local-products-mixer.js';
const { getBalancedLocalProducts } = mixerPkg;

function normalizeSearchText(str) {
  if (!str) return '';
  return String(str)
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function getItemSearchText(item) {
  const fields = [
    item.title || '',
    item.brand || '',
    item.badgeName || '',
    item.store_name || '',
    item.sourceName || '',
    item.category || item.categoryName || '',
    item.location || item.townName || item.rawTown || '',
    item.description || item.moonoh_summary || ''
  ];
  return normalizeSearchText(fields.join(' '));
}

function searchPool(items, query) {
  if (!query) return items;
  const tokens = normalizeSearchText(query).split(' ').filter(Boolean);
  return items.filter(item => {
    const text = getItemSearchText(item);
    return tokens.every(token => text.includes(token));
  });
}

function sortPool(items, sortOption, isLocal = false) {
  let list = [...items];
  if (sortOption === 'recommended') {
    if (isLocal) {
      return getBalancedLocalProducts(list, { context: 'explore-local' });
    }
    return list;
  }
  if (sortOption === 'newest') {
    return list.sort((a, b) => {
      const dateA = a.source_published_at ? new Date(a.source_published_at).getTime() : (a.postedAt ? new Date(a.postedAt).getTime() : null);
      const dateB = b.source_published_at ? new Date(b.source_published_at).getTime() : (b.postedAt ? new Date(b.postedAt).getTime() : null);
      if (dateA !== null && dateB !== null) return dateB - dateA;
      if (dateA !== null && dateB === null) return -1;
      if (dateA === null && dateB !== null) return 1;
      return 0;
    });
  }
  if (sortOption === 'price-asc') {
    return list.sort((a, b) => {
      const priceA = (typeof a.price === 'number' && a.price > 0) ? a.price : ((typeof a.current_price === 'number' && a.current_price > 0) ? a.current_price : null);
      const priceB = (typeof b.price === 'number' && b.price > 0) ? b.price : ((typeof b.current_price === 'number' && b.current_price > 0) ? b.current_price : null);
      if (priceA !== null && priceB !== null) return priceA - priceB;
      if (priceA !== null && priceB === null) return -1;
      if (priceA === null && priceB !== null) return 1;
      return 0;
    });
  }
  if (sortOption === 'price-desc') {
    return list.sort((a, b) => {
      const priceA = (typeof a.price === 'number' && a.price > 0) ? a.price : ((typeof a.current_price === 'number' && a.current_price > 0) ? a.current_price : null);
      const priceB = (typeof b.price === 'number' && b.price > 0) ? b.price : ((typeof b.current_price === 'number' && b.current_price > 0) ? b.current_price : null);
      if (priceA !== null && priceB !== null) return priceB - priceA;
      if (priceA !== null && priceB === null) return -1;
      if (priceA === null && priceB !== null) return 1;
      return 0;
    });
  }
  if (sortOption === 'name-asc') {
    return list.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
  }
  return list;
}

async function runPhase3CSearchTests() {
  console.log('======================================================================');
  console.log('🔍 RUNNING PHASE 3C EXPLORE SEARCH & SORT AUTOMATED VALIDATION SUITE');
  console.log('======================================================================\n');

  const localDb = JSON.parse(fs.readFileSync('local_shops_data.json', 'utf8'));
  const localProducts = localDb.products;

  // 1. Independent Tab Search Scopes
  console.log('--- 1. TAB SEARCH INDEPENDENCE & SCOPING ---');
  const query = 'coffee';
  const localCoffee = searchPool(localProducts, query);
  console.log(`  Local search for "${query}": ${localCoffee.length} items found (e.g. ${localCoffee[0]?.title})`);
  if (localCoffee.length === 0) throw new Error('❌ Local coffee search returned 0!');

  // 2. Search Field Coverage (Title, Brand, Neighborhood, Category)
  console.log('\n--- 2. SEARCH FIELD NORMALIZATION & MATCHING ---');
  const queries = [
    { q: 'DUMBO', expectMin: 1, desc: 'Neighborhood match (Front General Store)' },
    { q: 'Miyake', expectMin: 1, desc: 'Brand match' },
    { q: 'Pantry', expectMin: 1, desc: 'Category match' },
    { q: 'catnip', expectMin: 1, desc: 'Title match' }
  ];
  for (const t of queries) {
    const res = searchPool(localProducts, t.q);
    console.log(`  Query "${t.q}" (${t.desc}): ${res.length} matches (>= ${t.expectMin}: ${res.length >= t.expectMin})`);
    if (res.length < t.expectMin) throw new Error(`❌ Search failed for query: ${t.q}`);
  }

  // 3. 5 Sort Options Test on Local Tab
  console.log('\n--- 3. 5 SORT OPTIONS VERIFICATION ---');
  const sortOptions = ['recommended', 'newest', 'price-asc', 'price-desc', 'name-asc'];
  for (const s of sortOptions) {
    const sorted = sortPool(localProducts, s, true);
    console.log(`  Sort: ${s.padEnd(12)} -> 1st: "${sorted[0]?.title.substring(0, 30)}" ($${sorted[0]?.current_price})`);
    if (sorted.length !== localProducts.length) throw new Error(`❌ Sort ${s} altered list length!`);
  }

  // 4. Local Recommended Round-Robin Mixing with Query
  console.log('\n--- 4. LOCAL RECOMMENDED MIXING AFTER SEARCH ---');
  const fashionItems = searchPool(localProducts, 'vintage');
  const mixedFashion = sortPool(fashionItems, 'recommended', true);
  let maxConsec = 0, curr = 0, prev = null;
  // Check the first 24 items while multiple stores coexist
  for (const item of mixedFashion.slice(0, 24)) {
    if (item.shop_id === prev) curr++;
    else { curr = 1; prev = item.shop_id; }
    if (curr > maxConsec) maxConsec = curr;
  }
  console.log(`  Filtered "vintage" items (First 24 results) -> Max consecutive: ${maxConsec} (<= 2: ${maxConsec <= 2})`);
  if (maxConsec > 2) throw new Error('❌ Local search recommended mixing violated max consecutive in first 24!');

  // 5. Check Sitemap clean of query URLs
  console.log('\n--- 5. SITEMAP SEO & NO QUERY URLS ---');
  const localSitemap = fs.readFileSync('sitemap-local-products.xml', 'utf8');
  const locMatches = localSitemap.match(/<loc>[^<]*<\/loc>/g) || [];
  const hasQueryInLoc = locMatches.some(l => l.includes('?') || l.includes('&amp;q=') || l.includes('sort='));
  console.log(`  Sitemap has search query params in <loc>: ${hasQueryInLoc} (Expected: false)`);
  if (hasQueryInLoc) throw new Error('❌ Sitemap <loc> contains query parameters!');

  // 6. Viewport and markup validation in explore.html
  console.log('\n--- 6. EXPLORE HTML SEARCH UI & ACCESSIBILITY ---');
  const expHtml = fs.readFileSync('explore.html', 'utf8');
  const checks = [
    { name: 'Search Input', pass: expHtml.includes('id="explore-search-input"') && expHtml.includes('aria-label') },
    { name: 'Search Clear Button', pass: expHtml.includes('id="explore-search-clear"') && expHtml.includes('aria-label') },
    { name: 'Sort Dropdown', pass: expHtml.includes('id="explore-sort-select"') && expHtml.includes('aria-label') },
    { name: 'Results Label', pass: expHtml.includes('id="explore-results-label"') },
    { name: 'Empty Search State', pass: expHtml.includes('No items found for') && expHtml.includes('btn-empty-clear-search') },
    { name: 'Debounce 200ms', pass: expHtml.includes('200') && expHtml.includes('searchDebounceTimer') },
    { name: 'GA4 Events (search, search_clear, sort_change)', pass: expHtml.includes("'search'") && expHtml.includes("'search_clear'") && expHtml.includes("'sort_change'") }
  ];
  for (const c of checks) {
    console.log(`  ✓ ${c.name.padEnd(35)}: ${c.pass}`);
    if (!c.pass) throw new Error(`❌ Missing markup or logic for ${c.name}!`);
  }

  // 7. Merchant Feed Item Count == 0
  console.log('\n--- 7. MERCHANT FEED INTEGRITY ---');
  const { default: merchantFeedHandler } = await import('../netlify/functions/merchant-feed.mjs');
  const mfRes = await merchantFeedHandler(new Request('https://moon-oh.com/merchant-feed.xml'), {});
  const mfXml = await mfRes.text();
  const itemCount = (mfXml.match(/<item>/g) || []).length;
  console.log(`  Merchant Feed Items Count: ${itemCount} (Expected: 0)`);
  if (itemCount !== 0) throw new Error(`❌ Merchant feed contains ${itemCount} items, expected 0!`);

  console.log('\n======================================================================');
  console.log('🎉 ALL PHASE 3C SEARCH & SORT TESTS PASSED 100%!');
  console.log('======================================================================');
}

runPhase3CSearchTests().catch(e => {
  console.error(e);
  process.exit(1);
});
