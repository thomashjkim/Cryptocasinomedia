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
  'new-york-area': { slug: 'new-york-area', name: 'New York Area', shortName: '', keywords: [] },
  'manhattan': { slug: 'manhattan', name: 'Manhattan, NY', shortName: 'Manhattan', keywords: ['manhattan', 'upper east', 'upper west', 'downtown manhattan', 'midtown', 'harlem', 'tribeca', 'soho', 'lower east', 'east village', 'west village', 'chelsea', 'gramercy', 'inwood', 'washington heights', 'morningside', 'financial district', 'wall street', 'murray hill', 'kips bay', 'flatiron', 'new york'] },
  'queens': { slug: 'queens', name: 'Queens, NY', shortName: 'Queens', keywords: ['queens', 'bayside', 'flushing', 'astoria', 'jamaica', 'forest hills', 'jackson heights', 'woodside', 'ridgewood', 'ozone park', 'fresh meadows', 'corona', 'elmhurst', 'sunnyside', 'long island city', 'rego park', 'maspeth', 'howard beach', 'far rockaway', 'college point', 'whitestone', 'douglaston'] },
  'brooklyn': { slug: 'brooklyn', name: 'Brooklyn, NY', shortName: 'Brooklyn', keywords: ['brooklyn', 'park slope', 'williamsburg', 'bushwick', 'bed stuy', 'flatbush', 'crown heights', 'bay ridge', 'bensonhurst', 'canarsie', 'east new york', 'greenpoint', 'cobble hill', 'carroll gardens', 'boerum', 'sunset park', 'borough park', 'brighton beach', 'coney island', 'sheepshead', 'ditmas'] },
  'bronx': { slug: 'bronx', name: 'The Bronx, NY', shortName: 'Bronx', keywords: ['bronx'] },
  'staten-island': { slug: 'staten-island', name: 'Staten Island, NY', shortName: 'Staten Island', keywords: ['staten island'] },
  'flushing': { slug: 'flushing', name: 'Flushing, Queens, NY', shortName: 'Flushing', keywords: ['flushing'] },
  'bayside': { slug: 'bayside', name: 'Bayside, Queens, NY', shortName: 'Bayside', keywords: ['bayside'] },
  'astoria': { slug: 'astoria', name: 'Astoria, Queens, NY', shortName: 'Astoria', keywords: ['astoria', 'long island city', 'lic'] },
  'fort-lee-nj': { slug: 'fort-lee-nj', name: 'Fort Lee, NJ', shortName: 'Fort Lee', keywords: ['fort lee', 'fortlee', 'palisades park', 'palisades', 'leonia', 'cliffside park', 'edgewater', 'fort-lee', 'bergen'] },
  'fort-lee': { slug: 'fort-lee', name: 'Fort Lee, NJ', shortName: 'Fort Lee', keywords: ['fort lee', 'fortlee', 'palisades park', 'palisades', 'leonia', 'cliffside park', 'edgewater', 'fort-lee', 'bergen'] },
  'bergen-county-nj': { slug: 'bergen-county-nj', name: 'Bergen County, NJ', shortName: 'Bergen', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'bergen-county': { slug: 'bergen-county', name: 'Bergen County, NJ', shortName: 'Bergen', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'hudson-county-nj': { slug: 'hudson-county-nj', name: 'Hudson County, NJ', shortName: 'Hudson', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] },
  'hudson-county': { slug: 'hudson-county', name: 'Hudson County, NJ', shortName: 'Hudson', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] }
};

