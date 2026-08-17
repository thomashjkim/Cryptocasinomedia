import defaultHandler from '../netlify/functions/item-detail.mjs';

async function testHappierDetail() {
  console.log('=== TESTING HAPPIER GROCERY ITEM DETAIL LOCALLY ===\n');

  const testPaths = [
    '/local-product/happier-grocery/happier-organic-ceremonial-matcha-100g',
    '/local-product/happier-grocery/artisanal-country-sourdough-loaf',
    '/local-product/happier-grocery/single-origin-72-dark-chocolate-bar'
  ];

  for (const p of testPaths) {
    console.log(`Testing URL: ${p}`);
    const req = new Request(`https://moon-oh.com${p}`);
    const res = await defaultHandler(req, {});
    console.log(`  Status: ${res.status}`);
    const html = await res.text();

    // 1. Check Canonical
    const canonMatch = html.match(/<link [^>]*rel=["']canonical["'][^>]*href=["']([^"']+)["']/i) || html.match(/<link [^>]*href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
    console.log(`  Canonical: ${canonMatch ? canonMatch[1] : 'NONE'}`);

    // 2. Check H1
    const h1Matches = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/gi) || [];
    console.log(`  H1 Count: ${h1Matches.length} | Text: ${h1Matches[0] ? h1Matches[0].replace(/<[^>]+>/g, '').trim() : 'NONE'}`);

    // 3. Check JSON-LD
    const jsonLdMatch = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/i);
    if (jsonLdMatch) {
      const graphData = JSON.parse(jsonLdMatch[1]);
      const productNode = (graphData['@graph'] || []).find(n => n['@type'] === 'Product') || graphData;
      console.log(`  JSON-LD @type: ${productNode['@type']}`);
      console.log(`  JSON-LD Name: ${productNode['name']}`);
      console.log(`  JSON-LD Brand: ${JSON.stringify(productNode['brand'])}`);
      console.log(`  JSON-LD Offers Seller: ${JSON.stringify(productNode['offers']?.seller)}`);
      console.log(`  JSON-LD has shippingDetails: ${'shippingDetails' in (productNode['offers'] || {})}`);
      console.log(`  JSON-LD has hasMerchantReturnPolicy: ${'hasMerchantReturnPolicy' in (productNode['offers'] || {})}`);
    } else {
      console.log('  ❌ NO JSON-LD FOUND');
    }

    // 4. Check CTA & Outbound URL
    const hasCTA = html.includes('View on Happier Grocery') || html.includes('View at Happier Grocery');
    const hasOutbound = html.includes('https://shop.happiergrocery.com/product/');
    console.log(`  CTA present: ${hasCTA} | Outbound Link present: ${hasOutbound}`);

    // 5. Check Handled Disclosure
    const hasDisclosure = html.includes('Shipping, returns, and checkout are handled by Happier Grocery');
    console.log(`  Handled Disclosure present: ${hasDisclosure}`);

    // 6. Check Image URL
    const hasCloudfront = html.includes('cloudfront.net');
    const hasUnsplash = html.includes('unsplash.com');
    console.log(`  Image source: Cloudfront=${hasCloudfront} | Unsplash=${hasUnsplash}`);
    console.log('--------------------------------------------------\n');
  }
}

testHappierDetail().catch(console.error);
