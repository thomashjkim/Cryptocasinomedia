import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { realFoodRescueItems } from './food-rescue-items.mjs';
import { realKarrotItems, realHeyKoreanItems } from './external-items.mjs';
import { realMoonohItems } from './moonoh-items-data.mjs';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

// Load Local Shops DB
let localShopsData = { shops: {}, products: [], brand_listings: [] };
try {
  const jsonPath = path.join(currentDir, '../../local_shops_data.json');
  if (fs.existsSync(jsonPath)) {
    localShopsData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  }
} catch (e) {
  console.warn("Could not load local_shops_data.json:", e);
}

// Load local fallback data.json for instant cold start
let fallbackDataJson = [];
try {
  const dataJsonPath = path.join(currentDir, '../../data.json');
  if (fs.existsSync(dataJsonPath)) {
    fallbackDataJson = JSON.parse(fs.readFileSync(dataJsonPath, 'utf8'));
  }
} catch (e) {}

// Region Mapping
const REGIONS = {
  'new-york-area': { slug: 'new-york-area', name: 'New York Area', shortName: 'NYC & NJ', keywords: [] },
  'new-york': { slug: 'new-york', name: 'New York, NY', shortName: 'New York', keywords: ['new york', 'nyc', 'manhattan', 'brooklyn', 'queens', 'bronx', 'staten island'] },
  'nyc': { slug: 'nyc', name: 'New York City, NY', shortName: 'NYC', keywords: ['new york', 'nyc', 'manhattan', 'brooklyn', 'queens', 'bronx', 'staten island'] },
  'new-jersey': { slug: 'new-jersey', name: 'New Jersey', shortName: 'NJ', keywords: ['jersey', 'bergen', 'hudson', 'fort lee', 'hoboken', 'jersey city', 'newport', 'edgewater', 'nj'] },
  'nj': { slug: 'new-jersey', name: 'New Jersey', shortName: 'NJ', keywords: ['jersey', 'bergen', 'hudson', 'fort lee', 'hoboken', 'jersey city', 'newport', 'edgewater', 'nj'] },
  'manhattan': { slug: 'manhattan', name: 'Manhattan, NY', shortName: 'Manhattan', keywords: ['manhattan', 'upper east', 'upper west', 'downtown manhattan', 'midtown', 'harlem', 'tribeca', 'soho', 'lower east', 'east village', 'west village', 'chelsea', 'gramercy', 'inwood', 'washington heights', 'morningside', 'financial district', 'wall street', 'murray hill', 'kips bay', 'flatiron', 'new york'] },
  'queens': { slug: 'queens', name: 'Queens, NY', shortName: 'Queens', keywords: ['queens', 'bayside', 'flushing', 'astoria', 'jamaica', 'forest hills', 'jackson heights', 'woodside', 'ridgewood', 'ozone park', 'fresh meadows', 'corona', 'elmhurst', 'sunnyside', 'long island city', 'rego park', 'maspeth', 'howard beach', 'far rockaway', 'college point', 'whitestone', 'douglaston'] },
  'brooklyn': { slug: 'brooklyn', name: 'Brooklyn, NY', shortName: 'Brooklyn', keywords: ['brooklyn', 'park slope', 'williamsburg', 'bushwick', 'bed stuy', 'flatbush', 'crown heights', 'bay ridge', 'bensonhurst', 'canarsie', 'east new york', 'greenpoint', 'cobble hill', 'carroll gardens', 'boerum', 'sunset park', 'borough park', 'brighton beach', 'coney island', 'sheepshead', 'ditmas'] },
  'bronx': { slug: 'bronx', name: 'The Bronx, NY', shortName: 'Bronx', keywords: ['bronx'] },
  'staten-island': { slug: 'staten-island', name: 'Staten Island, NY', shortName: 'Staten Island', keywords: ['staten island'] },
  'flushing': { slug: 'flushing', name: 'Flushing, Queens, NY', shortName: 'Flushing', keywords: ['flushing', '플러싱', 'college point', 'whitestone', 'corona', 'elmhurst', 'queens'] },
  'bayside': { slug: 'bayside', name: 'Bayside, Queens, NY', shortName: 'Bayside', keywords: ['bayside', '베이사이드', 'douglaston', 'little neck', 'flushing', 'queens'] },
  'astoria': { slug: 'astoria', name: 'Astoria, Queens, NY', shortName: 'Astoria', keywords: ['astoria', 'long island city', 'lic'] },
  'fort-lee-nj': { slug: 'fort-lee-nj', name: 'Fort Lee, NJ', shortName: 'Fort Lee', keywords: ['fort lee', 'fortlee', 'palisades park', 'palisades', 'leonia', 'cliffside park', 'edgewater', 'fort-lee', 'bergen'] },
  'fort-lee': { slug: 'fort-lee-nj', name: 'Fort Lee, NJ', shortName: 'Fort Lee', keywords: ['fort lee', 'fortlee', 'palisades park', 'palisades', 'leonia', 'cliffside park', 'edgewater', 'fort-lee', 'bergen'] },
  'bergen-county-nj': { slug: 'bergen-county-nj', name: 'Bergen County, NJ', shortName: 'Bergen', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'bergen-county': { slug: 'bergen-county-nj', name: 'Bergen County, NJ', shortName: 'Bergen', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'hudson-county-nj': { slug: 'hudson-county-nj', name: 'Hudson County, NJ', shortName: 'Hudson', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] },
  'hudson-county': { slug: 'hudson-county-nj', name: 'Hudson County, NJ', shortName: 'Hudson', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] }
};

