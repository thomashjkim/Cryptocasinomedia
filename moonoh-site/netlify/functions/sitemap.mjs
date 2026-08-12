import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default async (req, context) => {
  try {
    const xmlPath = path.join(__dirname, '../../sitemap.xml');
    if (fs.existsSync(xmlPath)) {
      const xml = fs.readFileSync(xmlPath, 'utf8');
      return new Response(xml, {
        status: 200,
        headers: {
          "Content-Type": "application/xml; charset=utf-8",
          "Cache-Control": "public, max-age=3600, s-maxage=3600"
        }
      });
    }
  } catch (e) {}

  const todayIso = new Date().toISOString().split('T')[0];
  const fallbackXml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://moon-oh.com/</loc><lastmod>${todayIso}</lastmod><priority>1.0</priority></url>
  <url><loc>https://moon-oh.com/explore</loc><lastmod>${todayIso}</lastmod><priority>0.9</priority></url>
</urlset>`;
  return new Response(fallbackXml, {
    status: 200,
    headers: { "Content-Type": "application/xml; charset=utf-8" }
  });
};

export const config = {
  path: "/sitemap.xml"
};
