import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { realFoodRescueItems } from './food-rescue-items.mjs';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

// Region Mapping
const REGIONS = {
  'manhattan': { name: 'Manhattan, NY', keywords: ['manhattan', 'upper east', 'upper west', 'downtown manhattan', 'midtown', 'harlem', 'tribeca', 'soho', 'lower east', 'east village', 'west village', 'chelsea', 'gramercy', 'inwood', 'washington heights', 'morningside', 'financial district', 'wall street', 'murray hill', 'kips bay', 'flatiron'] },
  'queens': { name: 'Queens, NY', keywords: ['queens', 'bayside', 'flushing', 'astoria', 'jamaica', 'forest hills', 'jackson heights', 'woodside', 'ridgewood', 'ozone park', 'fresh meadows', 'corona', 'elmhurst', 'sunnyside', 'long island city', 'rego park', 'maspeth', 'howard beach', 'far rockaway', 'college point', 'whitestone', 'douglaston'] },
  'brooklyn': { name: 'Brooklyn, NY', keywords: ['brooklyn', 'park slope', 'williamsburg', 'bushwick', 'bed stuy', 'flatbush', 'crown heights', 'bay ridge', 'bensonhurst', 'canarsie', 'east new york', 'greenpoint', 'cobble hill', 'carroll gardens', 'boerum', 'sunset park', 'borough park', 'brighton beach', 'coney island', 'sheepshead', 'ditmas'] },
  'bronx': { name: 'The Bronx, NY', keywords: ['bronx'] },
  'staten-island': { name: 'Staten Island, NY', keywords: ['staten island'] },
  'bergen-county': { name: 'Bergen County, NJ', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'hudson-county': { name: 'Hudson County, NJ', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] }
};

// Category Mapping
const CATEGORIES = {
  'electronics': { name: 'Electronics', keywords: ['electronics', 'phone', 'laptop', 'appliances', 'audio', 'gadget', 'ink', 'camera', 'tv', 'monitor', 'headphone', 'airpods', 'ipad', 'charger', 'speaker', 'printer', 'game', 'ps5', 'nintendo', 'xbox'] },
  'furniture': { name: 'Furniture', keywords: ['furniture', 'sofa', 'table', 'chair', 'bed', 'desk', 'couch', 'dresser', 'mattress', 'shelf'] },
  'womens-fashion': { name: "Women's Fashion", keywords: ["women's fashion", 'women', 'dress', 'handbag', 'skirt', 'coat'] },
  'mens-fashion': { name: "Men's Fashion", keywords: ["men's fashion", 'men', 'suit', 'jacket'] },
  'shoes': { name: 'Shoes', keywords: ['shoes', 'sneakers', 'boots', 'sandals', 'shoe', 'nike', 'adidas'] },
  'home-garden': { name: 'Home & Garden', keywords: ['home, garden & diy', 'home', 'garden', 'kitchen', 'utensil', 'decor'] },
  'health-beauty': { name: 'Health & Beauty', keywords: ['health', 'beauty', 'cosmetics'] },
  'pet-supplies': { name: 'Pet Supplies', keywords: ['pet', 'dog', 'cat'] },
  'baby-kids': { name: 'Baby & Kids', keywords: ['baby & kids', 'baby', 'kids', 'stroller', 'toy'] },
  'sports-leisure': { name: 'Sports & Leisure', keywords: ['sports', 'leisure', 'bike', 'ski', 'exercise'] },
  'toys-games': { name: 'Toys & Games', keywords: ['toys', 'games', 'card', 'figure'] },
  'jewelry-watches': { name: 'Jewelry & Watches', keywords: ['jewelry', 'watches', 'ring', 'earrings', 'watch'] },
  'luggages-bags': { name: 'Luggages & Bags', keywords: ['luggages', 'bags', 'pouch', 'backpack', 'tote', 'wallet', 'bag'] },
  'antiques': { name: 'Antiques', keywords: ['antiques', 'vintage', 'collectible'] },
  'arts-books-music': { name: 'Arts, Books & Music', keywords: ['arts', 'books', 'music', 'book', 'print'] },
  'food-groceries': { name: 'Food & Groceries', keywords: ['food', 'groceries', 'snack', 'sauce', 'oil', 'rice', 'tea', 'noodle', 'kimchi', 'pantry', 'drink', 'beverage', 'korean food', 'cookie', 'juice', 'chip'] },
  'used-items': { name: 'Used Items', keywords: ['used items'] },
  'other': { name: 'Other', keywords: ['other', 'general'] }
};

let cachedCombinedItems = null;
let lastFetchTime = 0;
const CACHE_TTL_MS = 15 * 1000;

