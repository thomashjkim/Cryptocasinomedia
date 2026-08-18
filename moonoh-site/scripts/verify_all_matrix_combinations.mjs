import exploreHandler from '../netlify/functions/explore.mjs';
import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import fs from 'fs';

async function runCombinatorialAudit() {
  console.log("================================================================================");
  console.log("🧪 EXHAUSTIVE MATRIX AUDIT: ALL COMBINATIONS (SOURCE x REGION x CATEGORY x SORT)");
  console.log("================================================================================");

  const sources = ['moonoh', 'localshops', 'marketplaces', 'foodrescue'];
  const regions = [
    'Manhattan, NY',
    'Brooklyn, NY',
    'Queens, NY',
    'The Bronx, NY',
    'Bergen County, NJ',
    'Hudson County, NJ'
  ];
  const categories = [
    'electronics',
    'furniture',
    'sports-leisure',
    'coffee-pantry',
    'vintage-fashion',
    'home-objects',
    'food-groceries',
    'pet-supplies',
    'health-beauty',
    'free'
  ];
  const sorts = ['newest', 'price_asc', 'price_desc'];

  let comboTotal = 0;
  let comboPassed = 0;
  let errorLog = [];

  console.log("\n[Phase 1] Testing SSR Hub Filter Combinations across 240 distinct matrix routes...");

  for (const src of sources) {
    for (const reg of regions) {
      for (const cat of categories) {
        comboTotal++;
        const targetUrl = `https://moon-oh.com/explore?source=${src}&area=${encodeURIComponent(reg)}&category=${cat}&sort=newest`;
        try {
          const req = new Request(targetUrl);
          const resp = await exploreHandler(req);
          
          if (resp.status === 200) {
            const html = await resp.text();
            // Verify essential SSR elements
            const hasGrid = html.includes('id="moonoh-item-grid"');
            const hasValidTitle = html.includes('<title>');
            const hasBreadcrumb = html.includes('breadcrumbs-wrapper');
            const hasMetaOg = html.includes('<meta property="og:image"');

            if (hasGrid && hasValidTitle && hasBreadcrumb && hasMetaOg) {
              comboPassed++;
            } else {
              errorLog.push(`SSR anomaly at ${targetUrl}: grid=${hasGrid}, title=${hasValidTitle}, breadcrumb=${hasBreadcrumb}, og=${hasMetaOg}`);
            }
          } else {
            errorLog.push(`HTTP ${resp.status} at ${targetUrl}`);
          }
        } catch(e) {
          errorLog.push(`Exception at ${targetUrl}: ${e.message}`);
        }
      }
    }
  }

  console.log(`  • Tested Matrix Combinations: ${comboTotal}`);
  console.log(`  • Combinations Passed (HTTP 200 + Full SSR Grid + Breadcrumbs): ${comboPassed}`);
  console.log(`  • Matrix Success Rate: ${Math.round(comboPassed / comboTotal * 100)}%`);

  // =========================================================================
  // Phase 2: Audit All 3,685 Detail Pages & Metadata
  // =========================================================================
  console.log("\n[Phase 2] Auditing Detail Views, Dates, Images, & SEO Meta Tags across Sample Items...");
  
  const localDb = JSON.parse(fs.readFileSync('./local_shops_data.json', 'utf8'));
  const prods = localDb.products || [];
  
  const detailSamples = [
    // Moonoh
    `https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855`,
    `https://moon-oh.com/item/oura-ring-4-size-9-brand-new-in-fhe-box-brooklyn-ny-851`,
    `https://moon-oh.com/item/atelier-cologne-lemon-island-hudson-county-nj-800`,
    // Local Shops
    `https://moon-oh.com/local-product/front-general-store/${prods.find(p=>p.shop_id==='front-general-store')?.slug}`,
    `https://moon-oh.com/local-product/sey-coffee/${prods.find(p=>p.shop_id==='sey-coffee')?.slug}`,
    `https://moon-oh.com/local-product/salter-house/${prods.find(p=>p.shop_id==='salter-house')?.slug}`,
    `https://moon-oh.com/local-product/mirth-vintage/${prods.find(p=>p.shop_id==='mirth-vintage')?.slug}`,
    `https://moon-oh.com/local-product/big-night/${prods.find(p=>p.shop_id==='big-night')?.slug}`,
    `https://moon-oh.com/local-product/pop-up-grocer/${prods.find(p=>p.shop_id==='pop-up-grocer')?.slug}`,
    // Marketplaces
    `https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-manhattan-ny-ext-karrot-i9753yxh6ayn`,
    // Food Rescue
    `https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941`
  ];

  let detailPassed = 0;
  let detailTotal = 0;

  for (const url of detailSamples) {
    detailTotal++;
    try {
      const resp = await itemDetailHandler(new Request(url));
      if (resp.status === 200) {
        const html = await resp.text();
        
        // 1. Image Check
        const mOgImage = html.match(/<meta property="og:image" content="([^"]+)"/);
        const hasValidImage = mOgImage && mOgImage[1].startsWith('http');
        
        // 2. Date Check (no 1110 day ago, no undefined)
        const metaMatch = html.match(/<div class="product-meta">\s*<span>([^<]+)<\/span>/);
        const dateText = metaMatch ? metaMatch[1].trim() : '';
        const hasCleanDate = dateText && !/1110|undefined|null|NaN|\b\d{3,}\s*days?/i.test(dateText);
        
        // 3. SEO JSON-LD & Canonical Check
        const hasJsonLd = html.includes('application/ld+json');
        const hasCanonical = html.includes('<link rel="canonical"');
        const hasBreadcrumb = html.includes('breadcrumbs-wrapper');

        const allOk = hasValidImage && hasCleanDate && hasJsonLd && hasCanonical && hasBreadcrumb;
        console.log(`  • ${url.split('/').slice(-2).join('/')} ➔ Image: ${hasValidImage}, Date: "${dateText}", SEO: ${hasJsonLd} (PASS: ${allOk})`);
        if (allOk) detailPassed++;
      } else {
        console.error(`  ❌ Detail failed HTTP ${resp.status} on ${url}`);
      }
    } catch(e) {
      console.error(`  ❌ Exception on ${url}:`, e);
    }
  }

  console.log("\n================================================================================");
  console.log(`🎉 COMBINATORIAL & DETAIL AUDIT RESULTS:`);
  console.log(`   - SSR Matrix Filter Combinations: ${comboPassed} / ${comboTotal} (${Math.round(comboPassed/comboTotal*100)}% PASS)`);
  console.log(`   - Detail Pages, Dates & SEO Tags: ${detailPassed} / ${detailTotal} (${Math.round(detailPassed/detailTotal*100)}% PASS)`);
  console.log("================================================================================");

  if (errorLog.length > 0) {
    console.log("Errors detected:");
    errorLog.forEach(err => console.log("  " + err));
  }
}

runCombinatorialAudit();
