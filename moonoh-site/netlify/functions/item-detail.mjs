import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

function getLocalShopsDb() {
  try {
    const jsonPath = path.join(currentDir, '../../local_shops_data.json');
    if (fs.existsSync(jsonPath)) {
      return JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    }
  } catch (e) {}
  try {
    const jsonPathAlt = path.join(process.cwd(), 'local_shops_data.json');
    if (fs.existsSync(jsonPathAlt)) {
      return JSON.parse(fs.readFileSync(jsonPathAlt, 'utf8'));
    }
  } catch (e) {}
  return { shops: {}, products: [] };
}


function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Compute human-readable "X days ago" from a millisecond timestamp
function computeTimeAgo(ms) {
  if (!ms || ms <= 0) return 'Recently';
  const diff = Date.now() - ms;
  if (diff < 0) return 'Just now';
  const mins  = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days  = Math.floor(diff / 86400000);
  const months = Math.floor(days / 30);
  const years  = Math.floor(days / 365);
  if (mins < 2)   return 'Just now';
  if (hours < 1)  return `${mins} min ago`;
  if (hours < 24) return hours === 1 ? '1 hour ago' : `${hours} hours ago`;
  if (days === 1) return '1 day ago';
  if (days <= 6)  return `${days} days ago`;
  if (days <= 13) return '1 week ago';
  if (days <= 29) return `${Math.floor(days/7)} weeks ago`;
  if (months <= 1) return '1 month ago';
  if (months <= 11) return `${months} months ago`;
  if (years === 1) return '1 year ago';
  return `${years} years ago`;
}

function formatDisplayTimeAgo(rawStr, sourceType) {
  // NOTE: sourceType is no longer used for hard-coded labels — real timestamps are always preferred.
  // Callers should pass a ms timestamp as rawStr, or a "X days ago" style string.

  if (!rawStr || rawStr === 'undefined' || rawStr === 'null' || rawStr === 'None') return 'Recently';

  // If rawStr is a millisecond timestamp (number or numeric string > 10^12)
  const asNum = Number(rawStr);
  if (!isNaN(asNum) && asNum > 1000000000000) {
    return computeTimeAgo(asNum);
  }

  let raw = String(rawStr).trim().replace(/\.+$/, '');

  // Check days ago: e.g. "1110 day ago.", "750 days ago", "1 day ago"
  const mDay = raw.match(/(\d+)\s*days?\s*ago/i);
  if (mDay) {
    const days = parseInt(mDay[1], 10);
    if (days > 365) return 'Over a year ago';
    if (days > 60)  return `${Math.floor(days/30)} months ago`;
    if (days === 1) return '1 day ago';
    return `${days} days ago`;
  }

  // Check months / years ago
  if (/year|month/i.test(raw)) {
    const mMonth = raw.match(/(\d+)\s*months?\s*ago/i);
    if (mMonth) {
      const months = parseInt(mMonth[1], 10);
      if (months === 1) return '1 month ago';
      if (months > 12) return 'Over a year ago';
      return `${months} months ago`;
    }
    const mYear = raw.match(/(\d+)\s*years?\s*ago/i);
    if (mYear) {
      const yrs = parseInt(mYear[1], 10);
      return yrs === 1 ? '1 year ago' : `${yrs} years ago`;
    }
    return 'Over a year ago';
  }

  // Check hours / minutes
  const mHour = raw.match(/(\d+)\s*hours?\s*ago/i);
  if (mHour) {
    const hrs = parseInt(mHour[1], 10);
    return hrs === 1 ? '1 hour ago' : `${hrs} hours ago`;
  }

  const mMin = raw.match(/(\d+)\s*mins?\s*ago|minutes?\s*ago/i);
  if (mMin) return 'Just now';

  if (/^(today|yesterday)$/i.test(raw)) {
    return raw.charAt(0).toUpperCase() + raw.slice(1).toLowerCase();
  }

  return 'Recently';
}


function getCategorySlug(catStr) {
  if (!catStr) return 'other';
  let c = String(catStr).toLowerCase().trim();
  if (c.includes('vintage') || (c.includes('fashion') && (c.includes('vintage') || c.includes('clothing')))) return 'vintage-fashion';
  if (c.includes('coffee') || c.includes('pantry')) return 'coffee-pantry';
  if (c.includes('home & objects') || c.includes('objects') || c.includes('tableware')) return 'home-objects';
  if (c.includes('gifts') || c.includes('culture')) return 'gifts-culture';
  if (c.includes('food') || c.includes('grocer') || c.includes('drink') || c.includes('snack')) return 'food-groceries';
  if (c.includes('furniture')) return 'furniture';
  if (c.includes('electronic') || c.includes('appliance')) return 'electronics';
  if (c.includes('health') || c.includes('beauty')) return 'health-beauty';
  if (c.includes('women')) return 'womens-fashion';
  if (c.includes('men')) return 'mens-fashion';
  if (c.includes('shoe')) return 'shoes';
  if (c.includes('baby') || c.includes('kid')) return 'baby-kids';
  if (c.includes('sports') || c.includes('leisure')) return 'sports-leisure';
  if (c.includes('toy') || c.includes('game')) return 'toys-games';
  if (c.includes('jewelry') || c.includes('watch')) return 'jewelry-watches';
  if (c.includes('luggage') || c.includes('bag')) return 'luggages-bags';
  if (c.includes('pet')) return 'pet-supplies';
  if (c.includes('antique')) return 'antiques';
  if (c.includes('art') || c.includes('book') || c.includes('music')) return 'arts-books-music';
  if (c.includes('free')) return 'free';
  return c.replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') || 'other';
}

function generateCategorySlugUrl(catStr, regionStr, sourceParam) {
  const s = sourceParam || 'moonoh';
  const catSlug = getCategorySlug(catStr);
  const loc = regionStr || 'Manhattan, NY';
  return `/explore?source=${encodeURIComponent(s)}&area=${encodeURIComponent(loc)}&category=${encodeURIComponent(catSlug)}`;
}

function generateRegionSlugUrl(locStr, sourceParam) {
  const s = sourceParam || 'moonoh';
  const loc = locStr || 'Manhattan, NY';
  return `/explore?source=${encodeURIComponent(s)}&area=${encodeURIComponent(loc)}`;
}

function generateSlug(title, locationStr, productNo) {
  let cleanTitle = (title || 'item')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
  
  if (!cleanTitle) cleanTitle = 'item';
  if (cleanTitle.length > 50) {
    cleanTitle = cleanTitle.substring(0, 50).replace(/-$/, '');
  }

  let locSlug = 'nyc-ny';
  if (locationStr) {
    let l = locationStr.toLowerCase();
    if (l.includes('bayside')) locSlug = 'bayside-queens-ny';
    else if (l.includes('flushing')) locSlug = 'flushing-queens-ny';
    else if (l.includes('astoria')) locSlug = 'astoria-queens-ny';
    else if (l.includes('queens')) locSlug = 'queens-ny';
    else if (l.includes('brooklyn')) locSlug = 'brooklyn-ny';
    else if (l.includes('manhattan')) locSlug = 'manhattan-ny';
    else if (l.includes('palisades')) locSlug = 'palisades-park-nj';
    else if (l.includes('fort lee')) locSlug = 'fort-lee-nj';
    else {
      locSlug = l.replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
    }
  }

  return `/item/${cleanTitle}-${locSlug}-${productNo}`;
}

function standardizeLocationName(locStr) {
  if (!locStr) return 'Manhattan, NY';
  let l = String(locStr).toLowerCase().trim();
  if (l.includes('manhattan') || l.includes('soho') || l.includes('tribeca') || l.includes('midtown') || l.includes('new york') || l.includes('ny, ny')) return 'Manhattan, NY';
  if (l.includes('queens') || l.includes('bayside') || l.includes('flushing') || l.includes('astoria') || l.includes('lic')) return 'Queens, NY';
  if (l.includes('brooklyn') || l.includes('greenpoint') || l.includes('williamsburg') || l.includes('bushwick') || l.includes('dumbo')) return 'Brooklyn, NY';
  if (l.includes('bronx')) return 'The Bronx, NY';
  if (l.includes('staten island')) return 'Staten Island, NY';
  if (l.includes('hudson') || l.includes('jersey city') || l.includes('hoboken')) return 'Hudson County, NJ';
  if (l.includes('bergen') || l.includes('fort lee') || l.includes('palisades') || l.includes('ridgefield') || l.includes('closter')) return 'Bergen County, NJ';
  if (l.includes('nassau') || l.includes('great neck') || l.includes('long island')) return 'Nassau County, NY';
  return locStr.replace(/^[0-9]+mi\s*·\s*/i, '').trim() || 'Manhattan, NY';
}

import { realFoodRescueItems } from './food-rescue-items.mjs';
import { realKarrotItems, realHeyKoreanItems } from './external-items.mjs';

const allRealExternalItems = {};
for (const item of [...(realKarrotItems || []), ...(realHeyKoreanItems || [])]) {
  if (item && item.id) {
    allRealExternalItems[item.id.toLowerCase()] = item;
  }
}

function getExternalItemById(extId) {
  const key = (extId || '').toLowerCase();

  // 1. Direct lookup in karrot/heykorean dict
  if (allRealExternalItems[key]) {
    return allRealExternalItems[key];
  }

  // 2. KimC items live in realFoodRescueItems — look there first
  const source = key.split('-')[0];
  if (source === 'kimc') {
    if (Array.isArray(realFoodRescueItems)) {
      const found = realFoodRescueItems.find(item => item && item.id && item.id.toLowerCase() === key);
      if (found) return found;
      // fallback: return first kimc item rather than a wrong heykorean item
      return realFoodRescueItems[0] || null;
    }
    return null;
  }

  return null;
}

