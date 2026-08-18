import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function runAudit() {
  console.log("================================================================================");
  console.log("🔍 COMPREHENSIVE 10-POINT AUDIT & VERIFICATION");
  console.log("================================================================================");

  const localDb = JSON.parse(fs.readFileSync("./local_shops_data.json", "utf8"));
  const prods = localDb.products || [];
  const seyProd = prods.find(p => p.shop_id === "sey-coffee");
  const popProd = prods.find(p => p.shop_id === "pop-up-grocer");

  let passed = 0;
  let total = 0;

  // Point 1 & 6: Pop Up Grocer pricing
  console.log("\n[Point 1 & 6] Testing Pop Up Grocer Pricing & Detail Rendering:");
  total += 5;
  const popUpGrocerItems = prods.filter(p => p.shop_id === 'pop-up-grocer');
  const zeroPriceItems = popUpGrocerItems.filter(p => !p.current_price || p.current_price <= 0);
  console.log(`  • Pop Up Grocer total items: ${popUpGrocerItems.length}`);
  console.log(`  • Items with 0 or missing price: ${zeroPriceItems.length} (PASS: ${zeroPriceItems.length === 0})`);
  if (zeroPriceItems.length === 0) passed += 2;

  const samplePopUpSlug = popProd ? popProd.slug : 'prind';
  const popUpReq = new Request(`https://moon-oh.com/local-product/pop-up-grocer/${samplePopUpSlug}`);
  const popUpResp = await itemDetailHandler(popUpReq);
  const popUpHtml = await popUpResp.text();
  console.log(`  • Sample Detail Page HTTP Status: ${popUpResp.status}`);
  if (popUpResp.status === 200) passed++;
  const hasCheckPrice = popUpHtml.includes("Check price at retailer");
  console.log(`  • Contains 'Check price at retailer': ${hasCheckPrice} (PASS: ${!hasCheckPrice})`);
  if (!hasCheckPrice) passed++;
  const hasValidPrice = /\$\d+(\.\d{2})?/.test(popUpHtml);
  console.log(`  • Contains valid formatted price: ${hasValidPrice} (PASS: ${hasValidPrice})`);
  if (hasValidPrice) passed++;

  // Point 2: Location Dropdown
  console.log("\n[Point 2] Testing Location Dropdown & Fort Lee Consolidation:");
  total += 3;
  const exploreHtml = fs.readFileSync('explore.html', 'utf8');
  const indexHtml = fs.readFileSync('index.html', 'utf8');
  const hasFtLeeExplore = exploreHtml.includes('value="Fort Lee"');
  const hasFtLeeIndex = indexHtml.includes('value="Fort Lee"');
  const hasBergen = exploreHtml.includes('Bergen County, NJ');
  console.log(`  • explore.html has separate Fort Lee option: ${hasFtLeeExplore} (PASS: ${!hasFtLeeExplore})`);
  if (!hasFtLeeExplore) passed++;
  console.log(`  • index.html has separate Fort Lee option: ${hasFtLeeIndex} (PASS: ${!hasFtLeeIndex})`);
  if (!hasFtLeeIndex) passed++;
  console.log(`  • Bergen County option present: ${hasBergen} (PASS: ${hasBergen})`);
  if (hasBergen) passed++;

  // Point 3: '1mi' Distance Text Removal
  console.log("\n[Point 3] Testing '1mi' Distance Text Removal:");
  total += 3;
  const moonohData = fs.readFileSync('data.json', 'utf8');
  const mktData = fs.readFileSync('netlify/functions/external-items.mjs', 'utf8');
  const foodData = fs.readFileSync('netlify/functions/food-rescue-items.mjs', 'utf8');
  const has1miMoonoh = (moonohData.match(/1mi\s*·/g) || []).length;
  const has1miMkt = (mktData.match(/1mi\s*·/g) || []).length;
  const has1miFood = (foodData.match(/1mi\s*·/g) || []).length;
  console.log(`  • '1mi · ' in moonoh data: ${has1miMoonoh} (PASS: ${has1miMoonoh === 0})`);
  if (has1miMoonoh === 0) passed++;
  console.log(`  • '1mi · ' in marketplace data: ${has1miMkt} (PASS: ${has1miMkt === 0})`);
  if (has1miMkt === 0) passed++;
  console.log(`  • '1mi · ' in food rescue data: ${has1miFood} (PASS: ${has1miFood === 0})`);
  if (has1miFood === 0) passed++;

  // Point 4: Location Standardization & Meetup Preference
  console.log("\n[Point 4] Testing Location Standardization & Meetup Preference:");
  total += 3;
  const item855Req = new Request('https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855');
  const item855Resp = await itemDetailHandler(item855Req);
  const item855Html = await item855Resp.text();
  console.log(`  • Latest Moonoh Item (No. 855) Detail HTTP Status: ${item855Resp.status}`);
  if (item855Resp.status === 200) passed++;
  const hasGenericNYC = item855Html.includes('<span>NYC</span>');
  console.log(`  • Shows generic 'NYC': ${hasGenericNYC} (PASS: ${!hasGenericNYC})`);
  if (!hasGenericNYC) passed++;
  const hasMeetupPref = item855Html.includes('The Bronx, NY');
  console.log(`  • Shows Meetup Preference 'The Bronx, NY': ${hasMeetupPref} (PASS: ${hasMeetupPref})`);
  if (hasMeetupPref) passed++;

  // Point 5: Breadcrumbs Navigation
  console.log("\n[Point 5] Testing Breadcrumbs Navigation across 4 sources:");
  total += 5;
  const bcTestUrls = [
    `https://moon-oh.com/local-product/sey-coffee/${seyProd ? seyProd.slug : 'coffee'}`,
    `https://moon-oh.com/local-product/pop-up-grocer/${samplePopUpSlug}`,
    'https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-manhattan-ny-ext-karrot-i9753yxh6ayn',
    'https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941',
    'https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855'
  ];
  for (const u of bcTestUrls) {
    const r = await itemDetailHandler(new Request(u));
    const h = await r.text();
    const isOk = r.status === 200 && h.includes('breadcrumbs-wrapper');
    const label = u.split('/')[3];
    console.log(`  • ${label} detail status: ${r.status} (${u.split('/').pop()})`);
    if (isOk) passed++;
  }

  // Point 6: Mobile Button Non-wrapping
  console.log("\n[Point 6] Testing Mobile Button Non-wrapping Style:");
  total++;
  const hasNoWrapBtn = popUpHtml.includes('white-space: nowrap') && popUpHtml.includes('.cta-btn-main');
  console.log(`  • Detail view includes .cta-btn-main with white-space: nowrap: ${hasNoWrapBtn} (PASS: ${hasNoWrapBtn})`);
  if (hasNoWrapBtn) passed++;

  // Point 7: Favorite Heart Icon Removal
  console.log("\n[Point 7] Testing Favorite Heart Icon Removal:");
  total++;
  const hasHeartIcon = popUpHtml.includes('like-badge') || item855Html.includes('like-badge');
  console.log(`  • Detail view has like-badge: ${hasHeartIcon} (PASS: ${!hasHeartIcon})`);
  if (!hasHeartIcon) passed++;

  // Point 8: Moonoh Live Sync
  console.log("\n[Point 8] Testing Moonoh Live Data Sync & Hidden Item Exclusion:");
  total += 3;
  const moonohItems = JSON.parse(moonohData);
  console.log(`  • Total synced visible Moonoh items: ${moonohItems.length} (PASS: ${moonohItems.length >= 590})`);
  if (moonohItems.length >= 590) passed++;
  const topNo = Math.max(...moonohItems.map(i => parseInt(i.no || i.id, 10) || 0));
  console.log(`  • Highest item No: ${topNo} (PASS: ${topNo >= 855})`);
  if (topNo >= 855) passed++;
  const has852 = moonohItems.some(i => String(i.no) === '852');
  console.log(`  • Hidden item No.852 excluded: ${!has852} (PASS: ${!has852})`);
  if (!has852) passed++;

  // Point 9: Explore SSR Performance
  console.log("\n[Point 9] Testing Instant In-Memory Explore SSR Performance:");
  total += 2;
  const startT = Date.now();
  const expResp = await exploreHandler(new Request('https://moon-oh.com/explore'));
  const duration = Date.now() - startT;
  console.log(`  • Explore SSR Status: ${expResp.status} | Response Time: ${duration}ms (PASS: ${expResp.status === 200 && duration < 300})`);
  if (expResp.status === 200) passed++;
  if (duration < 300) passed++;

  // Point 10: OpenGraph & Schema.org Matching
  console.log("\n[Point 10] Testing Schema.org & OpenGraph Image Matching:");
  total += 2;
  const mOg = popUpHtml.match(/<meta property="og:image" content="([^"]+)"/);
  const mJsonLd = popUpHtml.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  const ogImg = mOg ? mOg[1] : '';
  const jsonLdImg = mJsonLd ? mJsonLd[1].includes(ogImg) : false;
  console.log(`  • og:image: ${ogImg.substring(0, 60)}...`);
  console.log(`  • JSON-LD image contains og:image: ${jsonLdImg} (PASS: ${jsonLdImg})`);
  if (ogImg) passed++;
  if (jsonLdImg) passed++;

  console.log("\n================================================================================");
  if (passed === total) {
    console.log(`🎉 OVERALL 10-POINT AUDIT RESULT: ALL 10 CHECKS 100% PASSED! (${passed}/${total})`);
  } else {
    console.log(`🎉 OVERALL 10-POINT AUDIT RESULT: ${passed} / ${total} PASSED`);
  }
  console.log("================================================================================");
}

runAudit();
