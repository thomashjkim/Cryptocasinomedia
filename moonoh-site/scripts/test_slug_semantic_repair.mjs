import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testSlugSemanticRepair() {
  console.log('=== TESTING HAPPIER GROCERY SLUG SEMANTIC REPAIR LOCALLY ===\n');

  // 1. Test New Authentic Canonical URLs
  const newCanonicalSamples = [
    '/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups',
    '/local-product/happier-grocery/if-you-care-baking-pan-loaf',
    '/local-product/happier-grocery/biobag-quart-bags',
    '/local-product/happier-grocery/marak-sage-3-4oz-candle',
    '/local-product/happier-grocery/thousand-hills-ribeye-steak'
  ];

  console.log('--- 1. NEW AUTHENTIC CANONICAL URLS (Expect HTTP 200 + Self-Canonical) ---');
  for (const p of newCanonicalSamples) {
    const res = await itemDetailHandler(new Request(`https://moon-oh.com${p}`), {});
    const html = await res.text();
    const canonMatch = html.match(/<link [^>]*rel=["']canonical["'][^>]*href=["']([^"']+)["']/i) || html.match(/<link [^>]*href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
    const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    const isSelfCanon = canonMatch && canonMatch[1] === `https://moon-oh.com${p}`;
    console.log(`URL: ${p}`);
    console.log(`  Status: ${res.status} | Self-Canonical: ${isSelfCanon} | H1: ${h1Match ? h1Match[1].trim() : 'NONE'}`);
  }

  console.log('\n--- 2. OLD PLACEHOLDER SLUGS (Expect HTTP 404 + X-Robots-Tag: noindex, NO 301) ---');
  const oldPlaceholderSamples = [
    '/local-product/happier-grocery/happier-organic-ceremonial-matcha-100g',
    '/local-product/happier-grocery/artisanal-country-sourdough-loaf',
    '/local-product/happier-grocery/single-origin-72-dark-chocolate-bar',
    '/local-product/happier-grocery/organic-dark-roast-espresso-beans-12oz'
  ];

  for (const p of oldPlaceholderSamples) {
    const res = await itemDetailHandler(new Request(`https://moon-oh.com${p}`), {});
    const noindex = res.headers.get('x-robots-tag') === 'noindex';
    console.log(`URL: ${p}`);
    console.log(`  Status: ${res.status} (Expected 404) | Noindex Header: ${noindex}`);
  }
}

testSlugSemanticRepair().catch(console.error);