function inferCategoryFromText(title = '', description = '', rawCategory = '') {
  const text = (title + ' ' + (description || '')).toLowerCase();
  const raw = (rawCategory || '').toLowerCase().trim();

  // If rawCategory is explicitly provided and not generic, prioritize it
  if (raw && !['used items', 'other', 'general', ''].includes(raw)) {
    const standardCategories = [
      'Electronics & appliances', 'Furniture', "Women's & Men's Fashion", 'Shoes', 'Baby & kids',
      'Sports & leisure', 'Luggages & bags', 'Food & Groceries', 'Pet supplies', 'Health & beauty',
      'Antiques & collections', 'Arts, books, music, movies & tickets', 'Jewelry & watches',
      'Coffee & Pantry', 'Vintage & Fashion', 'Home & Objects', 'Gifts & Culture', 'Free'
    ];
    const match = standardCategories.find(c => c.toLowerCase() === raw || raw.includes(c.toLowerCase()) || c.toLowerCase().includes(raw));
    if (match) return match;
    return rawCategory;
  }

  // 1. Electronics & Appliances
  if (/(macbook|imac|laptop|computer|monitor|iphone|galaxy|ipad|nintendo|ps5|ps4|playstation|xbox|gaming|console|tv|television|camera|printer|scanner|radiator|heater|aircon|air.?conditioner|air.?fryer|microwave|vacuum|refrigerator|fridge|coffee.?maker|coffee.?machine|nespresso|keurig|blender|cooker|calculator|keyboard|ram|router|headphone|airpods|speaker|bluetooth|vr|tablet|kindle|drone|hair.?dryer|hair.?iron|crimper|straightener|curler|curling|wired|electric|led|charger|battery|cable|amplifier|projector)|노트북|컴퓨터|모니터|아이폰|아이패드|에어컨|선풍기|히터|히타|청소기|스피커|전자레인지|냉장고|변압기|디바이스|와인셀러/i.test(text)) {
    return 'Electronics & appliances';
  }

  // 2. Pet Supplies
  if (/(pet|dog|cat|puppy|kitten|aquarium|leash|collar|crate|kennel|litter|kibble|ecofetch|chuckit)|강아지|고양이|반려/i.test(text)) {
    return 'Pet supplies';
  }

  // 3. Health & Beauty
  if (/(beauty|cosmetic|cosmetics|perfume|cologne|cream|lotion|soap|facial|brush|makeup|serum|skincare|sunscreen|foundation|lipstick|mascara|eyeshadow|toner|shampoo|conditioner|thermometer|blood.?pressure|massage|eye.?drops|eyedrops|rohto|mentholatum|lycee)|화장품|향수|비누|메이크업|브러쉬|스킨케어|안약/i.test(text)) {
    return 'Health & beauty';
  }

  // 4. Sports & Leisure
  if (/(ski|snowboard|bmx|bike|bicycle|golf|putter|vokey|driver|treadmill|exercise|dumbbell|sled|inversion.?table|racket|tent|camping|yoga|weights|gym|fishing|surfboard|skateboard|scooter|paddle)|자전거|골프|스키|운동|거꾸리|썰매|헬스|라이딩복|런닝머신/i.test(text)) {
    return 'Sports & leisure';
  }

  // 5. Furniture
  if (/(chair|chairs|table|tables|desk|desks|bed|beds|daybed|sofa|sofas|couch|dresser|mattress|shelf|shelves|cabinet|stool|stools|nightstand|nighttable|bench|ottoman|bookcase|wardrobe|armchair|recliner|loveseat|futon|hutch|credenza|sectional|media.?console|entertainment.?center|tv.?stand)|테이블|의자|소파|침대|책상|서랍|가구|식탁|선반|수납장/i.test(text)) {
    return 'Furniture';
  }

  // 6. Baby & Kids
  if (/(baby|kid|kids|toddler|stroller|crib|diaper|toy|toys|lego|gundam|sylvanian|calico.?critters|bassinet|highchair|playpen|car.?seat|infant|newborn|doll|action.?figure|children)|유아|아동|유모차|장난감|레고|베시넷/i.test(text)) {
    return 'Baby & kids';
  }

  // 7. Shoes
  if (/(shoe|shoes|sneaker|sneakers|boot|boots|sandal|sandals|hunter|nike|adidas|jordan|heel|heels|loafer|pump|pumps|mule|slipper|espadrille|converse|vans|chuck.?taylor|new.?balance|air.?force|yeezy)|신발|운동화|구두|부츠|슬리퍼/i.test(text)) {
    return 'Shoes';
  }

  // 8. Luggages & Bags
  if (/(bag|bags|backpack|backpacks|luggage|suitcase|tote|purse|handbag|crossbody|duffle|clutch|briefcase|wallet|cardholder|pouch)|가방|백팩|캐리어|토트백|핸드백|지갑/i.test(text)) {
    return 'Luggages & bags';
  }

  // 9. Women's Fashion
  if (/(dress|skirt|blouse|coat|jacket|bra|lingerie|heels|earring|necklace|bracelet|jewelry|leggings|cardigan|sweater|hoodie|scarf|maternity)|원피스|스커트|블라우스|코트|자켓|가디건|스웨터|여성/i.test(text)) {
    return "Women's & Men's Fashion";
  }

  // 10. Men's Fashion
  if (/(suit|blazer|tie|tuxedo|cufflinks|mens|men.?wear)|정장|수트|넥타이|남성/i.test(text)) {
    return "Women's & Men's Fashion";
  }

  // 11. Food & Groceries
  if (/(food|snack|ramen|noodle|rice|tea|coffee|kimchi|sauce|oil|spices|candy|cookie|drink|juice|beverage|korean.?food|gourmet|pantry|groceries|grocery)|식품|라면|과자|김치|쌀|간식|음료/i.test(text)) {
    return 'Food & Groceries';
  }

  // 12. Arts, Books & Music
  if (/(book|books|novel|textbook|comic|manga|album|vinyl|cd|dvd|instrument|guitar|piano|violin|ukulele|flute|drum|art|painting|drawing|canvas|poster|ticket|tickets)|책|도서|만화|음반|기타|피아노|바이올린|악기|그림|티켓/i.test(text)) {
    return 'Arts, books, music, movies & tickets';
  }

  // 13. Antiques & Collections
  if (/(antique|vintage|collectible|collection|figurine|statue|memorabilia|coin|stamp|rare)|골동품|빈티지|수집품|피규어/i.test(text)) {
    return 'Antiques & collections';
  }

  // 14. Jewelry & Watches
  if (/(ring|necklace|bracelet|earring|jewelry|watch|rolex|omega|cartier|gold|silver|diamond)|반지|목걸이|귀걸이|시계|보석/i.test(text)) {
    return 'Jewelry & watches';
  }

  return 'Other';
}


