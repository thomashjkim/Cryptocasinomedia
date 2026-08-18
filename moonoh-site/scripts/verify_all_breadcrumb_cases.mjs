import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function runBreadcrumbExhaustiveVerification() {
  console.log("================================================================================");
  console.log("🔍 EXHAUSTIVE BREADCRUMB & FILTER COMBINATION VERIFICATION (ALL 4 SOURCES)");
  console.log("================================================================================");

  const localDb = JSON.parse(fs.readFileSync('./local_shops_data.json', 'utf8'));
  const prods = localDb.products || [];
  const seyProd = prods.find(p => p.shop_id === 'sey-coffee');
  const popProd = prods.find(p => p.shop_id === 'pop-up-grocer');
  const fgsProd = prods.find(p => p.shop_id === 'front-general-store');
  const saltProd = prods.find(p => p.shop_id === 'salter-house');

  const testCases = [
    {
      type: "Local Shop (SEY Coffee)",
      url: `https://moon-oh.com/local-product/sey-coffee/${seyProd ? seyProd.slug : '2026-pepe-jose-jijon-and-francisco-vintimilla-putushio-2nd-harvest-ecuador'}`,
      expectedSource: "localshops",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Coffee & Pantry",
      expectedCategorySlug: "coffee-pantry",
      expectedShop: "sey-coffee"
    },
    {
      type: "Local Shop (Pop Up Grocer)",
      url: `https://moon-oh.com/local-product/pop-up-grocer/${popProd ? popProd.slug : 'prind'}`,
      expectedSource: "localshops",
      expectedRegion: "Manhattan, NY",
      expectedCategory: "Coffee & Pantry",
      expectedCategorySlug: "coffee-pantry",
      expectedShop: "pop-up-grocer"
    },
    {
      type: "Local Shop (Front General Store)",
      url: `https://moon-oh.com/local-product/front-general-store/${fgsProd ? fgsProd.slug : 'issey-miyake-bow-tie-pleated-zip-up-jacket'}`,
      expectedSource: "localshops",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Vintage & Fashion",
      expectedCategorySlug: "vintage-fashion",
      expectedShop: "front-general-store"
    },
    {
      type: "Local Shop (Salter House)",
      url: `https://moon-oh.com/local-product/salter-house/${saltProd ? saltProd.slug : 'bienaime-jours-heureux-bar-soap'}`,
      expectedSource: "localshops",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: saltProd ? saltProd.moonoh_category : "Home & Objects",
      expectedCategorySlug: saltProd && saltProd.moonoh_category === "Health & beauty" ? "health-beauty" : "home-objects",
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
      expectedCategory: "Pet supplies",
      expectedCategorySlug: "pet-supplies"
    },
    {
      type: "Moonoh Listing (No. 855)",
      url: "https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855",
      expectedSource: "moonoh",
      expectedRegion: "The Bronx, NY",
      expectedCategory: "Sports & leisure",
      expectedCategorySlug: "sports-leisure"
    },
    {
      type: "Moonoh Listing (No. 851)",
      url: "https://moon-oh.com/item/oura-ring-4-size-9-brand-new-in-fhe-box-brooklyn-ny-851",
      expectedSource: "moonoh",
      expectedRegion: "Brooklyn, NY",
      expectedCategory: "Electronics & appliances",
      expectedCategorySlug: "electronics"
    }
  ];

  let passed = 0;
  let total = 0;

  for (const tc of testCases) {
    console.log(`\n================================================================================`);
    console.log(`▶ Testing Detail View: ${tc.type}`);
    console.log(`  URL: ${tc.url}`);
    console.log(`================================================================================`);

    try {
      const req = new Request(tc.url);
      const resp = await itemDetailHandler(req);
      
      if (resp.status !== 200) {
        console.error(`  ❌ Failed with status ${resp.status}`);
        continue;
      }

      const html = await resp.text();
      
      // 1. Verify Tab Link
      total++;
      const expectedTabHref = `/explore?source=${tc.expectedSource}`;
      const hasTabLink = html.includes(`href="${expectedTabHref}"`);
      console.log(`  [1] Tab Link: ${expectedTabHref} (Found in Breadcrumb: ${hasTabLink})`);
      if (hasTabLink) passed++;

      // 2. Verify Region Link with Source + Area
      total++;
      const expectedRegionHref = `/explore?source=${tc.expectedSource}&area=${encodeURIComponent(tc.expectedRegion)}`;
      const hasRegionLink = html.includes(`href="${expectedRegionHref}"`);
      console.log(`  [2] Region Link: ${expectedRegionHref} (Found in Breadcrumb: ${hasRegionLink})`);
      if (hasRegionLink) passed++;

      // 3. Verify Category Link with Source + Area + Category
      total++;
      const expectedCatHref = `/explore?source=${tc.expectedSource}&area=${encodeURIComponent(tc.expectedRegion)}&category=${tc.expectedCategorySlug}`;
      const hasCatLink = html.includes(`href="${expectedCatHref}"`);
      console.log(`  [3] Category Link: ${expectedCatHref} (Found in Breadcrumb: ${hasCatLink})`);
      if (hasCatLink) passed++;

      // 4. Verify Shop Profile Link (for Local Shops)
      if (tc.expectedShop) {
        total++;
        const expectedShopHref = `/local-shops/${tc.expectedShop}`;
        const hasShopLink = html.includes(`href="${expectedShopHref}"`);
        console.log(`  [4] Shop Profile Link: ${expectedShopHref} (Found in Breadcrumb: ${hasShopLink})`);
        if (hasShopLink) passed++;
      }

      // 5. Test Explore Hub SSR Response for the Category Link
      total++;
      const exploreTargetUrl = `https://moon-oh.com${expectedCatHref}`;
      const expReq = new Request(exploreTargetUrl);
      const expResp = await exploreHandler(expReq);
      const expPass = expResp.status === 200;
      console.log(`  [5] Target Category Filter SSR Response: HTTP ${expResp.status} (PASS: ${expPass})`);
      if (expPass) passed++;

    } catch (err) {
      console.error(`  ❌ Error executing test case for ${tc.url}:`, err);
    }
  }

  console.log(`\n================================================================================`);
  console.log(`🎉 BREADCRUMB AUDIT SCORE: ${passed} / ${total} (${Math.round(passed/total*100)}% PASS)`);
  console.log(`================================================================================`);
}

runBreadcrumbExhaustiveVerification();
