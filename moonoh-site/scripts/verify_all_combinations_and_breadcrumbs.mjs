import itemDetailHandler from '../netlify/functions/item-detail.mjs';
import exploreHandler from '../netlify/functions/explore.mjs';
import fs from 'fs';

async function verifyAllCombinations() {
  console.log('=' .repeat(80));
  console.log('🔍 FULL AUDIT: SITEMAP COMBINATIONS, TABS, REGIONS, SHOPS, CATEGORIES & BREADCRUMBS');
  console.log('=' .repeat(80));

  let totalChecks = 0;
  let passChecks = 0;
  const issues = [];

  function check(cond, desc) {
    totalChecks++;
    if (cond) {
      passChecks++;
      console.log(`  ✅ ${desc}`);
    } else {
      issues.push(desc);
      console.log(`  ❌ FAIL: ${desc}`);
    }
  }

  // =========================================================================
  // 1. ALL URLS IN sitemap-pages.xml
  // =========================================================================
  console.log('\n[1] Testing all landing pages in sitemap-pages.xml');
  const pagesXml = fs.readFileSync('sitemap-pages.xml', 'utf8');
  const pageUrls = (pagesXml.match(/<loc>([^<]+)<\/loc>/g) || []).map(l => l.replace(/<\/?loc>/g, ''));
  
  console.log(`  Found ${pageUrls.length} URLs in sitemap-pages.xml`);

  for (const urlStr of pageUrls) {
    const urlObj = new URL(urlStr);
    const path = urlObj.pathname;
    
    // Skip static pages handled directly by netlify html redirects (about, terms, privacy, safety-trust, root)
    if (['/', '/about', '/terms', '/privacy', '/safety-trust'].includes(path)) {
      continue;
    }

    const resp = await exploreHandler(new Request(urlStr));
    const html = await resp.text();
    const is200 = resp.status === 200;
    const hasTitle = /<title>[^<]+<\/title>/.test(html);
    const hasH1 = /<h1[^>]*>[^<]+<\/h1>/.test(html);
    const hasCanonical = html.includes('rel="canonical"');
    const hasBreadcrumbSchema = html.includes('"@type": "BreadcrumbList"') || html.includes('"@type":"BreadcrumbList"');
    const hasCollectionSchema = html.includes('"@type": "CollectionPage"') || html.includes('"@type":"CollectionPage"');
    const cardCount = (html.match(/class="item-card"/g) || []).length;

    const ok = is200 && hasTitle && hasH1 && hasCanonical && hasBreadcrumbSchema;
    check(ok, `${path} (HTTP ${resp.status}, Title, H1, Canonical, BreadcrumbList, Cards: ${cardCount})`);
  }

  // =========================================================================
  // 2. ALL SHOP PROFILE PAGES IN sitemap-shops.xml
  // =========================================================================
  console.log('\n[2] Testing all 7 Local Shop Profile Pages in sitemap-shops.xml');
  const shopsXml = fs.readFileSync('sitemap-shops.xml', 'utf8');
  const shopUrls = (shopsXml.match(/<loc>([^<]+)<\/loc>/g) || []).map(l => l.replace(/<\/?loc>/g, ''));

  for (const shopUrl of shopUrls) {
    const resp = await exploreHandler(new Request(shopUrl));
    const html = await resp.text();
    const is200 = resp.status === 200;
    const hasTitle = /<title>[^<]+<\/title>/.test(html);
    const hasCanonical = html.includes('rel="canonical"');
    const hasBreadcrumbSchema = html.includes('BreadcrumbList');
    const cardCount = (html.match(/class="item-card"/g) || []).length;
    const path = new URL(shopUrl).pathname;

    const ok = is200 && hasTitle && hasCanonical && hasBreadcrumbSchema && cardCount > 0;
    check(ok, `Shop Profile ${path} (HTTP ${resp.status}, Cards: ${cardCount}, Title, Canonical, Breadcrumb)`);
  }

  // =========================================================================
  // 3. SOURCE TABS & QUERY PARAM COMBINATIONS + AEO SUMMARY DATA ACCURACY
  // =========================================================================
  console.log('\n[3] Testing Source Tabs, Region & Category Query Filter Combinations + AEO Summary');
  const queryCombos = [
    { label: 'All Items default', url: 'https://moon-oh.com/explore' },
    { label: 'Moonoh only', url: 'https://moon-oh.com/explore?source=moonoh' },
    { label: 'Local Shops only', url: 'https://moon-oh.com/explore?source=localshops' },
    { label: 'Marketplaces only', url: 'https://moon-oh.com/explore?source=marketplaces' },
    { label: 'Food Rescue only', url: 'https://moon-oh.com/explore?source=foodrescue' },
    { label: 'Moonoh + Brooklyn', url: 'https://moon-oh.com/explore?source=moonoh&area=Brooklyn%2C%20NY' },
    { label: 'Moonoh + Manhattan', url: 'https://moon-oh.com/explore?source=moonoh&area=Manhattan%2C%20NY' },
    { label: 'Moonoh + Queens', url: 'https://moon-oh.com/explore?source=moonoh&area=Queens%2C%20NY' },
    { label: 'LocalShops + Brooklyn', url: 'https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY' },
    { label: 'LocalShops + Manhattan', url: 'https://moon-oh.com/explore?source=localshops&area=Manhattan%2C%20NY' },
    { label: 'Marketplaces + Brooklyn', url: 'https://moon-oh.com/explore?source=marketplaces&area=Brooklyn%2C%20NY' },
    { label: 'Marketplaces + Manhattan', url: 'https://moon-oh.com/explore?source=marketplaces&area=Manhattan%2C%20NY' },
    { label: 'Category Furniture + Manhattan', url: 'https://moon-oh.com/explore/manhattan/furniture' },
    { label: 'Category Electronics + Brooklyn', url: 'https://moon-oh.com/explore/brooklyn/electronics' },
    { label: 'Category Fashion + Queens', url: 'https://moon-oh.com/explore/queens/fashion' },
    { label: 'Category Baby & Kids + Bronx', url: 'https://moon-oh.com/explore/bronx/baby-kids' },
    { label: 'Category Home & Garden + Staten Island', url: 'https://moon-oh.com/explore/staten-island/home-garden' },
    { label: 'Category Coffee & Pantry + Brooklyn', url: 'https://moon-oh.com/explore/brooklyn/food-groceries' }
  ];

  for (const combo of queryCombos) {
    const resp = await exploreHandler(new Request(combo.url));
    const html = await resp.text();
    const is200 = resp.status === 200;
    const cardCount = (html.match(/class="item-card"/g) || []).length;
    const hasGrid = html.includes('moonoh-item-grid');
    const hasSummaryCard = html.includes('aeo-summary-card');

    check(is200 && cardCount > 0 && hasGrid, `${combo.label} (${combo.url}) -> HTTP ${resp.status}, Cards: ${cardCount}, Summary: ${hasSummaryCard}`);
  }

  // =========================================================================
  // 4. BREADCRUMB NAVIGATION DEEP VERIFICATION (DETAIL PAGES)
  // =========================================================================
  console.log('\n[4] Deep Breadcrumb Navigation Verification across Detail Pages');
  const breadcrumbTests = [
    {
      label: 'Moonoh Item (No.857)',
      url: 'https://moon-oh.com/item/dolce-and-gabbana-pour-homme-the-bronx-ny-857',
      expectedCrumbs: ['Explore', 'The Bronx, NY', "Men's Fashion"]
    },
    {
      label: 'Local Shop Item (SEY Coffee)',
      url: 'https://moon-oh.com/local-product/sey-coffee/2026-pepe-jose-jijon-and-francisco-vintimilla-putushio-2nd-harvest-ecuador',
      expectedCrumbs: ['Local Shops', 'SEY Coffee', 'Brooklyn, NY', 'Coffee & Pantry']
    },
    {
      label: 'Local Shop Item (Front General Store)',
      url: 'https://moon-oh.com/local-product/front-general-store/issey-miyake-bow-tie-pleated-zip-up-jacket',
      expectedCrumbs: ['Local Shops', 'Front General Store', 'Brooklyn, NY']
    },
    {
      label: 'Local Shop Item (Salter House)',
      url: 'https://moon-oh.com/local-product/salter-house/bienaime-jours-heureux-bar-soap',
      expectedCrumbs: ['Local Shops', 'Salter House', 'Brooklyn, NY']
    },
    {
      label: 'Food Rescue Item (Kim\'C Market)',
      url: 'https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941',
      expectedCrumbs: ['Food Rescue', 'Brooklyn, NY', 'Food & Groceries']
    },
    {
      label: 'Karrot Marketplace Item',
      url: 'https://moon-oh.com/item/paquete-completo-por-tan-solo-40-manhattan-ny-ext-karrot-dmk9c6jcqym7',
      expectedCrumbs: ['Marketplaces', 'Manhattan, NY']
    },
    {
      label: 'HeyKorean Marketplace Item',
      url: 'https://moon-oh.com/item/motorola-moto-g-prepaid-queens-ny-ext-heykorean-669585',
      expectedCrumbs: ['Marketplaces', 'Queens, NY']
    }
  ];

  for (const bt of breadcrumbTests) {
    const resp = await itemDetailHandler(new Request(bt.url));
    const html = await resp.text();
    const hasBar = html.includes('class="breadcrumb-bar"');
    const hasSchema = html.includes('"@type": "BreadcrumbList"') || html.includes('"@type":"BreadcrumbList"');
    
    let allCrumbsFound = true;
    const missingCrumbs = [];
    for (const crumb of bt.expectedCrumbs) {
      if (!html.includes(crumb)) {
        allCrumbsFound = false;
        missingCrumbs.push(crumb);
      }
    }

    const ok = resp.status === 200 && hasBar && hasSchema && allCrumbsFound;
    check(ok, `Breadcrumbs on ${bt.label} (${bt.expectedCrumbs.join(' › ')}) ${missingCrumbs.length ? '[Missing: ' + missingCrumbs.join(',') + ']' : ''}`);
  }

  // =========================================================================
  // 5. SUMMARY
  // =========================================================================
  console.log('\n' + '=' .repeat(80));
  console.log(`COMBINATIONS & BREADCRUMBS AUDIT RESULT: ${passChecks} / ${totalChecks} PASSED`);
  if (issues.length === 0) {
    console.log('🎉 100% ALL COMBINATIONS, TABS, REGIONS, SHOPS, CATEGORIES & BREADCRUMBS VERIFIED PERFECTLY!');
  } else {
    console.log('❌ ISSUES DETECTED:');
    issues.forEach(i => console.log('  - ' + i));
  }
  console.log('=' .repeat(80));
}

verifyAllCombinations();
