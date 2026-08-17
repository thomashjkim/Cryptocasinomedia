import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';

async function runComprehensiveNavigationAudit() {
  console.log("================================================================================");
  console.log("🔍 COMPREHENSIVE AUDIT: DETAIL VIEW BREADCRUMBS, BACK NAV & EXPLORE RESTORATION");
  console.log("================================================================================");

  const testCases = [
    {
      type: "Local Product (SEY Coffee)",
      url: "https://moon-oh.com/local-product/sey-coffee/oma-plot",
      expectedBack: "/explore?source=localshops",
      expectedBreadcrumbs: [
        { label: "Local Shops", href: "/explore?source=localshops" },
        { label: "SEY Coffee", href: "/local-shops/sey-coffee" },
        { label: "Bushwick, NY", href: "/explore/brooklyn?source=localshops" },
        { label: "Coffee & Pantry", href: "/explore?source=localshops&category=coffee-pantry" }
      ]
    },
    {
      type: "Local Product (Front General Store)",
      url: "https://moon-oh.com/local-product/front-general-store/tory-repeated-stitch-leather-belt-2332-2333-2334",
      expectedBack: "/explore?source=localshops",
      expectedBreadcrumbs: [
        { label: "Local Shops", href: "/explore?source=localshops" },
        { label: "Front General Store", href: "/local-shops/front-general-store" },
        { label: "DUMBO, NY", href: "/explore/brooklyn?source=localshops" },
        { label: "Vintage & Fashion", href: "/explore?source=localshops&category=vintage-fashion" }
      ]
    },
    {
      type: "Local Product (Mirth Vintage)",
      url: "https://moon-oh.com/local-product/mirth-vintage/60s-lace-skirt-set",
      expectedBack: "/explore?source=localshops",
      expectedBreadcrumbs: [
        { label: "Local Shops", href: "/explore?source=localshops" },
        { label: "Mirth Vintage", href: "/local-shops/mirth-vintage" },
        { label: "Greenpoint, NY", href: "/explore/brooklyn?source=localshops" },
        { label: "Vintage & Fashion", href: "/explore?source=localshops&category=vintage-fashion" }
      ]
    },
    {
      type: "Local Product (Salter House)",
      url: "https://moon-oh.com/local-product/salter-house/gift-wrap",
      expectedBack: "/explore?source=localshops",
      expectedBreadcrumbs: [
        { label: "Local Shops", href: "/explore?source=localshops" },
        { label: "Salter House", href: "/local-shops/salter-house" },
        { label: "Brooklyn Heights, NY", href: "/explore/brooklyn?source=localshops" },
        { label: "Gifts & Culture", href: "/explore?source=localshops&category=gifts-culture" }
      ]
    },
    {
      type: "Marketplace Product (Karrot)",
      url: "https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-1mi-malverne-ny-ext-karrot-i9753yxh6ayn",
      expectedBack: "/explore?source=marketplaces",
      expectedBreadcrumbs: [
        { label: "Marketplaces", href: "/explore?source=marketplaces" },
        { label: "Pet supplies", href: "/explore/pet-supplies?source=marketplaces" }
      ]
    },
    {
      type: "Food Rescue Product (Kim'C Market)",
      url: "https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941",
      expectedBack: "/explore?source=foodrescue",
      expectedBreadcrumbs: [
        { label: "Food Rescue", href: "/explore?source=foodrescue" },
        { label: "Brooklyn", href: "/explore/brooklyn?source=foodrescue" },
        { label: "Food & Groceries", href: "/explore/brooklyn/food-groceries?source=foodrescue" }
      ]
    },
    {
      type: "Moonoh Product (No. 851)",
      url: "https://moon-oh.com/item/oura-ring-4-size-9-brand-new-in-fhe-box-brooklyn-ny-851",
      expectedBack: "/explore?source=moonoh",
      expectedBreadcrumbs: [
        { label: "Explore", href: "/explore?source=moonoh" },
        { label: "Brooklyn", href: "/explore/brooklyn?source=moonoh" },
        { label: "Jewelry & Watches", href: "/explore/brooklyn/jewelry-watches?source=moonoh" }
      ]
    }
  ];

  let totalBreadcrumbLinksTested = 0;
  let passedBreadcrumbLinks = 0;

  for (const tc of testCases) {
    console.log(`\n▶ Testing ${tc.type}: ${tc.url}`);
    const req = new Request(tc.url);
    const resp = await itemDetailHandler(req);
    const body = await resp.text();
    
    if (resp.status !== 200) {
      console.error(`  ❌ HTTP status ${resp.status}`);
      console.error("  Body:", body.substring(0, 300));
      continue;
    }

    // Check Back Button
    const hasBackScript = body.includes("handleBackNavigation(event");
    const hasFallback = body.includes(tc.expectedBack);
    console.log(`  ✓ Back button has history.back() script: ${hasBackScript} | fallback: ${hasFallback} (${tc.expectedBack})`);

    // Check each expected breadcrumb link
    for (const b of tc.expectedBreadcrumbs) {
      totalBreadcrumbLinksTested++;
      const hasHref = body.includes(`href="${b.href}"`) || body.includes(`href="${b.href.replace(/&/g, '&amp;')}"`);
      if (hasHref) {
        passedBreadcrumbLinks++;
        console.log(`  ✓ Breadcrumb Link: [${b.label}] -> ${b.href} (Found: true)`);
        
        // Also test that the breadcrumb target URL actually works on Explore SSR!
        const exploreTargetUrl = `https://moon-oh.com${b.href}`;
        const expReq = new Request(exploreTargetUrl);
        const expResp = await exploreHandler(expReq);
        const expOk = expResp.status === 200;
        console.log(`      └─ Target Explore SSR HTTP status: ${expResp.status} (OK: ${expOk})`);
      } else {
        console.error(`  ❌ Missing Breadcrumb Link: [${b.label}] -> expected href: ${b.href}`);
      }
    }
  }

  console.log("\n================================================================================");
  console.log(`🎉 COMPREHENSIVE NAVIGATION AUDIT SUMMARY:`);
  console.log(`  • Breadcrumb links tested: ${totalBreadcrumbLinksTested}`);
  console.log(`  • Breadcrumb links passed: ${passedBreadcrumbLinks} / ${totalBreadcrumbLinksTested} (100% OK: ${passedBreadcrumbLinks === totalBreadcrumbLinksTested})`);
  console.log("================================================================================");
}

runComprehensiveNavigationAudit();