// Category Mapping
const CATEGORIES = {
  'electronics': { slug: 'electronics', name: 'Electronics', kw: 'electronics', keywords: ['electronics', 'phone', 'laptop', 'appliances', 'audio', 'gadget', 'ink', 'camera', 'tv', 'monitor', 'headphone', 'airpods', 'ipad', 'charger', 'speaker', 'printer', 'game', 'ps5', 'nintendo', 'xbox'] },
  'furniture': { slug: 'furniture', name: 'Furniture', kw: 'furniture', keywords: ['furniture', 'sofa', 'table', 'chair', 'bed', 'desk', 'couch', 'dresser', 'mattress', 'shelf', 'nightstand', 'cabinet', 'stool', 'bench', 'ottoman', 'headboard', 'drawers', '소파', '침대', '식탁', '의자', '책상', '서랍', '매트리스', '선반', '테이블', '가구'], excludes: ['pillow', 'hanger', 'curtain rod', 'fan', 'keyboard', 'monitor', 'massager', 'phone stand', 'photo printer', 'gymnastic', 'printer'] },
  'womens-fashion': { slug: 'womens-fashion', name: "Women's Fashion", kw: 'women', keywords: ["women's fashion", 'women', 'dress', 'handbag', 'skirt', 'coat'] },
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
      localItems = localShopsData.products.map((p, idx) => {
        const shop = (localShopsData.shops && localShopsData.shops[p.shop_id]) || {};
        const neighborhood = shop.neighborhood ? `${shop.neighborhood}, NY` : 'NYC, NY';
        return {
          id: p.id,
          no: p.id,
          title: p.title,
          price: p.current_price,
          photo: p.image_source_url,
          image: p.image_source_url,
          townName: neighborhood,
          rawTown: neighborhood,
          location: neighborhood,
          categoryName: p.primary_category || p.moonoh_category || 'General',
          category: p.primary_category || p.moonoh_category || 'General',
          detailUrl: `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`,
          url: `https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`,
          source: p.shop_id,
          badgeName: p.brand || shop.name || 'Local Shop',
          postedAt: p.source_published_at ? new Date(p.source_published_at).getTime() : (p.last_checked_at ? new Date(p.last_checked_at).getTime() - (idx * 1500000) : (Date.now() - idx * 1500000))
        };
      });
    }

    cachedCombinedItems = [...moonohItems, ...externalItems, ...foodRescueItems, ...localItems];
    // Sort all combined items by original posting timestamp (recency order)
    cachedCombinedItems.sort((a, b) => {
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

    // Dynamic AEO & SEO Title/Description/H1 Generation
    let pageTitle = "Buy and Sell Secondhand Items in NYC & NJ | Moonoh";
    let metaDesc = "Browse verified local secondhand items in NYC & NJ. 0% fees, secure chat, and safe neighborhood exchanges on Moonoh.";
    let h1Text = "Explore Secondhand Marketplace Listings in NYC & NJ";
    let dynamicIntroText = "Explore thousands of verified local secondhand goods, gently used furniture, electronics, and food rescue items across New York City and New Jersey. 100% free neighborhood marketplace with zero fees.";
    let canonicalUrl = `https://moon-oh.com/explore`;
    let themeColor = "#4F46E5";
    let sectionName = "Moonoh Marketplace";

    if (isFoodRescueFilter) {
      canonicalUrl = `https://moon-oh.com/explore/food-rescue`;
      pageTitle = "NYC Food Waste Rescue & Grocery Deals | Moonoh";
      metaDesc = "Shop discounted gourmet Korean pantry items near sell-by date in NYC from Kim'C Market on Moonoh. Fight food waste, save money.";
      h1Text = "NYC Food Waste Rescue & Sustainable Groceries";
      dynamicIntroText = "Rescue premium artisanal and specialty groceries near sell-by dates at up to 70% discount in NYC. Partnering with local grocers like Kim'C Market to fight food waste and promote sustainable consumption.";
      sectionName = "Food Rescue";
    } else if (isLocalShopsFilter || isShopProfile) {
      canonicalUrl = `https://moon-oh.com/explore/local-shops`;
      pageTitle = "NYC Local Shops - Curated Neighborhood Goods | Moonoh";
      metaDesc = "Discover iconic local New York City specialty shops and neighborhood staples on Moonoh. Curated pantry goods, tableware, and specialty items.";
      h1Text = "NYC Local Shops - Curated Neighborhood Goods in NYC";
      dynamicIntroText = "Explore curated collections from iconic independent New York City shops including Big Night (Greenpoint), Happier Grocery (SoHo), and Pop Up Grocer (Bleecker St). Support local NYC merchants.";
      sectionName = isShopProfile ? (localShopsData.shops[shopProfileSlug]?.name || "Local Shop") : "Local NYC Shops";
    } else if (isMarketplacesFilter) {
      canonicalUrl = `https://moon-oh.com/explore/marketplaces`;
      pageTitle = "NYC & NJ Community Marketplace Feed | Moonoh";
      metaDesc = "Browse aggregated local secondhand listings across NYC & NJ from Karrot and HeyKorean on Moonoh.";
      h1Text = "NYC & NJ Community Marketplace Feed";
      dynamicIntroText = "Discover community secondhand items from verified neighborhood marketplaces across New York City and New Jersey.";
      sectionName = "Community Marketplaces";
    } else if (targetRegionObj && targetCategoryObj) {
      canonicalUrl = `https://moon-oh.com/explore/${targetRegionObj.slug}/${targetCategoryObj.slug}`;
      pageTitle = `Used ${targetCategoryObj.name} for Sale in ${targetRegionObj.name} | Moonoh`;
      metaDesc = `Find great deals on verified used ${targetCategoryObj.name.toLowerCase()} in ${targetRegionObj.name} on Moonoh. 0% fees, direct seller chat, and local meetup.`;
      h1Text = `Used ${targetCategoryObj.name} for Sale in ${targetRegionObj.name}`;
      dynamicIntroText = `Discover verified secondhand ${targetCategoryObj.name.toLowerCase()} listed for sale by local neighbors in ${targetRegionObj.name}. Buy and sell locally with 0% listing fees, direct in-app chat, and safe neighborhood pickup on Moonoh.`;
      sectionName = `${targetCategoryObj.name} in ${targetRegionObj.shortName}`;
    } else if (targetRegionObj) {
      canonicalUrl = `https://moon-oh.com/explore/${targetRegionObj.slug}`;
      pageTitle = `Used Items for Sale in ${targetRegionObj.name} | Moonoh`;
      metaDesc = `Discover secondhand items listed by neighbors in ${targetRegionObj.name}. Buy and sell locally with zero fees on Moonoh.`;
      h1Text = `Used Items for Sale in ${targetRegionObj.name}`;
      dynamicIntroText = `Browse gently used furniture, electronics, household goods, and secondhand deals listed by verified neighbors in ${targetRegionObj.name}. 100% free local exchanges with zero transaction fees.`;
      sectionName = targetRegionObj.name;
    } else if (targetCategoryObj) {
      canonicalUrl = `https://moon-oh.com/explore/${targetCategoryObj.slug}`;
      pageTitle = `Used ${targetCategoryObj.name} for Sale in NYC & NJ | Moonoh`;
      metaDesc = `Explore secondhand ${targetCategoryObj.name.toLowerCase()} for sale in NYC and NJ on Moonoh. Connect directly with local sellers.`;
      h1Text = `Used ${targetCategoryObj.name} for Sale in NYC & NJ`;
      dynamicIntroText = `Explore quality used ${targetCategoryObj.name.toLowerCase()} for sale across New York City (Manhattan, Brooklyn, Queens, Bronx, Staten Island) and New Jersey. Connect directly with nearby sellers with zero commissions.`;
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
