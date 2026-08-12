import { realFoodRescueItems } from './food-rescue-items.mjs';

export default async (req, context) => {
  const itemUrls = [];

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

  const todayIso = new Date().toISOString();

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${itemUrls.map(url => `  <url>
    <loc>${url}</loc>
    <lastmod>${todayIso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>`).join('\n')}
</urlset>`;

  return new Response(xml, {
    status: 200,
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "public, max-age=3600, s-maxage=3600"
    }
  });
};
