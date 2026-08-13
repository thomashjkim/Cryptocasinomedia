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
  'new-york-area': { name: 'New York Area', shortName: '', keywords: [] },
  'manhattan': { name: 'Manhattan, NY', shortName: 'Manhattan', keywords: ['manhattan', 'upper east', 'upper west', 'downtown manhattan', 'midtown', 'harlem', 'tribeca', 'soho', 'lower east', 'east village', 'west village', 'chelsea', 'gramercy', 'inwood', 'washington heights', 'morningside', 'financial district', 'wall street', 'murray hill', 'kips bay', 'flatiron', 'new york'] },
  'queens': { name: 'Queens, NY', shortName: 'Queens', keywords: ['queens', 'bayside', 'flushing', 'astoria', 'jamaica', 'forest hills', 'jackson heights', 'woodside', 'ridgewood', 'ozone park', 'fresh meadows', 'corona', 'elmhurst', 'sunnyside', 'long island city', 'rego park', 'maspeth', 'howard beach', 'far rockaway', 'college point', 'whitestone', 'douglaston'] },
  'brooklyn': { name: 'Brooklyn, NY', shortName: 'Brooklyn', keywords: ['brooklyn', 'park slope', 'williamsburg', 'bushwick', 'bed stuy', 'flatbush', 'crown heights', 'bay ridge', 'bensonhurst', 'canarsie', 'east new york', 'greenpoint', 'cobble hill', 'carroll gardens', 'boerum', 'sunset park', 'borough park', 'brighton beach', 'coney island', 'sheepshead', 'ditmas'] },
  'bronx': { name: 'The Bronx, NY', shortName: 'Bronx', keywords: ['bronx'] },
  'staten-island': { name: 'Staten Island, NY', shortName: 'Staten Island', keywords: ['staten island'] },
  'flushing': { name: 'Flushing, Queens, NY', shortName: 'Flushing', keywords: ['flushing'] },
  'bayside': { name: 'Bayside, Queens, NY', shortName: 'Bayside', keywords: ['bayside'] },
  'astoria': { name: 'Astoria, Queens, NY', shortName: 'Astoria', keywords: ['astoria', 'long island city', 'lic'] },
  'fort-lee-nj': { name: 'Fort Lee, NJ', shortName: 'Fort Lee', keywords: ['fort lee', 'fortlee', 'palisades park', 'palisades', 'leonia', 'cliffside park', 'edgewater', 'fort-lee', 'bergen'] },
  'fort-lee': { name: 'Fort Lee, NJ', shortName: 'Fort Lee', keywords: ['fort lee', 'fortlee', 'palisades park', 'palisades', 'leonia', 'cliffside park', 'edgewater', 'fort-lee', 'bergen'] },
  'bergen-county-nj': { name: 'Bergen County, NJ', shortName: 'Bergen', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'bergen-county': { name: 'Bergen County, NJ', shortName: 'Bergen', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'hudson-county-nj': { name: 'Hudson County, NJ', shortName: 'Hudson', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] },
  'hudson-county': { name: 'Hudson County, NJ', shortName: 'Hudson', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] }
};

