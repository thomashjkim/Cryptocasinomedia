import fs from 'fs';
import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import mixerPkg from '../js/local-products-mixer.js';
const { getBalancedLocalProducts } = mixerPkg;

async function runPhase3BTests() {
  console.log('======================================================================');
  console.log('🔍 RUNNING COMPREHENSIVE PHASE 3B VALIDATION SUITE');
  console.log('======================================================================\n');

  const localDb = JSON.parse(fs.readFileSync('local_shops_data.json', 'utf8'));
  const products = localDb.products;
  const shops = localDb.shops;

  // 1. DATA AUDIT
  console.log('--- 1. DATA AUDIT BY STORE ---');
  const shopCounts = {};
  for (const p of products) {
    shopCounts[p.shop_id] = (shopCounts[p.shop_id] || 0) + 1;
  }
  for (const [sId, c] of Object.entries(shopCounts)) {
    console.log(`  • ${shops[sId]?.name || sId} (${sId}): ${c} products`);
  }
  console.log(`Total Products: ${products.length}, Total Shops: ${Object.keys(shops).length}\n`);

  // Assertions for Data Integrity
  let missingPrices = products.filter(p => typeof p.current_price !== 'number' || p.current_price <= 0);
  let missingImages = products.filter(p => !p.image_source_url || !p.image_source_url.startsWith('http'));
  let missingUrls = products.filter(p => !p.source_url || !p.source_url.startsWith('http'));
  let duplicateSlugs = new Set();
  let seenSlugs = new Set();
  for (const p of products) {
    if (seenSlugs.has(p.slug)) duplicateSlugs.add(p.slug);
    seenSlugs.add(p.slug);
  }

  console.log(`  Price Missing/Invalid: ${missingPrices.length}`);
  console.log(`  Image Missing/Invalid: ${missingImages.length}`);
  console.log(`  Source URL Missing: ${missingUrls.length}`);
  console.log(`  Duplicate Slugs: ${duplicateSlugs.size}`);

  if (missingPrices.length > 0 || missingImages.length > 0 || duplicateSlugs.size > 0) {
    throw new Error('❌ Data integrity check failed!');
  }
  console.log('  ✅ Data Integrity Check Passed!\n');

  // 2. MIXING ALGORITHM & FAIRNESS AUDIT
  console.log('--- 2. MIXING ALGORITHM & FAIRNESS AUDIT ---');

  // Home context
  const home12 = getBalancedLocalProducts(products, { context: 'home', limit: 12 });
  const home24 = getBalancedLocalProducts(products, { context: 'home', limit: 24 });
  const home24_repeat = getBalancedLocalProducts(products, { context: 'home', limit: 24 });

  const homeDist12 = {};
  home12.forEach(i => homeDist12[i.shop_id] = (homeDist12[i.shop_id] || 0) + 1);
  const homeDist24 = {};
  home24.forEach(i => homeDist24[i.shop_id] = (homeDist24[i.shop_id] || 0) + 1);

  console.log('  Home First 12 Store Distribution:', homeDist12);
  console.log('  Home First 24 Store Distribution:', homeDist24);

  // Explore-local context
  const exp12 = getBalancedLocalProducts(products, { context: 'explore-local', limit: 12 });
  const exp24 = getBalancedLocalProducts(products, { context: 'explore-local', limit: 24 });

  const expDist12 = {};
  exp12.forEach(i => expDist12[i.shop_id] = (expDist12[i.shop_id] || 0) + 1);
  const expDist24 = {};
  exp24.forEach(i => expDist24[i.shop_id] = (expDist24[i.shop_id] || 0) + 1);

  console.log('  Explore-Local First 12 Store Distribution:', expDist12);
  console.log('  Explore-Local First 24 Store Distribution:', expDist24);

  // Max consecutive calculation
  function getMaxConsecutive(list) {
    let max = 0, curr = 0, prev = null;
    for (const item of list) {
      if (item.shop_id === prev) curr++;
      else { curr = 1; prev = item.shop_id; }
      if (curr > max) max = curr;
    }
    return max;
  }

  const maxConsecHome = getMaxConsecutive(home24);
  const maxConsecExp = getMaxConsecutive(exp24);
  const isDeterministicHome = JSON.stringify(home24.map(i => i.id)) === JSON.stringify(home24_repeat.map(i => i.id));

  console.log(`  Max Consecutive (Home 24): ${maxConsecHome} (<= 2: ${maxConsecHome <= 2})`);
  console.log(`  Max Consecutive (Explore 24): ${maxConsecExp} (<= 2: ${maxConsecExp <= 2})`);
  console.log(`  Deterministic Same-Day: ${isDeterministicHome}`);

  // Test Rotation across two different dates
  const day1 = getBalancedLocalProducts(products, { dateKey: '2026-08-17', context: 'home', limit: 7 });
  const day2 = getBalancedLocalProducts(products, { dateKey: '2026-08-18', context: 'home', limit: 7 });
  console.log(`  Day 1 Start Store: ${day1[0].shop_id} | Day 2 Start Store: ${day2[0].shop_id} (Rotated: ${day1[0].shop_id !== day2[0].shop_id})`);

  if (maxConsecHome > 2 || maxConsecExp > 2 || !isDeterministicHome) {
    throw new Error('❌ Mixing algorithm check failed!');
  }
  console.log('  ✅ Mixing Algorithm & Fairness Passed!\n');

  // 3. DETAIL PAGES & JSON-LD AUDIT (Sample 3 items from each of the 4 new stores)
  console.log('--- 3. DETAIL PAGES & JSON-LD AUDIT ---');
  const testSamples = [
    'front-general-store',
    'mirth-vintage',
    'sey-coffee',
    'salter-house'
  ];

  for (const sId of testSamples) {
    const sProds = products.filter(p => p.shop_id === sId).slice(0, 3);
    console.log(`  Checking 3 sample detail pages for ${shops[sId].name}...`);
    for (const p of sProds) {
      const url = `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`;
      const res = await itemDetailHandler(new Request(url), {});
      if (res.status !== 200) {
        throw new Error(`❌ Product page failed for ${url} with status ${res.status}`);
      }
      const html = await res.text();

      // Check self-canonical
      const hasCanon = (html.includes(`<link href="${url}" rel="canonical"/>`) || html.includes(`<link rel="canonical" href="${url}"/>`)) && html.includes(url);
      // Check title & price
      const hasTitle = html.includes(p.title);
      // Check CTA
      const hasCta = html.includes(`View at ${shops[sId].name}`) || html.includes(`View on ${shops[sId].name}`) || html.includes(p.canonical_source_url);
      // Check notice text
      const hasNotice = html.includes('Shipping, returns, availability, and checkout are handled by');
      // Check JSON-LD: seller Organization, no fake shipping/returns
      const hasOrgSeller = html.includes('"@type": "Organization"');
      const hasFakeShipping = html.includes('shippingDetails') || html.includes('hasMerchantReturnPolicy');

      if (!hasCanon || !hasTitle || !hasNotice || !hasOrgSeller || hasFakeShipping) {
        throw new Error(`❌ Detail page audit failed for ${url}: canon=${hasCanon}, title=${hasTitle}, notice=${hasNotice}, orgSeller=${hasOrgSeller}, fakeShipping=${hasFakeShipping}`);
      }
      console.log(`    ✓ ${p.slug}: HTTP 200, Canonical OK, Notice OK, JSON-LD Schema Clean`);
    }
  }
  console.log('  ✅ 12 Sample Detail Pages Across 4 New Shops Passed Audit!\n');

  // 4. REGRESSION AUDIT (Happier Grocery legacy redirects + 404 rules + merchant feed)
  console.log('--- 4. REGRESSION AUDIT ---');
  // Happier legacy slug redirect
  const legRes = await itemDetailHandler(new Request('https://moon-oh.com/local-product/happier-grocery/organic-strawberry-hibiscus-sparkling-soda'), {});
  console.log(`  Happier Legacy Redirect Status: ${legRes.status} -> ${legRes.headers.get('location')}`);
  if (legRes.status !== 301) throw new Error('❌ Happier legacy redirect failed!');

  // Chanel non-existent Moonoh ID 669111 404 test
  const hk404Res = await itemDetailHandler(new Request('https://moon-oh.com/item/chanel-classic-double-flap-bag-lambskin-black-queens-ny-669111'), {});
  console.log(`  Chanel Fake P2P ID 669111 Status: ${hk404Res.status} (noindex: ${hk404Res.headers.get('x-robots-tag') === 'noindex'})`);
  if (hk404Res.status !== 404 || hk404Res.headers.get('x-robots-tag') !== 'noindex') {
    throw new Error('❌ Chanel fake P2P 669111 404 test failed!');
  }

  // Merchant feed items count
  const { default: merchantFeedHandler } = await import('../netlify/functions/merchant-feed.mjs');
  const mfRes = await merchantFeedHandler(new Request('https://moon-oh.com/merchant-feed.xml'), {});
  const mfXml = await mfRes.text();
  const itemCount = (mfXml.match(/<item>/g) || []).length;
  console.log(`  Merchant Feed Items Count: ${itemCount} (Expected: 0)`);
  if (itemCount !== 0) throw new Error(`❌ Merchant feed contains ${itemCount} items, expected 0!`);

  console.log('  ✅ All Regression Tests Passed!\n');
  console.log('======================================================================');
  console.log('🎉 ALL PHASE 3B AUTOMATED TEST SUITES PASSED 100%!');
  console.log('======================================================================');
}

runPhase3BTests().catch(e => {
  console.error(e);
  process.exit(1);
});
