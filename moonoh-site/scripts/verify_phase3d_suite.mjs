import fs from 'fs';
import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import mixerPkg from '../js/local-products-mixer.js';
const { getBalancedMarketplaceProducts, getBalancedLocalProducts } = mixerPkg;

async function runPhase3DTests() {
  console.log('======================================================================');
  console.log('🔍 RUNNING COMPREHENSIVE PHASE 3D VALIDATION SUITE');
  console.log('======================================================================\n');

  // 1. Check Karrot count & duplicates
  console.log('--- 1. KARROT INVENTORY & DEDUPLICATION AUDIT ---');
  const { realKarrotItems, realHeyKoreanItems } = await import('../netlify/functions/external-items.mjs');
  console.log(`  Total Karrot items: ${realKarrotItems.length} (Expected: 183: ${realKarrotItems.length === 183})`);
  console.log(`  Total HeyKorean items: ${realHeyKoreanItems.length} (Expected: 1318)`);
  console.log(`  Total Marketplace items: ${realKarrotItems.length + realHeyKoreanItems.length} (Expected: 1501)`);

  const seenIds = new Set();
  const seenUrls = new Set();
  let duplicateCount = 0;
  for (const item of realKarrotItems) {
    if (seenIds.has(item.id) || seenUrls.has(item.url)) duplicateCount++;
    seenIds.add(item.id);
    seenUrls.add(item.url);
  }
  console.log(`  Karrot Duplicate IDs/URLs: ${duplicateCount} (Expected: 0)`);
  if (realKarrotItems.length !== 183 || duplicateCount > 0) {
    throw new Error('❌ Karrot inventory or deduplication check failed!');
  }
  console.log('  ✅ Karrot Inventory & Deduplication Passed!\n');

  // 2. Sample 10 new Karrot item detail pages
  console.log('--- 2. SAMPLE 10 NEW KARROT DETAIL PAGES & CANONICAL AUDIT ---');
  function generateSlug(title, locationStr, productNo) {
    let cleanTitle = (title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
    if (!cleanTitle) cleanTitle = 'item';
    if (cleanTitle.length > 50) cleanTitle = cleanTitle.substring(0, 50).replace(/-$/, '');
    let locSlug = 'nyc-ny';
    if (locationStr) {
      let l = locationStr.toLowerCase();
      if (l.includes('bayside')) locSlug = 'bayside-queens-ny';
      else if (l.includes('flushing')) locSlug = 'flushing-queens-ny';
      else if (l.includes('astoria')) locSlug = 'astoria-queens-ny';
      else if (l.includes('queens')) locSlug = 'queens-ny';
      else if (l.includes('brooklyn')) locSlug = 'brooklyn-ny';
      else if (l.includes('manhattan')) locSlug = 'manhattan-ny';
      else if (l.includes('palisades')) locSlug = 'palisades-park-nj';
      else if (l.includes('fort lee')) locSlug = 'fort-lee-nj';
      else locSlug = l.replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
    }
    return `/item/${cleanTitle}-${locSlug}-${productNo}`;
  }

  const newKarrotSamples = realKarrotItems.slice(83, 93); // 10 newly added items
  for (const item of newKarrotSamples) {
    const slug = generateSlug(item.title, item.location || item.rawTown, `ext-${item.id}`);
    const url = `https://moon-oh.com${slug}`;

    const res = await itemDetailHandler(new Request(url), {});
    if (res.status !== 200) {
      throw new Error(`❌ Detail page ${url} returned HTTP ${res.status}`);
    }
    const html = await res.text();
    const hasCanonical = html.includes('rel="canonical"') && (html.includes(url) || html.includes(item.id));
    const hasTitle = html.includes(item.title);
    const hasSourceLink = html.includes(item.url);
    const hasOrgSeller = !html.includes('"@type": "Organization"') || html.includes('Moonoh'); // Not masquerading platform as seller
    const hasFakeShipping = html.includes('shippingDetails') || html.includes('hasMerchantReturnPolicy');

    if (!hasCanonical || !hasTitle || !hasSourceLink || hasFakeShipping) {
      throw new Error(`❌ Detail page verification failed for ${url}: canon=${hasCanonical}, title=${hasTitle}, link=${hasSourceLink}, fakeShipping=${hasFakeShipping}`);
    }
    console.log(`    ✓ ${item.id}: HTTP 200 | Title OK | Source Link OK | Self-Canonical OK`);
  }
  console.log('  ✅ 10 New Karrot Detail Pages Passed Audit!\n');

  // 3. Marketplace Shared Mixing Audit
  console.log('--- 3. MARKETPLACE SHARED MIXING AUDIT ---');
  const combinedMarketplace = [...realKarrotItems, ...realHeyKoreanItems];
  const mixed24 = getBalancedMarketplaceProducts(combinedMarketplace, { limit: 24, context: 'explore-marketplace' });
  const mixed24_home = getBalancedMarketplaceProducts(combinedMarketplace, { limit: 24, context: 'home-marketplace' });

  const dist24 = {};
  mixed24.forEach(i => dist24[i.source] = (dist24[i.source] || 0) + 1);
  console.log('  Explore First 24 Platform Distribution:', dist24);

  let maxConsec = 0, curr = 0, prev = null;
  for (const item of mixed24) {
    if (item.source === prev) curr++;
    else { curr = 1; prev = item.source; }
    if (curr > maxConsec) maxConsec = curr;
  }
  console.log(`  Max Consecutive Platform: ${maxConsec} (<= 2: ${maxConsec <= 2})`);
  if (maxConsec > 2) throw new Error('❌ Marketplace mixing exceeded max consecutive of 2!');
  console.log('  ✅ Marketplace Shared Mixing Passed!\n');

  // 4. Sitemap URL count integrity
  console.log('--- 4. SITEMAP ACCURACY AUDIT ---');
  const sitemapMarketplace = fs.readFileSync('sitemap-marketplace.xml', 'utf8');
  const marketUrlsCount = (sitemapMarketplace.match(/<loc>/g) || []).length;
  console.log(`  sitemap-marketplace.xml URLs: ${marketUrlsCount} (Expected: 1501: ${marketUrlsCount === 1501})`);
  if (marketUrlsCount !== 1501) throw new Error('❌ Marketplace sitemap URL count mismatch!');
  console.log('  ✅ Sitemap URLs Count Passed!\n');

  // 5. Merchant feed item count == 0
  console.log('--- 5. MERCHANT FEED INTEGRITY AUDIT ---');
  const { default: merchantFeedHandler } = await import('../netlify/functions/merchant-feed.mjs');
  const mfRes = await merchantFeedHandler(new Request('https://moon-oh.com/merchant-feed.xml'), {});
  const mfXml = await mfRes.text();
  const mfItemCount = (mfXml.match(/<item>/g) || []).length;
  console.log(`  Merchant Feed Items Count: ${mfItemCount} (Expected: 0)`);
  if (mfItemCount !== 0) throw new Error(`❌ Merchant feed contains ${mfItemCount} items, expected 0!`);
  console.log('  ✅ Merchant Feed Clean!\n');

  // 6. Regression: Happier Grocery & Chanel 669111
  console.log('--- 6. REGRESSION AUDIT (Happier Grocery & 404 Rules) ---');
  const hgRes = await itemDetailHandler(new Request('https://moon-oh.com/local-product/happier-grocery/yeowww-catnip-cat-toys-strawberry-red'), {});
  console.log(`  Happier Grocery Sample Status: ${hgRes.status} (Expected: 200)`);
  if (hgRes.status !== 200) throw new Error('❌ Happier Grocery sample failed!');

  const hk404Res = await itemDetailHandler(new Request('https://moon-oh.com/item/chanel-classic-double-flap-bag-lambskin-black-queens-ny-669111'), {});
  console.log(`  Chanel Fake P2P ID 669111 Status: ${hk404Res.status} (noindex: ${hk404Res.headers.get('x-robots-tag') === 'noindex'})`);
  if (hk404Res.status !== 404 || hk404Res.headers.get('x-robots-tag') !== 'noindex') {
    throw new Error('❌ Chanel fake P2P 669111 404 test failed!');
  }
  console.log('  ✅ Regression Tests Passed!\n');

  console.log('======================================================================');
  console.log('🎉 ALL PHASE 3D AUTOMATED TESTS PASSED 100%!');
  console.log('======================================================================');
}

runPhase3DTests().catch(e => {
  console.error(e);
  process.exit(1);
});
