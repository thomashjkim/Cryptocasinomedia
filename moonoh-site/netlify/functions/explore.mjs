import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { realFoodRescueItems } from './food-rescue-items.mjs';

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
          const loc = (raw.location || 'nyc-ny').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
          return {
            id: raw.id,
            title: raw.title,
            price: raw.price,
            photo: raw.image,
            townName: raw.location,
            rawTown: raw.rawTown || raw.location,
            categoryName: raw.category || 'General',
            detailUrl: `https://moon-oh.com/item/${clean}-${loc}-ext-${raw.id}`,
            source: raw.source || 'external',
            sourceName: raw.sourceName || 'Marketplace'
          };
        });
      }
    }

    let foodRescueItems = [];
    if (Array.isArray(realFoodRescueItems)) {
      foodRescueItems = realFoodRescueItems.map(item => {
        let clean = (item.title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
        if (clean.length > 50) clean = clean.substring(0, 50).replace(/-$/, '');
        return {
          id: item.id,
          title: item.title,
          price: item.price,
          photo: item.image,
          townName: 'Brooklyn, NY',
          rawTown: 'Brooklyn, NY',
          categoryName: item.categoryName || 'Food & Groceries',
          detailUrl: `https://moon-oh.com/item/${clean}-brooklyn-ny-ext-${item.id}`,
          source: 'kimc',
          sourceName: "Kim'C Market",
          handle: item.handle
        };
      });
    }

    cachedCombinedItems = [...moonohItems, ...foodRescueItems, ...externalItems];
    lastFetchTime = now;
    return cachedCombinedItems;
  } catch (e) {
    console.error("Error in fetchAllCombinedItems:", e);
    return cachedCombinedItems || [];
  }
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

    // 1. Path Parsing for 4 Discovery Routes & Shop Profile Pages
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

    if (pathSegments.length === 1) {
      const seg = pathSegments[0].toLowerCase();
      if (seg === 'food-rescue' || seg === 'foodrescue') isFoodRescuePage = true;
      else if (seg === 'local-shops' || seg === 'localshops') isLocalShopsPage = true;
      else if (seg === 'marketplaces' || seg === 'others') isMarketplacesPage = true;
    }

    const isFoodRescueFilter = isFoodRescuePage || qSource === 'food-rescue' || qSource === 'kimc';
    const isLocalShopsFilter = isLocalShopsPage || qSource === 'local-shops';
    const isMarketplacesFilter = isMarketplacesPage || qSource === 'marketplaces' || qSource === 'others';

    const allItems = await fetchAllCombinedItems();
    let filteredItems = [...allItems];

    if (isFoodRescueFilter) {
      filteredItems = filteredItems.filter(item => item.source === 'kimc');
    } else if (isMarketplacesFilter) {
      filteredItems = filteredItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
    } else if (isLocalShopsFilter) {
      filteredItems = []; // Local shops rendered from localShopsData
    } else {
      filteredItems = filteredItems.filter(item => !item.source || item.source === 'moonoh');
    }

    let template = getExploreTemplate();
    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    // 2. Build Page Metadata for Route
    let pageTitle = "Buy and Sell with Your NYC & NJ Neighbors | Moonoh";
    let metaDesc = "Browse secondhand items listed directly by Moonoh users. Chat with local sellers and arrange a safe neighborhood exchange.";
    let h1Text = "Buy and Sell with Your NYC & NJ Neighbors";
    let subtitleLabel = "Moonoh Marketplace";
    let canonicalUrl = `https://moon-oh.com${fullPath || '/explore'}`;
    let themeColor = "#4F46E5";

    if (isFoodRescuePage) {
      pageTitle = "Save Quality Food from Going to Waste | Moonoh Food Rescue";
      metaDesc = "Discover discounted food from trusted local shops before it goes to waste. Purchases are completed directly with each participating retailer.";
      h1Text = "Save Quality Food from Going to Waste";
      subtitleLabel = "Food Rescue";
      themeColor = "#006853";
    } else if (isLocalShopsPage) {
      pageTitle = "Discover Independent Shops in NYC | Moonoh Local Shops";
      metaDesc = "Explore distinctive groceries, pantry goods and home products from independent New York shops. Purchases are completed directly with each retailer.";
      h1Text = "Discover Independent Shops in NYC";
      subtitleLabel = "Local Shops";
      themeColor = "#05452E";
    } else if (isMarketplacesPage) {
      pageTitle = "Explore Listings Across Local Marketplaces | Moonoh";
      metaDesc = "Browse secondhand items found across NYC and NJ marketplace communities. Complete each transaction through the original marketplace.";
      h1Text = "Explore Listings Across Local Marketplaces";
      subtitleLabel = "Other Marketplaces";
      themeColor = "#2563EB";
    } else if (isShopProfile && shopProfileSlug && localShopsData.shops[shopProfileSlug]) {
      const shop = localShopsData.shops[shopProfileSlug];
      pageTitle = `${shop.name} - Independent NYC Local Shop | Moonoh`;
      metaDesc = shop.business_description;
      h1Text = shop.name;
      subtitleLabel = shop.name;
      themeColor = shop.theme_color || "#4F46E5";
    }

    // 3. Render Cards HTML
    let cardsHtml = '';

    if (isLocalShopsPage || isShopProfile) {
      const shopKeys = isShopProfile ? [shopProfileSlug] : Object.keys(localShopsData.shops);
      const featuredShopsHtml = shopKeys.map(k => {
        const s = localShopsData.shops[k];
        if (!s) return '';
        const badgeClass = s.verification_status === 'verified_partner' ? 'background:#E6F5F0; color:#006853; border:1px solid #99D6C4;' : 'background:#FFF7ED; color:#C2410C; border:1px solid #FFEDD5;';
        const badgeText = s.verification_status === 'verified_partner' ? 'Verified Partner' : 'Unclaimed';
        return `
          <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:16px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.04); display:flex; flex-direction:column; justify-content:space-between; position:relative;">
            <div>
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
                <span style="${badgeClass} font-size:11px; font-weight:700; padding:4px 10px; border-radius:9999px;">${badgeText}</span>
                <span style="font-size:12px; color:#6B7280;">📍 ${escapeHtml(s.neighborhood)}</span>
              </div>
              <h3 style="font-size:18px; font-weight:800; color:#111827; margin-bottom:6px;">${escapeHtml(s.name)}</h3>
              <p style="font-size:13.5px; color:#4B5563; line-height:1.5; margin-bottom:16px;">${escapeHtml(s.business_description)}</p>
            </div>
            <div>
              <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px;">
                ${(s.categories || []).map(c => `<span style="background:#F3F4F6; color:#4B5563; font-size:12px; padding:3px 10px; border-radius:9999px;">${escapeHtml(c)}</span>`).join('')}
              </div>
              <a href="/local-shops/${s.slug}" style="display:inline-flex; align-items:center; justify-content:center; width:100%; background:${s.theme_color || '#4F46E5'}; color:#FFFFFF; font-weight:700; font-size:13px; padding:10px 16px; border-radius:9999px; text-decoration:none; box-sizing:border-box;">View Shop Profile ↗</a>
            </div>
          </div>
        `;
      }).join('');

      // Products & Brand Listings Grid
      const prodsToRender = isShopProfile ? localShopsData.products.filter(p => p.shop_id === shopProfileSlug) : localShopsData.products;
      const brandsToRender = isShopProfile ? localShopsData.brand_listings.filter(b => b.shop_id === shopProfileSlug) : localShopsData.brand_listings;

      const productCards = prodsToRender.map(p => `
        <div class="moonoh-item-card" style="background:#fff; border:1px solid #E5E7EB; border-radius:16px; overflow:hidden; display:flex; flex-direction:column;">
          <div style="position:relative; width:100%; padding-top:100%; background:#F9FAFB;">
            <img src="${escapeHtml(p.image_source_url)}" alt="${escapeHtml(p.title)}" style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover;" loading="lazy">
          </div>
          <div style="padding:14px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
            <div>
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                <span style="font-size:12px; font-weight:700; color:#6B7280;">${escapeHtml(p.brand || 'Local Shop')}</span>
                <span style="background:#FFF7ED; color:#C2410C; font-size:10px; font-weight:700; padding:2px 8px; border-radius:9999px;">Unclaimed</span>
              </div>
              <h4 style="font-size:14px; font-weight:700; color:#111827; margin-bottom:6px; line-height:1.3; height:36px; overflow:hidden;">${escapeHtml(p.title)}</h4>
              <div style="font-size:16px; font-weight:800; color:#111827; margin-bottom:8px;">$${p.current_price > 0 ? p.current_price.toFixed(2) : 'Check price at retailer'}</div>
            </div>
            <a href="${escapeHtml(p.source_url)}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; justify-content:center; background:#4F46E5; color:#fff; font-size:12px; font-weight:700; padding:8px 12px; border-radius:9999px; text-decoration:none; margin-top:8px;">${escapeHtml(p.cta_text || 'View at Retailer ↗')}</a>
          </div>
        </div>
      `).join('');

      const brandCards = brandsToRender.map(b => `
        <div class="moonoh-item-card" style="background:#fff; border:1px solid #E5E7EB; border-radius:16px; overflow:hidden; display:flex; flex-direction:column;">
          <div style="position:relative; width:100%; padding-top:80%; background:#FFF7ED; display:flex; align-items:center; justify-content:center;">
            <img src="${escapeHtml(b.image_source_url)}" alt="${escapeHtml(b.name)}" style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:contain; padding:16px;" loading="lazy">
          </div>
          <div style="padding:14px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
            <div>
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                <span style="font-size:12px; font-weight:700; color:#FF5722;">Pop Up Grocer</span>
                <span style="background:#FFEDD5; color:#C2410C; font-size:10px; font-weight:700; padding:2px 8px; border-radius:9999px;">${escapeHtml(b.availability_type)}</span>
              </div>
              <h4 style="font-size:16px; font-weight:800; color:#111827; margin-bottom:6px;">${escapeHtml(b.name)}</h4>
              <p style="font-size:12px; color:#6B7280; margin-bottom:8px;">Aisle: ${escapeHtml(b.aisle)}</p>
            </div>
            <a href="${escapeHtml(b.source_url)}" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; justify-content:center; background:#FF5722; color:#fff; font-size:12px; font-weight:700; padding:8px 12px; border-radius:9999px; text-decoration:none; margin-top:8px;">Discover at Pop Up Grocer ↗</a>
          </div>
        </div>
      `).join('');

      cardsHtml = `
        <div style="grid-column:1/-1; margin-bottom:32px;">
          <h2 style="font-size:20px; font-weight:800; color:#111827; margin-bottom:16px;">Featured Independent Shops</h2>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
            ${featuredShopsHtml}
          </div>
        </div>
        <div style="grid-column:1/-1; margin-bottom:16px; display:flex; align-items:center; justify-content:space-between;">
          <h2 style="font-size:20px; font-weight:800; color:#111827; margin:0;">Product &amp; Brand Discovery</h2>
          <span style="font-size:13px; color:#6B7280;">Product information may change. Confirm pricing with retailer.</span>
        </div>
        ${productCards}
        ${brandCards}
      `;
    } else {
      const initialItems = filteredItems.slice(0, 40);
      cardsHtml = initialItems.map(item => `
        <div class="moonoh-item-card" style="background:#fff; border:1px solid #E5E7EB; border-radius:16px; overflow:hidden; display:flex; flex-direction:column;">
          <div style="position:relative; width:100%; padding-top:100%; background:#F3F4F6;">
            <img src="${escapeHtml(item.photo)}" alt="${escapeHtml(item.title)}" style="position:absolute; top:0; left:0; width:100%; height:100%; object-fit:cover;" loading="lazy">
          </div>
          <div style="padding:14px; display:flex; flex-direction:column; flex:1; justify-content:space-between;">
            <div>
              <div style="font-size:16px; font-weight:800; color:#111827; margin-bottom:4px;">$${typeof item.price === 'number' ? (item.price % 1 !== 0 ? item.price.toFixed(2) : item.price) : item.price}</div>
              <h4 style="font-size:14px; font-weight:700; color:#111827; margin-bottom:6px; line-height:1.3; height:36px; overflow:hidden;">${escapeHtml(item.title)}</h4>
              <div style="font-size:12px; color:#6B7280;">${escapeHtml(item.townName)}</div>
            </div>
            <a href="${escapeHtml(item.detailUrl)}" style="display:inline-flex; align-items:center; justify-content:center; background:#4F46E5; color:#fff; font-size:12px; font-weight:700; padding:8px 12px; border-radius:9999px; text-decoration:none; margin-top:10px;">View Item ↗</a>
          </div>
        </div>
      `).join('');
    }

    // 4. Inject into Template
    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(metaDesc)}" name="description"/>`)
      .replace(/<link [^>]*rel="canonical"[^>]*\/>/i, `<link rel="canonical" href="${canonicalUrl}"/>`)
      .replace('</head>', `<meta name="theme-color" content="${themeColor}"/></head>`);

    // Replace Title & Subtitle
    template = template
      .replace('Buy and sell used items in your neighborhood', escapeHtml(h1Text))
      .replace('Moonoh Marketplace', escapeHtml(subtitleLabel));

    // Replace Grid
    template = template.replace(
      '<div class="item-grid" id="moonoh-item-grid">',
      `<div class="item-grid" id="moonoh-item-grid">\n${cardsHtml}`
    );

    return new Response(template, {
      status: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=300, s-maxage=600'
      }
    });
  } catch (error) {
    console.error("Error in explore.mjs handler:", error);
    return new Response("Internal Server Error", { status: 500 });
  }
};
