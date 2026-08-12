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
  'manhattan': { name: 'Manhattan, NY', shortName: 'Manhattan', keywords: ['manhattan', 'upper east', 'upper west', 'downtown manhattan', 'midtown', 'harlem', 'tribeca', 'soho', 'lower east', 'east village', 'west village', 'chelsea', 'gramercy', 'inwood', 'washington heights', 'morningside', 'financial district', 'wall street', 'murray hill', 'kips bay', 'flatiron', 'new york'] },
  'queens': { name: 'Queens, NY', shortName: 'Queens', keywords: ['queens', 'bayside', 'flushing', 'astoria', 'jamaica', 'forest hills', 'jackson heights', 'woodside', 'ridgewood', 'ozone park', 'fresh meadows', 'corona', 'elmhurst', 'sunnyside', 'long island city', 'rego park', 'maspeth', 'howard beach', 'far rockaway', 'college point', 'whitestone', 'douglaston'] },
  'brooklyn': { name: 'Brooklyn, NY', shortName: 'Brooklyn', keywords: ['brooklyn', 'park slope', 'williamsburg', 'bushwick', 'bed stuy', 'flatbush', 'crown heights', 'bay ridge', 'bensonhurst', 'canarsie', 'east new york', 'greenpoint', 'cobble hill', 'carroll gardens', 'boerum', 'sunset park', 'borough park', 'brighton beach', 'coney island', 'sheepshead', 'ditmas'] },
  'bronx': { name: 'The Bronx, NY', shortName: 'The Bronx', keywords: ['bronx'] },
  'staten-island': { name: 'Staten Island, NY', shortName: 'Staten Island', keywords: ['staten island'] },
  'bergen-county': { name: 'Bergen County, NJ', shortName: 'Bergen County', keywords: ['bergen', 'hackensack', 'paramus', 'fort lee', 'englewood', 'teaneck', 'palisades', 'fair lawn', 'garfield', 'ridgewood nj', 'rutherford'] },
  'hudson-county': { name: 'Hudson County, NJ', shortName: 'Hudson County', keywords: ['hudson', 'jersey city', 'hoboken', 'bayonne', 'weehawken', 'union city', 'north bergen', 'secaucus', 'kearny'] }
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
  'other': { name: 'Other', kw: 'other', keywords: ['other', 'general'] }
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
          no: raw.no || raw.id,
          title: raw.title || "Secondhand Item",
          price: raw.price || 0,
          photo: raw.image || 'https://moon-oh.com/images/common/ico_profile_empty.png',
          image: raw.image || 'https://moon-oh.com/images/common/ico_profile_empty.png',
          townName: raw.location || 'NYC, NY',
          rawTown: raw.rawTown || raw.location || '',
          location: raw.location || 'NYC, NY',
          categoryName: raw.category || 'General',
          category: raw.category || 'General',
          detailUrl: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
          url: raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${raw.no || raw.id}`,
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
            categoryName: raw.category || 'General',
            category: raw.category || 'General',
            detailUrl: targetUrl,
            url: targetUrl,
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

    let targetRegionObj = null;
    let targetCategoryObj = null;

    if (pathSegments.length === 1) {
      const seg = pathSegments[0].toLowerCase();
      if (seg === 'food-rescue' || seg === 'foodrescue') isFoodRescuePage = true;
      else if (seg === 'local-shops' || seg === 'localshops' || seg === 'local') isLocalShopsPage = true;
      else if (seg === 'marketplaces' || seg === 'others') isMarketplacesPage = true;
      else if (REGIONS[seg]) targetRegionObj = REGIONS[seg];
      else if (CATEGORIES[seg]) targetCategoryObj = CATEGORIES[seg];
    } else if (pathSegments.length >= 2) {
      const seg1 = pathSegments[0].toLowerCase();
      const seg2 = pathSegments[1].toLowerCase();
      if (REGIONS[seg1]) targetRegionObj = REGIONS[seg1];
      if (CATEGORIES[seg2]) targetCategoryObj = CATEGORIES[seg2];
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
      // Include ALL sources across Moonoh, Marketplaces, Food Rescue & Local Shops for aggregate region/category pages
      filteredItems = allItems;

      // Filter by Region if present
      if (targetRegionObj) {
        filteredItems = filteredItems.filter(item => {
          const locStr = ((item.rawTown || '') + ' ' + (item.location || '') + ' ' + (item.townName || '')).toLowerCase();
          return targetRegionObj.keywords.some(kw => locStr.includes(kw));
        });
      }

      // Filter by Category if present
      if (targetCategoryObj) {
        filteredItems = filteredItems.filter(item => {
          const mainCat = (item.categoryName || item.category || '').toLowerCase();
          const titleStr = (item.title || '').toLowerCase();
          if (targetCategoryObj.excludes && targetCategoryObj.excludes.some(ex => titleStr.includes(ex))) {
            return false;
          }
          if (mainCat.includes(targetCategoryObj.kw)) return true;
          return targetCategoryObj.keywords.some(kw => titleStr.includes(kw) || mainCat.includes(kw));
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
      const priceStr = formatPriceStr(item.price);
      const targetUrl = item.detailUrl || item.url || `/item/item-${item.id}`;
      
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
            <img src="${escapeHtml(item.photo || item.image)}" alt="${safeTitle}" class="item-card-image" loading="lazy" onerror="this.onerror=null; this.src='/images/default-item-placeholder.png';">
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
      // Hide Source Tabs on AEO Aggregation Pages (/explore/{region}/{category}) so all items are combined with source badges
    if (targetRegionObj || targetCategoryObj) {
      template = template.replace('id="source-segment-wrap"', 'id="source-segment-wrap" style="display:none !important;"');
    }
    

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

    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(metaDesc)}" name="description"/>`)
      .replace(/<link [^>]*rel="canonical"[^>]*\/>/i, `<link rel="canonical" href="${canonicalUrl}"/>`)
      .replace('</head>', `${initialItemsScript}
${breadcrumbScript}
</head>`);

    // Inject AEO Summary Card & Cleanly Replace Entire Grid Block
    const gridBlockRegex = /<div class="item-grid" id="moonoh-item-grid">[\s\S]*?<\/div>/i;
    const newGridContent = (aeoSummaryHtml ? `${aeoSummaryHtml}\n` : '') + `<div class="item-grid" id="moonoh-item-grid">\n${cardsHtml}\n</div>`;
    template = template.replace(gridBlockRegex, newGridContent);

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
