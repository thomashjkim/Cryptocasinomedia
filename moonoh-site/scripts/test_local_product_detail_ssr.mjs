import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testProductUrls() {
  const testUrls = [
    'https://moon-oh.com/local-product/sey-coffee/oma-plot',
    'https://moon-oh.com/local-product/front-general-store/1-repeated-stitch-leather-belt',
    'https://moon-oh.com/local-product/mirth-vintage/60s-lace-skirt-set',
    'https://moon-oh.com/local-product/salter-house/add-gift-wrap',
    'https://moon-oh.com/local-product/big-night/24k-gold-plated-jigger',
    'https://moon-oh.com/local-product/pop-up-grocer/prind'
  ];

  console.log("================================================================================");
  console.log("🔍 TESTING LOCAL PRODUCT SSR DETAIL RENDERING");
  console.log("================================================================================");

  let passed = 0;
  for (const u of testUrls) {
    const req = new Request(u);
    try {
      const resp = await itemDetailHandler(req);
      const body = await resp.text();
      const status = resp.status;
      const isNotFound = body.includes("Product Not Found") || status === 404;
      const hasH1 = body.includes('<h1');
      console.log(`URL: ${u}`);
      console.log(`  -> Status: ${status} | Found: ${!isNotFound} | Has H1: ${hasH1}`);
      if (!isNotFound && status === 200) {
        passed++;
      }
    } catch (e) {
      console.error(`  -> Error: ${e}`);
    }
  }

  console.log(`\nResults: ${passed} / ${testUrls.length} passed!`);
}

testProductUrls();
