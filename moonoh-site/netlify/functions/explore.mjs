import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

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

          let catName = raw.category || '';
          if (!catName || catName === 'General' || catName === 'Used Items') {
            const lowTitle = (raw.title || '').toLowerCase();
            if (lowTitle.includes('phone') || lowTitle.includes('iphone') || lowTitle.includes('macbook') || lowTitle.includes('laptop') || lowTitle.includes('tv') || lowTitle.includes('camera') || lowTitle.includes('monitor') || lowTitle.includes('headphone') || lowTitle.includes('airpods') || lowTitle.includes('ipad') || lowTitle.includes('charger') || lowTitle.includes('speaker') || lowTitle.includes('printer') || lowTitle.includes('game') || lowTitle.includes('ps5') || lowTitle.includes('nintendo') || lowTitle.includes('xbox') || lowTitle.includes('ink')) {
              catName = 'Electronics';
            } else if (lowTitle.includes('sofa') || lowTitle.includes('couch') || lowTitle.includes('table') || lowTitle.includes('chair') || lowTitle.includes('bed') || lowTitle.includes('desk') || lowTitle.includes('dresser') || lowTitle.includes('mattress') || lowTitle.includes('shelf')) {
              catName = 'Furniture';
            } else if (lowTitle.includes('shoe') || lowTitle.includes('sneaker') || lowTitle.includes('boot') || lowTitle.includes('sandal') || lowTitle.includes('nike') || lowTitle.includes('adidas')) {
              catName = 'Shoes';
            } else if (lowTitle.includes('bag') || lowTitle.includes('pouch') || lowTitle.includes('backpack') || lowTitle.includes('tote') || lowTitle.includes('wallet')) {
              catName = 'Luggages & Bags';
            } else if (lowTitle.includes('ring') || lowTitle.includes('watch') || lowTitle.includes('jewelry') || lowTitle.includes('necklace')) {
              catName = 'Jewelry & Watches';
            } else {
              catName = 'Used Items';
            }
          }

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
            createdAt: raw.createdAt || Date.now(),
            timeAgo: raw.timeAgo || 'Recently'
          };
        });
      }
    }

    // Combine Moonoh + External items and sort by recency (createdAt timestamp, newest first)
    const combined = [...moonohItems, ...externalItems];
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
    const isMainUserEntrypoint = pathSegments.length === 0;
    const isOthersFilter = isOthersPage || qSource === 'others';

    // Rule Distinction:
    // 1. User Entrypoint (/explore): Show Moonoh native items ONLY by default unless ?source=others parameter is present.
    // 2. SEO Aggregation Pages (/explore/{region}/{category}): Merge Moonoh + Karrot + HeyKorean sorted by recency for maximum density.
    if (isOthersFilter) {
      filteredItems = filteredItems.filter(item => item.source === 'karrot' || item.source === 'heykorean' || item.source === 'external');
    } else if (isMainUserEntrypoint) {
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

    // Thin Content Protection: If region/category/others specified and items < 3, return 404
    if ((regionSlug || categorySlug || isOthersPage) && filteredItems.length < 3) {
      return new Response("No listings found for this region/category combination", { status: 404 });
    }

    let template = getExploreTemplate();
    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    // Dynamic Title & Meta Setup
    const regionObj = REGIONS[regionSlug];
    const categoryObj = CATEGORIES[categorySlug];

    const regionName = regionObj ? regionObj.name : "NYC & NJ";
    const categoryName = isOthersPage ? "Aggregated Items (Karrot & HeyKorean)" : (categoryObj ? categoryObj.name : "Secondhand Items");

    let pageTitle = "Explore Secondhand Items in NYC & NJ | Moonoh";
    let h1Text = "Explore Local Secondhand Items";
    let canonicalUrl = `https://moon-oh.com${url.pathname}`;

    if (isOthersPage) {
      pageTitle = regionObj ? `Karrot & HeyKorean Items in ${regionName} | Moonoh` : `Aggregated Karrot & HeyKorean Secondhand Items | Moonoh`;
      h1Text = regionObj ? `Karrot & HeyKorean Items in ${regionName}` : `Aggregated Karrot & HeyKorean Items`;
    } else if (regionObj && categoryObj) {
      pageTitle = `Used ${categoryName} in ${regionName} | Moonoh`;
      h1Text = `Used ${categoryName} in ${regionName}`;
    } else if (regionObj) {
      pageTitle = `Secondhand Items in ${regionName} | Moonoh`;
      h1Text = `Secondhand Items in ${regionName}`;
    } else if (categoryObj) {
      pageTitle = `Used ${categoryName} for Sale in NYC & NJ | Moonoh`;
      h1Text = `Used ${categoryName} for Sale`;
    }

    const itemCount = filteredItems.length;
    const introText = `Browse ${itemCount} verified ${categoryName.toLowerCase()} for sale in ${regionName} on Moonoh. Find local deals from individual sellers across neighborhoods — including listings aggregated from Karrot and HeyKorean. Meet up locally or contact sellers directly.`;

    // SSR Grid Cards HTML
    const initialItems = filteredItems.slice(0, 40);
    let cardsHtml = '';
    initialItems.forEach(item => {
      const priceStr = item.price > 0 ? `$${item.price.toLocaleString()}` : 'Free';
      const timeLoc = item.timeAgo ? `${item.timeAgo} · ${item.townName}` : item.townName;
      let badgeHtml = '';
      if (item.source === 'karrot') {
        badgeHtml = `<div class="item-card-badge badge-karrot" style="display:inline-block; background:#FF6F09; color:#fff; font-size:11px; font-weight:700; padding:2px 6px; border-radius:4px; margin-top:4px;">Karrot</div>`;
      } else if (item.source === 'heykorean') {
        badgeHtml = `<div class="item-card-badge badge-heykorean" style="display:inline-block; background:#5B21B6; color:#fff; font-size:11px; font-weight:700; padding:2px 6px; border-radius:4px; margin-top:4px;">HeyKorean</div>`;
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

    // Interlinking Section (Internal Links Juice)
    const relatedLinks = [
      { name: 'Electronics in Queens', url: '/explore/queens/electronics' },
      { name: 'Furniture in Brooklyn', url: '/explore/brooklyn/furniture' },
      { name: 'Shoes in Manhattan', url: '/explore/manhattan/shoes' },
      { name: 'Baby & Kids in Bergen', url: '/explore/bergen-county/baby-kids' },
      { name: 'Furniture in Queens', url: '/explore/queens/furniture' },
      { name: 'Women\'s Fashion in Manhattan', url: '/explore/manhattan/womens-fashion' }
    ].filter(l => l.url !== url.pathname);

    const interlinkingHtml = `
      <div class="agg-interlink-section" style="max-width: 1200px; margin: 40px auto 20px; padding: 20px 0; border-top: 1px solid #E5E7EB; width: 100%;">
        <h3 style="font-size: 16px; font-weight: 700; color: #1F2937; margin-bottom: 12px;">Explore Related Local Aggregations</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          ${relatedLinks.map(l => `<a href="${l.url}" style="display: inline-block; padding: 6px 14px; background: #F3F4F6; color: #4B5563; font-size: 13px; font-weight: 500; border-radius: 9999px; text-decoration: none;">${l.name}</a>`).join('')}
        </div>
      </div>
    `;

    // Hero Section HTML (H1 + Intro - 24px Gap and Full Container Width)
    const heroHtml = `
      <div class="agg-hero-section" style="margin-top: 24px; margin-bottom: 24px; width: 100%; box-sizing: border-box;">
        <h1 style="font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 8px; letter-spacing: -0.02em;">${escapeHtml(h1Text)}</h1>
        <p style="font-size: 15px; color: #4B5563; line-height: 1.6; margin-bottom: 0; width: 100%; max-width: 100%;">${escapeHtml(introText)}</p>
      </div>
    `;

    // JSON-LD Schemas
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
      "url": canonicalUrl
    };

    const faqSchema = {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": `Where can I buy used ${categoryName.toLowerCase()} in ${regionName}?`,
          "acceptedAnswer": {
            "@type": "Answer",
            "text": `You can browse ${itemCount} verified local secondhand ${categoryName.toLowerCase()} listings in ${regionName} on Moonoh, combining direct user uploads with aggregated listings from Karrot and HeyKorean.`
          }
        }
      ]
    };

    // If this is an external-only (/others) page, add noindex meta tag to head
    const robotsMeta = isOthersPage ? '\n  <meta name="robots" content="noindex, follow"/>' : '';

    const schemaScript = `
  <script type="application/ld+json">${JSON.stringify(itemListSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(collectionSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(faqSchema)}</script>
  <script>window.__INITIAL_ITEMS__ = ${JSON.stringify(filteredItems)};</script>
`;

    // Inject Title, Canonical & Schemas into <head>
    template = template
      .replace(/<title>.*?<\/title>/i, `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(/<meta content=".*?" name="description"\/>/i, `<meta content="${escapeHtml(introText)}" name="description"/>`)
      .replace(/<link href=".*?" rel="canonical"\/>/i, `<link href="${canonicalUrl}" rel="canonical"/>`)
      .replace('</head>', `${schemaScript}${robotsMeta}</head>`);

    // On aggregation landing pages, hide source tab switcher to avoid UI confusion
    if (!isMainUserEntrypoint) {
      template = template.replace(
        'id="source-segment-wrap"',
        'id="source-segment-wrap" style="display:none;"'
      );
    }

    // Inject Hero Section & Grid HTML directly
    template = template.replace(
      '<div class="item-grid" id="moonoh-item-grid">',
      `${heroHtml}\n<div class="item-grid" id="moonoh-item-grid">\n${cardsHtml}`
    );

    // Inject Interlinking Links before footer
    template = template.replace('</main>', `${interlinkingHtml}\n</main>`);

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
