import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import merchantFeedHandler from '../netlify/functions/merchant-feed.mjs';
import fs from 'fs';

async function runPhase3Validation() {
  console.log('================================================================');
  console.log('  RUNNING PHASE 3A-2 FULL REGRESSION & VALIDATION TEST SUITE');
  console.log('================================================================\n');

  let passCount = 0;
  let failCount = 0;

  function assert(cond, msg) {
    if (cond) {
      console.log(`  ✅ PASS: ${msg}`);
      passCount++;
    } else {
      console.log(`  ❌ FAIL: ${msg}`);
      failCount++;
    }
  }

  // 1. Happier Grocery records in local_shops_data.json
  const localDb = JSON.parse(fs.readFileSync('local_shops_data.json', 'utf8'));
  const hgProds = localDb.products.filter(p => p.shop_id === 'happier-grocery');
  assert(hgProds.length === 30, `Total Happier Grocery records = ${hgProds.length} (expected 30)`);

  const validImgs = hgProds.filter(p => p.image_source_url && p.image_source_url.startsWith('https://d38cu1l1jdjf8r.cloudfront.net'));
  assert(validImgs.length === 30, `Records with authentic CloudFront primary images = ${validImgs.length} / 30`);

  const noUnsplash = hgProds.filter(p => p.image_source_url.includes('unsplash.com'));
  assert(noUnsplash.length === 0, `Unsplash placeholder images remaining = ${noUnsplash.length} (expected 0)`);

  // 2. New Authentic Detail Page
  const testDetail = await itemDetailHandler(new Request('https://moon-oh.com/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups'), {});
  assert(testDetail.status === 200, `Happier detail page status = ${testDetail.status}`);
  const htmlDetail = await testDetail.text();
  const canonMatch = htmlDetail.match(/<link [^>]*rel=["']canonical["'][^>]*href=["']([^"']+)["']/i) || htmlDetail.match(/<link [^>]*href=["']([^"']+)["'][^>]*rel=["']canonical["']/i);
  assert(canonMatch && canonMatch[1] === 'https://moon-oh.com/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups', `Happier detail is self-canonical (${canonMatch ? canonMatch[1] : 'NONE'})`);
  assert(htmlDetail.includes('View on Happier Grocery') || htmlDetail.includes('View at Happier Grocery'), 'Happier detail has correct CTA');
  assert(htmlDetail.includes('Shipping, returns, and checkout are handled by Happier Grocery'), 'Happier detail has handled disclosure');
  assert(!htmlDetail.includes('shippingDetails') && !htmlDetail.includes('hasMerchantReturnPolicy'), 'Happier detail has no fake shipping/return schema');

  // 3. Old Placeholder Slug Controlled 404
  const resOldPlaceholder = await itemDetailHandler(new Request('https://moon-oh.com/local-product/happier-grocery/happier-organic-ceremonial-matcha-100g'), {});
  assert(resOldPlaceholder.status === 404, `Old placeholder slug returns 404 = ${resOldPlaceholder.status}`);
  assert(resOldPlaceholder.headers.get('x-robots-tag') === 'noindex', 'Old placeholder slug returns X-Robots-Tag: noindex');

  // 4. Explore & Tabs
  const resExplore = await exploreHandler(new Request('https://moon-oh.com/explore'), {});
  assert(resExplore.status === 200, `Explore handler status = ${resExplore.status}`);
  const htmlExplore = await resExplore.text();
  assert(htmlExplore.includes('Happier Grocery') && htmlExplore.includes('Big Night'), 'Explore page includes all curated local shops');

  // 5. Phase 2 Redirect & 404 Samples
  const resLegacy = await itemDetailHandler(new Request('https://moon-oh.com/item/mr-potato-head-mug-downtown-manhattan-209'), {});
  assert(resLegacy.status === 301, `Legacy slug 1-hop 301 status = ${resLegacy.status}`);
  assert(resLegacy.headers.get('location') === 'https://moon-oh.com/item/mr-potato-head-mug-manhattan-ny-209', 'Legacy slug redirect destination is correct');

  const resChanel404 = await itemDetailHandler(new Request('https://moon-oh.com/item/chanel-woc-wallet-on-chain-1mi-queens-ny-ext-heykorean-669111'), {});
  assert(resChanel404.status === 404, `Mismatched Chanel WOC 669111 status = ${resChanel404.status}`);
  assert(resChanel404.headers.get('x-robots-tag') === 'noindex', 'Mismatched Chanel WOC 669111 has X-Robots-Tag: noindex');

  // 6. Merchant Center Feed
  const resFeed = await merchantFeedHandler(new Request('https://moon-oh.com/merchant-feed.xml'), {});
  assert(resFeed.status === 200, `Merchant feed status = ${resFeed.status}`);
  const feedXml = await resFeed.text();
  const itemCount = (feedXml.match(/<item>/g) || []).length;
  assert(itemCount === 0, `Merchant feed items = ${itemCount} (expected 0)`);

  console.log('\n================================================================');
  console.log(`  VALIDATION SUMMARY: ${passCount} PASSED / ${failCount} FAILED`);
  console.log('================================================================\n');

  if (failCount > 0) {
    process.exit(1);
  }
}

runPhase3Validation().catch(e => {
  console.error(e);
  process.exit(1);
});
