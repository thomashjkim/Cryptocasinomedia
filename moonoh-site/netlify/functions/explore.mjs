import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

// Serverless Cache for Items
let cachedItems = null;
let lastFetchTime = 0;
const CACHE_TTL_MS = 15 * 1000; // 15 seconds cache for instant app upload updates

async function fetchAllItems() {
  const now = Date.now();
  if (cachedItems && (now - lastFetchTime) < CACHE_TTL_MS) {
    return cachedItems;
  }

  try {
    const listRes = await fetch("https://moon-oh.com/api/items");
    const itemsData = await listRes.json();

    if (Array.isArray(itemsData) && itemsData.length > 0) {
      const items = itemsData.map(raw => {
        const id = raw.no || raw.id;
        const title = raw.title || "Secondhand Item";
        const price = raw.price || 0;
        const photo = raw.image || 'https://moon-oh.com/images/common/ico_profile_empty.png';
        const townName = raw.location || 'NYC, NY';
        const rawTown = raw.rawTown || raw.location || '';
        const categoryName = raw.category || 'General';
        const detailUrl = raw.url ? `https://moon-oh.com${raw.url}` : `https://moon-oh.com/item/item-${id}`;

        return { id, title, price, photo, townName, rawTown, categoryName, detailUrl };
      });

      cachedItems = items;
      lastFetchTime = now;
      return items;
    }
  } catch (err) {
    console.error("Error fetching items in explore.mjs:", err);
  }

  return cachedItems || [];
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
    const items = await fetchAllItems();
    let template = getExploreTemplate();

    if (!template) {
      return new Response("Error reading explore.html template", { status: 500 });
    }

    // Generate SSR Item Grid HTML for first 30 items
    const initialItems = items.slice(0, 36);
    let cardsHtml = '';
    initialItems.forEach(item => {
      const priceStr = item.price > 0 ? `$${item.price}` : 'Free';
      cardsHtml += `
        <div class="item-card" onclick="location.href='${item.detailUrl}'" style="cursor:pointer;">
          <div class="item-card-img-wrap">
            <img src="${escapeHtml(item.photo)}" alt="${escapeHtml(item.title)}" class="item-card-img" loading="lazy"/>
          </div>
          <div class="item-card-info">
            <div class="item-card-price">${priceStr}</div>
            <div class="item-card-title">${escapeHtml(item.title)}</div>
            <div class="item-card-location">${escapeHtml(item.townName)}</div>
          </div>
        </div>
      `;
    });

    // Generate ItemList JSON-LD schema
    const itemListSchema = {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Explore Secondhand Items in NYC & NJ",
      "description": "Browse hundreds of verified local secondhand items in NYC & NJ on Moonoh.",
      "numberOfItems": items.length,
      "itemListElement": initialItems.map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "name": item.title,
        "url": item.detailUrl,
        "image": item.photo
      }))
    };

    const schemaScript = `\n  <script type="application/ld+json">\n  ${JSON.stringify(itemListSchema, null, 2)}\n  </script>\n  <script>window.__INITIAL_ITEMS__ = ${JSON.stringify(items)};</script>\n`;

    // Inject JSON-LD & window.__INITIAL_ITEMS__ into head
    template = template.replace('</head>', `${schemaScript}</head>`);

    // Inject cardsHtml into #moonoh-item-grid
    template = template.replace(
      '<div class="item-grid" id="moonoh-item-grid">',
      `<div class="item-grid" id="moonoh-item-grid">\n${cardsHtml}`
    );

    return new Response(template, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=300, s-maxage=600, stale-while-revalidate=1200"
      }
    });

  } catch (error) {
    console.error("Error in explore.mjs SSR:", error);
    // Fallback to static explore.html
    const exploreHtmlPath = path.join(process.cwd(), 'explore.html');
    const html = fs.readFileSync(exploreHtmlPath, 'utf-8');
    return new Response(html, {
      status: 200,
      headers: { "Content-Type": "text/html; charset=utf-8" }
    });
  }
};