export default async (req, context) => {
  try {
    const url = new URL(req.url);
    const localShopsDb = getLocalShopsDb();
    let isExternal = false;
    let externalUrl = "";
    let externalSource = "";
    
    let title = "";
    let price = 0;
    let priceStr = "";
    let description = "";
    let townName = "NYC";
    let address = "New York, NY, USA";
    let strDayCount = "Recently";
    let sellerName = "Moonoh User";
    let vendorName = "Moonoh";
    let likeCount = 1;
    let categoryName = "Other";
    let lat = 40.7128;
    let lng = -74.0060;
    let productNo = "";
    let photos = [];
    let mainPhoto = "";
    let extId = "";
    let postedAt = 0;
    let postedAtIso = "";

    const localProductMatch = url.pathname.match(/\/local-product\/([^\/]+)\/([^\/]+)/i);
    const extMatch = url.pathname.match(/-ext-(karrot-[a-z0-9_-]+|heykorean-[a-z0-9_-]+|kimc-[a-z0-9_-]+)/i);

    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      const prodSlug = localProductMatch[2];
      let localItem = null;
      const localShopsDb = getLocalShopsDb();
      localItem = (localShopsDb.products || []).find(p => p.shop_id === shopSlug && (p.slug === prodSlug || p.legacy_slug === prodSlug || p.id === prodSlug));
      if (localItem && prodSlug === localItem.legacy_slug && localItem.legacy_slug !== localItem.slug) {
        return new Response(null, {
          status: 301,
          headers: {
            "Location": `https://moon-oh.com/local-product/${shopSlug}/${localItem.slug}`,
            "Cache-Control": "public, max-age=86400"
          }
        });
      }

      if (localItem) {
        isExternal = true;
        title = localItem.title;
        price = Number(localItem.current_price) || 0;
        priceStr = price > 0 ? (price % 1 !== 0 ? `$${price.toFixed(2)}` : `$${Math.round(price).toLocaleString()}`) : (price === 0 ? "Free" : `$${price}`);
        description = localItem.moonoh_summary || `${localItem.title} from ${localItem.brand || shopSlug}.`;

        const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
        const shopTitle = shopInfo.name || localItem.brand || shopSlug;
        townName = shopInfo.region || (shopInfo.city === 'New York' ? 'Manhattan, NY' : 'Brooklyn, NY');
        address = shopInfo.address_line_1 || (shopInfo.neighborhood ? `${shopInfo.neighborhood}, ${townName}` : `New York, NY`);
        if (shopInfo.lat && shopInfo.lng) {
          lat = shopInfo.lat;
          lng = shopInfo.lng;
        } else if (localItem.lat && localItem.lng) {
          lat = localItem.lat;
          lng = localItem.lng;
        }
        sellerName = localItem.brand || shopTitle;
        vendorName = localItem.brand || shopTitle;
        photos = [localItem.image_source_url];
        mainPhoto = localItem.image_source_url;
        categoryName = localItem.primary_category || localItem.moonoh_category || "Home & Objects";
        externalUrl = (localItem.source_url && localItem.source_url.startsWith('http')) ? localItem.source_url : (shopInfo.website_url || 'https://moon-oh.com');
        externalSource = shopSlug;

        // Calculate accurate timestamp and human-readable time ago for Local Products
        if (localItem.source_published_at) {
          const pubTime = new Date(localItem.source_published_at).getTime();
          if (!isNaN(pubTime) && pubTime > 0) {
            postedAt = pubTime;
            postedAtIso = new Date(postedAt).toISOString();
            strDayCount = computeTimeAgo(postedAt);
          }
        }
        if (!postedAt && localItem.last_checked_at) {
          const chkTime = new Date(localItem.last_checked_at).getTime();
          if (!isNaN(chkTime) && chkTime > 0) {
            postedAt = chkTime;
            postedAtIso = new Date(postedAt).toISOString();
            strDayCount = computeTimeAgo(postedAt);
          }
        }
        if (!postedAt) {
          postedAt = Date.now();
          postedAtIso = new Date(postedAt).toISOString();
          strDayCount = "Recently listed";
        }
      } else {
        return new Response("Product Not Found", {
          status: 404,
          headers: {
            "X-Robots-Tag": "noindex",
            "Content-Type": "text/plain; charset=utf-8"
          }
        });
      }
    } else if (extMatch) {
      isExternal = true;
      extId = extMatch[1].toLowerCase();
      productNo = extId;
      const extItem = getExternalItemById(extId);
      if (!extItem) {
        return new Response("Product Not Found", {
          status: 404,
          headers: {
            "X-Robots-Tag": "noindex",
            "Content-Type": "text/plain; charset=utf-8"
          }
        });
      }

      title = extItem.title;
      price = extItem.price;
      priceStr = price > 0 ? (price % 1 !== 0 ? `$${price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : `$${Math.round(price).toLocaleString()}`) : "Free";
      description = extItem.source === 'kimc'
        ? `Discover ${title} from Kim'C Market for ${priceStr}. Part of Kim'C Market's Fight Food Waste collection. Check current availability and complete your purchase at Kim'C Market.`
        : (extItem.description || `${extItem.title} listed in ${extItem.rawTown || extItem.location}. Originally posted on ${extItem.sourceName}.`);
      townName = standardizeLocationName(extItem.location || extItem.rawTown || 'Brooklyn, NY');
      address = extItem.rawTown || extItem.location || 'Brooklyn, NY';
      sellerName = extItem.sellerName || (extItem.source === 'karrot' ? 'Karrot Seller' : (extItem.source === 'kimc' ? "Kim'C Market" : 'HeyKorean Seller'));
      vendorName = extItem.source === 'kimc' ? "Kim'C Market" : (extItem.vendor || extItem.sellerName || "Moonoh");

      // Calculate postedAt, postedAtIso, and strDayCount for External items (Karrot, HeyKorean, Food Rescue)
      if (extItem.postedAt && typeof extItem.postedAt === 'number' && extItem.postedAt > 1000000000000) {
        postedAt = extItem.postedAt;
        postedAtIso = new Date(postedAt).toISOString();
        strDayCount = computeTimeAgo(postedAt);
      } else if (extItem.timeAgo && extItem.timeAgo !== 'Community Listing' && extItem.timeAgo !== 'Food Rescue') {
        strDayCount = formatDisplayTimeAgo(extItem.timeAgo);
        const dMatch = String(extItem.timeAgo).match(/(\d+)\s*days?\s*ago/i);
        const hMatch = String(extItem.timeAgo).match(/(\d+)\s*hours?\s*ago/i);
        if (dMatch) { postedAt = Date.now() - parseInt(dMatch[1], 10) * 86400000; }
        else if (hMatch) { postedAt = Date.now() - parseInt(hMatch[1], 10) * 3600000; }
        else { postedAt = Date.now(); }
        postedAtIso = new Date(postedAt).toISOString();
      } else {
        // Parse from image url if available
        const img = extItem.image || '';
        const hkMatch = img.match(/\/market\/item\/(\d{4})\/(\d{2})\/(\d{2})\//);
        if (hkMatch) {
          const [_, year, month, day] = hkMatch;
          postedAt = new Date(`${year}-${month}-${day}T12:00:00Z`).getTime();
          postedAtIso = new Date(postedAt).toISOString();
          strDayCount = computeTimeAgo(postedAt);
        } else {
          postedAt = Date.now();
          postedAtIso = new Date(postedAt).toISOString();
          strDayCount = "Recently listed";
        }
      }

      photos = [extItem.image];
      mainPhoto = extItem.image;
      categoryName = extItem.source === 'kimc' ? 'Food & Groceries' : inferCategoryFromText(title, description, extItem.category);
      externalUrl = extItem.url || extItem.detailUrl || (extItem.source === 'kimc' ? 'https://kimcmarket.com' : '');
      externalSource = extItem.source;
      if (extItem.lat && extItem.lng) { lat = extItem.lat; lng = extItem.lng; }
    } else {
      const pathParts = url.pathname.split('-');
      const productNoStr = pathParts.pop() || pathParts.pop(); // last part of slug is productNo
      productNo = productNoStr;

      if (!productNo || isNaN(parseInt(productNo, 10))) {
        return new Response("Product Not Found", {
          status: 404,
          headers: {
            "X-Robots-Tag": "noindex",
            "Content-Type": "text/plain; charset=utf-8"
          }
        });
      }

      // 1. Fetch Item Detail from app.do
      const detailParams = new URLSearchParams();
      detailParams.append('kind', 'getProductDetail');
      detailParams.append('productNo', productNo);

      const detailRes = await fetch("http://52.44.113.58:8080/app.do", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: detailParams
      });

      const d = await detailRes.json();

      if (!d || !d.title || d.isShow !== 'Y') {
        return new Response("Product Not Found", {
          status: 404,
          headers: {
            "X-Robots-Tag": "noindex",
            "Content-Type": "text/plain; charset=utf-8"
          }
        });
      }

      title = d.title || "Secondhand Item";
      price = d.price || 0;
      priceStr = price > 0 ? (price % 1 !== 0 ? `$${price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : `$${Math.round(price).toLocaleString()}`) : "Free";
      description = d.content || title;
      townName = standardizeLocationName(d.productTownName || d.address || "Manhattan, NY");
      address = d.address || "New York, NY, USA";
      strDayCount = formatDisplayTimeAgo(d.strDayCount, "moonoh");
      sellerName = d.sellerUserName || "Moonoh User";
      likeCount = d.likeCount || 0;
      categoryName = inferCategoryFromText(title, description, d.categoryName);
      lat = parseFloat(d.productY) || 40.7128;
      lng = parseFloat(d.productX) || -74.0060;

      // Extract postedAt timestamp for schema.org / OG tags
      if (d.postedAt && typeof d.postedAt === 'number' && d.postedAt > 1000000000000) {
        postedAt = d.postedAt;
        postedAtIso = new Date(postedAt).toISOString();
      } else if (d.strDayCount) {
        // Approximate from strDayCount string e.g. "3 days ago"
        const dMatch = String(d.strDayCount).match(/(\d+)\s*days?\s*ago/i);
        const hMatch = String(d.strDayCount).match(/(\d+)\s*hours?\s*ago/i);
        if (dMatch) { postedAt = Date.now() - parseInt(dMatch[1]) * 86400000; }
        else if (hMatch) { postedAt = Date.now() - parseInt(hMatch[1]) * 3600000; }
        else { postedAt = Date.now(); }
        postedAtIso = new Date(postedAt).toISOString();
      } else {
        postedAt = Date.now();
        postedAtIso = new Date(postedAt).toISOString();
      }

      // Photos Processing
      const normalizeToWebImg = (path) => {
        if (!path) return '';
        if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
          return path;
        }
        let p = path.replace(/^\/image-proxy\//, '');
        if (/\.heic$/i.test(p)) {
          const lastSlash = p.lastIndexOf('/');
          if (lastSlash !== -1) {
            const dir = p.substring(0, lastSlash + 1);
            const filename = p.substring(lastSlash + 1);
            const dotIdx = filename.lastIndexOf('.');
            const base = dotIdx !== -1 ? filename.substring(0, dotIdx) : filename;
            return `/image-proxy/${dir}thumbnail_${base}.jpg`;
          }
        }
        return `/image-proxy/${p}`;
      };

      if (d.strPictureUrlArray) {
        try {
          const arr = JSON.parse(d.strPictureUrlArray);
          photos = arr.map(p => normalizeToWebImg(p.fileUrl || ""));
        } catch (e) {}
      }

      if (photos.length === 0 && d.pictureUrl) {
        photos.push(normalizeToWebImg(d.pictureUrl));
      }
      if (photos.length === 0) {
        photos.push("images/default-item-placeholder.png");
      }

      mainPhoto = photos[0];
    }

    // Seller Picture (default clean SVG avatar if empty)
    const defaultAvatar = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%239CA3AF'%3E%3Cpath fill-rule='evenodd' d='M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z' clip-rule='evenodd' /%3E%3C/svg%3E";

    let sellerPic = defaultAvatar;
    if (!isExternal && typeof d !== 'undefined' && d && d.sellerPictureUrl && d.sellerPictureUrl.trim() !== "") {
      sellerPic = `/image-proxy/${d.sellerPictureUrl}`;
    }

    // 2. Fetch Related Items
    let relatedHtml = "";
    try {
      if (isExternal) {
        let selected = [];
        if (externalSource === 'kimc') {
          // Kim'C Market items MUST only recommend other Kim'C Market gourmet food rescue items!
          const allKimc = Array.isArray(realFoodRescueItems) ? realFoodRescueItems : [];
          selected = allKimc.filter(item => item && item.id && item.id !== extId).slice(0, 5);
        } else {
          // Handle External Related Items dynamically from allRealExternalItems
          const allItemsArr = Object.values(allRealExternalItems || {});
          const allExt = allItemsArr.filter(item => item && item.id && item.id !== extId);
          
          // Simple deterministic hash sort helper
          const getHash = (str) => {
            let h = 0;
            const s = String(str || '');
            for (let i = 0; i < s.length; i++) {
              h = (Math.imul(31, h) + s.charCodeAt(i)) | 0;
            }
            return Math.abs(h);
          };

          const currentSeed = getHash(extId || 'default');

          // 1. Same category items (case-insensitive & inferred category)
          const currentCat = String(categoryName || '').trim().toLowerCase();
          const sameCategory = allExt.filter(item => {
            const itemCat = inferCategoryFromText(item.title, item.description, item.category || item.categoryName).trim().toLowerCase();
            return itemCat === currentCat;
          });

          // Sort items deterministically based on product ID and current item seed
          const sortFn = (a, b) => (getHash(a.id) ^ currentSeed) - (getHash(b.id) ^ currentSeed);

          sameCategory.sort(sortFn);

          selected = sameCategory.slice(0, 5);
        }

        relatedHtml = selected.map(rel => {
          const p = Number(rel.price) || 0;
          const rPriceStr = p > 0 ? (p % 1 !== 0 ? `$${p.toFixed(2)}` : `$${Math.round(p).toLocaleString()}`) : "Free";
          const safeRelTitle = String(rel.title || "Item").replace(/"/g, '&quot;');
          const relSlug = generateSlug(rel.title, rel.rawTown || rel.location, `ext-${rel.id}`);
          const relImg = rel.image || "/images/default-item-placeholder.png";

          return `
            <a class="related-card" href="${relSlug}">
              <img src="${relImg}" class="related-card-img" alt="${safeRelTitle}" loading="lazy" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';"/>
              <div class="related-card-info">
                <div class="related-card-price">${rPriceStr}</div>
                <div class="related-card-name">${safeRelTitle}</div>
              </div>
            </a>
          `;
        }).join('');
      } else {
        // Handle Internal Moonoh Related Items from admin.do API
        const loginParams = new URLSearchParams();
        loginParams.append('kind', 'login');
        loginParams.append('id', 'admin');
        loginParams.append('password', '1234');
        
        const loginRes = await fetch("http://52.44.113.58:8080/admin.do", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: loginParams
        });
        const cookies = loginRes.headers.get('set-cookie');

        const dataParams = new URLSearchParams();
        dataParams.append('kind', 'getProductArray');
        dataParams.append('page', '0');
        dataParams.append('viewCount', '60');

        const dataRes = await fetch("http://52.44.113.58:8080/admin.do", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookies || ""
          },
          body: dataParams
        });

        const data = await dataRes.json();
        const allItems = (data.productArray || []).filter(item => item && item.no !== productNo && item.isShow === "Y");

        const currentCatLower = String(categoryName || '').trim().toLowerCase();
        const sameCat = allItems.filter(item => {
          const cat = inferCategoryFromText(item.title, item.content || item.title, item.categoryName).trim().toLowerCase();
          return cat === currentCatLower;
        });

        let seed = 0;
        for (let i = 0; i < String(productNo).length; i++) {
          seed += String(productNo).charCodeAt(i);
        }
        const pseudoRandom = (i) => {
          const x = Math.sin(seed + i) * 10000;
          return x - Math.floor(x);
        };
        const customSort = (arr) => [...arr].sort((a, b) => pseudoRandom(parseInt(a.no, 10) || 0) - pseudoRandom(parseInt(b.no, 10) || 0));

        const rawRelated = customSort(sameCat).slice(0, 5);

        const relatedWithDetails = await Promise.all(
          rawRelated.map(async (rel) => {
            let rPrice = rel.price || 0;
            let rLoc = rel.productTownName || townName;
            try {
              const pParams = new URLSearchParams();
              pParams.append('kind', 'getProductDetail');
              pParams.append('productNo', rel.no);

              const pRes = await fetch("http://52.44.113.58:8080/app.do", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: pParams
              });
              const pData = await pRes.json();
              if (pData) {
                if (typeof pData.price === 'number') rPrice = pData.price;
                if (pData.address || pData.productTownName) rLoc = pData.address || pData.productTownName;
              }
            } catch (e) {}

            let relImg = "images/common/ico_profile_empty.png";
            if (rel.pictureUrl) {
              const parts = rel.pictureUrl.split('/');
              const fileName = parts.pop();
              const pPath = parts.join('/') + '/';
              const dotIndex = fileName.lastIndexOf('.');
              const thumb = "thumbnail_" + (dotIndex !== -1 ? fileName.substring(0, dotIndex) : fileName) + ".jpg";
              relImg = `/image-proxy/${pPath}${thumb}`;
            }
            const relSlug = generateSlug(rel.title, rLoc, rel.no);
            const relPriceStr = rPrice > 0 ? `$${rPrice.toLocaleString()}` : "Free";
            const safeRelTitle = (rel.title || "").replace(/"/g, '&quot;');

            return `
              <a class="related-card" href="${relSlug}">
                <img src="${relImg}" class="related-card-img" alt="${safeRelTitle}" loading="lazy" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';"/>
                <div class="related-card-info">
                  <div class="related-card-price">${relPriceStr}</div>
                  <div class="related-card-name">${safeRelTitle}</div>
                </div>
              </a>
            `;
          })
        );

        relatedHtml = relatedWithDetails.join('');
      }
    } catch (e) {}

