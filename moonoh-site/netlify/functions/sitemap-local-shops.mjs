import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

export default async function handler(request) {
  let localData = { shops: {}, products: [] };
  try {
    const jsonPath = path.join(currentDir, '../../local_shops_data.json');
    if (fs.existsSync(jsonPath)) {
      localData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    }
  } catch (e) {}

  const shops = localData.shops || {};
  const products = localData.products || [];
  const now = new Date().toISOString();

  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://moon-oh.com/explore/local-shops</loc>
    <lastmod>${now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
`;

  // Shop Profile Pages
  for (const shopSlug of Object.keys(shops)) {
    xml += `  <url>
    <loc>https://moon-oh.com/local-shops/${shopSlug}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n`;
  }

  // Local Product Pages
  for (const p of products) {
    if (!p.slug || !p.shop_id) continue;
    xml += `  <url>
    <loc>https://moon-oh.com/local-product/${p.shop_id}/${p.slug}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>\n`;
  }

  xml += `</urlset>`;

  return new Response(xml, {
    status: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=86400, s-maxage=86400'
    }
  });
}
