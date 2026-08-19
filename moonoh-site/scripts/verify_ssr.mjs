import itemDetailHandler from './netlify/functions/item-detail.mjs';
import exploreHandler from './netlify/functions/explore.mjs';
import fs from 'fs';

async function run() {
  const db = JSON.parse(fs.readFileSync('./local_shops_data.json','utf8'));
  let pass=0, fail=0, issues=[];

  // === [6] LOCAL SHOP DETAIL SPOT CHECK ===
  console.log('[6] 로컬샵 디테일 페이지 스팟 체크');
  const shopIds = ['sey-coffee','salter-house','mirth-vintage','big-night','front-general-store','pop-up-grocer'];
  for (const shopId of shopIds) {
    const item = db.products.find(p => p.shop_id === shopId && p.image_source_url && p.image_source_url.startsWith('http'));
    if (!item) { console.log('  ❌ '+shopId+': 아이템 없음'); fail++; continue; }
    const url = 'https://moon-oh.com' + item.url;
    const resp = await itemDetailHandler(new Request(url));
    const html = await resp.text();
    const hasOgImg = html.includes('og:image') && html.includes('https://');
    const hasPrice = html.includes('$');
    const hasBc = html.includes('breadcrumb-bar');
    const hasCanon = html.includes('canonical');
    const hasJsonLd = html.includes('application/ld+json');
    const allOk = resp.status===200 && hasOgImg && hasPrice && hasBc && hasCanon && hasJsonLd;
    if(allOk) pass++; else { fail++; issues.push(shopId+' bc:'+hasBc+' canon:'+hasCanon+' img:'+hasOgImg); }
    const titleTag = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || 'N/A';
    const imgTag = (html.match(/og:image[^>]*content="([^"]+)"/) || html.match(/og:image" content="([^"]+)"/) || ['',''])[1];
    console.log('  '+(allOk?'✅':'❌')+' '+shopId);
    console.log('    상품: '+item.title.substring(0,50));
    console.log('    title tag: '+titleTag.substring(0,60));
    console.log('    img/price/bc/canon/jsonld: '+hasOgImg+'/'+hasPrice+'/'+hasBc+'/'+hasCanon+'/'+hasJsonLd);
  }

  // === [7] MOONOH NEW ITEMS ===
  console.log('\n[7] Moonoh 신규 물건 디테일');
  const moonohTests = [
    ['No.857 D&G Pour Homme', '/item/dolce-and-gabbana-pour-homme-the-bronx-ny-857'],
    ['No.856 Anker Power Bank', '/item/power-bank-anker-25k-manhattan-ny-856'],
  ];
  for (const [label, path] of moonohTests) {
    const resp = await itemDetailHandler(new Request('https://moon-oh.com'+path));
    const html = await resp.text();
    const hasOgImg = html.includes('og:image') && html.includes('https://');
    const hasPrice = html.includes('$');
    const hasBc = html.includes('breadcrumb-bar');
    const hasJsonLd = html.includes('application/ld+json');
    const hasCanon = html.includes('canonical');
    const titleTag = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || 'N/A';
    const dateSpan = (html.match(/product-meta[^>]*>[\s\S]{0,30}<span>([^<]+)<\/span>/) || [])[1] || 'N/A';
    const allOk = resp.status===200 && hasOgImg && hasPrice && hasBc && hasJsonLd;
    if(allOk) pass++; else { fail++; issues.push(label); }
    console.log('  '+(allOk?'✅':'❌')+' '+label);
    console.log('    title: '+titleTag.substring(0,60));
    console.log('    날짜: '+dateSpan+' | img/price/bc/jsonld: '+hasOgImg+'/'+hasPrice+'/'+hasBc+'/'+hasJsonLd);
  }

  // === [8] EXPLORE FILTER TESTS ===
  console.log('\n[8] Explore SSR 필터 체크');
  const filterTests = [
    ['Moonoh / Brooklyn', 'https://moon-oh.com/explore?source=moonoh&area=Brooklyn%2C%20NY'],
    ['Moonoh / Bronx', 'https://moon-oh.com/explore?source=moonoh&area=The%20Bronx%2C%20NY'],
    ['LocalShops / Brooklyn (전체)', 'https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY'],
    ['LocalShops / Manhattan', 'https://moon-oh.com/explore?source=localshops&area=Manhattan%2C%20NY'],
    ['LocalShops / Brooklyn / Vintage', 'https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY&category=vintage-fashion'],
    ['LocalShops / Brooklyn / Coffee', 'https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY&category=coffee-pantry'],
    ['All / Manhattan', 'https://moon-oh.com/explore?area=Manhattan%2C%20NY'],
    ['Marketplace / Manhattan', 'https://moon-oh.com/explore?source=marketplaces&area=Manhattan%2C%20NY'],
    ['Food Rescue', 'https://moon-oh.com/explore?source=foodrescue'],
    ['Default / all', 'https://moon-oh.com/explore'],
  ];
  for (const [label, url] of filterTests) {
    const resp = await exploreHandler(new Request(url));
    const html = await resp.text();
    const cards = (html.match(/item-card-img-wrap/g)||[]).length;
    const hasMeta = html.includes('<meta name="description"');
    const hasCanon = html.includes('canonical');
    const hasH1 = html.includes('<h1');
    const ok = resp.status===200 && cards > 0 && hasMeta;
    if(ok) pass++; else { fail++; issues.push('Filter:'+label+' cards='+cards); }
    console.log('  '+(ok?'✅':'❌')+' '+label+' | 카드: '+cards+' | meta: '+hasMeta+' | h1: '+hasH1);
  }

  // === FINAL ===
  console.log('\n' + '='.repeat(60));
  console.log('TOTAL: '+pass+' PASS / '+fail+' FAIL');
  if(issues.length) { console.log('이슈:'); issues.forEach(i => console.log('  ❌ '+i)); }
  console.log('='.repeat(60));
}
run();