function isSemanticallyCompatible(incomingPath, expectedPath) {
  const getTokens = (p) => {
    const clean = p.replace(/^\/(item|local-product)\//, '')
      .replace(/-ext-[a-z0-9-]+$/, '')
      .replace(/-\d+$/, '')
      .replace(/-(nyc-ny|manhattan-ny|queens-ny|brooklyn-ny|flushing-queens-ny|bayside-queens-ny|astoria-queens-ny|fort-lee-nj|palisades-park-nj|bergen-county-nj|hudson-county-nj|1mi-[a-z-]+)/g, '')
      .replace(/-/g, ' ')
      .toLowerCase();
    const words = clean.match(/[a-z0-9]{2,}/g) || [];
    const stopwords = new Set(['item', 'for', 'sale', 'and', 'the', 'with', 'usa', 'nyc', 'ny', 'nj', 'new', 'used']);
    return words.filter(w => !stopwords.has(w));
  };

  const incomingTokens = getTokens(incomingPath);
  const expectedTokens = getTokens(expectedPath);
  
  // Generic structural alias (e.g. "item-12345" or "-12345") is a valid redirect
  if (incomingTokens.length === 0 || expectedTokens.length === 0) {
    return true;
  }

  // Check if any significant token overlaps
  const hasOverlap = incomingTokens.some(t => expectedTokens.includes(t)) || 
                     expectedTokens.some(t => incomingTokens.includes(t));
  
  return hasOverlap;
}

    // Page URL & Canonical (Enforce strict 301 Permanent Redirect for semantic aliases only)
    let expectedCanonicalPath = "";
    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      const prodSlug = localProductMatch[2];
      expectedCanonicalPath = `/local-product/${shopSlug}/${prodSlug}`;
    } else if (isExternal && extId) {
      expectedCanonicalPath = generateSlug(title, townName, `ext-${extId}`);
    } else {
      expectedCanonicalPath = generateSlug(title, townName, productNo);
    }

    if (url.pathname !== expectedCanonicalPath) {
      // If incoming URL has completely unrelated keywords from the current listing, return 404
      if (!isSemanticallyCompatible(url.pathname, expectedCanonicalPath)) {
        return new Response("Not Found", {
          status: 404,
          headers: { "Content-Type": "text/plain", "X-Robots-Tag": "noindex" }
        });
      }

      return new Response(null, {
        status: 301,
        headers: {
          "Location": `https://moon-oh.com${expectedCanonicalPath}`,
          "Cache-Control": "public, max-age=31536000, immutable"
        }
      });
    }

    const canonicalUrl = `https://moon-oh.com${expectedCanonicalPath}`;
    const absMainPhoto = mainPhoto.startsWith('http') ? mainPhoto : `https://moon-oh.com${mainPhoto}`;
    const absPhotos = (photos && photos.length > 0) 
      ? photos.map(p => p.startsWith('http') ? p : `https://moon-oh.com${p}`) 
      : [absMainPhoto];

    let sourceDisplayName = "Karrot";
    if (externalSource === 'heykorean') sourceDisplayName = "HeyKorean";
    else if (externalSource === 'kimc') sourceDisplayName = "Kim'C Market";
    else if (externalSource === 'happier-grocery') sourceDisplayName = "Happier Grocery";
    else if (externalSource === 'big-night') sourceDisplayName = "Big Night";
    else if (externalSource === 'pop-up-grocer') sourceDisplayName = "Pop Up Grocer";
    else if (externalSource === 'front-general-store') sourceDisplayName = "Front General Store";
    else if (externalSource === 'mirth-vintage') sourceDisplayName = "Mirth Vintage";
    else if (externalSource === 'sey-coffee') sourceDisplayName = "SEY Coffee";
    else if (externalSource === 'salter-house') sourceDisplayName = "Salter House";

    let bannerBg = "#FFF7ED";
    let bannerBorder = "#FFEDD5";
    let bannerColor = "#C2410C";
    let btnBgColor = "#4F46E5";
    let btnTextColor = "#FFFFFF";

    if (externalSource === "kimc") {
      bannerBg = "#E6F5F0";
      bannerBorder = "#99D6C4";
      bannerColor = "#006853";
      btnBgColor = "#006853";
    } else if (externalSource === "happier-grocery") {
      bannerBg = "#E8F8EE";
      bannerBorder = "#B9E8C7";
      bannerColor = "#1DAA4A";
      btnBgColor = "#1DAA4A";
      btnTextColor = "#FFFFFF";
    } else if (externalSource === "pop-up-grocer") {
      bannerBg = "#EBF4FF";
      bannerBorder = "#B8D9FF";
      bannerColor = "#005CFF";
      btnBgColor = "#005CFF";
    } else if (externalSource === "big-night") {
      bannerBg = "#FFF1F0";
      bannerBorder = "#FFCCC7";
      bannerColor = "#F63616";
      btnBgColor = "#F63616";
    } else if (externalSource === "front-general-store") {
      bannerBg = "#EDF2F7";
      bannerBorder = "#CBD5E0";
      bannerColor = "#1A202C";
      btnBgColor = "#2C3E50";
    } else if (externalSource === "mirth-vintage") {
      bannerBg = "#F9FAFB";
      bannerBorder = "#E5E7EB";
      bannerColor = "#111827";
      btnBgColor = "#000000";
      btnTextColor = "#FFFFFF";
    } else if (externalSource === "sey-coffee") {
      bannerBg = "#F3F4F6";
      bannerBorder = "#E5E7EB";
      bannerColor = "#111827";
      btnBgColor = "#1F2937";
    } else if (externalSource === "salter-house") {
      bannerBg = "#E6F5F0";
      bannerBorder = "#99D6C4";
      bannerColor = "#007A4B";
      btnBgColor = "#007A4B";
      btnTextColor = "#FFFFFF";
    } else if (externalSource === "heykorean") {
      bannerBg = "#EBF4FF";
      bannerBorder = "#B8D9FF";
      bannerColor = "#2D8CFF";
      btnBgColor = "#2D8CFF";
    } else if (externalSource === "karrot") {
      bannerBg = "#FFF7ED";
      bannerBorder = "#FFEDD5";
      bannerColor = "#C2410C";
      btnBgColor = "#FF6F0F";
    }

    // Custom meta values for local shops, food rescue vs secondhand marketplace items
    let pageTitle = `Used ${title} for Sale in ${townName} | Moonoh`;
    if (price === 0 || price === '0' || priceStr === 'Free') {
      pageTitle = `Free ${title} in ${townName} | Moonoh`;
    }
    let metaDescription = `Buy gently used ${title} (${priceStr}) in ${townName} on Moonoh — the 100% free neighborhood marketplace app for NYC & NJ. Zero fees, secure in-app chat, and safe local meetups.`;

    if (externalSource === 'kimc') {
      pageTitle = `${title} | Food Rescue at Kim'C Market in ${townName} - Moonoh`;
      metaDescription = `Discover ${title} for ${priceStr} from Kim'C Market in ${townName}. Part of the Fight Food Waste collection on Moonoh. Shipping, returns, and checkout are handled directly by Kim'C Market.`;
    } else if (['happier-grocery', 'big-night', 'pop-up-grocer', 'front-general-store', 'mirth-vintage', 'sey-coffee', 'salter-house'].includes(externalSource) || localProductMatch) {
      pageTitle = `${title} | ${sourceDisplayName} in ${townName} - Moonoh`;
      metaDescription = `Discover ${title} (${priceStr}) curated from ${sourceDisplayName} in ${townName}. Browse neighborhood specialty goods, vintage, and artisanal items on Moonoh.`;
    }

    
    // Determine exact source context and fallback URLs
    let currentSourceKey = 'moonoh';
    let fallbackExploreUrl = '/explore?source=moonoh';
    let breadcrumbHtml = '';

    if (localProductMatch) {
      const shopSlug = localProductMatch[1];
      currentSourceKey = 'localshops';
      fallbackExploreUrl = '/explore?source=localshops';
      const shopInfo = (localShopsDb.shops && localShopsDb.shops[shopSlug]) || {};
      const shopDisplayName = shopInfo.name || sellerName || 'Local Shop';
      const shopProfileUrl = `/local-shops/${shopSlug}`;
      const regionLinkUrl = generateRegionSlugUrl(townName, 'localshops');
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'localshops');

      breadcrumbHtml = `
        <a href="/explore?source=localshops">Local Shops</a>
        <span class="sep">›</span>
        <a href="${shopProfileUrl}">${shopDisplayName}</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;
    } else if (isExternal) {
      if (externalSource === 'kimc') {
        currentSourceKey = 'foodrescue';
        fallbackExploreUrl = '/explore?source=foodrescue';
        const regionLinkUrl = generateRegionSlugUrl(townName, 'foodrescue');
        const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'foodrescue');
        breadcrumbHtml = `
          <a href="/explore?source=foodrescue">Food Rescue</a>
          <span class="sep">›</span>
          <a href="${regionLinkUrl}">${townName}</a>
          <span class="sep">›</span>
          <a href="${categoryLinkUrl}">${categoryName}</a>
          <span class="sep">›</span>
        `;
      } else {
        currentSourceKey = 'marketplaces';
        fallbackExploreUrl = '/explore?source=marketplaces';
        const regionLinkUrl = generateRegionSlugUrl(townName, 'marketplaces');
        const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'marketplaces');
        breadcrumbHtml = `
          <a href="/explore?source=marketplaces">Marketplaces</a>
          <span class="sep">›</span>
          <a href="${regionLinkUrl}">${townName}</a>
          <span class="sep">›</span>
          <a href="${categoryLinkUrl}">${categoryName}</a>
          <span class="sep">›</span>
        `;
      }
    } else {
      currentSourceKey = 'moonoh';
      fallbackExploreUrl = '/explore?source=moonoh';
      const regionLinkUrl = generateRegionSlugUrl(townName, 'moonoh');
      const categoryLinkUrl = generateCategorySlugUrl(categoryName, townName, 'moonoh');
      breadcrumbHtml = `
        <a href="/explore?source=moonoh">Explore</a>
        <span class="sep">›</span>
        <a href="${regionLinkUrl}">${townName}</a>
        <span class="sep">›</span>
        <a href="${categoryLinkUrl}">${categoryName}</a>
        <span class="sep">›</span>
      `;
    }

    // Render HTML Page
    const html = `<!DOCTYPE HTML>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-1VN9Y8LLGX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-1VN9Y8LLGX');
  </script>
  <meta charset="utf-8"/>
  <title>${pageTitle}</title>
  <meta content="${metaDescription.replace(/"/g, '&quot;')}" name="description"/>
  <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport"/>
  
  <!-- Open Graph / Meta -->
  <meta property="og:title" content="${pageTitle}"/>
  <meta property="og:description" content="${metaDescription.substring(0, 160)}"/>
  <meta property="og:image" content="${absMainPhoto}"/>
  <meta property="og:image:secure_url" content="${absMainPhoto}"/>
  <meta property="og:url" content="${canonicalUrl}"/>
  <meta property="og:type" content="product"/>
  ${postedAtIso ? `<meta property="article:published_time" content="${postedAtIso}"/>` : ''}
  ${postedAtIso ? `<meta property="article:section" content="${categoryName}"/>` : ''}
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="${pageTitle}"/>
  <meta name="twitter:description" content="${metaDescription.substring(0, 160)}"/>
  <meta name="twitter:image" content="${absMainPhoto}"/>
  <link rel="image_src" href="${absMainPhoto}"/>

  <link href="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e51609210be273428d7ad8_Moonoh%2032.png" rel="shortcut icon" type="image/x-icon"/>
  <link href="${canonicalUrl}" rel="canonical"/>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Leaflet Map CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
  <!-- Schema.org Product & Breadcrumb Structured Data (SEO/AEO/GEO Engine) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org/",
    "@graph": [
      {
        "@type": "Organization",
        "@id": "https://moon-oh.com/#organization",
        "name": "Moonoh Inc.",
        "url": "https://moon-oh.com",
        "logo": "https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e51874e4a73ff20cb673ec_Logo.svg",
        "sameAs": [
          "https://www.instagram.com/moonoh_market",
          "https://www.threads.net/@moonoh_market",
          "https://www.tiktok.com/@moonoh_market",
          "https://apps.apple.com/us/app/moonoh/id6477390079",
          "https://play.google.com/store/apps/details?id=com.moonoh"
        ]
      },
      {
        "@type": "WebPage",
        "@id": ${JSON.stringify(canonicalUrl)},
        "url": ${JSON.stringify(canonicalUrl)},
        "name": ${JSON.stringify(pageTitle)},
        "primaryImageOfPage": {
          "@type": "ImageObject",
          "url": ${JSON.stringify(absMainPhoto)}
        }
      },
      {
        "@type": "Product",
        "@id": ${JSON.stringify(`${canonicalUrl}#product`)},
        "name": ${JSON.stringify(externalSource === 'kimc' ? `${title} - Kim'C Market` : title)},
        "image": ${JSON.stringify(absPhotos)},
        "description": ${JSON.stringify(metaDescription)},
        "category": ${JSON.stringify(categoryName)},
        "sku": ${JSON.stringify(`MOONOH-${productNo}`)},
        "mpn": ${JSON.stringify(`MPN-${productNo}`)},
        "identifier": ${JSON.stringify(`MOONOH-${productNo}`)},
        ${postedAtIso ? `"datePublished": ${JSON.stringify(postedAtIso)},` : ''}
        "brand": {
          "@type": "Brand",
          "name": ${JSON.stringify(externalSource === 'kimc' ? "Kim'C Market" : (isExternal && strDayCount === 'Local Shop' ? sourceDisplayName : (vendorName || "Secondhand")))}
        },
        "offers": {
          "@type": "Offer",
          "url": ${JSON.stringify(externalSource === 'kimc' ? externalUrl : (isExternal ? externalUrl : canonicalUrl))},
          "priceCurrency": "USD",
          "price": "${price}",
          "priceValidUntil": "2027-12-31T23:59:59Z",
          "validFrom": ${JSON.stringify(postedAtIso || "2026-01-01T00:00:00Z")},
          "availability": ${JSON.stringify(externalSource === 'kimc' ? 'https://schema.org/OutOfStock' : 'https://schema.org/InStock')},
          "itemCondition": ${JSON.stringify(externalSource === 'kimc' ? 'https://schema.org/NewCondition' : (isExternal ? 'https://schema.org/NewCondition' : 'https://schema.org/UsedCondition'))}${
            (externalSource === 'kimc' || (isExternal && strDayCount === 'Local Shop'))
              ? `,
          "seller": {
            "@type": "Organization",
            "name": ${JSON.stringify(sourceDisplayName)},
            "url": ${JSON.stringify(externalUrl)}
          }`
              : (sellerName && sellerName !== 'Moonoh' && sellerName !== 'HeyKorean' && sellerName !== 'Karrot')
                ? `,
          "seller": {
            "@type": "Person",
            "name": ${JSON.stringify(sellerName)}
          }`
                : ''
          }
        }
      }
    ]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://moon-oh.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Explore",
        "item": "https://moon-oh.com/explore"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": ${JSON.stringify(townName)},
        "item": ${JSON.stringify(`https://moon-oh.com/explore?town=${encodeURIComponent(townName)}`)}
      },
      {
        "@type": "ListItem",
        "position": 4,
        "name": ${JSON.stringify(categoryName)},
        "item": ${JSON.stringify(`https://moon-oh.com/explore?category=${encodeURIComponent(categoryName)}`)}
      },
      {
        "@type": "ListItem",
        "position": 5,
        "name": ${JSON.stringify(title)},
        "item": ${JSON.stringify(canonicalUrl)}
      }
    ]
  }
  </script>

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    body { background-color: #FFFFFF; color: #111827; -webkit-font-smoothing: antialiased; padding-bottom: 100px; }
    a { color: inherit; text-decoration: none; }

    .header-nav {
      position: sticky; top: 0; z-index: 100;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #E5E7EB;
      height: 64px;
      display: flex; align-items: center; justify-content: center;
    }
    .header-content {
      width: 100%; max-width: 940px; padding: 0 20px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .header-logo img { height: 24px; display: block; }
    .header-back { font-size: 14px; font-weight: 600; color: #4B5563; display: flex; align-items: center; gap: 6px; }
    .back-text-short { display: none; }
    @media (max-width: 768px) {
      .back-text-full { display: none; }
      .back-text-short { display: inline; }
    }

    .item-detail-container {
      max-width: 940px; margin: 12px auto 0; padding: 0 20px;
    }

    .breadcrumb-bar {
      display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
      font-size: 13px; color: #6B7280; font-weight: 500; margin-top: 4px; margin-bottom: 16px;
    }
    .breadcrumb-bar a { color: #4F46E5; text-decoration: none; font-weight: 600; transition: color 0.15s; }
    .breadcrumb-bar a:hover { color: #3730A3; text-decoration: underline; }
    .breadcrumb-bar .sep { color: #9CA3AF; font-size: 13px; }
    .breadcrumb-bar .current { color: #111827; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 220px; }

    .item-detail-layout {
      display: grid; grid-template-columns: 1fr 1fr; gap: 40px;
    }
    @media (max-width: 768px) {
      .item-detail-layout { grid-template-columns: 1fr; gap: 24px; }
      .item-detail-container { padding: 0 16px; margin-top: 4px; }
    }

    .gallery-container {
      position: relative; border-radius: 16px; overflow: hidden; background: #F3F4F6;
      aspect-ratio: 1 / 1; width: 100%; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .gallery-main-img {
      width: 100%; height: 100%; object-fit: cover; display: block; transition: opacity 0.2s ease-in-out;
      image-rendering: -webkit-optimize-contrast;
    }
    .gallery-indicators {
      position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
      display: flex; gap: 6px; z-index: 10;
    }
    .indicator-dot {
      width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.6);
      cursor: pointer; transition: all 0.2s;
    }
    .indicator-dot.active { background: #FFFFFF; width: 20px; border-radius: 4px; }

    
    

    .gallery-thumbnails {
      display: flex; gap: 10px; margin-top: 12px; overflow-x: auto; padding-bottom: 4px;
    }
    .thumb-item {
      width: 72px; height: 72px; border-radius: 10px; overflow: hidden; flex-shrink: 0;
      cursor: pointer; border: 2px solid transparent; opacity: 0.65; transition: all 0.2s;
    }
    .thumb-item.active { border-color: #4F46E5; opacity: 1; transform: scale(1.02); }
    .thumb-item img { width: 100%; height: 100%; object-fit: cover; }

    .info-section { display: flex; flex-direction: column; }
    .product-title {
      font-size: 22px; font-weight: 700; line-height: 1.35; color: #111827; margin-bottom: 12px;
    }
    .product-price {
      font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 6px;
    }
    .product-meta {
      font-size: 14px; color: #6B7280; margin-bottom: 24px; display: flex; align-items: center; gap: 6px;
    }

    .divider { height: 1px; background-color: #E5E7EB; margin: 20px 0; }

    .section-block { margin-bottom: 24px; }
    .section-title { font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 10px; }
    .description-text { font-size: 15px; line-height: 1.6; color: #374151; white-space: pre-line; }

    .seller-card { display: flex; align-items: center; gap: 14px; padding: 12px 0; }
    .seller-avatar { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; background: #E5E7EB; }
    .seller-name { font-size: 16px; font-weight: 700; color: #111827; }
    .seller-loc { font-size: 13px; color: #6B7280; margin-top: 2px; }

    .meetup-address {
      font-size: 14px; font-weight: 600; color: #111827; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;
    }
    #map-box {
      width: 100%; height: 220px; border-radius: 20px; overflow: hidden;
      border: 1px solid #E5E7EB; z-index: 1; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .custom-leaflet-pin { background: transparent !important; border: none !important; }

    .report-link { display: inline-block; font-size: 13px; color: #9CA3AF; text-decoration: underline; margin-top: 12px; cursor: pointer; }

    .bottom-bar {
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000;
      background: #FFFFFF; border-top: 1px solid #E5E7EB;
      padding: 14px 0;
      box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.06);
      display: flex; justify-content: center;
    }
    .bottom-bar-content {
      width: 100%; max-width: 940px; padding: 0 20px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .bottom-price { font-size: 20px; font-weight: 800; color: #111827; }
    .bottom-price-label { font-size: 12px; color: #6B7280; font-weight: 500; }
    
    .chat-btn {
      background: #4F46E5; color: #FFFFFF;
      font-size: 16px; font-weight: 700;
      padding: 12px 48px; border-radius: 999px;
      border: none; cursor: pointer;
      box-shadow: none;
      transition: background 0.2s, transform 0.1s;
    }
    .chat-btn:hover { background: #4338CA; box-shadow: none; }
    .chat-btn:active { transform: scale(0.97); }

    .related-section { max-width: 940px; margin: 48px auto 0; padding: 0 20px; }
    .related-title { font-size: 20px; font-weight: 700; margin-bottom: 20px; color: #111827; }
    .related-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
    @media (max-width: 768px) { .related-grid { grid-template-columns: repeat(2, 1fr); } }
    .related-card { background: #FFF; border-radius: 12px; overflow: hidden; border: 1px solid #E5E7EB; cursor: pointer; }
    .related-card-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; background: #F3F4F6; }
    .related-card-info { padding: 10px; }
    .related-card-price { font-size: 15px; font-weight: 700; color: #111; }
    .related-card-name { font-size: 13px; color: #4B5563; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }

    .moonoh-modal-overlay {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(4px);
      display: flex; align-items: center; justify-content: center;
      z-index: 9999; opacity: 0; pointer-events: none; transition: opacity 0.2s;
    }
    .moonoh-modal-overlay.active { opacity: 1; pointer-events: auto; }
    .moonoh-modal {
      background: #FFF; border-radius: 24px; padding: 36px 32px 32px; width: 90%; max-width: 400px; text-align: center; position: relative;
    }
    .moonoh-modal-close {
      position: absolute; top: 16px; right: 16px; font-size: 24px; border: none; background: none; cursor: pointer; color: #9CA3AF;
    }
    .header-share-btn {
      display: flex; align-items: center; gap: 6px;
      background: #F3F4F6; color: #374151;
      border: none; padding: 6px 14px; border-radius: 999px;
      font-size: 13px; font-weight: 600; cursor: pointer;
      transition: background 0.2s, transform 0.1s;
    }
    .header-share-btn:hover { background: #E5E7EB; color: #111827; }
    .header-share-btn:active { transform: scale(0.96); }
  
    .cta-btn-main {
      width: 100%;
      box-sizing: border-box;
      border: none;
      padding: 14px 16px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 15px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      text-decoration: none;
      white-space: nowrap;
      transition: opacity 0.2s, transform 0.1s;
    }
    .cta-btn-main:hover { opacity: 0.92; }
    .cta-btn-main:active { transform: scale(0.98); }
    @media (max-width: 480px) {
      .cta-btn-main {
        font-size: 13.5px !important;
        padding: 12px 10px !important;
        white-space: nowrap !important;
        letter-spacing: -0.2px !important;
      }
      .cta-btn-main span {
        white-space: nowrap !important;
      }
    }

</style>
</head>
<body>

    <!-- Top Header -->
  <header class="header-nav">
    <div class="header-content">
      <a href="${fallbackExploreUrl}" class="header-back" onclick="handleBackNavigation(event, '${fallbackExploreUrl}')">
        ← <span class="back-text-full">Back to Explore</span><span class="back-text-short">Back</span>
      </a>
      <a href="/" class="header-logo">
        <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e51874e4a73ff20cb673ec_Logo.svg" alt="moonoh logo"/>
      </a>
      <button class="header-share-btn" onclick="openShareModal()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
        <span>Share</span>
      </button>
    </div>
  </header>

  <!-- Product Detail Container -->
  <main class="item-detail-container">

    <!-- Smart Filter-Linked Breadcrumbs -->
    <nav class="breadcrumb-bar" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="sep">›</span>
      ${breadcrumbHtml}
      <span class="current">${title}</span>
    </nav>

    <div class="item-detail-layout">
      
      <!-- Left Column: Gallery -->
      <div>
        <div class="gallery-container">
          <img id="main-image" itemprop="image" fetchpriority="high" src="${mainPhoto}" alt="${escapeHtml(title)} for sale in ${escapeHtml(townName)}" class="gallery-main-img" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';"/>
          
          <div class="gallery-indicators" id="indicators">
            ${photos.map((_, i) => `<div class="indicator-dot ${i===0?'active':''}" onclick="switchImage(${i})"></div>`).join('')}
          </div>
        </div>
        
        <div class="gallery-thumbnails">
          ${photos.map((p, i) => `
            <div class="thumb-item ${i===0?'active':''}" onclick="switchImage(${i})">
              <img src="${p}" alt="${title} - Photo ${i+1} view in ${townName}" onerror="this.src='images/common/ico_profile_empty.png'"/>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Right Column: Info & Description -->
      <div class="info-section">
        <h1 class="product-title">${title}</h1>
        <div class="product-price">${priceStr}</div>
        <div class="product-meta">
          <span>${strDayCount}</span>
          <span>·</span>
          <span>${townName}</span>
        </div>

        ${isExternal ? `
        <div style="background:${bannerBg}; border:1px solid ${bannerBorder}; border-radius:12px; padding:12px 16px; margin-bottom:20px; font-size:13px; color:${bannerColor}; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
          <span>🛒 <strong>${sourceDisplayName}</strong> · Shipping, returns, availability, and checkout are handled by ${sourceDisplayName}.</span>
          <div style="display:flex; align-items:center; gap:12px;">
            <a href="/contact?claim=true&store=${encodeURIComponent(sourceDisplayName)}" onclick="if(typeof gtag==='function')gtag('event','claim_business_click',{store_name:'${sourceDisplayName}',destination_url:'/contact?claim=true'});" style="font-size:11px; color:${bannerColor}; opacity:0.85; text-decoration:underline;">Claim store</a>
            <a href="${externalUrl}" target="_blank" rel="noopener noreferrer" onclick="if(typeof gtag==='function')gtag('event','click_external_source',{item_id:'${productNo}',item_name:${JSON.stringify(title)},source:'${externalSource}',store_name:'${sourceDisplayName}',destination_url:'${externalUrl}'});" style="color:${bannerColor}; font-weight:700; text-decoration:underline;">View on ${sourceDisplayName} ↗</a>
          </div>
        </div>
        ` : ''}

        <div class="divider"></div>

        <!-- Description -->
        <div class="section-block">
          <h2 class="section-title">Description</h2>
          <p class="description-text">${description}</p>
        </div>

        <div class="divider"></div>

        <!-- Seller Info -->
        <div class="section-block">
          <h2 class="section-title">Seller information</h2>
          <div class="seller-card">
            <img src="${sellerPic}" alt="${sellerName}" class="seller-avatar" onerror="this.onerror=null; this.src='${defaultAvatar}';"/>
            <div>
              <div class="seller-name">${sellerName}</div>
              <div class="seller-loc">${townName}</div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- How to Purchase / Contact Seller -->
        <div class="section-block" style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:16px; padding:20px; margin-top:8px; margin-bottom:8px;">
          <h2 class="section-title" style="margin-top:0; font-size:16px; color:#111827;">${isExternal ? "How to View & Purchase" : "How to Contact Seller"}</h2>
          <p style="font-size:14px; color:#4B5563; margin-bottom:14px; line-height:1.5;">${isExternal ? `This item is listed on ${sourceDisplayName}. Shipping, returns, availability, and checkout are handled by ${sourceDisplayName}. Click below to view the official listing on ${sourceDisplayName}.` : `Download the free Moonoh app to chat directly with ${sellerName}, arrange local in-person pickup in ${townName}, and complete your exchange with zero fees.`}</p>
          ${isExternal 
            ? `<a href="${externalUrl}" target="_blank" rel="noopener noreferrer" onclick="if(typeof gtag==='function')gtag('event','click_external_source',{item_id:'${productNo}',item_name:${JSON.stringify(title)},source:'${externalSource}',store_name:'${sourceDisplayName}',destination_url:'${externalUrl}'});" class="cta-btn-main" style="background:${btnBgColor}; color:${btnTextColor || "#FFFFFF"};"><span>View on ${sourceDisplayName}</span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>`
            : `<a href="https://apps.apple.com/us/app/moonoh/id6477390079" target="_blank" rel="noopener noreferrer" onclick="if(typeof gtag==='function')gtag('event','contact_seller',{item_id:'${productNo}',item_name:${JSON.stringify(title)},location:'${townName}',category:'${categoryName}'});"  style="width:100%; background:#4F46E5; color:#FFFFFF; border:none; padding:14px; border-radius:12px; font-weight:700; font-size:15px; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; gap:8px; text-decoration:none;"><span>Open App to Message Seller</span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M12 5l7 7-7 7"/></svg></a>`
          }
        </div>

        <div class="divider"></div>

        <!-- Meetup Preference & Map -->
        <div class="section-block">
          <h2 class="section-title">Meetup preference</h2>
          <div class="meetup-address">
            <span>${address}</span>
            <span style="color:#9CA3AF;">›</span>
          </div>
          <div id="map-box"></div>
        </div>

        <a class="report-link" onclick="openModal()">Report this listing</a>
      </div>

    </div>
  </main>

  <!-- Related Items Section -->
  <section class="related-section">
    <h2 class="related-title">More items in ${categoryName}</h2>
    <div class="related-grid">
      ${relatedHtml}
    </div>
  </section>

  <!-- Crawlable Footer for Transparency & SEO -->
  <footer style="background:#F9FAFB; border-top:1px solid #E5E7EB; margin-top:64px; padding:48px 20px 120px; font-size:13px; color:#6B7280;">
    <div style="max-width:940px; margin:0 auto; display:grid; grid-template-columns:2fr 1fr 1fr; gap:32px;">
      <div>
        <h4 style="font-size:15px; font-weight:800; color:#111827; margin-bottom:8px;">Moonoh Inc.</h4>
        <p style="line-height:1.6; margin-bottom:8px;">8 Spruce Street, New York, NY 10038<br/>Phone: +1 (917) 584-5177 | Email: info@moon-oh.com</p>
        <p style="font-size:12px; color:#9CA3AF;">© 2026 Moonoh Inc. All rights reserved. Peer-to-peer neighborhood marketplace.</p>
      </div>
      <div>
        <h4 style="font-size:14px; font-weight:700; color:#111827; margin-bottom:10px;">Support &amp; Policy</h4>
        <ul style="list-style:none; padding:0; margin:0; line-height:2.0;">
          <li><a href="/return-policy" style="color:#4F46E5; font-weight:600; text-decoration:underline;">Marketplace Transaction Policy</a></li>
          <li><a href="/terms" style="color:#4F46E5; font-weight:600; text-decoration:underline;">Terms of Use</a></li>
          <li><a href="/privacy" style="color:#4F46E5; font-weight:600; text-decoration:underline;">Privacy Policy</a></li>
          <li><a href="/disclaimer" style="color:#4B5563; text-decoration:none;">Disclaimer</a></li>
        </ul>
      </div>
      <div>
        <h4 style="font-size:14px; font-weight:700; color:#111827; margin-bottom:10px;">Company</h4>
        <ul style="list-style:none; padding:0; margin:0; line-height:2.0;">
          <li><a href="/about" style="color:#4B5563; text-decoration:none;">About Us</a></li>
          <li><a href="/press" style="color:#4B5563; text-decoration:none;">Press &amp; Media</a></li>
          <li><a href="/contact" style="color:#4B5563; text-decoration:none;">Contact Us</a></li>
          <li><a href="/fraud-prevention" style="color:#4B5563; text-decoration:none;">Fraud Prevention</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <!-- Fixed Bottom Bar -->
  <div class="bottom-bar">
    <div class="bottom-bar-content">
      <div>
        <div class="bottom-price">${priceStr}</div>
        <div class="bottom-price-label">Initial price</div>
      </div>
      ${isExternal 
        ? `<a href="${externalUrl}" target="_blank" rel="noopener noreferrer" onclick="if(typeof gtag==='function')gtag('event','click_external_source',{item_id:'${productNo}',item_name:${JSON.stringify(title)},source:'${externalSource}',store_name:'${sourceDisplayName}',destination_url:'${externalUrl}'});"  class="chat-btn" style="display:inline-flex; align-items:center; justify-content:center; gap:6px; text-decoration:none; background:${btnBgColor};">View on ${sourceDisplayName} <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>`
        : `<a href="https://apps.apple.com/us/app/moonoh/id6477390079" target="_blank" rel="noopener noreferrer" onclick="if(typeof gtag==='function')gtag('event','contact_seller',{item_id:'${productNo}',item_name:${JSON.stringify(title)},location:'${townName}',category:'${categoryName}'});"  class="chat-btn" style="display:inline-flex; align-items:center; justify-content:center; gap:6px; text-decoration:none;">Chat with Seller in App</a>`
      }
    </div>
  </div>

  <!-- Download Modal -->
  <div class="moonoh-modal-overlay" id="moonoh-download-modal">
    <div class="moonoh-modal">
      <button class="moonoh-modal-close" onclick="closeModal()">×</button>
      <h3 style="font-size:22px; font-weight:800; color:#111827; margin-bottom:12px;">Get the Moonoh App</h3>
      <p style="font-size:14px; color:#6B7280; margin-bottom:28px; line-height:1.5;">Want to chat with <strong style="color:#111827;">${sellerName}</strong> to buy this item?<br/>Download the free Moonoh app to start secure chat.</p>
      <div style="display:flex; flex-direction:column; gap:12px;">
        <a href="https://apps.apple.com/us/app/moonoh/id6477390079" target="_blank" onclick="if(typeof gtag==='function')gtag('event','open_in_app',{source:'ios',destination_url:'https://apps.apple.com/us/app/moonoh/id6477390079'});" >
          <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e3defb38f948f6f3f18a51_appstore.svg" width="100%" style="max-width:220px; margin:0 auto; display:block;">
        </a>
        <a href="https://play.google.com/store/apps/details?id=com.moonoh" target="_blank" onclick="if(typeof gtag==='function')gtag('event','open_in_app',{source:'android',destination_url:'https://play.google.com/store/apps/details?id=com.moonoh'});" >
          <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/66f20cadd9e770db9e8cf5d7_Google_Play_Store_badge_EN.svg%20(1).png" width="100%" style="max-width:220px; margin:0 auto; display:block;">
        </a>
      </div>
    </div>
  </div>

  <!-- Share Popup Modal -->
  <div class="moonoh-modal-overlay" id="moonoh-share-modal">
    <div class="moonoh-modal" style="max-width: 380px;">
      <button class="moonoh-modal-close" onclick="closeShareModal()">×</button>
      <h3 style="font-size:20px; font-weight:800; color:#111827; margin-bottom:6px;">Share Listing</h3>
      <p style="font-size:13px; color:#6B7280; margin-bottom:24px;">Share this item via Email or copy link to share.</p>
      
      <div style="display:flex; flex-direction:column; gap:12px;">
        <a id="share-email-btn" href="#" target="_blank" style="display:flex; align-items:center; justify-content:center; gap:10px; background:#F3F4F6; color:#111827; border:1px solid #E5E7EB; padding:12px; border-radius:12px; font-weight:600; font-size:14px; text-decoration:none; transition:background 0.2s;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          <span>Share via Email</span>
        </a>

        <button id="share-copy-btn" onclick="copyShareLink()" style="display:flex; align-items:center; justify-content:center; gap:10px; background:#4F46E5; color:#FFFFFF; border:none; padding:12px; border-radius:12px; font-weight:600; font-size:14px; cursor:pointer; transition:all 0.2s;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span id="copy-btn-text">Copy Link</span>
        </button>
      </div>
    </div>
  </div>

  <script>
    const photos = ${JSON.stringify(photos)};

    function switchImage(index) {
      if (!photos[index]) return;
      const mainImg = document.getElementById('main-image');
      mainImg.style.opacity = '0.4';
      setTimeout(() => {
        mainImg.src = photos[index];
        mainImg.style.opacity = '1';
      }, 100);

      const thumbs = document.querySelectorAll('.thumb-item');
      thumbs.forEach((t, i) => t.classList.toggle('active', i === index));

      const dots = document.querySelectorAll('.indicator-dot');
      dots.forEach((d, i) => d.classList.toggle('active', i === index));
    }

    function openShareModal() {
      const modal = document.getElementById("moonoh-share-modal");
      const emailBtn = document.getElementById("share-email-btn");
      const title = ${JSON.stringify(title)};
      const price = ${JSON.stringify(priceStr)};
      const town = ${JSON.stringify(townName)};
      
      const mailSubject = encodeURIComponent("Check out this listing on Moonoh: " + title);
      const mailBody = encodeURIComponent("Hi!\\n\\nI found this " + title + " (" + price + ") in " + town + " on Moonoh marketplace:\\n" + window.location.href + "\\n\\nCheck it out!");
      if (emailBtn) emailBtn.href = "mailto:?subject=" + mailSubject + "&body=" + mailBody;

      const copyText = document.getElementById("copy-btn-text");
      if (copyText) copyText.innerText = "Copy Link";

      if (modal) modal.classList.add("active");
    }

    function closeShareModal() {
      const modal = document.getElementById("moonoh-share-modal");
      if (modal) modal.classList.remove("active");
    }

    function copyShareLink() {
      const copyBtnText = document.getElementById("copy-btn-text");
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(window.location.href).then(() => {
          if (copyBtnText) copyBtnText.innerText = "Link Copied! ✓";
          setTimeout(() => {
            if (copyBtnText) copyBtnText.innerText = "Copy Link";
            closeShareModal();
          }, 1500);
        }).catch(() => {
          prompt("Copy listing URL:", window.location.href);
        });
      } else {
        prompt("Copy listing URL:", window.location.href);
      }
    }

    
    function handleAppDownload(e) {
      if (e && e.preventDefault) e.preventDefault();
      var ua = navigator.userAgent || '';
      if (/iPhone|iPad|iPod/i.test(ua)) {
        window.open('https://apps.apple.com/us/app/moonoh/id6477390079', '_blank');
      } else if (/Android/i.test(ua)) {
        window.open('https://play.google.com/store/apps/details?id=com.moonoh', '_blank');
      } else {
        openModal();
      }
    }

    function openModal() {
      const modal = document.getElementById('moonoh-download-modal');
      if (modal) modal.classList.add('active');
    }
    
    function closeModal() {
      const modal = document.getElementById('moonoh-download-modal');
      if (modal) modal.classList.remove('active');
    }

    document.addEventListener("DOMContentLoaded", () => {
      const dlModal = document.getElementById('moonoh-download-modal');
      if (dlModal) {
        dlModal.addEventListener('click', function(e) {
          if (e.target === this) closeModal();
        });
      }

      const shareModal = document.getElementById('moonoh-share-modal');
      if (shareModal) {
        shareModal.addEventListener('click', function(e) {
          if (e.target === this) closeShareModal();
        });
      }

      const lat = ${lat};
      const lng = ${lng};
      const mapBox = document.getElementById('map-box');
      if (mapBox && typeof L !== 'undefined') {
        const map = L.map('map-box', {
          center: [lat, lng],
          zoom: 15,
          zoomControl: false,
          attributionControl: false
        });

        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
          maxZoom: 19,
          detectRetina: true
        }).addTo(map);

        L.circle([lat, lng], {
          color: '#5850EC',
          weight: 3,
          fillColor: '#5850EC',
          fillOpacity: 0.22,
          radius: 280
        }).addTo(map);

        const customPinIcon = L.divIcon({
          className: 'custom-leaflet-pin',
          html: \`
            <div style="position: relative; width: 34px; height: 46px; transform: translate(-50%, -100%);">
              <svg width="34" height="46" viewBox="0 0 38 50" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0px 3px 6px rgba(0,0,0,0.3));">
                <path d="M19 0C8.50659 0 0 8.50659 0 19C0 31.75 16.625 47.75 17.375 48.5C18.25 49.375 19.75 49.375 20.625 48.5C21.375 47.75 38 31.75 38 19C38 8.50659 29.4934 0 19 0Z" fill="url(#pin-grad)"/>
                <circle cx="19" cy="18" r="6" fill="#FFFFFF"/>
                <defs>
                  <linearGradient id="pin-grad" x1="19" y1="0" x2="19" y2="50" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#38BDF8"/>
                    <stop offset="1" stop-color="#0284C7"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
          \`,
          iconSize: [34, 46],
          iconAnchor: [17, 46]
        });

        L.marker([lat, lng], { icon: customPinIcon }).addTo(map);
      }
    });
  </script>
  <script>
    function handleBackNavigation(e, fallbackUrl) {
      e.preventDefault();
      if (window.history.length > 1 && document.referrer && (document.referrer.includes(window.location.host) || document.referrer.includes('moon-oh.com')) && !document.referrer.includes('/item/') && !document.referrer.includes('/local-product/')) {
        window.history.back();
      } else {
        window.location.href = fallbackUrl;
      }
    }
  </script>
</body>
</html>`;

    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=0, must-revalidate, s-maxage=0"
      }
    });

  } catch (error) {
    return new Response(`Error rendering item detail: ${error.message}`, { status: 500 });
  }
};