// Category Mapping
const CATEGORIES = {
  'electronics': { name: 'Electronics', kw: 'electronics', keywords: ['electronics', 'phone', 'laptop', 'appliances', 'audio', 'gadget', 'ink', 'camera', 'tv', 'monitor', 'headphone', 'airpods', 'ipad', 'charger', 'speaker', 'printer', 'game', 'ps5', 'nintendo', 'xbox'] },
  'furniture': { name: 'Furniture', kw: 'furniture', keywords: ['furniture', 'sofa', 'table', 'chair', 'bed', 'desk', 'couch', 'dresser', 'mattress', 'shelf', 'nightstand', 'cabinet', 'stool', 'bench', 'ottoman', 'headboard', 'drawers', '소파', '침대', '식탁', '의자', '책상', '서랍', '매트리스', '선반', '테이블', '가구'], excludes: ['pillow', 'hanger', 'curtain rod', 'fan', 'keyboard', 'monitor', 'massager', 'phone stand', 'photo printer', 'gymnastic', 'printer'] },
  'womens-fashion': { name: "Women's Fashion", kw: 'women', keywords: ["women's fashion", 'women', 'dress', 'handbag', 'skirt', 'coat'] },
  'mens-fashion': { name: "Men's Fashion", kw: 'men', keywords: ["men's fashion", 'men', 'suit', 'jacket'] },
  'shoes': { name: 'Shoes', kw: 'shoe', keywords: ['shoes', 'sneakers', 'boots', 'sandals', 'shoe', 'nike', 'adidas'] },
  'home-garden': { name: 'Home & Garden', kw: 'home', keywords: ['home, garden & diy', 'home', 'garden', 'kitchen', 'utensil', 'decor'] },
  'health-beauty': { name: 'Health & Beauty', kw: 'health', keywords: ['health', 'beauty', 'cosmetics'] },
  'pet-supplies': { name: 'Pet Supplies', kw: 'pet', keywords: ['pet', 'dog', 'cat'] },
  'baby-kids': { name: 'Baby & Kids', kw: 'baby', keywords: ['baby & kids', 'baby', 'kids', 'stroller', 'toy'] },
  'sports-leisure': { name: 'Sports & Leisure', kw: 'sport', keywords: ['sports', 'leisure', 'bike', 'ski', 'exercise'] },
  'toys-games': { name: 'Toys & Games', kw: 'toy', keywords: ['toys', 'games', 'card', 'figure'] },
  'jewelry-watches': { name: 'Jewelry & Watches', kw: 'jewelry', keywords: ['jewelry', 'watches', 'ring', 'earrings', 'watch'] },
  'luggages-bags': { name: 'Luggages & Bags', kw: 'bag', keywords: ['luggages', 'bags', 'pouch', 'backpack', 'tote', 'wallet', 'bag'] },
  'antiques': { name: 'Antiques', kw: 'antique', keywords: ['antiques', 'vintage', 'collectible'] },
  'arts-books-music': { name: 'Arts, Books & Music', kw: 'art', keywords: ['arts', 'books', 'music', 'book', 'print'] },
  'food-groceries': { name: 'Food & Groceries', kw: 'food', keywords: ['food', 'groceries', 'snack', 'sauce', 'oil', 'rice', 'tea', 'noodle', 'kimchi', 'pantry', 'drink', 'beverage', 'korean food', 'cookie', 'juice', 'chip'] },
  'free': { name: 'Free Items', kw: 'free', isFree: true, keywords: ['free'] },
  'other': { name: 'Other', kw: 'other', keywords: ['other', 'general'] }
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
      townName: raw.townName || raw.location || 'NYC, NY',
      rawTown: raw.rawTown || raw.location || '',
      location: raw.location || 'NYC, NY',
      categoryName: raw.categoryName || raw.category || 'General',
      category: raw.categoryName || raw.category || 'General',
      detailUrl: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
      url: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
      source: 'moonoh',
      postedAt: Date.now() - idx * 1800000
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
      localItems = localShopsData.products.map((p, idx) => ({
        id: p.id,
        no: p.id,
        title: p.title,
        price: p.current_price,
        photo: p.image_source_url,
        image: p.image_source_url,
        townName: p.shop_id === 'happier-grocery' ? 'Soho, NY' : (p.shop_id === 'big-night' ? 'Greenpoint, NY' : 'West Village, NY'),
        rawTown: p.shop_id === 'happier-grocery' ? 'Soho, NY' : (p.shop_id === 'big-night' ? 'Greenpoint, NY' : 'West Village, NY'),
        location: p.shop_id === 'happier-grocery' ? 'Soho, NY' : (p.shop_id === 'big-night' ? 'Greenpoint, NY' : 'West Village, NY'),
        categoryName: p.moonoh_category || 'Food & Groceries',
        category: p.moonoh_category || 'Food & Groceries',
        detailUrl: `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`,
        url: `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`,
        source: p.shop_id,
        badgeName: p.brand || (localShopsData.shops[p.shop_id] ? localShopsData.shops[p.shop_id].name : 'Local Shop'),
        postedAt: p.last_checked_at ? new Date(p.last_checked_at).getTime() - (idx * 1500000) : (Date.now() - idx * 1500000)
      }));
    }

    cachedCombinedItems = [...moonohItems, ...externalItems, ...foodRescueItems, ...localItems];
    // Sort all combined items by original posting timestamp (recency order)
    cachedCombinedItems.sort((a, b) => (b.postedAt || 0) - (a.postedAt || 0));
    
    lastFetchTime = now;
    return cachedCombinedItems;
  } catch (e) {
    console.error("Error in fetchAllCombinedItems:", e);
    return cachedCombinedItems || [];
  }
}

