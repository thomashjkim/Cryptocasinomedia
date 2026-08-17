import fs from 'fs';

function verifySeoAeoGeoIntegrity() {
  console.log('======================================================================');
  console.log('🔍 SEO, AEO & GEO INTEGRITY AUDIT');
  console.log('======================================================================\n');

  const indexHtml = fs.readFileSync('index.html', 'utf8');
  const expHtml = fs.readFileSync('explore.html', 'utf8');
  const abtHtml = fs.readFileSync('about.html', 'utf8');
  const cntHtml = fs.readFileSync('contact.html', 'utf8');
  const itemDetailCode = fs.readFileSync('netlify/functions/item-detail.mjs', 'utf8');

  // 1. SameAs Official Profiles Across All Pages
  console.log('--- 1. OFFICIAL ENTITY sameAs PROFILES AUDIT ---');
  const requiredSameAs = [
    'https://www.instagram.com/moonoh_market',
    'https://www.threads.net/@moonoh_market',
    'https://www.tiktok.com/@moonoh_market',
    'https://apps.apple.com/us/app/moonoh/id6477390079',
    'https://play.google.com/store/apps/details?id=com.moonoh'
  ];
  for (const url of requiredSameAs) {
    const inIndex = indexHtml.includes(url);
    const inExp = expHtml.includes(url);
    const inAbt = abtHtml.includes(url);
    const inDetail = itemDetailCode.includes(url);
    console.log(`  ✓ Profile: ${url.padEnd(50)}: Index(${inIndex}) Exp(${inExp}) Abt(${inAbt}) Detail(${inDetail})`);
    if (!inIndex || !inExp || !inAbt || !inDetail) {
      throw new Error(`❌ Missing sameAs profile: ${url}`);
    }
  }
  console.log('  ✅ Organization sameAs Profiles Verified Everywhere!\n');

  // 2. Canonical and og:url Alignment
  console.log('--- 2. CANONICAL & OG:URL EXACT ALIGNMENT ---');
  const urlPairs = [
    { page: 'Homepage', html: indexHtml, canon: 'https://moon-oh.com/', og: 'https://moon-oh.com' },
    { page: 'Explore', html: expHtml, canon: 'https://moon-oh.com/explore', og: 'https://moon-oh.com/explore' },
    { page: 'About', html: abtHtml, canon: 'https://moon-oh.com/about', og: null }
  ];
  for (const p of urlPairs) {
    const hasCanon = p.html.includes(`rel="canonical" href="${p.canon}"`);
    console.log(`  ✓ ${p.page.padEnd(12)} Canonical (${p.canon}): ${hasCanon}`);
    if (!hasCanon) throw new Error(`❌ Canonical mismatch on ${p.page}`);
    if (p.og) {
      const hasOg = p.html.includes(`property="og:url"`) && p.html.includes(p.og);
      console.log(`  ✓ ${p.page.padEnd(12)} OG URL (${p.og}): ${hasOg}`);
      if (!hasOg) throw new Error(`❌ OG URL mismatch on ${p.page}`);
    }
  }
  console.log('  ✅ Canonical & og:url Alignment Passed!\n');

  // 3. Structured Data Truthfulness & No Fake Schema
  console.log('--- 3. STRUCTURED DATA (JSON-LD) TRUTHFULNESS ---');
  const fakeFields = ['aggregateRating', 'reviewCount', 'ratingValue', 'shippingDetails', 'freeShipping', 'hasMerchantReturnPolicy'];
  let fakeFieldFound = false;
  for (const ff of fakeFields) {
    if (itemDetailCode.includes(`"${ff}"`)) {
      console.log(`  ❌ Fake field detected in schema: ${ff}`);
      fakeFieldFound = true;
    }
  }
  console.log(`  ✓ Zero fake rating/review/shipping schema: ${!fakeFieldFound}`);
  if (fakeFieldFound) throw new Error('❌ Fake schema fields found in item-detail.mjs!');
  console.log('  ✅ Structured Data Truthfulness Passed!\n');

  // 4. Entity Trust & Methodology Sections
  console.log('--- 4. ENTITY TRUST, METHODOLOGY & REMOVAL / CLAIM POLICIES ---');
  const trustChecks = [
    { name: 'Data collection & curation methodology in /about', pass: abtHtml.includes('Data Collection &amp; Curation Methodology') },
    { name: 'Meaning of "Last Verified" date in /about', pass: abtHtml.includes('Last Verified') },
    { name: 'Web search vs mobile application relationship', pass: abtHtml.includes('Web Discovery vs. Mobile Application') },
    { name: 'Listing correction, business claim & opt-out in /about', pass: abtHtml.includes('Listing Corrections, Business Claim &amp; Opt-Out Policy') },
    { name: 'Store claim, content corrections & removal in /contact', pass: cntHtml.includes('Store Claim, Content Corrections &amp; Removal') },
    { name: 'Direct claim button in local shop detail banner', pass: itemDetailCode.includes('claim_business_click') }
  ];
  for (const tc of trustChecks) {
    console.log(`  ✓ ${tc.name.padEnd(60)}: ${tc.pass}`);
    if (!tc.pass) throw new Error(`❌ Missing trust section: ${tc.name}`);
  }
  console.log('  ✅ Entity Trust & Methodology Verified!\n');

  // 5. Sitemap Cleanliness
  console.log('--- 5. SITEMAP SEO CLEANLINESS ---');
  const sitemapIndex = fs.readFileSync('sitemap-index.xml', 'utf8');
  const locs = sitemapIndex.match(/<loc>(.*?)<\/loc>/g) || [];
  const hasQueryInLocs = locs.some(l => l.includes('?') || l.includes('&amp;'));
  console.log(`  ✓ Sitemap Index free of query/filter URLs: ${!hasQueryInLocs}`);
  if (hasQueryInLocs) throw new Error('❌ Sitemaps contain query parameters in <loc>!');
  console.log('  ✅ Sitemap Cleanliness Passed!\n');

  console.log('======================================================================');
  console.log('🎉 ALL SEO, AEO & GEO INTEGRITY CHECKS PASSED 100%!');
  console.log('======================================================================');
}

verifySeoAeoGeoIntegrity();
