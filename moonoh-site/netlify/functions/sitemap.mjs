import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { realFoodRescueItems } from './food-rescue-items.mjs';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

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

  return `https://moon-oh.com/item/${cleanTitle}-${locSlug}-${productNo}`;
}

let cachedXml = null;
let lastCacheTimestamp = 0;
const CACHE_DURATION_MS = 3600000; // 1 hour cache for sitemap

async function buildSitemapXml() {
  const itemUrls = [];

  // Add Kim C Market Food Rescue items
  if (Array.isArray(realFoodRescueItems)) {
    realFoodRescueItems.forEach(item => {
      if (item && item.id) {
        let cleanTitle = (item.title || 'item')
          .toLowerCase()
          .replace(/[^a-z0-9\s-]/g, '')
          .trim()
          .replace(/\s+/g, '-')
          .replace(/-+/g, '-');
        if (cleanTitle.length > 50) cleanTitle = cleanTitle.substring(0, 50).replace(/-$/, '');
        itemUrls.push(`https://moon-oh.com/item/${cleanTitle}-brooklyn-ny-ext-${item.id}`);
      }
    });
  }

  // Add Local Shops items
  try {
    const jsonPath = path.join(currentDir, '../../local_shops_data.json');
    if (fs.existsSync(jsonPath)) {
      const localDb = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      (localDb.products || []).forEach(p => {
        if (p.slug && p.shop_id) {
          itemUrls.push(`https://moon-oh.com/local-product/${p.shop_id}/${p.slug}`);
        }
      });
      Object.keys(localDb.shops || {}).forEach(sSlug => {
        itemUrls.push(`https://moon-oh.com/local-shops/${sSlug}`);
      });
    }
  } catch (e) {}

  try {
    const res = await fetch("https://moon-oh.com/api/items", {
      signal: AbortSignal.timeout(8000)
    });
    if (res.ok) {
      const items = await res.json();
      if (Array.isArray(items)) {
        items.forEach(item => {
          if (item) {
            const itemNo = item.no || item.id;
            const itemTitle = item.title || 'item';
            const itemLoc = item.location || item.townName || 'NYC';
            const slug = item.url ? `https://moon-oh.com${item.url}` : generateSlug(itemTitle, itemLoc, itemNo);
            itemUrls.push(slug);
          }
        });
      }
    }
  } catch (e) {
    console.warn("Backend fetch warning in sitemap.mjs, serving aggregation and static URLs:", e.message);
  }

  const regionSlugs = ['manhattan', 'queens', 'brooklyn', 'bronx', 'staten-island', 'bergen-county', 'hudson-county'];
  const categorySlugs = ['food-groceries', 'electronics', 'furniture', 'womens-fashion', 'mens-fashion', 'shoes', 'home-garden', 'health-beauty', 'pet-supplies', 'baby-kids', 'sports-leisure', 'toys-games', 'jewelry-watches', 'luggages-bags', 'antiques', 'arts-books-music', 'used-items', 'other'];

  const aggregationUrls = [];
  regionSlugs.forEach(r => aggregationUrls.push(`https://moon-oh.com/explore/${r}`));
  categorySlugs.forEach(c => aggregationUrls.push(`https://moon-oh.com/explore/${c}`));
  regionSlugs.forEach(r => {
    categorySlugs.forEach(c => {
      aggregationUrls.push(`https://moon-oh.com/explore/${r}/${c}`);
    });
  });

  const staticUrls = [
    'https://moon-oh.com/',
    'https://moon-oh.com/explore',
    'https://moon-oh.com/explore/food-rescue',
    'https://moon-oh.com/explore/local-shops',
    'https://moon-oh.com/explore/marketplaces',
    'https://moon-oh.com/about',
    'https://moon-oh.com/press',
    'https://moon-oh.com/contact',
    'https://moon-oh.com/terms',
    'https://moon-oh.com/privacy',
    'https://moon-oh.com/disclaimer',
    'https://moon-oh.com/fraud-prevention',
    'https://moon-oh.com/return-policy'
  ];

  const todayIso = new Date().toISOString();

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${todayIso}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>`).join('\n')}
${aggregationUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${todayIso}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>`).join('\n')}
${itemUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${todayIso}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.7</priority>\n  </url>`).join('\n')}
</urlset>`;

  return xml;
}

export default async (req, context) => {
  const now = Date.now();
  if (cachedXml && (now - lastCacheTimestamp) < CACHE_DURATION_MS) {
    return new Response(cachedXml, {
      status: 200,
      headers: {
        "Content-Type": "application/xml; charset=utf-8",
        "Cache-Control": "public, max-age=3600, s-maxage=3600"
      }
    });
  }

  try {
    const xml = await buildSitemapXml();
    cachedXml = xml;
    lastCacheTimestamp = now;

    return new Response(xml, {
      status: 200,
      headers: {
        "Content-Type": "application/xml; charset=utf-8",
        "Cache-Control": "public, max-age=3600, s-maxage=3600"
      }
    });
  } catch (error) {
    console.error("sitemap.mjs error:", error);
    if (cachedXml) {
      return new Response(cachedXml, {
        status: 200,
        headers: { "Content-Type": "application/xml; charset=utf-8" }
      });
    }
    const todayIso = new Date().toISOString();
    const fallbackXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://moon-oh.com/</loc><lastmod>${todayIso}</lastmod><priority>1.0</priority></url>
  <url><loc>https://moon-oh.com/explore</loc><lastmod>${todayIso}</lastmod><priority>0.9</priority></url>
</urlset>`;
    return new Response(fallbackXml, {
      status: 200,
      headers: { "Content-Type": "application/xml; charset=utf-8" }
    });
  }
};

export const config = {
  path: "/sitemap.xml"
};