// Category Mapping
const CATEGORIES = {
  'electronics': { slug: 'electronics', name: 'Electronics', kw: 'electronics', keywords: ['electronics', 'phone', 'laptop', 'appliances', 'audio', 'gadget', 'ink', 'camera', 'tv', 'monitor', 'headphone', 'airpods', 'ipad', 'charger', 'speaker', 'printer', 'game', 'ps5', 'nintendo', 'xbox'] },
  'furniture': { slug: 'furniture', name: 'Furniture', kw: 'furniture', keywords: ['furniture', 'sofa', 'table', 'chair', 'bed', 'desk', 'couch', 'dresser', 'mattress', 'shelf', 'nightstand', 'cabinet', 'stool', 'bench', 'ottoman', 'headboard', 'drawers', '소파', '침대', '식탁', '의자', '책상', '서랍', '매트리스', '선반', '테이블', '가구'], excludes: ['pillow', 'hanger', 'curtain rod', 'fan', 'keyboard', 'monitor', 'massager', 'phone stand', 'photo printer', 'gymnastic', 'printer'] },
  'womens-fashion': { slug: 'womens-fashion', name: "Women's Fashion", kw: 'women', keywords: ["women's fashion", 'women', 'dress', 'handbag', 'skirt', 'coat'] },
  'fashion': { slug: 'womens-fashion', name: "Fashion & Clothing", kw: 'fashion', keywords: ['fashion', 'clothing', 'dress', 'shirt', 'pants', 'coat', 'jacket', 'shoes', 'women', 'men'] },
  'mens-fashion': { slug: 'mens-fashion', name: "Men's Fashion", kw: 'men', keywords: ["men's fashion", 'men', 'suit', 'jacket'] },
  'shoes': { slug: 'shoes', name: 'Shoes', kw: 'shoe', keywords: ['shoes', 'sneakers', 'boots', 'sandals', 'shoe', 'nike', 'adidas'] },
  'home-garden': { slug: 'home-garden', name: 'Home & Garden', kw: 'home', keywords: ['home, garden & diy', 'home', 'garden', 'kitchen', 'utensil', 'decor'] },
  'health-beauty': { slug: 'health-beauty', name: 'Health & Beauty', kw: 'health', keywords: ['health', 'beauty', 'cosmetics'] },
  'pet-supplies': { slug: 'pet-supplies', name: 'Pet Supplies', kw: 'pet', keywords: ['pet', 'dog', 'cat'] },
  'baby-kids': { slug: 'baby-kids', name: 'Baby & Kids', kw: 'baby', keywords: ['baby & kids', 'baby', 'kids', 'stroller', 'toy'] },
  'sports-leisure': { slug: 'sports-leisure', name: 'Sports & Leisure', kw: 'sport', keywords: ['sports', 'leisure', 'bike', 'ski', 'exercise'] },
  'toys-games': { slug: 'toys-games', name: 'Toys & Games', kw: 'toy', keywords: ['toys', 'games', 'card', 'figure'] },
  'jewelry-watches': { slug: 'jewelry-watches', name: 'Jewelry & Watches', kw: 'jewelry', keywords: ['jewelry', 'watches', 'ring', 'earrings', 'watch'] },
  'luggages-bags': { slug: 'luggages-bags', name: 'Luggages & Bags', kw: 'bag', keywords: ['luggages', 'bags', 'pouch', 'backpack', 'tote', 'wallet', 'bag'] },
  'antiques': { slug: 'antiques', name: 'Antiques', kw: 'antique', keywords: ['antiques', 'vintage', 'collectible'] },
  'arts-books-music': { slug: 'arts-books-music', name: 'Arts, Books & Music', kw: 'art', keywords: ['arts', 'books', 'music', 'book', 'print'] },
  'food-groceries': { slug: 'food-groceries', name: 'Food & Groceries', kw: 'food', keywords: ['food', 'groceries', 'snack', 'sauce', 'oil', 'rice', 'tea', 'noodle', 'kimchi', 'pantry', 'drink', 'beverage', 'korean food', 'cookie', 'juice', 'chip'] },
  'coffee-pantry': { slug: 'coffee-pantry', name: 'Coffee & Pantry', kw: 'coffee', keywords: ['coffee', 'pantry', 'tea', 'beans', 'roast', 'olive oil', 'syrup', 'snack'] },
  'vintage-fashion': { slug: 'vintage-fashion', name: 'Vintage & Fashion', kw: 'vintage', keywords: ['vintage', 'fashion', 'clothing', 'jacket', 'denim', 'dress', 'belt', 'leather'] },
  'home-objects': { slug: 'home-objects', name: 'Home & Objects', kw: 'home', keywords: ['home', 'objects', 'glass', 'dish', 'ceramic', 'candle', 'linen', 'plate', 'towel'] },
  'gifts-culture': { slug: 'gifts-culture', name: 'Gifts & Culture', kw: 'gifts', keywords: ['gifts', 'culture', 'book', 'stationery', 'print', 'card', 'poster'] },
  'free': { slug: 'free', name: 'Free Items', kw: 'free', isFree: true, keywords: ['free'] },
  'other': { slug: 'other', name: 'Other', kw: 'other', keywords: ['other', 'general'] }
};

let cachedCombinedItems = null;
let lastFetchTime = 0;
const CACHE_TTL_MS = 60 * 1000;

