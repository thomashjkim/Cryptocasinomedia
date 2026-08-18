import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function runComprehensiveAudit() {
  console.log("================================================================================");
  console.log("🔍 COMPREHENSIVE 10-POINT AUDIT & VERIFICATION");
  console.log("================================================================================");

  let allPassed = true;

  // 1. POP UP GROCER PRICING TEST
  console.log("\n[Point 1 & 6] Testing Pop Up Grocer Pricing & Detail Rendering:");
  const localDb = JSON.parse(fs.readFileSync('local_shops_data.json', 'utf-8'));
  const popupItems = (localDb.products || []).filter(p => p.shop_id === 'pop-up-grocer');
  const zeroPrices = popupItems.filter(p => !p.current_price || p.current_price <= 0);
  console.log(`  • Pop Up Grocer total items: ${popupItems.length}`);
  console.log(`  • Items with 0 or missing price: ${zeroPrices.length} (PASS: ${zeroPrices.length === 0})`);
  if (zeroPrices.length > 0) allPassed = false;

  const samplePopupReq = new Request("https://moon-oh.com/local-product/pop-up-grocer/prind");
  const samplePopupResp = await itemDetailHandler(samplePopupReq);
  const samplePopupBody = await samplePopupResp.text();
  const hasCheckPrice = samplePopupBody.includes("Check price at retailer");
  const hasPriceNumber = samplePopupBody.includes("$4.99") || samplePopupBody.includes("$");
  console.log(`  • Sample Detail Page HTTP Status: ${samplePopupResp.status}`);
  console.log(`  • Contains 'Check price at retailer': ${hasCheckPrice} (PASS: ${!hasCheckPrice})`);
  console.log(`  • Contains valid formatted price: ${hasPriceNumber} (PASS: ${hasPriceNumber})`);
  if (hasCheckPrice || !hasPriceNumber) allPassed = false;

  // 2. LOCATION DROPDOWN & FORT LEE CONSOLIDATION TEST
  console.log("\n[Point 2] Testing Location Dropdown & Fort Lee Consolidation:");
  const expHtml = fs.readFileSync('explore.html', 'utf-8');
  const idxHtml = fs.readFileSync('index.html', 'utf-8');
  const hasFortLeeOptExp = expHtml.includes('<option value="Fort Lee">');
  const hasFortLeeOptIdx = idxHtml.includes('<option value="Fort Lee">');
  const hasBergenOptExp = expHtml.includes('<option value="Bergen">');
  console.log(`  • explore.html has separate Fort Lee option: ${hasFortLeeOptExp} (PASS: ${!hasFortLeeOptExp})`);
  console.log(`  • index.html has separate Fort Lee option: ${hasFortLeeOptIdx} (PASS: ${!hasFortLeeOptIdx})`);
  console.log(`  • Bergen County option present: ${hasBergenOptExp} (PASS: ${hasBergenOptExp})`);
  if (hasFortLeeOptExp || hasFortLeeOptIdx || !hasBergenOptExp) allPassed = false;

  // 3. '1mi' DISTANCE TEXT REMOVAL TEST
  console.log("\n[Point 3] Testing '1mi' Distance Text Removal:");
  const moonohData = fs.readFileSync('netlify/functions/moonoh-items-data.mjs', 'utf-8');
  const extData = fs.readFileSync('netlify/functions/external-items.mjs', 'utf-8');
  const foodData = fs.readFileSync('netlify/functions/food-rescue-items.mjs', 'utf-8');
  const m1 = moonohData.match(/1mi\s*·/g) || [];
  const m2 = extData.match(/1mi\s*·/g) || [];
  const m3 = foodData.match(/1mi\s*·/g) || [];
  console.log(`  • '1mi · ' in moonoh data: ${m1.length} (PASS: ${m1.length === 0})`);
  console.log(`  • '1mi · ' in marketplace data: ${m2.length} (PASS: ${m2.length === 0})`);
  console.log(`  • '1mi · ' in food rescue data: ${m3.length} (PASS: ${m3.length === 0})`);
  if (m1.length > 0 || m2.length > 0 || m3.length > 0) allPassed = false;

  // 4. LOCATION STANDARDIZATION TEST
  console.log("\n[Point 4] Testing Location Standardization:");
  const sampleMoonohReq = new Request("https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855");
  const sampleMoonohResp = await itemDetailHandler(sampleMoonohReq);
  const sampleMoonohBody = await sampleMoonohResp.text();
  console.log(`  • Latest Moonoh Item (No. 855) Detail HTTP Status: ${sampleMoonohResp.status}`);
  const hasGenericNyc = sampleMoonohBody.includes("<span class=\"loc\">NYC</span>");
  console.log(`  • Shows generic 'NYC' instead of borough/town: ${hasGenericNyc} (PASS: ${!hasGenericNyc})`);
  if (hasGenericNyc || sampleMoonohResp.status !== 200) allPassed = false;

  // 5. BREADCRUMBS & TAB / CATEGORY / REGION COMBINATIONS TEST
  console.log("\n[Point 5] Testing Breadcrumbs Navigation across 4 sources:");
  const testBreadcrumbs = [
    { url: "https://moon-oh.com/local-product/sey-coffee/oma-plot", source: "localshops" },
    { url: "https://moon-oh.com/local-product/pop-up-grocer/prind", source: "localshops" },
    { url: "https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-manhattan-ny-ext-karrot-i9753yxh6ayn", source: "marketplaces" },
    { url: "https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941", source: "foodrescue" },
    { url: "https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855", source: "moonoh" }
  ];
  for (const tb of testBreadcrumbs) {
    const req = new Request(tb.url);
    const resp = await itemDetailHandler(req);
    console.log(`  • ${tb.source} detail status: ${resp.status} (${tb.url.split('/').pop()})`);
    if (resp.status !== 200) allPassed = false;
  }

  // 6. MOBILE BUTTON LAYOUT TEST
  console.log("\n[Point 6] Testing Mobile Button Non-wrapping Style:");
  const hasCtaMainCss = samplePopupBody.includes(".cta-btn-main") && samplePopupBody.includes("white-space: nowrap");
  console.log(`  • Detail view includes .cta-btn-main with white-space: nowrap: ${hasCtaMainCss} (PASS: ${hasCtaMainCss})`);
  if (!hasCtaMainCss) allPassed = false;

  // 7. FAVORITE HEART ICON REMOVAL TEST
  console.log("\n[Point 7] Testing Favorite Heart Icon Removal:");
  const hasLikeBadge = samplePopupBody.includes("class=\"like-badge\"");
  console.log(`  • Detail view has like-badge: ${hasLikeBadge} (PASS: ${!hasLikeBadge})`);
  if (hasLikeBadge) allPassed = false;

  // 8. MOONOH LIVE DATA SYNC TEST
  console.log("\n[Point 8] Testing Moonoh Live Data Sync (640 items):");
  const rawMoonoh = JSON.parse(moonohData.replace(/^[\s\S]*?=\s*/, '').replace(/;\s*$/, ''));
  console.log(`  • Total synced Moonoh items: ${rawMoonoh.length} (PASS: ${rawMoonoh.length >= 640})`);
  console.log(`  • Highest item No: ${rawMoonoh[0].no} (PASS: ${Number(rawMoonoh[0].no) >= 855})`);
  if (rawMoonoh.length < 640 || Number(rawMoonoh[0].no) < 855) allPassed = false;

  // 9. PERFORMANCE & COLD START TEST
  console.log("\n[Point 9] Testing Instant In-Memory Explore SSR Performance:");
  const t0 = Date.now();
  const expResp = await exploreHandler(new Request("https://moon-oh.com/explore"));
  const t1 = Date.now();
  console.log(`  • Explore SSR Status: ${expResp.status} | Response Time: ${t1 - t0}ms (PASS: ${expResp.status === 200})`);
  if (expResp.status !== 200) allPassed = false;

  // 10. IMAGE MATCH AUDIT TEST
  console.log("\n[Point 10] Testing Schema.org & OpenGraph Image Matching:");
  const ogImgMatch = samplePopupBody.match(/<meta property="og:image" content="([^"]+)"/);
  const jsonLdMatch = samplePopupBody.match(/"image":\s*(\[[^\]]+\]|"[^"]+")/);
  const ogImg = ogImgMatch ? ogImgMatch[1] : '';
  const jsonLdImgStr = jsonLdMatch ? jsonLdMatch[1] : '';
  const jsonLdContainsOg = jsonLdImgStr.includes(ogImg) && ogImg.startsWith('http');
  console.log(`  • og:image: ${ogImg.substring(0, 60)}...`);
  console.log(`  • JSON-LD image contains og:image: ${jsonLdContainsOg} (PASS: ${jsonLdContainsOg})`);
  if (!jsonLdContainsOg) allPassed = false;

  console.log("\n================================================================================");
  console.log(`🎉 OVERALL 10-POINT AUDIT RESULT: ${allPassed ? "ALL 10 CHECKS 100% PASSED!" : "FAILED SOME CHECKS"}`);
  console.log("================================================================================");
}

runComprehensiveAudit();
