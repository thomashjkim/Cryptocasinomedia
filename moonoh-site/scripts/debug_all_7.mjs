import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testDebugAll() {
  const urls = [
    "https://moon-oh.com/local-product/sey-coffee/oma-plot",
    "https://moon-oh.com/local-product/front-general-store/tory-repeated-stitch-leather-belt-2332-2333-2334",
    "https://moon-oh.com/local-product/mirth-vintage/60s-lace-skirt-set",
    "https://moon-oh.com/local-product/salter-house/gift-wrap",
    "https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-1mi-malverne-ny-ext-karrot-i9753yxh6ayn",
    "https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-1mi-brooklyn-ny-ext-kimc-8141248626941",
    "https://moon-oh.com/item/oura-ring-4-size-9-brand-new-in-fhe-box-1mi-brooklyn-ny-851"
  ];

  for (const u of urls) {
    const req = new Request(u);
    const resp = await itemDetailHandler(req);
    console.log(`\nURL: ${u}`);
    console.log(`  -> Status: ${resp.status}`);
    if (resp.status === 301) {
      console.log(`  -> Redirect Location: ${resp.headers.get('Location')}`);
    } else if (resp.status === 200) {
      const body = await resp.text();
      const m = body.match(/<nav class="breadcrumb-bar" aria-label="Breadcrumb">([\s\S]*?)<\/nav>/);
      if (m) {
        console.log(`  -> Breadcrumbs HTML:\n${m[1].trim()}`);
      }
    } else {
      const body = await resp.text();
      console.log(`  -> Error: ${body.substring(0, 200)}`);
    }
  }
}

testDebugAll();
