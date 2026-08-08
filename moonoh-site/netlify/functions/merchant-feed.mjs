// Google Merchant Center RSS 2.0 XML Product Feed
// Served at: https://moon-oh.com/merchant-feed.xml
// Format: Google Shopping compatible RSS 2.0 with g: namespace

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

// Map Moonoh categories to Google Product Category IDs
function getGoogleCategory(categoryName) {
  const cat = (categoryName || '').toLowerCase();
  if (cat.includes('women') || cat.includes('men') || cat.includes('clothing') || cat.includes('fashion') || cat.includes('skirt') || cat.includes('shirt') || cat.includes('pants') || cat.includes('dress')) return 'Apparel & Accessories > Clothing';
  if (cat.includes('shoe') || cat.includes('boot') || cat.includes('sneaker') || cat.includes('heel')) return 'Apparel & Accessories > Shoes';
  if (cat.includes('bag') || cat.includes('luggage') || cat.includes('purse') || cat.includes('backpack') || cat.includes('wallet') || cat.includes('pouch')) return 'Apparel & Accessories > Handbags, Wallets & Cases';
  if (cat.includes('jewelry') || cat.includes('necklace') || cat.includes('ring') || cat.includes('bracelet') || cat.includes('earring')) return 'Apparel & Accessories > Jewelry';
  if (cat.includes('watch')) return 'Apparel & Accessories > Jewelry > Watches';
  if (cat.includes('electronic') || cat.includes('phone') || cat.includes('laptop') || cat.includes('computer') || cat.includes('tablet') || cat.includes('camera')) return 'Electronics';
  if (cat.includes('furniture') || cat.includes('sofa') || cat.includes('chair') || cat.includes('table') || cat.includes('desk') || cat.includes('bed')) return 'Furniture';
  if (cat.includes('toy') || cat.includes('game') || cat.includes('kids') || cat.includes('baby') || cat.includes('child')) return 'Toys & Games';
  if (cat.includes('book') || cat.includes('magazine')) return 'Media > Books';
  if (cat.includes('sport') || cat.includes('fitness') || cat.includes('gym') || cat.includes('outdoor')) return 'Sporting Goods';
  if (cat.includes('beauty') || cat.includes('health') || cat.includes('skincare') || cat.includes('makeup') || cat.includes('cosmetic')) return 'Health & Beauty';
  if (cat.includes('kitchen') || cat.includes('cookware') || cat.includes('appliance') || cat.includes('home')) return 'Home & Garden';
  if (cat.includes('art') || cat.includes('craft') || cat.includes('music') || cat.includes('instrument')) return 'Arts & Entertainment';
  if (cat.includes('pet') || cat.includes('dog') || cat.includes('cat')) return 'Animals & Pet Supplies';
  if (cat.includes('car') || cat.includes('vehicle') || cat.includes('auto')) return 'Vehicles & Parts';
  return 'Apparel & Accessories'; // default safe fallback for secondhand marketplace
}

function escapeXml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

// Global cache to avoid hammering the backend on every request
let cachedXml = null;
let cacheTimestamp = 0;
const CACHE_DURATION_MS = 3600000; // 1 hour cache - Google only fetches once a day anyway