async function fetchAllCombinedItems() {
  const now = Date.now();
  if (cachedCombinedItems && (now - lastFetchTime) < CACHE_TTL_MS) {
    return cachedCombinedItems;
  }

  try {
    const [moonohRes, externalRes] = await Promise.allSettled([
      fetch("https://moon-oh.com/api/items"),
      fetch("https://moon-oh.com/api/external-items")
    ]);

    let moonohItems = [];
    if (moonohRes.status === 'fulfilled' && moonohRes.value.ok) {
      const data = await moonohRes.value.json();
      if (Array.isArray(data)) {
        moonohItems = data.map(raw => ({
          id: raw.no || raw.id,
          title: raw.title || "Secondhand Item",
          price: raw.price || 0,
          photo: raw.image || 'https://moon-oh.com/images/common/ico_profile_empty.png',
          townName: raw.location || 'NYC, NY',
          rawTown: raw.rawTown || raw.location || '',
          categoryName: raw.category || 'General',
          detailUrl: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
          source: 'moonoh'
        }));
      }
    }

    let externalItems = [];
    if (externalRes.status === 'fulfilled' && externalRes.value.ok) {
      const data = await externalRes.value.json();
      if (Array.isArray(data)) {
        externalItems = data.map(raw => {
          let clean = (raw.title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
          if (clean.length > 50) clean = clean.substring(0, 50).replace(/-$/, '');
          let loc = 'nyc-ny';
          let low = String(raw.rawTown || raw.location || '').toLowerCase();
          if (low.includes('bayside')) loc = 'bayside-queens-ny';
          else if (low.includes('flushing')) loc = 'flushing-queens-ny';
          else if (low.includes('astoria')) loc = 'astoria-queens-ny';
          else if (low.includes('queens')) loc = 'queens-ny';
          else if (low.includes('brooklyn')) loc = 'brooklyn-ny';
          else if (low.includes('manhattan')) loc = 'manhattan-ny';
          else if (low.includes('palisades')) loc = 'palisades-park-nj';
          else if (low.includes('fort lee')) loc = 'fort-lee-nj';

          const slug = `/item/${clean}-${loc}-ext-${raw.id}`;

          function inferCategoryFromText(title = '', description = '', rawCategory = '') {
            const text = (title + ' ' + description).toLowerCase();

            if (/food|snack|chip|chips|cookie|cookies|noodle|noodles|ramen|rice|tea|sauce|kimchi|drink|beverage|gourmet|grocer|식품|과자|라면|햇반|김치/i.test(text) || (rawCategory && /food|grocery|groceries|gourmet/i.test(rawCategory))) {
              return 'Food & Groceries';
            }
            if (/table|chair|sofa|desk|bed|couch|dresser|mattress|shelf|cabinet|stand|lamp|light|furniture|테이블|스탠드|조명|의자|소파|침대|책상|서랍|가구|식탁/i.test(text)) {
              return 'Furniture';
            }
            if (/phone|iphone|galaxy|ipad|macbook|laptop|computer|monitor|tv|television|speaker|headphone|airpods|camera|printer|cartridge|ink|charger|appliance|fridge|microwave|vacuum|닌텐도|게임|nintendo|ps5|xbox|appliances|electronics/i.test(text)) {
              return 'Electronics';
            }
            if (/shoe|shoes|sneaker|sneakers|boot|boots|sandal|sandals|nike|adidas|jordan|heel|heels|신발|운동화|구두|부츠/i.test(text)) {
              return 'Shoes';
            }
            if (/\bwomen\b|\bwomens\b|\bwomen's\b|dress|skirt|blouse|handbag|purse|bra|leggings|원피스|스커트|여성|핸드백/i.test(text)) {
              return "Women's Fashion";
            }
            if (/\bmen\b|\bmens\b|\bmen's\b|suit|jacket|coat|tuxedo|남성|정장|자켓/i.test(text)) {
              return "Men's Fashion";
            }
            if (/baby|kid|kids|stroller|crib|diaper|toy|toys|lego|유아|아동|유모차|장난감|레고/i.test(text)) {
              return 'Baby & Kids';
            }
            if (/bike|bicycle|bmx|ski|snowboard|golf|racket|exercise|treadmill|dumbbell|tent|camping|자전거|골프|스키|운동/i.test(text)) {
              return 'Sports & Leisure';
            }
            if (/kitchen|utensil|pan|pot|cookware|dish|towel|plant|garden|decor|frame|art|curtain|mug|cup|주방|냄비|그릇|화분|인테리어|액자/i.test(text)) {
              return 'Home & Garden';
            }
            if (/bag|backpack|luggage|suitcase|tote|pouch|wallet|가방|백팩|캐리어|지갑/i.test(text)) {
              return 'Luggages & Bags';
            }
            if (/game|card|trading|collectible|figure|board game|카드|보드게임|피규어/i.test(text)) {
              return 'Toys & Games';
            }
            if (/book|novel|dvd|cd|vinyl|album|art|print|painting|책|음반|소설/i.test(text)) {
              return 'Arts, Books & Music';
            }
            if (/watch|ring|necklace|bracelet|jewelry|시계|반지|목걸이|보석/i.test(text)) {
              return 'Jewelry & Watches';
            }
            if (/dog|cat|pet|leash|crate|강아지|고양이|반려동물/i.test(text)) {
              return 'Pet Supplies';
            }
            if (/beauty|cosmetic|perfume|cream|lotion|화장품|향수/i.test(text)) {
              return 'Health & Beauty';
            }

            if (rawCategory && rawCategory.toLowerCase() !== 'used items' && rawCategory.toLowerCase() !== 'general') {
              return rawCategory;
            }

            return 'Other';
          }

          let catName = inferCategoryFromText(raw.title, raw.description, raw.category);

          return {
            id: raw.id,
            title: raw.title || "Secondhand Item",
            price: raw.price || 0,
            photo: raw.image || 'https://moon-oh.com/images/common/ico_profile_empty.png',
            townName: raw.location || 'NYC, NY',
            rawTown: raw.rawTown || raw.location || '',
            categoryName: catName,
            detailUrl: `https://moon-oh.com${slug}`,
            source: raw.source || 'external',
            createdAt: raw.createdAt || 0,
            timeAgo: raw.timeAgo || 'Recently'
          };
        });
      }
    }

    // Assign stable descending timestamps to external items to preserve Karrot & HeyKorean interleaving
    const baseTime = Date.now();
    const externalItemsWithTime = externalItems.map((item, idx) => ({
      ...item,
      createdAt: item.createdAt || (baseTime - idx * 1000)
    }));

    // Combine Moonoh + Food Rescue + External items and sort by recency
    const combined = [...moonohItems, ...realFoodRescueItems, ...externalItemsWithTime];
    combined.sort((a, b) => {
      const timeA = a.createdAt || 0;
      const timeB = b.createdAt || 0;
      return timeB - timeA;
    });

    cachedCombinedItems = combined;
    lastFetchTime = now;
    return combined;

  } catch (err) {
    console.error("Error in fetchAllCombinedItems:", err);
  }

  return cachedCombinedItems || [];
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function getExploreTemplate() {
  const possiblePaths = [
    path.resolve(process.cwd(), 'explore.html'),
    path.resolve(currentDir, '../../explore.html'),
    path.resolve(currentDir, '../explore.html'),
    './explore.html'
  ];
  for (const p of possiblePaths) {
    try {
      if (fs.existsSync(p)) {
        return fs.readFileSync(p, 'utf-8');
      }
    } catch (e) {}
  }
  return null;
}

export default async (req, context) => {
  try {
    const url = new URL(req.url);

    // 1. Check for legacy query parameters and 301 Redirect to clean path URL
    const qLocation = url.searchParams.get('location') || url.searchParams.get('town');
    const qCategory = url.searchParams.get('category');
    const qSource = url.searchParams.get('source');

    if (qLocation || qCategory || qSource) {
      let rSlug = '';
      let cSlug = '';

      if (qLocation) {
        const low = qLocation.toLowerCase();
        for (const [key, obj] of Object.entries(REGIONS)) {
          if (obj.keywords.some(kw => low.includes(kw)) || low.includes(key)) {
            rSlug = key;
            break;
          }
        }
      }

      if (qCategory) {
        const low = qCategory.toLowerCase();
        for (const [key, obj] of Object.entries(CATEGORIES)) {
          if (obj.keywords.some(kw => low.includes(kw)) || low.includes(key)) {
            cSlug = key;
            break;
          }
        }
      }

      if (qLocation || qCategory) {
        let redirectPath = '/explore';
        if (rSlug && cSlug) redirectPath = `/explore/${rSlug}/${cSlug}`;
        else if (rSlug) redirectPath = `/explore/${rSlug}`;
        else if (cSlug) redirectPath = `/explore/${cSlug}`;

        if (redirectPath !== url.pathname) {
          return new Response(null, {
            status: 301,
            headers: { "Location": redirectPath }
          });
        }
      }
    }

    // 2. Parse URL Path Segments
    const pathSegments = url.pathname.replace(/^\/explore\/?/, '').split('/').filter(Boolean);

    let regionSlug = null;
    let categorySlug = null;
    let isOthersPage = false;
    let isFoodRescuePage = false;
    const isMainUserEntrypoint = pathSegments.length === 0;

    if (pathSegments.length === 1) {
      const seg = pathSegments[0].toLowerCase();
      if (seg === 'food-rescue' || seg === 'foodrescue') {
        isFoodRescuePage = true;
      } else if (seg === 'marketplaces' || seg === 'others') {
        isOthersPage = true;
      } else if (REGIONS[seg]) {
        regionSlug = seg;
      } else if (CATEGORIES[seg]) {
        categorySlug = seg;
      }
    } else if (pathSegments.length >= 2) {
      const seg1 = pathSegments[0].toLowerCase();
      const seg2 = pathSegments[1].toLowerCase();
      if (REGIONS[seg1]) regionSlug = seg1;
      if (CATEGORIES[seg2]) categorySlug = seg2;
    }

    const isFoodRescueFilter = isFoodRescuePage || qSource === 'food-rescue' || qSource === 'foodrescue' || qSource === 'kimc';
    const isOthersFilter = isOthersPage || qSource === 'marketplaces' || qSource === 'others';

    // 3. Fetch ALL combined items (Moonoh + Food Rescue + Karrot + HeyKorean)
    const allItems = await fetchAllCombinedItems();
    let filteredItems = [...allItems];

    if (isFoodRescueFilter) {
      filteredItems = filteredItems.filter(item => item.source === 'kimc');
    } else if (isOthersFilter) {
      filteredItems = filteredItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
    } else if (isMainUserEntrypoint && !qSource) {
      filteredItems = filteredItems.filter(item => item.source === 'moonoh');
    }

    // Filter by Region (for aggregation pages)
    if (regionSlug && REGIONS[regionSlug]) {
      const kws = REGIONS[regionSlug].keywords;
      filteredItems = filteredItems.filter(item => {
        const locStr = ((item.rawTown || '') + ' ' + (item.townName || '')).toLowerCase();
        return kws.some(kw => locStr.includes(kw));
      });
    }

    // Filter by Category (for aggregation pages)
    if (categorySlug && CATEGORIES[categorySlug]) {
      const kws = CATEGORIES[categorySlug].keywords;
      filteredItems = filteredItems.filter(item => {
        const catStr = (item.categoryName || '').toLowerCase() + ' ' + (item.title || '').toLowerCase();
        return kws.some(kw => catStr.includes(kw));
      });
    }

    let template = getExploreTemplate();
    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    // Dynamic Title & Meta Setup
    const regionObj = REGIONS[regionSlug];
    const categoryObj = CATEGORIES[categorySlug];

    const regionName = regionObj ? regionObj.name : "NYC & NJ";
    const categoryName = isOthersPage ? "Marketplace Items" : (categoryObj ? categoryObj.name : "Local Items");

    let pageTitle = "Explore Local Marketplace Items in NYC & NJ | Moonoh";
    let h1Text = "Buy and sell used items in your neighborhood";
    let canonicalUrl = `https://moon-oh.com${url.pathname}`;

    if (isFoodRescuePage) {
      pageTitle = `Kim'C Market Food Rescue Deals in Brooklyn, NY | Moonoh`;
      h1Text = `Fight Food Waste with Kim'C Market Food Rescue`;
    } else if (isOthersPage) {
      pageTitle = regionObj ? `Karrot & HeyKorean Items in ${regionName} | Moonoh` : `Aggregated Karrot & HeyKorean Marketplace Items | Moonoh`;
      h1Text = regionObj ? `Karrot & HeyKorean Items in ${regionName}` : `Aggregated Karrot & HeyKorean Items`;
    } else if (regionObj && categoryObj) {
      pageTitle = `Used ${categoryName} in ${regionName} | Moonoh`;
      h1Text = `Used ${categoryName} in ${regionName}`;
    } else if (regionObj) {
      pageTitle = `Marketplace Items in ${regionName} | Moonoh`;
      h1Text = `Marketplace Items in ${regionName}`;
    } else if (categoryObj) {
      pageTitle = `Used ${categoryName} for Sale in NYC & NJ | Moonoh`;
      h1Text = `Used ${categoryName} for Sale`;
    }

    const itemCount = filteredItems.length;

    // ── Stats Computation ──────────────────────────────────────────────────────
    const pricedItems = filteredItems.filter(i => i.price > 0);
    const prices = pricedItems.map(i => i.price).sort((a, b) => a - b);
    const medianPrice = prices.length > 0
      ? (prices.length % 2 === 0 ? (prices[prices.length / 2 - 1] + prices[prices.length / 2]) / 2 : prices[Math.floor(prices.length / 2)])
      : 0;
    const minPrice = prices.length > 0 ? prices[0] : 0;
    const maxPrice = prices.length > 0 ? prices[prices.length - 1] : 0;
    const freeCount = filteredItems.filter(i => i.price <= 0).length;

    const moonohCount = filteredItems.filter(i => i.source === 'moonoh').length;
    const kimcCount = filteredItems.filter(i => i.source === 'kimc').length;
    const karrotCount = filteredItems.filter(i => i.source === 'karrot').length;
    const heykoreanCount = filteredItems.filter(i => i.source === 'heykorean').length;

    // Most recently listed
    const sortedByRecent = [...filteredItems].sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
    const mostRecentItem = sortedByRecent[0];
    let lastListedStr = 'Recently';
    if (mostRecentItem && mostRecentItem.timeAgo) {
      lastListedStr = mostRecentItem.timeAgo;
    }

    const avgPriceStr = medianPrice > 0 ? `$${Math.round(medianPrice).toLocaleString()} median` : 'Free items available';
    const priceRangeStr = (minPrice > 0 && maxPrice > 0)
      ? `$${Math.round(minPrice).toLocaleString()} – $${Math.round(maxPrice).toLocaleString()}`
      : (freeCount > 0 ? 'Free & paid items' : 'Prices vary');

    // ── robots meta: 0-4 items → noindex, follow ───────────────────────────
    let robotsMeta = '';
    if (isOthersPage || (regionSlug || categorySlug) && itemCount < 5) {
      robotsMeta = '\n  <meta name="robots" content="noindex, follow"/>';
    }

    let introText = "";
    if (isFoodRescuePage) {
      introText = `Browse ${itemCount} verified Food Rescue & Sell-by deals from Kim'C Market in Brooklyn, NY. Save authentic Korean gourmet items near sell-by date with deep discounts while fighting local NYC food waste.`;
    } else if (isOthersPage) {
      introText = `Browse aggregated local marketplace items for sale in ${regionName} from Karrot and HeyKorean.`;
    } else if (itemCount > 0) {
      introText = `Browse ${itemCount} verified items for sale in ${regionName} on Moonoh. Find local deals from neighbors — including listings from Karrot and HeyKorean. ${avgPriceStr}. Meet up safely across ${regionName} neighborhoods.`;
    } else {
      introText = `Explore verified items in ${regionName} on Moonoh. Connect with local sellers across ${regionName} neighborhoods.`;
    }

    // ── SSR Grid Cards ─────────────────────────────────────────────────────────
    const initialItems = filteredItems.slice(0, 40);
    let cardsHtml = '';

    if (initialItems.length === 0) {
      cardsHtml = `
        <div style="text-align:center; padding:50px 20px; grid-column:1/-1; background:#F9FAFB; border-radius:16px; border:1px dashed #E5E7EB; margin:16px 0;">
          <div style="font-size:44px; margin-bottom:12px;">📦</div>
          <h3 style="font-size:20px; font-weight:700; color:#111827; margin-bottom:8px;">No ${escapeHtml(categoryName)} items in ${escapeHtml(regionName)} right now</h3>
          <p style="color:#6B7280; font-size:15px; max-width:480px; margin:0 auto 24px; line-height:1.5;">We couldn't find any listings matching this filter right now. Check back soon or explore nearby areas.</p>
          <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
            ${regionSlug ? `<a href="/explore/${regionSlug}" style="display:inline-block; background:#3a46e2; color:#fff; font-weight:600; padding:10px 22px; border-radius:999px; text-decoration:none; font-size:14px;">Browse all items in ${escapeHtml(regionName)}</a>` : ''}
            <a href="/explore" style="display:inline-block; background:#F3F4F6; color:#374151; font-weight:600; padding:10px 22px; border-radius:999px; text-decoration:none; font-size:14px;">Explore all NYC items</a>
          </div>
        </div>
      `;
    } else {
      initialItems.forEach(item => {
        const priceStr = item.price > 0 ? `$${item.price.toLocaleString()}` : 'Free';
        const timeLoc = item.timeAgo ? `${item.timeAgo} · ${item.townName}` : item.townName;
        let badgeHtml = '';
        if (item.source === 'karrot') {
          badgeHtml = `<div class="item-card-badge badge-karrot" style="display:inline-block; background:#FFF7ED; color:#C2410C; border:1px solid #FFD0B0; font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:4px; margin-top:4px; line-height:1.2;">Karrot</div>`;
        } else if (item.source === 'heykorean') {
          badgeHtml = `<div class="item-card-badge badge-heykorean" style="display:inline-block; background:#EBF4FF; color:#2D8CFF; border:1px solid #B8D9FF; font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:4px; margin-top:4px; line-height:1.2;">HeyKorean</div>`;
        } else if (item.source === 'kimc') {
          badgeHtml = `<div class="item-card-badge badge-kimc" style="display:inline-block; background:#E6F5F0; color:#006853; border:1px solid #99D6C4; font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:4px; margin-top:4px; line-height:1.2;">Kim'C Market</div>`;
        } else {
          badgeHtml = `<div class="item-card-badge badge-moonoh" style="display:inline-block; background:#EDEFFC; color:#3a46e2; border:1px solid #C7CEFA; font-size:10.5px; font-weight:700; padding:1px 6px; border-radius:4px; margin-top:4px; line-height:1.2;">Moonoh</div>`;
        }

        cardsHtml += `
          <div class="item-card" onclick="location.href='${item.detailUrl}'" style="cursor:pointer;">
            <div class="item-card-img-wrap">
              <img src="${escapeHtml(item.photo)}" alt="${escapeHtml(item.title)}" class="item-card-img" loading="lazy" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';"/>
            </div>
            <div class="item-card-info">
              <div class="item-card-price">${priceStr}</div>
              <div class="item-card-title">${escapeHtml(item.title)}</div>
              <div class="item-card-location">${escapeHtml(timeLoc)}</div>
              ${badgeHtml}
            </div>
          </div>
        `;
      });
    }

    // ── Dynamic Interlinking ───────────────────────────────────────────────────
    const ALL_REGIONS = ['manhattan', 'queens', 'brooklyn', 'bronx', 'staten-island', 'bergen-county', 'hudson-county'];
    const ALL_CATS = ['electronics', 'furniture', 'shoes', 'womens-fashion', 'mens-fashion', 'home-garden', 'baby-kids', 'sports-leisure', 'toys-games', 'jewelry-watches', 'luggages-bags', 'arts-books-music', 'health-beauty', 'pet-supplies'];

    let relatedLinks = [];
    if (regionSlug && categorySlug) {
      // Region+Category page: link to same category in other regions + same region other categories
      ALL_REGIONS.filter(r => r !== regionSlug).slice(0, 4).forEach(r => {
        relatedLinks.push({ name: `${CATEGORIES[categorySlug].name} in ${REGIONS[r].name.split(',')[0]}`, url: `/explore/${r}/${categorySlug}` });
      });
      ALL_CATS.filter(c => c !== categorySlug).slice(0, 4).forEach(c => {
        relatedLinks.push({ name: `${CATEGORIES[c].name} in ${regionObj.name.split(',')[0]}`, url: `/explore/${regionSlug}/${c}` });
      });
    } else if (regionSlug) {
      // Region page: link to top categories in this region
      ALL_CATS.slice(0, 8).forEach(c => {
        relatedLinks.push({ name: `${CATEGORIES[c].name} in ${regionObj.name.split(',')[0]}`, url: `/explore/${regionSlug}/${c}` });
      });
      ALL_REGIONS.filter(r => r !== regionSlug).slice(0, 4).forEach(r => {
        relatedLinks.push({ name: `Items in ${REGIONS[r].name.split(',')[0]}`, url: `/explore/${r}` });
      });
    } else if (categorySlug) {
      // Category page: link to this category in each region
      ALL_REGIONS.forEach(r => {
        relatedLinks.push({ name: `${categoryObj.name} in ${REGIONS[r].name.split(',')[0]}`, url: `/explore/${r}/${categorySlug}` });
      });
      ALL_CATS.filter(c => c !== categorySlug).slice(0, 5).forEach(c => {
        relatedLinks.push({ name: `Used ${CATEGORIES[c].name} — NYC & NJ`, url: `/explore/${c}` });
      });
    } else {
      relatedLinks = [
        { name: 'Electronics in Queens', url: '/explore/queens/electronics' },
        { name: 'Furniture in Brooklyn', url: '/explore/brooklyn/furniture' },
        { name: 'Shoes in Manhattan', url: '/explore/manhattan/shoes' },
        { name: 'Baby & Kids in Bergen County', url: '/explore/bergen-county/baby-kids' },
        { name: 'Furniture in Queens', url: '/explore/queens/furniture' },
        { name: "Women's Fashion in Manhattan", url: '/explore/manhattan/womens-fashion' }
      ];
    }
    relatedLinks = relatedLinks.filter(l => l.url !== url.pathname).slice(0, 12);

    // ── Dynamic FAQ (3-4 items per page type) ─────────────────────────────────
    const lastVerifiedDate = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    let faqItems = [];

    if (regionObj && categoryObj) {
      faqItems = [
        {
          q: `Where can I buy used ${categoryName} in ${regionName}?`,
          a: `You can browse ${itemCount} verified used ${categoryName.toLowerCase()} listings in ${regionName} on Moonoh. Listings come from local sellers on Moonoh, Karrot, and HeyKorean — all aggregated in one place. Prices range from ${priceRangeStr}. Last verified: ${lastVerifiedDate}.`
        },
        {
          q: `What is the average price for used ${categoryName} in ${regionName}?`,
          a: `Based on ${pricedItems.length} active listings in ${regionName}, the median price for used ${categoryName.toLowerCase()} is ${avgPriceStr}. Prices range from ${priceRangeStr}. ${freeCount > 0 ? `${freeCount} item${freeCount > 1 ? 's are' : ' is'} listed for free.` : ''} Prices are updated as sellers post new listings.`
        },
        {
          q: `How do I safely buy used ${categoryName} locally in ${regionName}?`,
          a: `Moonoh recommends meeting in a public place such as a coffee shop, library, or police station parking lot in ${regionName.split(',')[0]}. Always view the item in person before paying. Use Moonoh's in-app chat to communicate securely with the seller. Never send payment before inspecting the item.`
        },
        {
          q: `How do I sell used ${categoryName} in ${regionName} on Moonoh?`,
          a: `Download the free Moonoh app (iOS or Android), create a listing with photos and a price, and choose your preferred meetup neighborhood in ${regionName.split(',')[0]}. Your listing will appear to buyers searching for ${categoryName.toLowerCase()} in ${regionName}. Moonoh charges 0% seller fees.`
        }
      ];
    } else if (regionObj) {
      // Compute top categories in this region from filteredItems
      const catCounts = {};
      filteredItems.forEach(item => {
        const cn = item.categoryName || 'Other';
        catCounts[cn] = (catCounts[cn] || 0) + 1;
      });
      const topCats = Object.entries(catCounts).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([n]) => n).join(', ');

      faqItems = [
        {
          q: `What secondhand items are for sale in ${regionName} right now?`,
          a: `There are currently ${itemCount} verified secondhand items listed in ${regionName} on Moonoh. Popular categories include ${topCats || 'electronics, furniture, and fashion'}. Prices range from ${priceRangeStr}. New listings are added daily from local sellers and aggregated from Karrot and HeyKorean.`
        },
        {
          q: `How do I find local deals near me in ${regionName}?`,
          a: `Moonoh aggregates secondhand listings from local sellers in ${regionName} alongside listings from Karrot and HeyKorean. Browse by category using the filters above, or download the Moonoh app to get real-time notifications for new items near you in ${regionName.split(',')[0]}.`
        },
        {
          q: `Is Moonoh available in ${regionName}?`,
          a: `Yes — Moonoh serves buyers and sellers throughout ${regionName}, covering neighborhoods including ${(REGIONS[regionSlug]?.keywords || []).slice(0, 4).join(', ')}. With ${itemCount} active listings, it is one of the most active local marketplaces for secondhand goods in the area.`
        }
      ];
    } else if (categoryObj) {
      faqItems = [
        {
          q: `Where can I find used ${categoryName} for sale near me in NYC & NJ?`,
          a: `Moonoh currently has ${itemCount} verified used ${categoryName.toLowerCase()} listings across NYC and NJ, including Manhattan, Queens, Brooklyn, The Bronx, Staten Island, Bergen County, and Hudson County. Listings come from local sellers and are aggregated from Karrot and HeyKorean. Last verified: ${lastVerifiedDate}.`
        },
        {
          q: `What is the average price for used ${categoryName} in New York?`,
          a: `Based on ${pricedItems.length} active listings across NYC & NJ, the median price for used ${categoryName.toLowerCase()} is ${avgPriceStr}. Prices range from ${priceRangeStr}. ${freeCount > 0 ? `${freeCount} items are listed for free.` : ''}`
        },
        {
          q: `How do I buy used ${categoryName} safely through Moonoh?`,
          a: `Browse listings on Moonoh's explore page, then use the in-app chat to contact the seller. Arrange to meet at a public location in your neighborhood. Inspect the item before any payment. Moonoh recommends meeting at police station parking lots or busy public areas for safe local exchanges. Never wire money or send payment before inspecting.`
        }
      ];
    }

    // ── Stats Bar HTML ─────────────────────────────────────────────────────────
    const statsBarHtml = (regionSlug || categorySlug || isOthersPage) ? `
      <div class="agg-stats-bar" style="display:flex; flex-wrap:wrap; gap:12px; margin-bottom:20px; margin-top:4px;">
        <div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#F3F4F6; border-radius:9999px; padding:6px 14px; font-size:13px; font-weight:600; color:#111827;">
          <span style="color:#4F46E5;">📦</span> ${itemCount.toLocaleString()} items
        </div>
        ${medianPrice > 0 ? `<div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#F3F4F6; border-radius:9999px; padding:6px 14px; font-size:13px; font-weight:600; color:#111827;"><span style="color:#059669;">💰</span> ${avgPriceStr}</div>` : ''}
        ${(minPrice > 0 && maxPrice > 0) ? `<div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#F3F4F6; border-radius:9999px; padding:6px 14px; font-size:13px; color:#4B5563;">Range: ${priceRangeStr}</div>` : ''}
        <div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#F3F4F6; border-radius:9999px; padding:6px 14px; font-size:13px; color:#4B5563;">🕐 Last listed: ${lastListedStr}</div>
        ${moonohCount > 0 ? `<div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#EDEFFC; border-radius:9999px; padding:6px 14px; font-size:12px; color:#3a46e2; font-weight:600;">Moonoh: ${moonohCount}</div>` : ''}
        ${karrotCount > 0 ? `<div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#FFF7ED; border-radius:9999px; padding:6px 14px; font-size:12px; color:#C2410C;">Karrot: ${karrotCount}</div>` : ''}
        ${heykoreanCount > 0 ? `<div class="stat-chip" style="display:flex; align-items:center; gap:6px; background:#EBF4FF; border-radius:9999px; padding:6px 14px; font-size:12px; color:#2D8CFF;">HeyKorean: ${heykoreanCount}</div>` : ''}
      </div>` : '';

    // ── Hero Section ───────────────────────────────────────────────────────────
    const heroHtml = `
      <div class="agg-hero-section" style="margin-top:24px; margin-bottom:24px; width:100%; box-sizing:border-box;">
        <h1 style="font-size:28px; font-weight:800; color:#111827; margin-bottom:8px; letter-spacing:-0.02em;">${escapeHtml(h1Text)}</h1>
        <p style="font-size:15px; color:#4B5563; line-height:1.6; margin-bottom:16px; width:100%; max-width:100%;">${escapeHtml(introText)}</p>
        ${statsBarHtml}
      </div>
    `;

    // ── Visual FAQ Section ─────────────────────────────────────────────────────
    const faqHtml = faqItems.length > 0 ? `
      <div class="agg-faq-section" style="max-width:1200px; margin:48px auto 0; padding:0 0 40px; border-top:1px solid #E5E7EB; width:100%;">
        <h2 style="font-size:20px; font-weight:700; color:#111827; margin-bottom:20px; margin-top:28px;">Frequently Asked Questions</h2>
        <div style="display:flex; flex-direction:column; gap:16px;">
          ${faqItems.map(f => `
            <details style="background:#F9FAFB; border:1px solid #E5E7EB; border-radius:12px; padding:16px 20px; cursor:pointer;">
              <summary style="font-size:15px; font-weight:600; color:#111827; list-style:none; display:flex; justify-content:space-between; align-items:center;">
                ${escapeHtml(f.q)}
                <span style="font-size:20px; color:#9CA3AF; margin-left:12px; flex-shrink:0;">+</span>
              </summary>
              <p style="font-size:14px; color:#4B5563; line-height:1.7; margin-top:12px; margin-bottom:0;">${escapeHtml(f.a)}</p>
            </details>
          `).join('')}
        </div>
      </div>
    ` : '';

    // ── Interlinking Section ───────────────────────────────────────────────────
    const interlinkingHtml = `
      <div class="agg-interlink-section" style="max-width:1200px; margin:32px auto 20px; padding:20px 0; border-top:1px solid #E5E7EB; width:100%;">
        <h3 style="font-size:16px; font-weight:700; color:#1F2937; margin-bottom:12px;">Explore Related Categories & Neighborhoods</h3>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
          ${relatedLinks.map(l => `<a href="${l.url}" style="display:inline-block; padding:6px 14px; background:#F3F4F6; color:#4B5563; font-size:13px; font-weight:500; border-radius:9999px; text-decoration:none;">${l.name}</a>`).join('')}
        </div>
      </div>
    `;

    // ── JSON-LD Schemas ────────────────────────────────────────────────────────
    const itemListSchema = {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": h1Text,
      "description": introText,
      "numberOfItems": filteredItems.length,
      "itemListElement": initialItems.map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "name": item.title,
        "url": item.detailUrl,
        "image": item.photo
      }))
    };

    const breadcrumbsElements = [
      { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://moon-oh.com/" },
      { "@type": "ListItem", "position": 2, "name": "Explore", "item": "https://moon-oh.com/explore" }
    ];

    if (regionObj) {
      breadcrumbsElements.push({
        "@type": "ListItem",
        "position": breadcrumbsElements.length + 1,
        "name": regionName,
        "item": `https://moon-oh.com/explore/${regionSlug}`
      });
    }

    if (categoryObj) {
      breadcrumbsElements.push({
        "@type": "ListItem",
        "position": breadcrumbsElements.length + 1,
        "name": categoryName,
        "item": canonicalUrl
      });
    }

    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": breadcrumbsElements
    };

    const collectionSchema = {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": h1Text,
      "description": introText,
      "url": canonicalUrl,
      "dateModified": new Date().toISOString()
    };

    const faqSchema = faqItems.length > 0 ? {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": faqItems.map(f => ({
        "@type": "Question",
        "name": f.q,
        "acceptedAnswer": { "@type": "Answer", "text": f.a }
      }))
    } : null;

    const extItemsForPreload = allItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
    const foodRescueForPreload = allItems.filter(item => item.source === 'kimc');

    const schemaScript = `
  <script type="application/ld+json">${JSON.stringify(itemListSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(collectionSchema)}</script>
  ${faqSchema ? `<script type="application/ld+json">${JSON.stringify(faqSchema)}</script>` : ''}
  <script>
    window.__INITIAL_ITEMS__ = ${JSON.stringify(filteredItems)};
    window.__INITIAL_EXTERNAL_ITEMS__ = ${JSON.stringify(extItemsForPreload)};
    window.__INITIAL_FOOD_RESCUE__ = ${JSON.stringify(foodRescueForPreload)};
  </script>
`;

    // ── Inject into Template ───────────────────────────────────────────────────
    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(introText)}" name="description"/>`)
      .replace(/<link [^>]*rel="canonical"[^>]*\/>/i, `<link rel="canonical" href="${canonicalUrl}"/>`)
      .replace('</head>', `${schemaScript}${robotsMeta}</head>`);

    // On aggregation landing pages, hide source tab switcher
    if (!isMainUserEntrypoint) {
      template = template.replace(
        'id="source-segment-wrap"',
        'id="source-segment-wrap" style="display:none;"'
      );
    }

    // Inject Hero Section + Grid
    template = template.replace(
      '<div class="item-grid" id="moonoh-item-grid">',
      `${heroHtml}\n<div class="item-grid" id="moonoh-item-grid">\n${cardsHtml}`
    );

    // Inject FAQ + Interlinking before </main>
    template = template.replace('</main>', `${faqHtml}\n${interlinkingHtml}\n</main>`);

    return new Response(template, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=300, s-maxage=600, stale-while-revalidate=1200"
      }
    });

  } catch (error) {
    console.error("Error in explore.mjs SSR:", error);
    const exploreHtmlPath = path.join(process.cwd(), 'explore.html');
    const html = fs.readFileSync(exploreHtmlPath, 'utf-8');
    return new Response(html, {
      status: 200,
      headers: { "Content-Type": "text/html; charset=utf-8" }
    });
  }
};
