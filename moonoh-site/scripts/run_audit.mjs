import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function fullValidation() {
  console.log('=== STARTING 100% PRE-DEPLOY INTEGRITY AUDIT ===\n');

  const localDb = JSON.parse(fs.readFileSync('./local_shops_data.json', 'utf8'));
  const moonohData = JSON.parse(fs.readFileSync('./data.json', 'utf8'));

  let totalTests = 0;
  let passedTests = 0;
  const failures = [];

  function assert(condition, message) {
    totalTests++;
    if (condition) {
      passedTests++;
      console.log('  ✅ ' + message);
    } else {
      failures.push(message);
      console.log('  ❌ FAIL: ' + message);
    }
  }

  // 1. Moonoh Data Audit
  console.log('[1] Moonoh Items Audit');
  assert(moonohData.length === 597, 'Total visible Moonoh items is 597');
  const has856 = moonohData.some(i => String(i.no) === '856');
  const has857 = moonohData.some(i => String(i.no) === '857');
  assert(has856 && has857, 'New items No.856 and No.857 are present');
  const missingMoonohImg = moonohData.filter(i => !i.image && !i.photo).length;
  assert(missingMoonohImg === 0, '0 missing images in Moonoh dataset');

  // 2. Local Shops Catalog Audit
  console.log('\n[2] Local Shops Catalog Audit');
  assert(localDb.products.length === 2215, 'Total Local Shop products is 2,215');
  const shopBreakdown = {};
  localDb.products.forEach(p => {
    shopBreakdown[p.shop_id] = (shopBreakdown[p.shop_id] || 0) + 1;
  });
  console.log('  Shop Counts:', JSON.stringify(shopBreakdown));
  
  const invalidImgs = localDb.products.filter(p => !p.image_source_url || !p.image_source_url.startsWith('http'));
  assert(invalidImgs.length === 0, '100% of Local Shop products have valid HTTPS image URLs (0 missing)');
  
  const invalidPrices = localDb.products.filter(p => !p.current_price || isNaN(parseFloat(p.current_price)));
  assert(invalidPrices.length === 0, '100% of Local Shop products have valid prices');

  const invalidUrls = localDb.products.filter(p => !p.url || !p.url.startsWith('/local-product/'));
  assert(invalidUrls.length === 0, '100% of Local Shop products have correct /local-product/ URLs');

  // 3. Marketplaces Audit (Karrot 500 + HeyKorean 1442)
  console.log('\n[3] Marketplaces Audit');
  const extModule = await import('../netlify/functions/external-items.mjs');
  const karrotItems = extModule.realKarrotItems || [];
  const heyItems = extModule.realHeyKoreanItems || [];
  assert(karrotItems.length === 500, `Karrot items count is exactly 500 (found ${karrotItems.length})`);
  assert(heyItems.length === 1442, `HeyKorean items count is 1,442 (found ${heyItems.length})`);
  
  const karrotNoImg = karrotItems.filter(i => !i.image || !i.image.startsWith('http')).length;
  assert(karrotNoImg === 0, '100% of 500 Karrot items have valid HTTPS images');
  
  const karrotNYLocs = karrotItems.filter(i => i.location && (i.location.includes('NY') || i.location.includes('NJ'))).length;
  assert(karrotNYLocs === 500, '100% of 500 Karrot items have standard NYC / NJ borough locations');

  // 4. Sitemaps & robots.txt Audit
  console.log('\n[4] Sitemaps & robots.txt Audit');
  const sitemapConfigs = [
    { file: 'sitemap.xml', minUrls: 6 },
    { file: 'sitemap-index.xml', minUrls: 6 },
    { file: 'sitemap-moonoh.xml', exactUrls: 597 },
    { file: 'sitemap-local-products.xml', exactUrls: 2215 },
    { file: 'sitemap-marketplace.xml', exactUrls: 1942 },
    { file: 'sitemap-food-rescue.xml', exactUrls: 15 },
    { file: 'sitemap-shops.xml', exactUrls: 7 },
    { file: 'sitemap-pages.xml', exactUrls: 69 }
  ];

  for (const sc of sitemapConfigs) {
    const xml = fs.readFileSync(sc.file, 'utf8');
    const locCount = (xml.match(/<loc>/g) || []).length;
    const lastModMatch = xml.match(/<lastmod>([^<]+)<\/lastmod>/);
    const lastMod = lastModMatch ? lastModMatch[1] : '';
    
    if (sc.exactUrls) {
      assert(locCount === sc.exactUrls, `${sc.file} contains exactly ${sc.exactUrls} URLs (found ${locCount})`);
    } else {
      assert(locCount >= sc.minUrls, `${sc.file} contains at least ${sc.minUrls} URLs (found ${locCount})`);
    }
    assert(lastMod === '2026-08-19', `${sc.file} lastmod is updated to today (2026-08-19)`);
  }

  const robots = fs.readFileSync('robots.txt', 'utf8');
  assert(robots.includes('sitemap.xml') && robots.includes('sitemap-local-products.xml') && robots.includes('sitemap-marketplace.xml'), 'robots.txt lists all required sitemaps');

  // 5. Detail Page SSR Spot-checks (Across all shop sources + Karrot + HeyKorean)
  console.log('\n[5] Detail Page SSR Spot-checks');
  
  const testShops = ['sey-coffee', 'front-general-store', 'salter-house', 'mirth-vintage', 'big-night', 'pop-up-grocer'];
  const testPaths = [
    '/item/dolce-and-gabbana-pour-homme-the-bronx-ny-857',
    '/item/power-bank-anker-25k-manhattan-ny-856',
    '/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941'
  ];

  // Add one item from each local shop
  for (const sId of testShops) {
    const item = localDb.products.find(p => p.shop_id === sId);
    if (item && item.url) {
      testPaths.push(item.url);
    }
  }

  // Add Karrot & HeyKorean samples
  if (karrotItems[0] && karrotItems[0].url) testPaths.push(karrotItems[0].url);
  if (karrotItems[1] && karrotItems[1].url) testPaths.push(karrotItems[1].url);
  testPaths.push('/item/motorola-moto-g-prepaid-queens-ny-ext-heykorean-669585');

  for (const path of testPaths) {
    const fullUrl = 'https://moon-oh.com' + path;
    const resp = await itemDetailHandler(new Request(fullUrl));
    const html = await resp.text();
    
    const is200 = resp.status === 200;
    const hasOgImg = /<meta property="og:image" content="https?:\/\/[^"]+"/.test(html);
    const hasPrice = html.includes('$') || html.includes('Free') || html.includes('free');
    const hasBreadcrumbs = html.includes('breadcrumb-bar');
    const hasCanonical = html.includes('rel="canonical"');
    const hasJsonLd = html.includes('application/ld+json');

    assert(is200 && hasOgImg && hasPrice && hasBreadcrumbs && hasCanonical && hasJsonLd,
      `SSR Page ${path} rendered perfectly (HTTP ${resp.status}, og:image, price, breadcrumb, canonical, json-ld)`
    );
  }

  // 6. Explore SSR Page Spot-checks
  console.log('\n[6] Explore SSR Page Spot-checks');
  const exploreUrls = [
    'https://moon-oh.com/explore',
    'https://moon-oh.com/explore?source=moonoh',
    'https://moon-oh.com/explore?source=localshops',
    'https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY',
    'https://moon-oh.com/explore?source=marketplaces',
    'https://moon-oh.com/explore?source=marketplaces&area=Manhattan%2C%20NY',
    'https://moon-oh.com/explore?source=marketplaces&area=Queens%2C%20NY'
  ];

  for (const url of exploreUrls) {
    const resp = await exploreHandler(new Request(url));
    const html = await resp.text();
    const is200 = resp.status === 200;
    const hasGrid = html.includes('moonoh-item-grid');
    const hasTitle = /<title>[^<]+<\/title>/.test(html);
    const hasDesc = html.includes('name="description"');
    assert(is200 && hasGrid && hasTitle && hasDesc,
      `Explore SSR ${url} rendered valid HTML with title, meta description & grid`
    );
  }

  console.log('\n' + '='.repeat(60));
  console.log(`AUDIT SUMMARY: ${passedTests} / ${totalTests} TESTS PASSED`);
  if (failures.length === 0) {
    console.log('🎉 ALL AUDITS 100% PASSED! READY FOR DEPLOYMENT.');
  } else {
    console.log('❌ FAILURES DETECTED:');
    failures.forEach(f => console.log('  - ' + f));
  }
  console.log('='.repeat(60));
}

fullValidation();
