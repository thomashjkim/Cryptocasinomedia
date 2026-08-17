// Google Merchant Center Feed Handler
// Moonoh is a person-to-person local secondhand marketplace without online web checkout.
// Per Google Merchant Center guidelines, C2C peer-to-peer listings and external store links
// are not eligible for automated Google Shopping feeds and are excluded from merchant feed output.

export default async (req, context) => {
  const nowRss = new Date().toUTCString();
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Moonoh Local Peer-to-Peer Marketplace</title>
    <link>https://moon-oh.com</link>
    <description>Moonoh is a peer-to-peer neighborhood marketplace for local in-person exchanges without web checkout.</description>
    <lastBuildDate>${nowRss}</lastBuildDate>
  </channel>
</rss>`;

  return new Response(xml, {
    status: 200,
    headers: {
      "Content-Type": "application/rss+xml; charset=UTF-8",
      "Cache-Control": "public, max-age=3600, s-maxage=3600",
      "Access-Control-Allow-Origin": "*"
    }
  });
};

export const config = {
  path: "/merchant-feed.xml"
};
