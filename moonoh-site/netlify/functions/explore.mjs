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

function formatPriceStr(price) {
  if (!price || price <= 0) return "Free";
  return price % 1 !== 0 ? "$" + price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) : "$" + Math.round(price).toLocaleString();
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

    if (pathSegments.length === 1) {
      const seg = pathSegments[0].toLowerCase();
      if (seg === 'food-rescue' || seg === 'foodrescue') isFoodRescuePage = true;
      else if (seg === 'local-shops' || seg === 'localshops' || seg === 'local') isLocalShopsPage = true;
      else if (seg === 'marketplaces' || seg === 'others') isMarketplacesPage = true;
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
      const brands = (isShopProfile ? localShopsData.brand_listings.filter(b => b.shop_id === shopProfileSlug) : localShopsData.brand_listings) || [];

      const formattedProds = prods.map(p => ({
        id: p.id,
        title: p.title,
        price: p.current_price,
        photo: p.image_source_url,
        townName: p.shop_id === 'happier-grocery' ? 'Soho, NY' : (p.shop_id === 'big-night' ? 'Greenpoint, NY' : 'NYC, NY'),
        categoryName: p.moonoh_category || 'Grocery',
        detailUrl: p.source_url,
        source: p.shop_id,
        badgeName: p.brand || (localShopsData.shops[p.shop_id] ? localShopsData.shops[p.shop_id].name : 'Local Shop')
      }));

      const formattedBrands = brands.map(b => ({
        id: b.id,
        title: b.name,
        price: 0,
        photo: b.image_source_url,
        townName: 'Greenwich Village, NY',
        categoryName: b.aisle || 'Grocery',
        detailUrl: b.source_url,
        source: b.shop_id,
        badgeName: 'Pop Up Grocer'
      }));

      filteredItems = [...formattedProds, ...formattedBrands];
    } else {
      filteredItems = allItems.filter(item => !item.source || item.source === 'moonoh');
    }

    let template = getExploreTemplate();
    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    let pageTitle = "Buy and Sell with Your NYC & NJ Neighbors | Moonoh";
    let metaDesc = "Browse secondhand items listed directly by Moonoh users. Chat with local sellers and arrange a safe neighborhood exchange.";
    let h1Text = "Buy and Sell with Your NYC & NJ Neighbors";
    let canonicalUrl = `https://moon-oh.com${fullPath || '/explore'}`;
    let themeColor = "#4F46E5";
    let sectionName = "Moonoh Marketplace";

    if (isFoodRescuePage) {
      pageTitle = "Save Quality Food from Going to Waste | Moonoh Food Rescue";
      metaDesc = "Discover discounted food from trusted local shops before it goes to waste. Purchases are completed directly with each participating retailer.";
      h1Text = "Buy and Sell with Your NYC & NJ Neighbors";
      themeColor = "#006853";
      sectionName = "Food Rescue";
    } else if (isLocalShopsPage) {
      pageTitle = "Discover Independent Shops in NYC | Moonoh Local Shops";
      metaDesc = "Explore distinctive groceries, pantry goods and home products from independent New York shops. Purchases are completed directly with each retailer.";
      h1Text = "Buy and Sell with Your NYC & NJ Neighbors";
      themeColor = "#05452E";
      sectionName = "Local Shops";
    } else if (isMarketplacesPage) {
      pageTitle = "Explore Listings Across Local Marketplaces | Moonoh";
      metaDesc = "Browse secondhand items found across NYC and NJ marketplace communities. Complete each transaction through the original marketplace.";
      h1Text = "Buy and Sell with Your NYC & NJ Neighbors";
      themeColor = "#2563EB";
      sectionName = "Other Marketplaces";
    } else if (isShopProfile && shopProfileSlug && localShopsData.shops[shopProfileSlug]) {
      const shop = localShopsData.shops[shopProfileSlug];
      pageTitle = `${shop.name} - Independent NYC Local Shop | Moonoh`;
      metaDesc = shop.business_description;
      h1Text = shop.name;
      themeColor = shop.theme_color || "#4F46E5";
      sectionName = shop.name;
    }

    // Render Items using EXACT standard Moonoh <a class="item-card"> format
    const initialItems = filteredItems.slice(0, 40);
    const cardsHtml = initialItems.map(item => {
      const itemTitle = item.title || 'Item';
      const safeTitle = escapeHtml(itemTitle);
      const priceStr = formatPriceStr(item.price);
      const targetUrl = item.detailUrl || `/item/item-${item.id}`;
      
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
            <img src="${escapeHtml(item.photo)}" alt="${safeTitle}" class="item-card-image" loading="lazy" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';">
          </div>
          <div class="item-card-content">
            <div class="item-card-price">${priceStr}</div>
            <div class="item-card-title">${safeTitle}</div>
            <div class="item-card-location">${escapeHtml(item.townName)}</div>
            ${badgeHtml}
          </div>
        </a>
      `;
    }).join('');

    // JSON-LD Breadcrumbs & Shop Profile Schema
    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://moon-oh.com/" },
        { "@type": "ListItem", "position": 2, "name": "Explore", "item": "https://moon-oh.com/explore" },
        { "@type": "ListItem", "position": 3, "name": sectionName, "item": canonicalUrl }
      ]
    };

    let shopSchemaHtml = '';
    if (isShopProfile && shopProfileSlug && localShopsData.shops[shopProfileSlug]) {
      const shop = localShopsData.shops[shopProfileSlug];
      const shopSchema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": shop.name,
        "description": shop.business_description,
        "url": shop.website_url,
        "image": shop.logo_url || shop.primary_image_url,
        "address": {
          "@type": "PostalAddress",
          "streetAddress": shop.address_line_1,
          "addressLocality": shop.city,
          "addressRegion": shop.state,
          "postalCode": shop.postal_code,
          "addressCountry": "US"
        }
      };
      shopSchemaHtml = `<script type="application/ld+json">${JSON.stringify(shopSchema)}</script>`;
    }

    const breadcrumbScript = `<script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>`;

    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(metaDesc)}" name="description"/>`)
      .replace(/<link [^>]*rel="canonical"[^>]*\/>/i, `<link rel="canonical" href="${canonicalUrl}"/>`)
      .replace('</head>', `<meta name="theme-color" content="${themeColor}"/>\n${breadcrumbScript}\n${shopSchemaHtml}\n</head>`);

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
