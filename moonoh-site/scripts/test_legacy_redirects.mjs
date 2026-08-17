import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testLegacyRedirects() {
  const testUrls = [
    'https://moon-oh.com/local-product/happier-grocery/organic-strawberry-hibiscus-sparkling-soda',
    'https://moon-oh.com/local-product/happier-grocery/artisanal-rosemary-infused-sea-salt-flakes',
    'https://moon-oh.com/local-product/happier-grocery/happier-organic-ceremonial-matcha-100g'
  ];

  for (const u of testUrls) {
    const res = await itemDetailHandler(new Request(u), {});
    console.log('Tested:', u);
    console.log('  Status:', res.status);
    console.log('  Location:', res.headers.get('location'));
    
    // Follow redirect
    if (res.status === 301) {
      const destUrl = res.headers.get('location');
      const resDest = await itemDetailHandler(new Request(destUrl), {});
      const html = await resDest.text();
      const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
      console.log('  Followed Destination:', destUrl, '=> Status:', resDest.status);
      console.log('  Rendered H1:', h1Match ? h1Match[1].trim() : 'NONE');
    }
    console.log('--------------------------------------------------');
  }
}

testLegacyRedirects().catch(console.error);
