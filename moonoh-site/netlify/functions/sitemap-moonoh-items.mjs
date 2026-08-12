export default async function handler(request) {
  const itemUrls = [];

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
            const itemTitle = (item.title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
            const slug = item.url ? `https://moon-oh.com${item.url}` : `https://moon-oh.com/item/${itemTitle}-nyc-ny-${itemNo}`;
            itemUrls.push(slug);
          }
        });
      }
    }
  } catch (e) {}

  const staticUrls = [
    'https://moon-oh.com/',
    'https://moon-oh.com/explore',
    'https://moon-oh.com/about',
    'https://moon-oh.com/press',
    'https://moon-oh.com/contact',
    'https://moon-oh.com/terms',
    'https://moon-oh.com/privacy',
    'https://moon-oh.com/disclaimer',
    'https://moon-oh.com/fraud-prevention',
    'https://moon-oh.com/return-policy'
  ];

  const now = new Date().toISOString();

  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${now}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>`).join('\n')}
${itemUrls.map(u => `  <url>\n    <loc>${u}</loc>\n    <lastmod>${now}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.7</priority>\n  </url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    status: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600'
    }
  });
}
