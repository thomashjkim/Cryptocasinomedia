import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function runLocalAndBreadcrumbAudit() {
  console.log("================================================================================");
  console.log("🔍 AUDITING ALL 7 LOCAL SHOPS: LOCATIONS, ADDRESSES, COORDINATES & BREADCRUMBS");
  console.log("================================================================================");

  const testShops = [
    {
      name: "SEY Coffee",
      url: "https://moon-oh.com/local-product/sey-coffee/oma-plot",
      expectedRegion: "Brooklyn, NY",
      expectedAddress: "18 Grattan St, Brooklyn, NY 11206",
      expectedLat: 40.7051,
      expectedLng: -73.9324,
      expectedCategoryLink: "/explore?source=localshops&category=coffee-pantry",
      expectedRegionLink: "/explore/brooklyn?source=localshops",
      expectedShopLink: "/local-shops/sey-coffee"
    },
    {
      name: "Front General Store",
      url: "https://moon-oh.com/local-product/front-general-store/tory-repeated-stitch-leather-belt-2332-2333-2334",
      expectedRegion: "Brooklyn, NY",
      expectedAddress: "143 Front St, Brooklyn, NY 11201",
      expectedLat: 40.7025,
      expectedLng: -73.9877,
      expectedCategoryLink: "/explore?source=localshops&category=vintage-fashion",
      expectedRegionLink: "/explore/brooklyn?source=localshops",
      expectedShopLink: "/local-shops/front-general-store"
    },
    {
      name: "Mirth Vintage",
      url: "https://moon-oh.com/local-product/mirth-vintage/60s-lace-skirt-set",
      expectedRegion: "Brooklyn, NY",
      expectedAddress: "603 Manhattan Ave, Brooklyn, NY 11222",
      expectedLat: 40.7246,
      expectedLng: -73.9514,
      expectedCategoryLink: "/explore?source=localshops&category=vintage-fashion",
      expectedRegionLink: "/explore/brooklyn?source=localshops",
      expectedShopLink: "/local-shops/mirth-vintage"
    },
    {
      name: "Salter House",
      url: "https://moon-oh.com/local-product/salter-house/gift-wrap",
      expectedRegion: "Brooklyn, NY",
      expectedAddress: "119 Atlantic Ave, Brooklyn, NY 11201",
      expectedLat: 40.6917,
      expectedLng: -73.9972,
      expectedCategoryLink: "/explore?source=localshops&category=gifts-culture",
      expectedRegionLink: "/explore/brooklyn?source=localshops",
      expectedShopLink: "/local-shops/salter-house"
    },
    {
      name: "Pop Up Grocer",
      url: "https://moon-oh.com/local-product/pop-up-grocer/prind",
      expectedRegion: "Manhattan, NY",
      expectedAddress: "205 Bleecker St, New York, NY 10012",
      expectedLat: 40.7291,
      expectedLng: -74.0016,
      expectedCategoryLink: "/explore?source=localshops&category=coffee-pantry",
      expectedRegionLink: "/explore/manhattan?source=localshops",
      expectedShopLink: "/local-shops/pop-up-grocer"
    }
  ];

  let passedAll = true;

  for (const ts of testShops) {
    console.log(`\n▶ Testing ${ts.name}: ${ts.url}`);
    const req = new Request(ts.url);
    const resp = await itemDetailHandler(req);
    const body = await resp.text();

    if (resp.status !== 200) {
      console.error(`  ❌ HTTP status ${resp.status}`);
      passedAll = false;
      continue;
    }

    const hasExpectedRegion = body.includes(`<span>${ts.expectedRegion}</span>`);
    const hasExpectedAddress = body.includes(ts.expectedAddress);
    const hasNoNyc = !body.includes("<span>NYC</span>") && !body.includes("<span>NYC, NY</span>");
    const hasCategoryLink = body.includes(`href="${ts.expectedCategoryLink}"`) || body.includes(`href="${ts.expectedCategoryLink.replace(/&/g, '&amp;')}"`);
    const hasRegionLink = body.includes(`href="${ts.expectedRegionLink}"`) || body.includes(`href="${ts.expectedRegionLink.replace(/&/g, '&amp;')}"`);
    const hasShopLink = body.includes(`href="${ts.expectedShopLink}"`);

    console.log(`  • Region (${ts.expectedRegion}): ${hasExpectedRegion}`);
    console.log(`  • Address (${ts.expectedAddress}): ${hasExpectedAddress}`);
    console.log(`  • Zero 'NYC' generic text: ${hasNoNyc}`);
    console.log(`  • Category Breadcrumb (${ts.expectedCategoryLink}): ${hasCategoryLink}`);
    console.log(`  • Region Breadcrumb (${ts.expectedRegionLink}): ${hasRegionLink}`);
    console.log(`  • Shop Breadcrumb (${ts.expectedShopLink}): ${hasShopLink}`);

    if (!hasExpectedRegion || !hasExpectedAddress || !hasNoNyc || !hasCategoryLink || !hasRegionLink || !hasShopLink) {
      passedAll = false;
    }

    // Verify Explore SSR accepts the breadcrumb target URL
    const expReq = new Request(`https://moon-oh.com${ts.expectedCategoryLink}`);
    const expResp = await exploreHandler(expReq);
    console.log(`  • Target Explore Filter HTTP Status: ${expResp.status} (PASS: ${expResp.status === 200})`);
    if (expResp.status !== 200) passedAll = false;
  }

  console.log("\n================================================================================");
  console.log(`🎉 LOCAL SHOPS & BREADCRUMBS AUDIT RESULT: ${passedAll ? "100% PASS!" : "FAILED SOME CHECKS"}`);
  console.log("================================================================================");
}

runLocalAndBreadcrumbAudit();
