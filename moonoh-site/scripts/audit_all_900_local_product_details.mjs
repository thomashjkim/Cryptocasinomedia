import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import fs from 'fs';

async function testAllShopProducts() {
  const data = JSON.parse(fs.readFileSync('./local_shops_data.json', 'utf8'));
  const prods = data.products;

  console.log("================================================================================");
  console.log(`🔍 FULL AUDIT: TESTING ALL ${prods.length} LOCAL PRODUCT DETAIL URLS`);
  console.log("================================================================================");

  let passed = 0;
  let failed = 0;
  const failedList = [];

  for (let i = 0; i < prods.length; i++) {
    const p = prods[i];
    const u = `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`;
    const req = new Request(u);
    try {
      const resp = await itemDetailHandler(req);
      const status = resp.status;
      if (status === 200) {
        passed++;
      } else {
        failed++;
        failedList.push({ url: u, status });
      }
    } catch (e) {
      failed++;
      failedList.push({ url: u, error: String(e) });
    }
  }

  console.log(`\n🎉 TOTAL AUDIT RESULT:`);
  console.log(`  • Passed: ${passed} / ${prods.length} (100% OK: ${passed === prods.length})`);
  console.log(`  • Failed: ${failed}`);
  if (failedList.length > 0) {
    console.log("Failed samples:", failedList.slice(0, 5));
  }
}

testAllShopProducts();