function inferCategoryFromText(title = '', description = '', rawCategory = '') {
  const text = (title + ' ' + (description || '')).toLowerCase();

  // 1. Electronics & Appliances
  if (/\b(macbook|imac|laptop|computer|monitor|iphone|galaxy|ipad|nintendo|ps5|xbox|tv|television|camera|printer|scanner|radiator|heater|aircon|air conditioner|air fryer|microwave|vacuum|refrigerator|fridge|coffee machine|nespresso|keurig|blender|cooker|calculator|keyboard|ram memory|router|headphone|airpods|speaker|bluetooth)\b|노트북|컴퓨터|모니터|아이폰|아이패드|에어컨|선풍기|히터|히타|청소기|스피커|전자레인지|변압기|디바이스|스페이스히터|훼이셜머신|부루스타|김치냉장고|김치 냉장고|냉장고|와인냉장고|와인셀러/i.test(text)) {
    return 'Electronics & appliances';
  }

  // 2. Sports & Leisure
  if (/\b(ski|snowboard|bmx|bike|bicycle|golf|putter|vokey|driver|treadmill|exercise|dumbbell|sled|inversion table|racket|tent|camping)\b|자전거|골프|스키|운동|거꾸리|썰매|미끼통|퍼터|드라이브|런닝머신|헬스|라이딩복/i.test(text)) {
    return 'Sports & leisure';
  }

  // 3. Furniture
  if (/\b(chair|chairs|table|tables|desk|desks|bed|beds|daybed|sofa|sofas|couch|dresser|mattress|shelf|shelves|cabinet|stool|stools|nightstand|nighttable|bench)\b|테이블|스탠드|조명|의자|소파|침대|책상|서랍|가구|식탁|스툴|체어|프레임|탁자|수납장|데이베드|바 스툴/i.test(text)) {
    return 'Furniture';
  }

  // 4. Baby & Kids
  if (/\b(baby|kid|kids|toddler|stroller|crib|diaper|toy|toys|lego|gundam|sylvanian|calico critters|bassinet|highchair)\b|유아|아동|유모차|장난감|레고|베시넷|하이체어|돌한복|돌 한복/i.test(text)) {
    return 'Baby & kids';
  }

  // 5. Shoes
  if (/\b(shoe|shoes|sneaker|sneakers|boot|boots|sandal|sandals|hunter|nike|adidas|jordan|heel|heels)\b|신발|운동화|구두|부츠|슬리퍼/i.test(text)) {
    return 'Shoes';
  }

  // 6. Luggages & Bags
  if (/\b(bag|bags|backpack|luggage|suitcase|tote|pouch|wallet|osprey)\b|가방|백팩|캐리어|지갑|배낭|파우치/i.test(text)) {
    return 'Luggages & bags';
  }

  // 7. Health & Beauty
  if (/\b(beauty|cosmetic|cosmetics|perfume|cream|lotion|soap|facial|brush|makeup|thermometer)\b|화장품|향수|비누|메이크업|브러쉬/i.test(text)) {
    return 'Health & beauty';
  }

  // 8. Home, Garden & DIY
  if (/\b(dish|dishes|plate|plates|bowl|bowls|cup|cups|mug|mugs|glass|soju|serving bowl|steamer|rice cooker|container|oil dispenser|dispenser|towel|towel set|paper|tissue|decor|decorations|mirror|curtain|plant|pot|pan|cookware|tool|plane|rock|rocks|gravel|vase|candle)\b|주방|냄비|그릇|화분|인테리어|액자|거울|장식|장식품|수저|화장지|소주잔|식기|김치통|밥그릇|찜기|유리병|정원용/i.test(text)) {
    return 'Home, garden & DIY';
  }

  // 9. Women's Fashion
  if (/\b(women|womens|women's|dress|skirt|blouse|handbag|purse)\b|원피스|스커트|여성|핸드백/i.test(text)) {
    return "Women's fashion";
  }

  // 10. Men's Fashion
  if (/\b(men|mens|men's|suit|tuxedo|dress shirt)\b|남성|정장|셔츠/i.test(text)) {
    return "Men's fashion";
  }

  // 11. Food & Groceries
  if (/\b(food|foods|snack|snacks|chip|chips|fruit chips|cookie|cookies|noodle|noodles|ramen|kimchi|drink|drinks|beverage|beverages|candy|chocolate|chocolates|matcha|yuzu|almond|almonds|honey|honeycomb|crisp|crisps|chili oil|olive oil|jam|jams|cacao|syrup|sourdough|ferrero|lollipop|lollipops|juice|soy sauce|sauce|vinegar|seaweed|rusk|rusks|curry|somyeon|ganjang)\b|식품|과자|라면|햇반|김치|음료|사탕|초콜릿|초콜렛|꽃다발|간식|음료수|소연/i.test(text)) {
    return 'Food & Groceries';
  }

  if (rawCategory && !['used items', 'general', 'other', 'food & groceries'].includes(rawCategory.toLowerCase())) {
    return rawCategory;
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

    const isFoodRescueFilter = isFoodRescuePage || qSource === 'food-rescue' || qSource === 'kimc';
    const isLocalShopsFilter = isLocalShopsPage || qSource === 'local-shops' || qSource === 'local';
    const isMarketplacesFilter = isMarketplacesPage || qSource === 'marketplaces' || qSource === 'others';

    const allItems = await fetchAllCombinedItems();
    let filteredItems = [];

    if (isFoodRescueFilter) {
      filteredItems = allItems.filter(item => item.source === 'kimc');
    } else if (isMarketplacesFilter) {
      filteredItems = allItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
    } else if (isLocalShopsFilter || isShopProfile) {
      const prods = (isShopProfile ? localShopsData.products.filter(p => p.shop_id === shopProfileSlug) : localShopsData.products) || [];
      filteredItems = prods.map(p => ({
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
    } else {
      // Default Moonoh tab: ONLY Moonoh items
      filteredItems = allItems.filter(item => item.source === 'moonoh' || (!item.source && !String(item.id||'').startsWith('karrot') && !String(item.id||'').startsWith('heykorean') && !String(item.id||'').startsWith('kimc')));
    }

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
          const num = parseFloat(p);
          return !isNaN(num) && num === 0;
        });
      } else {
        filteredItems = filteredItems.filter(item => {
          const mainCat = (item.categoryName || item.category || '').toLowerCase();
          const targetName = targetCategoryObj.name.toLowerCase();
          const targetKw = (targetCategoryObj.kw || '').toLowerCase();

          // Exact or keyword match on item's assigned category
          if (mainCat === targetName || (targetKw && mainCat.includes(targetKw))) {
            return true;
          }

          // Only fallback to title keywords if item's category is generic ('other', 'general', 'used items')
          if (['general', 'other', 'used items', ''].includes(mainCat)) {
            const titleStr = (item.title || '').toLowerCase();
            if (targetCategoryObj.excludes && targetCategoryObj.excludes.some(ex => titleStr.includes(ex))) {
              return false;
            }
            return targetCategoryObj.keywords.some(kw => {
              if (kw.length <= 4) {
                const regex = new RegExp(`\\b${kw}\\b`, 'i');
                return regex.test(titleStr);
              }
              return titleStr.includes(kw);
            });
          }

          return false;
        });
      }
    }

    let template = getExploreTemplate();
    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    // Dynamic AEO & SEO Title/Description Generation
    let pageTitle = "Buy and Sell Secondhand Items in NYC & NJ | Moonoh";
    let metaDesc = "Browse verified local secondhand items in NYC & NJ. 0% fees, secure chat, and safe neighborhood exchanges on Moonoh.";
    let h1Text = "Buy and sell used items in your neighborhood";
    let canonicalUrl = `https://moon-oh.com${fullPath || '/explore'}`;
    let themeColor = "#4F46E5";
    let sectionName = "Moonoh Marketplace";

    if (targetRegionObj && targetCategoryObj) {
      pageTitle = `Used ${targetCategoryObj.name} for Sale in ${targetRegionObj.name} | Moonoh`;
      metaDesc = `Find great deals on verified used ${targetCategoryObj.name.toLowerCase()} in ${targetRegionObj.name} on Moonoh. 0% fees, direct seller chat, and local meetup.`;
      h1Text = `Used ${targetCategoryObj.name} for Sale in ${targetRegionObj.name}`;
      sectionName = `${targetCategoryObj.name} in ${targetRegionObj.shortName}`;
    } else if (targetRegionObj) {
      pageTitle = `Used Items for Sale in ${targetRegionObj.name} | Moonoh`;
      metaDesc = `Discover secondhand items listed by neighbors in ${targetRegionObj.name}. Buy and sell locally with zero fees on Moonoh.`;
      h1Text = `Used Items for Sale in ${targetRegionObj.name}`;
      sectionName = targetRegionObj.name;
    } else if (targetCategoryObj) {
      pageTitle = `Used ${targetCategoryObj.name} for Sale in NYC & NJ | Moonoh`;
      metaDesc = `Explore secondhand ${targetCategoryObj.name.toLowerCase()} for sale in NYC and NJ on Moonoh. Connect directly with local sellers.`;
      h1Text = `Used ${targetCategoryObj.name} for Sale in NYC & NJ`;
      sectionName = targetCategoryObj.name;
    }

    // Render AEO Summary Statistics Section (for Answer Engines & Google AI Overviews)
    let aeoSummaryHtml = '';
    if (targetRegionObj || targetCategoryObj) {
      const itemCount = filteredItems.length;
      const prices = filteredItems.map(i => i.price).filter(p => p > 0);
      const avgPrice = prices.length > 0 ? (prices.reduce((a,b)=>a+b, 0) / prices.length) : 0;
      const freeCount = filteredItems.filter(i => i.price === 0).length;
      const locLabel = targetRegionObj ? targetRegionObj.name : "NYC & NJ";
      const catLabel = targetCategoryObj ? targetCategoryObj.name : "secondhand items";

      aeoSummaryHtml = `
      <section class="aeo-summary-card" style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:16px; padding:20px 24px; margin-bottom:28px;">
        <h2 style="font-size:18px; font-weight:800; color:#111827; margin-top:0; margin-bottom:8px;">Market Summary: ${escapeHtml(catLabel)} in ${escapeHtml(locLabel)}</h2>
        <p style="font-size:14.5px; color:#4B5563; line-height:1.6; margin:0;">
          Currently featuring <strong>${itemCount} active listings</strong> for ${escapeHtml(catLabel.toLowerCase())} in ${escapeHtml(locLabel)}.
          ${avgPrice > 0 ? `Average price is approximately <strong>$${Math.round(avgPrice)}</strong>.` : ''}
          ${freeCount > 0 ? ` Includes <strong>${freeCount} free items</strong> shared by local neighbors.` : ''}
          All listings feature 0% transaction fees and direct neighborhood chat on Moonoh.
        </p>
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
        badgeHtml = `<div class="item-card-badge badge-kimc">Kim'C Market</div>`;
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
            <div class="item-card-location">${escapeHtml(item.townName || item.location || 'NYC')}</div>
            ${badgeHtml}
          </div>
        </a>
      `;
    }).join('');

    // JSON-LD Breadcrumbs Schema
    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://moon-oh.com/" },
        { "@type": "ListItem", "position": 2, "name": "Explore", "item": "https://moon-oh.com/explore" },
        { "@type": "ListItem", "position": 3, "name": sectionName, "item": canonicalUrl }
      ]
    };

    const breadcrumbScript = `<script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>`;
    const initialItemsScript = `<script>window.__INITIAL_ITEMS__ = ${JSON.stringify(initialItems)};</script>`;

    if (targetRegionObj && targetRegionObj.shortName) {
      const regName = targetRegionObj.shortName;
      template = template.replace(`<option value="${regName}">`, `<option value="${regName}" selected="selected">`);
    }
    }

        // Highlight active source tab in SSR HTML
    if (isMarketplacesFilter) {
      template = template
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"')
        .replace('class="source-tab-btn" id="tab-source-marketplaces"', 'class="source-tab-btn active" id="tab-source-marketplaces"');
    } else if (isFoodRescueFilter) {
      template = template
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"')
        .replace('class="source-tab-btn" id="tab-source-foodrescue"', 'class="source-tab-btn active" id="tab-source-foodrescue"');
    } else if (isLocalShopsFilter || isShopProfile) {
      template = template
        .replace('class="source-tab-btn active" id="tab-source-moonoh"', 'class="source-tab-btn" id="tab-source-moonoh"')
        .replace('class="source-tab-btn" id="tab-source-localshops"', 'class="source-tab-btn active" id="tab-source-localshops"');
    }

    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(metaDesc)}" name="description"/>`)
      .replace(/<link [^>]*rel="canonical"[^>]*\/>/i, `<link rel="canonical" href="${canonicalUrl}"/>`)
      .replace('</head>', `${initialItemsScript}
${breadcrumbScript}
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