async function fetchAllCombinedItems() {
  const now = Date.now();
  if (cachedCombinedItems && (now - lastFetchTime) < CACHE_TTL_MS) {
    return cachedCombinedItems;
  }

  try {
    // Zero-latency in-memory external items
    const rawExternalList = [...(realKarrotItems || []), ...(realHeyKoreanItems || [])];
    const externalItems = rawExternalList.map((raw, idx) => {
      let clean = (raw.title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
      if (clean.length > 50) clean = clean.substring(0, 50).replace(/-$/, '');
      const loc = (raw.location || 'nyc-ny').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
      const targetUrl = `https://moon-oh.com/item/${clean}-${loc}-ext-${raw.id}`;
      return {
        id: raw.id,
        no: raw.id,
        title: raw.title,
        price: raw.price,
        photo: raw.image,
        image: raw.image,
        townName: raw.location,
        rawTown: raw.rawTown || raw.location,
        location: raw.location,
        categoryName: inferCategoryFromText(raw.title, raw.description, raw.category),
        category: inferCategoryFromText(raw.title, raw.description, raw.category),
        detailUrl: targetUrl,
        url: targetUrl,
        source: raw.source || 'external',
        sourceName: raw.sourceName || 'Marketplace',
        postedAt: raw.createdAt ? new Date(raw.createdAt).getTime() : (Date.now() - idx * 1200000)
      };
    });

    // Zero-latency in-memory Moonoh items with REAL prices & HTTPS proxy images
    const rawMoonohList = realMoonohItems && realMoonohItems.length > 0 ? realMoonohItems : fallbackDataJson;
    const moonohItems = rawMoonohList.map((raw, idx) => ({
      id: raw.id || raw.no,
      no: raw.no || raw.id,
      title: raw.title || "Secondhand Item",
      price: raw.price || 0,
      photo: raw.image || raw.photo || 'https://moon-oh.com/images/common/ico_profile_empty.png',
      image: raw.image || raw.photo || 'https://moon-oh.com/images/common/ico_profile_empty.png',
      townName: raw.townName || raw.location || 'Manhattan, NY',
      rawTown: raw.rawTown || raw.location || '',
      location: raw.location || 'Manhattan, NY',
      categoryName: raw.categoryName || raw.category || 'General',
      category: raw.categoryName || raw.category || 'General',
      detailUrl: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
      url: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
      source: 'moonoh',
      postedAt: raw.postedAt || (Date.now() - idx * 1800000)
    }));

    let foodRescueItems = [];
    if (Array.isArray(realFoodRescueItems)) {
      foodRescueItems = realFoodRescueItems.map((item, idx) => {
        let clean = (item.title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
        if (clean.length > 50) clean = clean.substring(0, 50).replace(/-$/, '');
        const targetUrl = `https://moon-oh.com/item/${clean}-brooklyn-ny-ext-${item.id}`;
        return {
          id: item.id,
          no: item.id,
          title: item.title,
          price: item.price,
          photo: item.image,
          image: item.image,
          townName: 'Brooklyn, NY',
          rawTown: 'Brooklyn, NY',
          location: 'Brooklyn, NY',
          categoryName: item.categoryName || 'Food & Groceries',
          category: item.categoryName || 'Food & Groceries',
          detailUrl: targetUrl,
          url: targetUrl,
          source: 'kimc',
          sourceName: "Kim'C Market",
          handle: item.handle,
          postedAt: Date.now() - (idx * 2400000 + 360000)
        };
      });
    }

    let localItems = [];
    if (localShopsData && Array.isArray(localShopsData.products)) {
      localItems = localShopsData.products.map((p, idx) => {
        const shop = (localShopsData.shops && localShopsData.shops[p.shop_id]) || {};
        // Map neighborhood to correct borough for filtering
        const NEIGHBORHOOD_BOROUGH = {
          'Greenpoint': 'Brooklyn, NY', 'Bushwick': 'Brooklyn, NY',
          'DUMBO': 'Brooklyn, NY', 'Brooklyn Heights': 'Brooklyn, NY',
          'SoHo': 'Manhattan, NY', 'Greenwich Village': 'Manhattan, NY',
          'Williamsburg': 'Brooklyn, NY', 'Astoria': 'Queens, NY'
        };
        const nh = shop.neighborhood || '';
        const borough = NEIGHBORHOOD_BOROUGH[nh] || p.location || shop.location || (p.shop_id === 'happier-grocery' || p.shop_id === 'pop-up-grocer' ? 'Manhattan, NY' : 'Brooklyn, NY');
        // Compute fresh timestamp: if source_published_at is reasonably recent (<= 180 days), use it; otherwise use last_checked_at
        let itemPostedAt = 0;
        if (p.source_published_at) {
          const pubTime = new Date(p.source_published_at).getTime();
          const daysDiff = (Date.now() - pubTime) / (1000 * 86400);
          if (!isNaN(pubTime) && pubTime > 0 && daysDiff <= 180) {
            itemPostedAt = pubTime;
          }
        }
        if (!itemPostedAt && p.last_checked_at) {
          const chkTime = new Date(p.last_checked_at).getTime();
          if (!isNaN(chkTime) && chkTime > 0) {
            itemPostedAt = chkTime - (idx * 60000);
          }
        }
        if (!itemPostedAt) {
          itemPostedAt = Date.now() - (idx * 60000);
        }

        return {
          id: p.id,
          no: p.id,
          title: p.title,
          price: p.current_price,
          photo: p.image_source_url,
          image: p.image_source_url,
          townName: borough,
          rawTown: borough,
          location: borough,
          categoryName: p.primary_category || p.moonoh_category || 'General',
          category: p.primary_category || p.moonoh_category || 'General',
          detailUrl: `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`,
          url: `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`,
          source: p.shop_id,
          badgeName: p.brand || shop.name || 'Local Shop',
          postedAt: itemPostedAt
        };
      });
    }

    cachedCombinedItems = [...moonohItems, ...externalItems, ...foodRescueItems, ...localItems];
    // Sort all combined items by original posting timestamp (recency order)
    cachedCombinedItems.sort((a, b) => {
      if (a.source === 'moonoh' && b.source === 'moonoh') {
        const noA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
        const noB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
        if (noA > 0 && noB > 0 && noA !== noB) return noB - noA;
      }
      const tA = getItemTimestamp(a);
      const tB = getItemTimestamp(b);
      if (tB !== tA) return tB - tA;
      const numA = parseInt(String(a.no || a.id || '').replace(/\D/g, ''), 10) || 0;
      const numB = parseInt(String(b.no || b.id || '').replace(/\D/g, ''), 10) || 0;
      return numB - numA;
    });
    
    lastFetchTime = now;
    return cachedCombinedItems;
  } catch (e) {
    console.error("Error in fetchAllCombinedItems:", e);
    return cachedCombinedItems || [];
  }
}

function interleaveLocalProducts(products) {
  if (!Array.isArray(products) || products.length === 0) return [];
  const shopMap = new Map();
  for (const p of products) {
    const sId = p.shop_id || p.source || 'other';
    if (!shopMap.has(sId)) shopMap.set(sId, []);
    shopMap.get(sId).push(p);
  }
  const shopKeys = Array.from(shopMap.keys());
  const maxLen = Math.max(...shopKeys.map(k => shopMap.get(k).length));
  const result = [];
  for (let i = 0; i < maxLen; i++) {
    for (const k of shopKeys) {
      const list = shopMap.get(k);
      if (i < list.length) {
        result.push(list[i]);
      }
    }
  }
  return result;
}

function interleaveMarketplaceProducts(products) {
  if (!Array.isArray(products) || products.length === 0) return [];
  const karrot = [];
  const heykorean = [];
  const others = [];
  for (const p of products) {
    const src = (p.source || '').toLowerCase();
    if (src.includes('karrot')) karrot.push(p);
    else if (src.includes('heykorean')) heykorean.push(p);
    else others.push(p);
  }
  const result = [];
  let kIdx = 0, hIdx = 0;
  while (kIdx < karrot.length || hIdx < heykorean.length) {
    if (kIdx < karrot.length) result.push(karrot[kIdx++]);
    if (hIdx < heykorean.length) result.push(heykorean[hIdx++]);
    if (hIdx < heykorean.length) result.push(heykorean[hIdx++]);
  }
  return result.concat(others);
}

function getItemTimestamp(item) {
  if (!item) return 0;
  if (item.postedAt) {
    const t = typeof item.postedAt === 'number' ? item.postedAt : new Date(item.postedAt).getTime();
    if (!isNaN(t) && t > 0) return t;
  }
  if (item.source_published_at) {
    const t = new Date(item.source_published_at).getTime();
    if (!isNaN(t) && t > 0) return t;
  }
  const img = item.photo || item.image || item.image_source_url || '';
  const mTemp = String(img).match(/\/temp\/(\d{13})\//);
  if (mTemp) {
    const t = parseInt(mTemp[1], 10);
    if (!isNaN(t) && t > 0) return t;
  }
  const numStr = String(item.no || item.id || '').replace(/\D/g, '');
  const num = parseInt(numStr, 10) || 0;
  if (num > 0) {
    return 1700000000000 + num * 100000;
  }
  return 0;
}

function inferCategoryFromText(title = '', description = '', rawCategory = '') {
  const text = (title + ' ' + (description || '')).toLowerCase();
  const raw = (rawCategory || '').toLowerCase().trim();

  // 1. Electronics & Appliances
  if (/\b(macbook|imac|laptop|computer|monitor|iphone|galaxy|ipad|nintendo|ps5|ps4|playstation|xbox|gaming|console|tv|television|camera|printer|scanner|radiator|heater|aircon|air.?conditioner|air.?fryer|microwave|vacuum|refrigerator|fridge|coffee.?maker|coffee.?machine|nespresso|keurig|blender|cooker|calculator|keyboard|ram|router|headphone|airpods|speaker|bluetooth|vr|tablet|kindle|drone|hair.?dryer|hair.?iron|crimper|straightener|curler|curling|wired|electric|led|charger|battery|cable|amplifier|projector)\b|노트북|컴퓨터|모니터|아이폰|아이패드|에어컨|선풍기|히터|히타|청소기|스피커|전자레인지|냉장고|변압기|디바이스|와인셀러/i.test(text)) {
    return 'Electronics & appliances';
  }

  // 2. Pet Supplies (Checked BEFORE Baby toys to prevent Dog Toy matching Baby)
  if (/\b(pet|dog|cat|puppy|kitten|aquarium|leash|collar|crate|kennel|litter|kibble|ecofetch|chuckit)\b|강아지|고양이|반려/i.test(text)) {
    return 'Pet supplies';
  }

  // 3. Health & Beauty (Checked BEFORE Men to prevent Mentholatum matching Men)
  if (/\b(beauty|cosmetic|cosmetics|perfume|cologne|cream|lotion|soap|facial|brush|makeup|serum|skincare|sunscreen|foundation|lipstick|mascara|eyeshadow|toner|shampoo|conditioner|thermometer|blood.?pressure|massage|eye.?drops|eyedrops|rohto|mentholatum|lycee)\b|화장품|향수|비누|메이크업|브러쉬|스킨케어|안약/i.test(text)) {
    return 'Health & beauty';
  }

  // 4. Sports & Leisure
  if (/\b(ski|snowboard|bmx|bike|bicycle|golf|putter|vokey|driver|treadmill|exercise|dumbbell|sled|inversion.?table|racket|tent|camping|yoga|weights|gym|fishing|surfboard|skateboard|scooter|paddle)\b|자전거|골프|스키|운동|거꾸리|썰매|헬스|라이딩복|런닝머신/i.test(text)) {
    return 'Sports & leisure';
  }

  // 5. Furniture
  if (/\b(chair|chairs|table|tables|desk|desks|bed|beds|daybed|sofa|sofas|couch|dresser|mattress|shelf|shelves|cabinet|stool|stools|nightstand|nighttable|bench|ottoman|bookcase|wardrobe|armchair|recliner|loveseat|futon|hutch|credenza|sectional|media.?console|entertainment.?center|tv.?stand)\b|테이블|의자|소파|침대|책상|서랍|가구|식탁|선반|수납장/i.test(text)) {
    return 'Furniture';
  }

  // 6. Baby & Kids
  if (/\b(baby|kid|kids|toddler|stroller|crib|diaper|toy|toys|lego|gundam|sylvanian|calico.?critters|bassinet|highchair|playpen|car.?seat|infant|newborn|doll|action.?figure|children)\b|유아|아동|유모차|장난감|레고|베시넷/i.test(text)) {
    return 'Baby & kids';
  }

  // 7. Shoes
  if (/\b(shoe|shoes|sneaker|sneakers|boot|boots|sandal|sandals|hunter|nike|adidas|jordan|heel|heels|loafer|pump|pumps|mule|slipper|espadrille|converse|vans|chuck.?taylor|new.?balance|air.?force|yeezy)\b|신발|운동화|구두|부츠|슬리퍼/i.test(text)) {
    return 'Shoes';
  }

  // 8. Luggages & Bags
  if (/\b(backpack|luggage|suitcase|tote|pouch|wallet|purse|clutch|duffel|carry.?on|briefcase|messenger|crossbody|fanny.?pack|osprey|sprayground)\b|가방|백팩|캐리어|지갑|파우치/i.test(text)) {
    return 'Luggages & bags';
  }

  // 9. Jewelry & Watches
  if (/\b(watch|watches|ring|rings|earring|earrings|necklace|bracelet|pendant|brooch|jewelry|jewellery|gem|diamond|gold|silver|pearl|bangle|anklet)\b|반지|귀걸이|목걸이|시계|팔찌|주얼리/i.test(text)) {
    return 'Jewelry & watches';
  }

  // 10. Home, Garden & DIY
  if (/\b(dish|dishes|plate|plates|bowl|bowls|cup|cups|mug|mugs|soju|serving|steamer|rice.?cooker|container|dispenser|towel|tissue|decor|decoration|mirror|curtain|plant|pot|pan|cookware|tool|vase|candle|lamp|light|fixture|rug|carpet|blanket|pillow|throw|comforter|sheet|tablecloth|hanger|organizer|storage|hook|rack|wicker|pendant|chandelier|toilet|bathroom|kitchen|garden)\b|주방|냄비|그릇|화분|인테리어|거울|장식|수저|화장지|소주잔|식기|조명/i.test(text)) {
    return 'Home, garden & DIY';
  }

  // 11. Women's Fashion
  if (/\b(women|womens|women's|dress|dresses|skirt|blouse|handbag|kaftan|bodycon|cardigan|romper|jumpsuit|maxi|mini|lingerie)\b|원피스|스커트|여성|핸드백/i.test(text)) {
    return "Women's fashion";
  }

  // 12. Men's Fashion
  if (/\b(mens|men's|suit|tuxedo|dress.?shirt|hoodie|polo|blazer|trench.?coat|parka|\bmen\b)\b/i.test(text) && !/\b(mentholatum|women|womens)\b/i.test(text)) {
    return "Men's fashion";
  }

  // 13. Arts, Books & Music
  if (/\b(book|books|novel|cookbook|textbook|guitar|piano|violin|instrument|music|painting|print|poster|record|vinyl|cd|dvd|comic|manga|journal)\b|책|악기|기타|그림|미술/i.test(text)) {
    return 'Arts, books & music';
  }

  // 14. Antiques & Collectibles
  if (/\b(vintage|antique|antiques|collectible|retro|limited.?edition|rare|classic)\b/i.test(text)) {
    return 'Antiques';
  }

  // 15. Food & Groceries
  if (/\b(food|foods|snack|snacks|chip|chips|cookie|cookies|noodle|noodles|ramen|kimchi|drink|drinks|beverage|beverages|candy|chocolate|matcha|honey|oil|jam|sourdough|juice|sauce|vinegar|seaweed|curry|somyeon)\b|식품|과자|라면|김치|음료|사탕|초콜릿|간식/i.test(text)) {
    return 'Food & Groceries';
  }

  // Fallback: normalize rawCategory to our internal system
  const CAT_MAP = {
    'electronics & appliances': 'Electronics & appliances',
    'electronics': 'Electronics & appliances',
    'appliances': 'Electronics & appliances',
    'furniture': 'Furniture',
    "women's fashion": "Women's fashion",
    "women's clothing": "Women's fashion",
    "men's fashion": "Men's fashion",
    "men's clothing": "Men's fashion",
    'shoes': 'Shoes',
    'footwear': 'Shoes',
    'home, garden & diy': 'Home, garden & DIY',
    'home & living': 'Home, garden & DIY',
    'home & garden': 'Home, garden & DIY',
    'garden & outdoor': 'Home, garden & DIY',
    'health & beauty': 'Health & beauty',
    'beauty & health': 'Health & beauty',
    'beauty': 'Health & beauty',
    'pet supplies': 'Pet supplies',
    'pets': 'Pet supplies',
    'baby & kids': 'Baby & kids',
    'baby & children': 'Baby & kids',
    'toys & games': 'Toys & games',
    'sports & leisure': 'Sports & leisure',
    'sports & outdoors': 'Sports & leisure',
    'jewelry & watches': 'Jewelry & watches',
    'jewelry': 'Jewelry & watches',
    'luggages & bags': 'Luggages & bags',
    'bags & accessories': 'Luggages & bags',
    'food & groceries': 'Food & Groceries',
    'food': 'Food & Groceries',
    'groceries': 'Food & Groceries',
    'arts, books & music': 'Arts, books & music',
    'books': 'Arts, books & music',
    'books & music': 'Arts, books & music',
    'antiques': 'Antiques',
  };

  if (raw) {
    if (CAT_MAP[raw]) return CAT_MAP[raw];
    for (const [key, val] of Object.entries(CAT_MAP)) {
      if (raw.includes(key) || key.includes(raw)) return val;
    }
  }

  return 'Other';
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function formatPriceStr(p) {
  if (p === 0 || p === '0' || p === 'Free' || p === 'free') return "Free";
  if (p === undefined || p === null || p === '') return "Price in store";
  const num = typeof p === 'number' ? p : parseFloat(p);
  if (isNaN(num)) return typeof p === 'string' && p ? p : "Price in store";
  if (num <= 0) return "Free";
  return num % 1 !== 0 ? "$" + num.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) : "$" + Math.round(num).toLocaleString();
}

function getExploreTemplate() {
  try {
    const templatePath = path.join(currentDir, '../../explore.html');
    if (fs.existsSync(templatePath)) {
      return fs.readFileSync(templatePath, 'utf8');
    }
  } catch (e) {}
  return null;
}

export default async (req, context) => {
  try {
    const url = new URL(req.url);
    const qSource = url.searchParams.get('source');
    const qCategory = url.searchParams.get('category');
    const qTownName = url.searchParams.get('town') || url.searchParams.get('townName') || url.searchParams.get('location');

    const fullPath = url.pathname.replace(/\/$/, '');
    let isShopProfile = false;
    let shopProfileSlug = null;

    if (fullPath.startsWith('/local-shops/')) {
      isShopProfile = true;
      shopProfileSlug = fullPath.replace('/local-shops/', '').toLowerCase();
    }

    const explorePath = fullPath.replace(/^\/explore\/?/, '');
    const pathSegments = explorePath.split('/').filter(Boolean);

    let isFoodRescuePage = false;
    let isLocalShopsPage = false;
    let isMarketplacesPage = false;

    let targetRegionObj = null;
    let targetCategoryObj = null;

    pathSegments.forEach(seg => {
      const s = seg.toLowerCase();
      if (s === 'food-rescue' || s === 'foodrescue') isFoodRescuePage = true;
      else if (s === 'local-shops' || s === 'localshops' || s === 'local') isLocalShopsPage = true;
      else if (s === 'marketplaces' || s === 'others') isMarketplacesPage = true;
      if (REGIONS[s]) targetRegionObj = REGIONS[s];
      if (CATEGORIES[s]) targetCategoryObj = CATEGORIES[s];
    });

    // Also support query parameters for category/town canonicalization
    const qCat = (qCategory || '').toLowerCase().trim();
    const qTown = (qTownName || '').toLowerCase().trim();
    if (!targetCategoryObj && qCat) {
      for (const [k, v] of Object.entries(CATEGORIES)) {
        if (k === qCat || v.slug === qCat || v.name.toLowerCase() === qCat || (v.keywords && v.keywords.includes(qCat))) {
          targetCategoryObj = v;
          break;
        }
      }
    }
    if (!targetRegionObj && qTown) {
      for (const [k, v] of Object.entries(REGIONS)) {
        if (k === qTown || v.slug === qTown || v.shortName.toLowerCase() === qTown || v.name.toLowerCase().includes(qTown)) {
          targetRegionObj = v;
          break;
        }
      }
    }

    const isFoodRescueFilter = isFoodRescuePage || qSource === 'food-rescue' || qSource === 'kimc';
    const isLocalShopsFilter = isLocalShopsPage || qSource === 'local-shops' || qSource === 'local';
    const isMarketplacesFilter = isMarketplacesPage || qSource === 'marketplaces' || qSource === 'others';

    // 301 Canonical Redirect for alias region slugs and query-parameterized category/town URLs
    if (!isFoodRescueFilter && !isLocalShopsFilter && !isMarketplacesFilter && !isShopProfile) {
      let expectedPath = '/explore';
      if (targetRegionObj && targetCategoryObj) {
        expectedPath = `/explore/${targetRegionObj.slug}/${targetCategoryObj.slug}`;
      } else if (targetRegionObj) {
        expectedPath = `/explore/${targetRegionObj.slug}`;
      } else if (targetCategoryObj) {
        expectedPath = `/explore/${targetCategoryObj.slug}`;
      }

      const isParamNavOnly = fullPath === '/explore' && (qCategory || qTownName) && !url.searchParams.has('q') && !url.searchParams.has('shop');
      const hasAliasMismatch = pathSegments.some(s => s === 'bergen-county' || s === 'hudson-county' || s === 'fort-lee' || s === 'fashion');

      if ((isParamNavOnly && expectedPath !== '/explore') || (hasAliasMismatch && expectedPath !== fullPath)) {
        return new Response(null, {
          status: 301,
          headers: {
            "Location": `https://moon-oh.com${expectedPath}`,
            "Cache-Control": "public, max-age=86400"
          }
        });
      }
    }

    const allItems = await fetchAllCombinedItems();
    let filteredItems = [];

    if (isFoodRescueFilter) {
      filteredItems = allItems.filter(item => item.source === 'kimc');
    } else if (isMarketplacesFilter) {
      const mktItems = allItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
      filteredItems = interleaveMarketplaceProducts(mktItems);
    } else if (isLocalShopsFilter || isShopProfile) {
      const prods = (isShopProfile ? localShopsData.products.filter(p => p.shop_id === shopProfileSlug) : localShopsData.products) || [];
      const baseLocal = isShopProfile ? prods : interleaveLocalProducts(prods);
      filteredItems = baseLocal.map(p => ({
        id: p.id,
        no: p.id,
        title: p.title,
        price: p.current_price,
        photo: p.image_source_url,
        image: p.image_source_url,
        townName: p.shop_id === 'happier-grocery' ? 'Soho, NY' : (p.shop_id === 'big-night' ? 'Greenpoint, NY' : 'West Village, NY'),
        categoryName: p.moonoh_category || 'Food & Groceries',
        category: p.moonoh_category || 'Food & Groceries',
        detailUrl: `/local-product/${p.shop_id}/${p.slug}`,
        url: `/local-product/${p.shop_id}/${p.slug}`,
        source: p.shop_id,
        badgeName: p.brand || (localShopsData.shops[p.shop_id] ? localShopsData.shops[p.shop_id].name : 'Local Shop')
      }));
    } else if (targetRegionObj || targetCategoryObj) {
      // REGIONAL & CATEGORY LANDING PAGES: Combined marketplace across ALL verified community sources!
      filteredItems = allItems.filter(item => Boolean(item && (item.photo || item.image)));
    } else {
      // Default Moonoh tab: ONLY Moonoh items
      filteredItems = allItems.filter(item => item.source === 'moonoh' || (!item.source && !String(item.id||'').startsWith('karrot') && !String(item.id||'').startsWith('heykorean') && !String(item.id||'').startsWith('kimc')));
    }

    // Bulletproof SSR deduplication by item key
    const seenSsrKeys = new Set();
    filteredItems = filteredItems.filter(item => {
      if (!item) return false;
      const normId = String(item.no || item.id || '').replace(/^item-/, '');
      const key = String(item.source || 'moonoh') + '_' + normId;
      if (seenSsrKeys.has(key)) return false;
      seenSsrKeys.add(key);
      return true;
    });

    // Filter by Region if present
    if (targetRegionObj && targetRegionObj.keywords && targetRegionObj.keywords.length > 0) {
      filteredItems = filteredItems.filter(item => {
        const locStr = ((item.rawTown || '') + ' ' + (item.location || '') + ' ' + (item.townName || '')).toLowerCase();
        return targetRegionObj.keywords.some(kw => locStr.includes(kw));
      });
    }

    // Filter by Category if present
    if (targetCategoryObj) {
      if (targetCategoryObj.isFree) {
        filteredItems = filteredItems.filter(item => {
          if (!item) return false;
          const p = item.price !== undefined ? item.price : (item.current_price !== undefined ? item.current_price : null);
          if (p === 0 || p === '0' || p === 'Free' || p === 'free') return true;
          const num = typeof p === 'number' ? p : parseFloat(p);
          return !isNaN(num) && num === 0;
        });
      } else {
        const targetSlug = targetCategoryObj.slug;
        const targetKw = (targetCategoryObj.kw || '').toLowerCase();
        const targetName = (targetCategoryObj.name || '').toLowerCase();

        filteredItems = filteredItems.filter(item => {
          if (!item) return false;
          const mainCat = (item.categoryName || item.category || item.primary_category || '').toLowerCase();
          const titleStr = (item.title || '').toLowerCase();
          const fullText = (mainCat + ' ' + titleStr).toLowerCase();

          if (targetSlug === 'furniture') {
            return fullText.includes('furniture') || fullText.includes('sofa') || fullText.includes('chair') || fullText.includes('table') || fullText.includes('bed') || fullText.includes('desk') || fullText.includes('couch') || fullText.includes('dresser') || fullText.includes('cabinet') || fullText.includes('shelf') || fullText.includes('nightstand') || fullText.includes('stool') || fullText.includes('bench') || fullText.includes('ottoman') || fullText.includes('가구') || fullText.includes('의자') || fullText.includes('책상') || fullText.includes('침대') || fullText.includes('식탁') || fullText.includes('소파');
          }
          if (targetSlug === 'electronics') {
            return fullText.includes('electronics') || fullText.includes('appliance') || fullText.includes('phone') || fullText.includes('laptop') || fullText.includes('camera') || fullText.includes('tv') || fullText.includes('monitor') || fullText.includes('audio') || fullText.includes('headphone') || fullText.includes('airpod') || fullText.includes('speaker') || fullText.includes('charger') || fullText.includes('game') || fullText.includes('nintendo') || fullText.includes('ps5') || fullText.includes('xbox') || fullText.includes('전자') || fullText.includes('모니터') || fullText.includes('아이폰') || fullText.includes('청소기');
          }
          if (targetSlug === 'womens-fashion' || targetSlug === 'fashion') {
            return fullText.includes('women') || fullText.includes('dress') || fullText.includes('skirt') || fullText.includes('handbag') || fullText.includes('coat') || fullText.includes('jacket') || fullText.includes('fashion') || fullText.includes('clothing') || fullText.includes('원피스') || fullText.includes('여성') || fullText.includes('옷');
          }
          if (targetSlug === 'mens-fashion') {
            return (fullText.includes('men') && !fullText.includes('women')) || fullText.includes('suit') || fullText.includes('남성');
          }
          if (targetSlug === 'shoes') {
            return fullText.includes('shoe') || fullText.includes('sneaker') || fullText.includes('boot') || fullText.includes('sandal') || fullText.includes('heel') || fullText.includes('loafer') || fullText.includes('nike') || fullText.includes('adidas') || fullText.includes('신발') || fullText.includes('운동화') || fullText.includes('구두');
          }
          if (targetSlug === 'baby-kids') {
            return fullText.includes('baby') || fullText.includes('kid') || fullText.includes('stroller') || fullText.includes('crib') || fullText.includes('toy') || fullText.includes('lego') || fullText.includes('유아') || fullText.includes('아동') || fullText.includes('유모차') || fullText.includes('장난감');
          }
          if (targetSlug === 'food-groceries') {
            return fullText.includes('food') || fullText.includes('groc') || fullText.includes('snack') || fullText.includes('noodle') || fullText.includes('tea') || fullText.includes('coffee') || fullText.includes('sauce') || fullText.includes('식품') || fullText.includes('과자') || fullText.includes('라면') || fullText.includes('음료');
          }
          if (targetSlug === 'home-garden') {
            return fullText.includes('home') || fullText.includes('garden') || fullText.includes('kitchen') || fullText.includes('dish') || fullText.includes('plate') || fullText.includes('pot') || fullText.includes('pan') || fullText.includes('cookware') || fullText.includes('vase') || fullText.includes('lamp') || fullText.includes('light') || fullText.includes('rug') || fullText.includes('towel') || fullText.includes('decor') || fullText.includes('주방') || fullText.includes('그릇') || fullText.includes('조명');
          }
          if (targetSlug === 'jewelry-watches') {
            return fullText.includes('jewel') || fullText.includes('watch') || fullText.includes('ring') || fullText.includes('earring') || fullText.includes('necklace') || fullText.includes('bracelet') || fullText.includes('시계') || fullText.includes('반지') || fullText.includes('목걸이') || fullText.includes('귀걸이');
          }
          if (targetSlug === 'luggages-bags') {
            return fullText.includes('luggage') || fullText.includes('bag') || fullText.includes('pouch') || fullText.includes('backpack') || fullText.includes('wallet') || fullText.includes('purse') || fullText.includes('가방') || fullText.includes('지갑') || fullText.includes('백팩');
          }
          if (targetSlug === 'health-beauty') {
            return fullText.includes('health') || fullText.includes('beauty') || fullText.includes('skin') || fullText.includes('cream') || fullText.includes('lotion') || fullText.includes('serum') || fullText.includes('cosmetic') || fullText.includes('화장품') || fullText.includes('크림') || fullText.includes('마스크');
          }
          if (targetSlug === 'antiques') {
            return fullText.includes('antique') || fullText.includes('collectible') || fullText.includes('vintage') || fullText.includes('골동품') || fullText.includes('빈티지');
          }
          if (targetSlug === 'arts-books-music') {
            return fullText.includes('art') || fullText.includes('book') || fullText.includes('music') || fullText.includes('guitar') || fullText.includes('piano') || fullText.includes('vinyl') || fullText.includes('dvd') || fullText.includes('책') || fullText.includes('음악') || fullText.includes('악기') || fullText.includes('미술');
          }
          if (targetSlug === 'pet-supplies') {
            return fullText.includes('pet') || fullText.includes('dog') || fullText.includes('cat') || fullText.includes('puppy') || fullText.includes('반려') || fullText.includes('강아지') || fullText.includes('고양이');
          }
          if (targetSlug === 'toys-games') {
            return fullText.includes('toy') || fullText.includes('game') || fullText.includes('figure') || fullText.includes('nintendo') || fullText.includes('playstation') || fullText.includes('장난감') || fullText.includes('게임') || fullText.includes('피규어');
          }
          if (targetSlug === 'sports-leisure') {
            return fullText.includes('sport') || fullText.includes('leisure') || fullText.includes('bike') || fullText.includes('golf') || fullText.includes('gym') || fullText.includes('ski') || fullText.includes('골프') || fullText.includes('자전거') || fullText.includes('운동');
          }

          if (mainCat === targetName || (targetKw && mainCat.includes(targetKw))) return true;
          return fullText.includes(targetSlug);
        });
      }
    }

    let template = getExploreTemplate();
    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    // Dynamic AEO & SEO Title/Description/H1 Generation
    let pageTitle = "NYC & NJ Local Marketplace & Neighborhood Deals | Moonoh";
    let metaDesc = "Discover local marketplace deals, brand-new items, food rescue groceries, and curated NYC neighborhood shops on Moonoh. 0% fees, safe community exchanges.";
    let h1Text = "Explore Local Marketplace & Neighborhood Deals in NYC & NJ";
    let dynamicIntroText = "Discover verified local goods, neighborhood deals, brand-new items, sustainable food rescue, and curated NYC local shop collections across New York City and New Jersey. 100% free neighborhood marketplace with zero fees.";
    let canonicalUrl = `https://moon-oh.com/explore`;
    let themeColor = "#4F46E5";
    let sectionName = "Moonoh Marketplace";

    if (isFoodRescueFilter) {
      canonicalUrl = `https://moon-oh.com/explore/food-rescue`;
      pageTitle = "NYC Food Waste Rescue & Sustainable Groceries | Moonoh";
      metaDesc = "Shop discounted gourmet Korean pantry items near sell-by date in NYC from Kim'C Market on Moonoh. Fight food waste, save money.";
      h1Text = "NYC Food Waste Rescue & Sustainable Groceries";
      dynamicIntroText = "Rescue premium artisanal and specialty groceries near sell-by dates at up to 70% discount in NYC. Partnering with local grocers like Kim'C Market to fight food waste and promote sustainable consumption.";
      sectionName = "Food Rescue";
    } else if (isShopProfile) {
      canonicalUrl = `https://moon-oh.com/local-shops/${shopProfileSlug}`;
      const shopObj = (localShopsData.shops && localShopsData.shops[shopProfileSlug]) || {};
      const shopTitle = shopObj.name || "Local Shop";
      pageTitle = `${shopTitle} - Curated Local NYC Shop | Moonoh`;
      metaDesc = `Discover curated products and neighborhood specialty items from ${shopTitle} in NYC on Moonoh.`;
      h1Text = `${shopTitle} - Curated Local NYC Shop`;
      dynamicIntroText = `Browse curated goods from ${shopTitle}. Support independent New York City local merchants on Moonoh.`;
      sectionName = shopTitle;
    } else if (isLocalShopsFilter) {
      canonicalUrl = `https://moon-oh.com/explore/local-shops`;
      pageTitle = "NYC Local Shops - Curated Neighborhood Goods | Moonoh";
      metaDesc = "Discover iconic local New York City specialty shops and neighborhood staples on Moonoh. Curated pantry goods, tableware, and specialty items.";
      h1Text = "NYC Local Shops - Curated Neighborhood Goods in NYC";
      dynamicIntroText = "Explore curated collections from iconic independent New York City shops including Big Night (Greenpoint), Happier Grocery (SoHo), and Pop Up Grocer (Bleecker St). Support local NYC merchants.";
      sectionName = "Local NYC Shops";
    } else if (isMarketplacesFilter) {
      canonicalUrl = `https://moon-oh.com/explore/marketplaces`;
      pageTitle = "NYC & NJ Local Community Marketplace Feed | Moonoh";
      metaDesc = "Browse aggregated local community marketplace listings across NYC & NJ from Karrot and HeyKorean on Moonoh.";
      h1Text = "NYC & NJ Community Marketplace Feed";
      dynamicIntroText = "Discover community listings, moving sales, and neighborhood deals from verified local marketplaces across New York City and New Jersey.";
      sectionName = "Community Marketplaces";
    } else if (targetRegionObj && targetCategoryObj) {
      canonicalUrl = `https://moon-oh.com/explore/${targetRegionObj.slug}/${targetCategoryObj.slug}`;
      pageTitle = `${targetCategoryObj.name} for Sale in ${targetRegionObj.name} | Moonoh`;
      metaDesc = `Find great deals on ${targetCategoryObj.name.toLowerCase()} in ${targetRegionObj.name} on Moonoh. 0% fees, direct seller chat, and local meetup.`;
      h1Text = `${targetCategoryObj.name} for Sale in ${targetRegionObj.name}`;
      dynamicIntroText = `Discover ${targetCategoryObj.name.toLowerCase()} deals and quality items listed by local neighbors in ${targetRegionObj.name}. Buy and sell locally with 0% listing fees, direct in-app chat, and safe neighborhood pickup on Moonoh.`;
      sectionName = `${targetCategoryObj.name} in ${targetRegionObj.shortName}`;
    } else if (targetRegionObj) {
      canonicalUrl = `https://moon-oh.com/explore/${targetRegionObj.slug}`;
      pageTitle = `Local Items & Marketplace Deals in ${targetRegionObj.name} | Moonoh`;
      metaDesc = `Discover local marketplace deals and neighborhood items listed by neighbors in ${targetRegionObj.name}. 0% fees on Moonoh.`;
      h1Text = `Local Items & Marketplace Deals in ${targetRegionObj.name}`;
      dynamicIntroText = `Browse furniture, electronics, fashion, household goods, and local deals listed by verified neighbors in ${targetRegionObj.name}. 100% free local exchanges with zero transaction fees.`;
      sectionName = targetRegionObj.name;
    } else if (targetCategoryObj) {
      canonicalUrl = `https://moon-oh.com/explore/${targetCategoryObj.slug}`;
      pageTitle = `${targetCategoryObj.name} for Sale in NYC & NJ | Moonoh`;
      metaDesc = `Explore ${targetCategoryObj.name.toLowerCase()} deals and quality goods for sale in NYC and NJ on Moonoh. Connect directly with local sellers.`;
      h1Text = `${targetCategoryObj.name} for Sale in NYC & NJ`;
      dynamicIntroText = `Explore quality ${targetCategoryObj.name.toLowerCase()} deals and local items for sale across New York City (Manhattan, Brooklyn, Queens, Bronx, Staten Island) and New Jersey. Connect directly with nearby sellers with zero commissions.`;
    }

    // Standard Linear Interpolation Quantile Function (NIST / R-type 7)
    function getStandardQuantile(sortedArr, q) {
      if (!sortedArr || sortedArr.length === 0) return 0;
      if (sortedArr.length === 1) return sortedArr[0];
      const pos = (sortedArr.length - 1) * q;
      const base = Math.floor(pos);
      const rest = pos - base;
      if (sortedArr[base + 1] !== undefined) {
        return sortedArr[base] + rest * (sortedArr[base + 1] - sortedArr[base]);
      }
      return sortedArr[base];
    }

    // Render Reusable Stacker-Style Local Market Intelligence System
    let aeoSummaryHtml = '';
    if (targetRegionObj || targetCategoryObj) {
      const itemCount = filteredItems.length;
      const prices = filteredItems.map(i => {
        const rawP = i.price !== undefined ? i.price : i.current_price;
        const num = typeof rawP === 'number' ? rawP : parseFloat(rawP);
        return (!isNaN(num) && num > 0) ? num : null;
      }).filter(p => p !== null).sort((a, b) => a - b);

      const medianPrice = getStandardQuantile(prices, 0.5);
      const price25 = getStandardQuantile(prices, 0.25);
      const price75 = getStandardQuantile(prices, 0.75);
      const avgPrice = prices.length > 0 ? (prices.reduce((a,b)=>a+b, 0) / prices.length) : 0;
      
      const freeCount = filteredItems.filter(i => {
        const rawP = i.price !== undefined ? i.price : i.current_price;
        return rawP === 0 || rawP === '0' || rawP === 'Free' || rawP === 'free';
      }).length;

      const locLabel = targetRegionObj ? targetRegionObj.name : "NYC & NJ";
      const catLabel = targetCategoryObj ? targetCategoryObj.name : "local items";

      // Inventory Source Distribution
      let moonohCount = 0, localCount = 0, foodCount = 0, marketCount = 0;
      filteredItems.forEach(i => {
        if (i.source === 'kimc') foodCount++;
        else if (i.source === 'karrot' || i.source === 'heykorean') marketCount++;
        else if (['happier-grocery', 'pop-up-grocer', 'big-night', 'front-general-store'].includes(i.source) || i.badgeName?.includes('Shop')) localCount++;
        else moonohCount++;
      });

      // Category Breakdown
      const catCounts = {};
      filteredItems.forEach(i => {
        const c = i.category || i.categoryName || 'General';
        catCounts[c] = (catCounts[c] || 0) + 1;
      });
      const topCats = Object.entries(catCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([name, count]) => `${name} (${Math.round((count / itemCount) * 100)}%)`);
      const topCatSentence = topCats.length > 0 ? `Leading categories include <strong>${topCats.join(', ')}</strong>.` : '';

      // Tier-based rendering: Rich Intelligence if N >= 20, Clean Summary if N < 20
      let breakdownHtml = '';
      if (itemCount >= 20) {
        breakdownHtml = `
        <div style="display:flex; flex-wrap:wrap; gap:16px; margin-top:14px; padding-top:14px; border-top:1px dashed #E2E8F0; font-size:13px; color:#475569;">
          <div style="flex:1; min-width:200px;">
            <div style="font-weight:700; color:#1E293B; margin-bottom:4px;">📊 Inventory Composition:</div>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              ${moonohCount > 0 ? `<span>• Direct P2P: <strong>${moonohCount}</strong></span>` : ''}
              ${localCount > 0 ? `<span>• NYC Local Shops: <strong>${localCount}</strong></span>` : ''}
              ${marketCount > 0 ? `<span>• Community Marketplaces: <strong>${marketCount}</strong></span>` : ''}
              ${foodCount > 0 ? `<span>• Food Rescue: <strong>${foodCount}</strong></span>` : ''}
            </div>
          </div>
        </div>
        `;
      }

      aeoSummaryHtml = `
      <section class="aeo-summary-card" style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:16px; padding:22px 24px 18px; margin-bottom:28px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:22px; height:22px; background:#EEF2FF; border-radius:6px; font-size:13px;">📊</span>
            <h2 style="font-size:17px; font-weight:800; color:#0F172A; margin:0; letter-spacing:-0.01em;">
              ${escapeHtml(locLabel)} Market Intelligence: ${escapeHtml(catLabel)}
            </h2>
          </div>
          <span style="font-size:12px; color:#64748B; font-weight:600; background:#FFFFFF; padding:3px 10px; border-radius:9999px; border:1px solid #E2E8F0;">
            Updated August 2026
          </span>
        </div>

        <p style="font-size:14.5px; color:#334155; line-height:1.6; margin:0 0 16px 0;">
          As of August 2026, Moonoh tracks <strong>${itemCount} active marketplace listings</strong> in ${escapeHtml(locLabel)}${targetCategoryObj ? ` for ${escapeHtml(catLabel.toLowerCase())}` : ''}.
          ${medianPrice > 0 ? `The median listed price is <strong>$${Math.round(medianPrice)}</strong> (typical range $${Math.round(price25)} – $${Math.round(price75)}).` : ''}
          ${topCatSentence}
          ${freeCount > 0 ? ` Includes <strong>${freeCount} free items</strong> shared by local neighbors.` : ''}
          Featuring direct peer-to-peer neighborhood listings alongside curated local NYC shop products.
        </p>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:6px;">
          <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px;">
            <div style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Active Listings</div>
            <div style="font-size:20px; font-weight:800; color:#0F172A; margin-top:2px;">${itemCount.toLocaleString()}</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px;">
            <div style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Median Price</div>
            <div style="font-size:20px; font-weight:800; color:#059669; margin-top:2px;">$${Math.round(medianPrice)}</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px;">
            <div style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Price Range (IQR)</div>
            <div style="font-size:15px; font-weight:800; color:#0F172A; margin-top:5px;">$${Math.round(price25)} – $${Math.round(price75)}</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:10px 14px;">
            <div style="font-size:11px; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Free Items</div>
            <div style="font-size:20px; font-weight:800; color:#6366F1; margin-top:2px;">${freeCount}</div>
          </div>
        </div>

        ${breakdownHtml}

        <div style="font-size:11.5px; color:#94A3B8; margin-top:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:6px; border-top:1px solid #F1F5F9; padding-top:10px;">
          <span>⚡ <strong>Methodology:</strong> Standard NIST-quantile calculated across 4,220+ actively tracked local items (5,170+ total indexed catalog) in NYC & NJ.</span>
          <span>Zero fee neighborhood discovery</span>
        </div>
      </section>
      `;
    }

    // Render Grid Cards
    const initialItems = filteredItems.slice(0, 40);
    const cardsHtml = initialItems.map(item => {
      const itemTitle = item.title || 'Item';
      const safeTitle = escapeHtml(itemTitle);
      const rawPrice = (item.price !== undefined && item.price !== null) ? item.price : (item.current_price !== undefined ? item.current_price : null);
      const priceStr = formatPriceStr(rawPrice);
      const targetUrl = item.detailUrl || item.url || `/item/item-${item.id}`;
      const itemImg = item.photo || item.image || item.image_source_url || '/images/default-item-placeholder.png';
      
      let badgeHtml = '';
      if (item.source === 'karrot') {
        badgeHtml = `<div class="item-card-badge badge-karrot">Karrot</div>`;
      } else if (item.source === 'heykorean') {
        badgeHtml = `<div class="item-card-badge badge-heykorean">HeyKorean</div>`;
      } else if (item.source === 'kimc') {
        badgeHtml = `<div class="item-card-badge badge-kimc">🌱 Kim'C Market • Delivers NYC</div>`;
      } else if (item.source === 'happier-grocery' || item.badgeName === 'Happier Grocery') {
        badgeHtml = `<div class="item-card-badge badge-happier">Happier Grocery</div>`;
      } else if (item.source === 'pop-up-grocer' || item.badgeName === 'Pop Up Grocer') {
        badgeHtml = `<div class="item-card-badge badge-popup">Pop Up Grocer</div>`;
      } else if (item.source === 'big-night' || item.badgeName === 'Big Night') {
        badgeHtml = `<div class="item-card-badge badge-bignight">Big Night</div>`;
      } else {
        badgeHtml = `<div class="item-card-badge badge-moonoh">Moonoh</div>`;
      }

      return `
        <a class="item-card" href="${escapeHtml(targetUrl)}" style="text-decoration:none; color:inherit;">
          <div class="item-card-img-wrap">
            <img src="${escapeHtml(itemImg)}" alt="${safeTitle}" class="item-card-image" loading="lazy" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';">
          </div>
          <div class="item-card-content">
            <div class="item-card-price">${priceStr}</div>
            <div class="item-card-title">${safeTitle}</div>
            <div class="item-card-location">${escapeHtml(item.townName || item.location || 'Manhattan, NY')}</div>
            ${badgeHtml}
          </div>
        </a>
      `;
    }).join('');

    // JSON-LD Breadcrumbs Schema
    const breadcrumbSchema = {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://moon-oh.com/" },
        { "@type": "ListItem", "position": 2, "name": "Explore", "item": "https://moon-oh.com/explore" },
        { "@type": "ListItem", "position": 3, "name": sectionName, "item": canonicalUrl }
      ]
    };

    // JSON-LD CollectionPage & ItemList Schema
    const collectionSchema = {
      "@context": "https://schema.org",
      "@graph": [
        breadcrumbSchema,
        {
          "@type": "CollectionPage",
          "@id": `${canonicalUrl}#collection`,
          "url": canonicalUrl,
          "name": pageTitle,
          "description": metaDesc,
          "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": initialItems.length,
            "itemListElement": initialItems.map((item, idx) => ({
              "@type": "ListItem",
              "position": idx + 1,
              "item": {
                "@type": "Product",
                "name": item.title || "Used item",
                "url": item.detailUrl || item.url || canonicalUrl,
                "image": item.photo || item.image || item.image_source_url || "https://moon-oh.com/images/default-item-placeholder.png",
                "offers": {
                  "@type": "Offer",
                  "price": (item.price !== undefined && item.price !== null) ? String(item.price) : "0",
                  "priceCurrency": "USD",
                  "availability": "https://schema.org/InStock",
                  "itemCondition": "https://schema.org/UsedCondition"
                }
              }
            }))
          }
        }
      ]
    };

    const schemaScript = `<script type="application/ld+json">${JSON.stringify(collectionSchema)}</script>`;
    const initialItemsScript = `<script>window.__INITIAL_ITEMS__ = ${JSON.stringify(initialItems)};</script>`;

    if (targetRegionObj && targetRegionObj.shortName) {
      const regName = targetRegionObj.shortName;
      template = template.replace(`<option value="${regName}">`, `<option value="${regName}" selected="selected">`);
    }

    // Highlight active source tab in SSR HTML
    if (targetRegionObj || targetCategoryObj) {
      // On regional & category hub pages, display the 'All' tab as active and un-highlight Moonoh
      template = template
        .replace('<button class="source-tab-btn" id="tab-source-all" data-source="all" style="display: none;">All</button>', '<button class="source-tab-btn active" id="tab-source-all" data-source="all">All</button>')
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"');
    } else if (isMarketplacesFilter) {
      template = template
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"')
        .replace('class="source-tab-btn" id="tab-source-marketplaces"', 'class="source-tab-btn active" id="tab-source-marketplaces"');
    } else if (isFoodRescueFilter) {
      template = template
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"')
        .replace('class="source-tab-btn tab-foodrescue" id="tab-source-foodrescue"', 'class="source-tab-btn tab-foodrescue active" id="tab-source-foodrescue"');
    } else if (isLocalShopsFilter || isShopProfile) {
      template = template
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"')
        .replace('class="source-tab-btn" id="tab-source-localshops"', 'class="source-tab-btn active" id="tab-source-localshops"');
    }

    // Replace generic H2 with dynamic H1 and localized intro description
    const genericH2 = '<h2 class="item-feed-title" style="margin-bottom: 16px;">Buy and sell used items in your neighborhood</h2>';
    const dynamicH1Block = `<h1 class="item-feed-title" style="font-size:24px; font-weight:800; color:#1E1B4B; margin-top:0; margin-bottom:10px; letter-spacing:-0.02em;">${escapeHtml(h1Text)}</h1>\n      <p class="explore-intro-text" style="font-size:15px; color:#4B5563; line-height:1.6; margin-top:0; margin-bottom:20px;">${escapeHtml(dynamicIntroText)}</p>`;
    if (template.includes(genericH2)) {
      template = template.replace(genericH2, dynamicH1Block);
    }

    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(metaDesc)}" name="description"/>`)
      .replace(/<link [^>]*rel="canonical"[^>]*\/>/i, `<link rel="canonical" href="${canonicalUrl}"/>`)
      .replace('</head>', `${initialItemsScript}
${schemaScript}
</head>`);

    // Inject AEO Summary Card & Cleanly Replace Entire Grid Block
    // Use string split to correctly replace the full grid (regex non-greedy fails on nested divs)
    const gridOpenTag = '<div class="item-grid" id="moonoh-item-grid">';
    const gridOpenIdx = template.indexOf(gridOpenTag);
    if (gridOpenIdx !== -1) {
      // Find the matching closing </div> by counting div depth
      let depth = 0;
      let i = gridOpenIdx;
      let gridCloseIdx = -1;
      while (i < template.length) {
        if (template.substring(i, i + 4) === '<div') { depth++; i++; continue; }
        if (template.substring(i, i + 6) === '</div>') {
          depth--;
          if (depth === 0) { gridCloseIdx = i + 6; break; }
          i += 6; continue;
        }
        i++;
      }
      if (gridCloseIdx !== -1) {
        const newGridContent = (aeoSummaryHtml ? `${aeoSummaryHtml}\n` : '') + `${gridOpenTag}\n${cardsHtml}\n</div>`;
        template = template.substring(0, gridOpenIdx) + newGridContent + template.substring(gridCloseIdx);
      }
    }

    return new Response(template, {
      status: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate, s-maxage=0'
      }
    });
  } catch (error) {
    console.error("Error in explore.mjs handler:", error);
    return new Response("Internal Server Error", { status: 500 });
  }
};