async function buildFeed() {
  // 1. Login to admin
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

  // 2. Get product list
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

  // 3. Fetch details for each item in batches of 50
  const chunkSize = 50;
  const feedItems = [];

  for (let i = 0; i < rawItems.length; i += chunkSize) {
    const chunk = rawItems.slice(i, i + chunkSize);
    const chunkResults = await Promise.all(
      chunk.map(async (item) => {
        let realPrice = item.price || 0;
        let rawLocStr = item.productTownName || "";
        let description = item.title || "";
        let imageUrl = "";
        let categoryName = item.categoryName || "";

        try {
          const detailParams = new URLSearchParams();
          detailParams.append('kind', 'getProductDetail');
          detailParams.append('productNo', item.no);

          const detailRes = await fetch("http://52.44.113.58:8080/app.do", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: detailParams
          });
          const d = await detailRes.json();

          if (d) {
            if (typeof d.price === 'number') realPrice = d.price;
            if (d.content) description = d.content;
            if (d.address || d.productTownName) rawLocStr = d.address || d.productTownName;
            if (d.categoryName) categoryName = d.categoryName;

            // Get full-resolution main image (not thumbnail)
            if (d.strPictureUrlArray) {
              try {
                const arr = JSON.parse(d.strPictureUrlArray);
                if (arr.length > 0) {
                  const path = arr[0].fileUrl || "";
                  imageUrl = `https://moon-oh.com/image-proxy/${path}`;
                }
              } catch (e) {}
            }
            if (!imageUrl && d.pictureUrl) {
              imageUrl = `https://moon-oh.com/image-proxy/${d.pictureUrl}`;
            }
          }
        } catch (e) {}

        // Fallback thumbnail image
        if (!imageUrl && item.pictureUrl) {
          const parts = item.pictureUrl.split('/');
          const fileName = parts.pop();
          const path = parts.join('/') + '/';
          const dotIndex = fileName.lastIndexOf('.');
          const thumbnailName = "thumbnail_" + (dotIndex !== -1 ? fileName.substring(0, dotIndex) : fileName) + ".jpg";
          imageUrl = `https://moon-oh.com/image-proxy/${path}${thumbnailName}`;
        }

        const productUrl = generateSlug(item.title, rawLocStr, item.no);
        const googleCategory = getGoogleCategory(categoryName);

        // Build town display string
        let townDisplay = rawLocStr || "New York, NY";
        if (townDisplay.includes(',')) {
          const parts = townDisplay.split(',').map(p => p.trim());
          townDisplay = parts.slice(0, 2).join(', ');
        }

        return {
          id: `moonoh-${item.no}`,
          title: item.title || "Secondhand Item",
          description: description,
          link: productUrl,
          imageUrl: imageUrl,
          price: realPrice,
          categoryName: categoryName,
          googleCategory: googleCategory,
          condition: "used",
          availability: "in_stock",
          brand: "Moonoh",
          location: townDisplay
        };
      })
    );
    feedItems.push(...chunkResults);
  }

  // 4. Build RSS 2.0 XML with Google Shopping namespace
  const now = new Date().toUTCString();
  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Moonoh Marketplace - New York City Secondhand Items</title>
    <link>https://moon-oh.com</link>
    <description>Buy and sell secondhand items locally in Queens, Brooklyn, Manhattan, and New York City. Moonoh connects your neighborhood for smart decluttering and amazing discoveries.</description>
    <language>en-us</language>
    <lastBuildDate>${now}</lastBuildDate>
`;

  for (const item of feedItems) {
    // Skip items with no image (Google requires image)
    if (!item.imageUrl) continue;
    // Skip items with price = 0 (Google Merchant Center requires a price for standard listings)
    const priceVal = parseFloat(item.price) || 0;
    const priceStr = priceVal > 0 ? `${priceVal.toFixed(2)} USD` : "1.00 USD"; // use $1 minimum for free items

    xml += `
    <item>
      <g:id>${escapeXml(item.id)}</g:id>
      <g:title>${escapeXml(item.title)}</g:title>
      <g:description>${escapeXml(item.description.substring(0, 5000))}</g:description>
      <g:link>${escapeXml(item.link)}</g:link>
      <g:image_link>${escapeXml(item.imageUrl)}</g:image_link>
      <g:price>${escapeXml(priceStr)}</g:price>
      <g:condition>${escapeXml(item.condition)}</g:condition>
      <g:availability>${escapeXml(item.availability)}</g:availability>
      <g:product_type>${escapeXml(item.categoryName)}</g:product_type>
      <g:google_product_category>${escapeXml(item.googleCategory)}</g:google_product_category>
      <g:brand>${escapeXml(item.brand)}</g:brand>
      <g:identifier_exists>no</g:identifier_exists>
      <g:shipping>
        <g:country>US</g:country>
        <g:service>Local Pickup</g:service>
        <g:price>0.00 USD</g:price>
      </g:shipping>
      <g:shipping_label>local_pickup</g:shipping_label>
    </item>`;
  }

  xml += `
  </channel>
</rss>`;

  return xml;
}

export default async (req, context) => {
  const now = Date.now();

  // Return cached XML if fresh (1 hour cache)
  if (cachedXml && (now - cacheTimestamp) < CACHE_DURATION_MS) {
    return new Response(cachedXml, {
      status: 200,
      headers: {
        "Content-Type": "application/rss+xml; charset=UTF-8",
        "Cache-Control": "public, max-age=3600, s-maxage=3600",
        "Access-Control-Allow-Origin": "*"
      }
    });
  }

  try {
    const xml = await buildFeed();
    cachedXml = xml;
    cacheTimestamp = Date.now();

    return new Response(xml, {
      status: 200,
      headers: {
        "Content-Type": "application/rss+xml; charset=UTF-8",
        "Cache-Control": "public, max-age=3600, s-maxage=3600",
        "Access-Control-Allow-Origin": "*"
      }
    });
  } catch (error) {
    console.error("merchant-feed.mjs error:", error);
    // Return a minimal valid feed on error so Google doesn't mark the feed as broken
    const errorXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Moonoh Marketplace</title>
    <link>https://moon-oh.com</link>
    <description>Moonoh local secondhand marketplace</description>
  </channel>
</rss>`;
    return new Response(cachedXml || errorXml, {
      status: 200,
      headers: {
        "Content-Type": "application/rss+xml; charset=UTF-8"
      }
    });
  }
};

export const config = {
  path: "/merchant-feed.xml"
};
