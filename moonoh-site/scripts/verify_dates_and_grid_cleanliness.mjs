import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function verifyAllDatesAndGrid() {
  console.log("================================================================================");
  console.log("🔍 COMPREHENSIVE DATE SANITIZATION & GRID CLEANLINESS AUDIT");
  console.log("================================================================================");

  let passed = 0;
  let total = 0;

  // 1. Test Grid View (Marketplace Tab)
  console.log("\n[Test 1] Testing Marketplace Grid View HTML for 'Today · ' prefix removal:");
  total++;
  const mktReq = new Request('https://moon-oh.com/explore/marketplaces');
  const mktResp = await exploreHandler(mktReq);
  const mktHtml = await mktResp.text();
  const hasTodayInGrid = mktHtml.includes('<div class="item-card-location">Today ·');
  console.log(`  • Contains 'Today ·' in item card location: ${hasTodayInGrid} (PASS: ${!hasTodayInGrid})`);
  if (!hasTodayInGrid) passed++;

  // 2. Test Detail Views for Date Cleanliness across items
  const itemsToTest = [
    { label: "Moonoh Latest (No. 855)", url: "https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855" },
    { label: "Moonoh Old Item (No. 800)", url: "https://moon-oh.com/item/item-800" },
    { label: "Moonoh Old Item (No. 700)", url: "https://moon-oh.com/item/item-700" },
    { label: "Moonoh Old Item (No. 500)", url: "https://moon-oh.com/item/item-500" },
    { label: "Moonoh Old Item (No. 300)", url: "https://moon-oh.com/item/item-300" },
    { label: "Moonoh Old Item (No. 100)", url: "https://moon-oh.com/item/item-100" },
    { label: "Marketplace (Karrot Item)", url: "https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-manhattan-ny-ext-karrot-i9753yxh6ayn" },
    { label: "Food Rescue (Kim'C Market)", url: "https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941" },
    { label: "Local Shop (SEY Coffee)", url: "https://moon-oh.com/local-product/sey-coffee/oma-plot" },
    { label: "Local Shop (Pop Up Grocer)", url: "https://moon-oh.com/local-product/pop-up-grocer/prind" }
  ];

  console.log("\n[Test 2] Testing Detail View Date Badges across all 4 sources:");
  for (const it of itemsToTest) {
    total++;
    try {
      const req = new Request(it.url);
      const resp = await itemDetailHandler(req);
      const html = await resp.text();
      
      const metaMatch = html.match(/<div class="product-meta">\s*<span>([^<]+)<\/span>/);
      const dateText = metaMatch ? metaMatch[1].trim() : 'N/A';
      
      const isBadDate = /1110|undefined|null|\b\d{3,}\s*days?|NaN/i.test(dateText);
      console.log(`  • ${it.label}: Date Badge = "${dateText}" (Valid & Clean: ${!isBadDate})`);
      if (!isBadDate) passed++;
    } catch(e) {
      console.error(`  • ${it.label} Error:`, e);
    }
  }

  console.log("\n================================================================================");
  console.log(`🎉 DATE & GRID AUDIT RESULT: ${passed} / ${total} (${Math.round(passed/total*100)}% PASS)`);
  console.log("================================================================================");
}

verifyAllDatesAndGrid();
