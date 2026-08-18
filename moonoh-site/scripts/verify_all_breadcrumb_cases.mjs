import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function runBreadcrumbExhaustiveVerification() {
  console.log("================================================================================");
  console.log("🔍 EXHAUSTIVE BREADCRUMB & FILTER COMBINATION VERIFICATION (ALL 4 SOURCES)");
  console.log("================================================================================");

  const testCases = [
    {
      type: "Local Shop (SEY Coffee)",
      url: "https://moon-oh.com/local-product/sey-coffee/oma-plot",
      expectedSource: "localshops",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Coffee & Pantry",
      expectedCategorySlug: "coffee-pantry",
      expectedShop: "sey-coffee"
    },
    {
      type: "Local Shop (Pop Up Grocer)",
      url: "https://moon-oh.com/local-product/pop-up-grocer/prind",
      expectedSource: "localshops",
      expectedRegion: "Manhattan, NY",
      expectedCategory: "Coffee & Pantry",
      expectedCategorySlug: "coffee-pantry",
      expectedShop: "pop-up-grocer"
    },
    {
      type: "Local Shop (Front General Store)",
      url: "https://moon-oh.com/local-product/front-general-store/tory-repeated-stitch-leather-belt-2332-2333-2334",
      expectedSource: "localshops",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Vintage & Fashion",
      expectedCategorySlug: "vintage-fashion",
      expectedShop: "front-general-store"
    },
    {
      type: "Local Shop (Salter House)",
      url: "https://moon-oh.com/local-product/salter-house/gift-wrap",
      expectedSource: "localshops",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Gifts & Culture",
      expectedCategorySlug: "gifts-culture",
      expectedShop: "salter-house"
    },
    {
      type: "Food Rescue (Kim'C Market)",
      url: "https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941",
      expectedSource: "foodrescue",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Food & Groceries",
      expectedCategorySlug: "food-groceries"
    },
    {
      type: "Marketplace (Karrot Item)",
      url: "https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-manhattan-ny-ext-karrot-i9753yxh6ayn",
      expectedSource: "marketplaces",
      expectedRegion: "Manhattan, NY",
      expectedCategory: "Pet Supplies",
      expectedCategorySlug: "pet-supplies"
    },
    {
      type: "Moonoh Listing (No. 855)",
      url: "https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855",
      expectedSource: "moonoh",
      expectedRegion: "The Bronx, NY",
      expectedCategory: "Sports & Leisure",
      expectedCategorySlug: "sports-leisure"
    },
    {
      type: "Moonoh Listing (No. 851)",
      url: "https://moon-oh.com/item/oura-ring-4-size-9-brand-new-in-fhe-box-brooklyn-ny-851",
      expectedSource: "moonoh",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Electronics & Appliances",
      expectedCategorySlug: "electronics"
    }
  ];

  let totalPassed = 0;
  let totalTests = 0;

  for (const tc of testCases) {
    console.log(`\n================================================================================`);
    console.log(`▶ Testing Detail View: ${tc.type}`);
    console.log(`  URL: ${tc.url}`);
    console.log(`================================================================================`);

    const req = new Request(tc.url);
    const resp = await itemDetailHandler(req);
    const html = await resp.text();

    if (resp.status !== 200) {
      console.error(`  ❌ Failed with status ${resp.status}`);
      continue;
    }

    // 1. Check Tab Link
    totalTests++;
    const tabUrl = `/explore?source=${tc.expectedSource}`;
    const hasTabLink = html.includes(`href="${tabUrl}"`);
    console.log(`  [1] Tab Link: ${tabUrl} (Found in Breadcrumb: ${hasTabLink})`);
    if (hasTabLink) totalPassed++;

    // 2. Check Region Link
    totalTests++;
    const regionUrl = `/explore?source=${encodeURIComponent(tc.expectedSource)}&area=${encodeURIComponent(tc.expectedRegion)}`;
    const hasRegionLink = html.includes(`href="${regionUrl}"`) || html.includes(`href="${regionUrl.replace(/&/g, '&amp;')}"`);
    console.log(`  [2] Region Link: ${regionUrl} (Found in Breadcrumb: ${hasRegionLink})`);
    if (hasRegionLink) totalPassed++;

    // 3. Check Category Link (Combined Source + Area + Category)
    totalTests++;
    const catUrl = `/explore?source=${encodeURIComponent(tc.expectedSource)}&area=${encodeURIComponent(tc.expectedRegion)}&category=${encodeURIComponent(tc.expectedCategorySlug)}`;
    const hasCatLink = html.includes(`href="${catUrl}"`) || html.includes(`href="${catUrl.replace(/&/g, '&amp;')}"`);
    console.log(`  [3] Category Link: ${catUrl} (Found in Breadcrumb: ${hasCatLink})`);
    if (hasCatLink) totalPassed++;

    // 4. If Local Shop, check Shop link
    if (tc.expectedShop) {
      totalTests++;
      const shopUrl = `/local-shops/${tc.expectedShop}`;
      const hasShopLink = html.includes(`href="${shopUrl}"`);
      console.log(`  [4] Shop Profile Link: ${shopUrl} (Found in Breadcrumb: ${hasShopLink})`);
      if (hasShopLink) totalPassed++;
    }

    // 5. Test Target Category Link in Explore SSR
    totalTests++;
    const expTargetReq = new Request(`https://moon-oh.com${catUrl}`);
    const expTargetResp = await exploreHandler(expTargetReq);
    console.log(`  [5] Target Category Filter SSR Response: HTTP ${expTargetResp.status} (PASS: ${expTargetResp.status === 200})`);
    if (expTargetResp.status === 200) totalPassed++;
  }

  console.log("\n================================================================================");
  console.log(`🎉 BREADCRUMB AUDIT SCORE: ${totalPassed} / ${totalTests} (${Math.round(totalPassed/totalTests*100)}% PASS)`);
  console.log("================================================================================");
}

runBreadcrumbExhaustiveVerification();
