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
  const loginParams = new URLSearchParams();
  loginParams.append('kind', 'login');
  loginParams.append('id', 'admin');
  loginParams.append('password', '1234');

  const loginRes = await fetch("http://52.44.113.58:8080/admin.do", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: loginParams
  });

  const cookieHeader = loginRes.headers.get('set-cookie') || '';
  const cookies = cookieHeader.split(';')[0] || '';

  const dataParams = new URLSearchParams();
  dataParams.append('kind', 'getProductArray');
  dataParams.append('page', '0');
  dataParams.append('viewCount', '1000');

  const dataRes = await fetch("http://52.44.113.58:8080/admin.do", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Cookie": cookies
    },
    body: dataParams
  });

  const data = await dataRes.json();
  const rawItems = (data && data.productArray)
    ? data.productArray.filter(item => item && item.isShow === "Y")
    : [];

  // Fetch detail address for exact URL slugs in batches of 80
  const chunkSize = 80;
  const itemUrls = [];

  for (let i = 0; i < rawItems.length; i += chunkSize) {
    const chunk = rawItems.slice(i, i + chunkSize);
    const chunkResults = await Promise.all(
      chunk.map(async (item) => {
        let rawLocStr = item.productTownName || "";
        try {
          const detailParams = new URLSearchParams();
          detailParams.append('kind', 'getProductDetail');
          detailParams.append('productNo', item.no);

          const detailRes = await fetch("http://52.44.113.58:8080/app.do", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: detailParams
          });
          const detailData = await detailRes.json();
          if (detailData && (detailData.address || detailData.productTownName)) {
            rawLocStr = detailData.address || detailData.productTownName;
          }
        } catch (e) {}

        return generateSlug(item.title, rawLocStr, item.no);
      })
    );
    itemUrls.push(...chunkResults);
  }

  const regionSlugs = ['manhattan', 'queens', 'brooklyn', 'bronx', 'staten-island', 'bergen-county', 'hudson-county'];
  const categorySlugs = ['electronics', 'furniture', 'womens-fashion', 'mens-fashion', 'shoes', 'home-garden', 'health-beauty', 'pet-supplies', 'baby-kids', 'sports-leisure', 'toys-games', 'jewelry-watches', 'luggages-bags', 'antiques', 'arts-books-music', 'used-items', 'other'];

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
    'https://moon-oh.com/about',
    'https://moon-oh.com/press',
    'https://moon-oh.com/contact',
    'https://moon-oh.com/terms',
    'https://moon-oh.com/privacy',
    'https://moon-oh.com/disclaimer',
    'https://moon-oh.com/fraud-prevention'
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>`).join('\n')}
${aggregationUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>`).join('\n')}
${itemUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>`).join('\n')}
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
    return new Response(`Error generating sitemap: ${error.message}`, { status: 500 });
  }
};

export const config = {
  path: "/sitemap.xml"
};
