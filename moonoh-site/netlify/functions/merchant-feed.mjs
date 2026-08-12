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

// Convert raw image paths to valid HTTPS thumbnail URLs supported by Google Merchant Center
function convertToJpgUrl(rawPath) {
  if (!rawPath) return "";
  
  if (rawPath.startsWith('http://52.44.113.58')) {
    const relativePath = rawPath.replace(/^http:\/\/52\.44\.113\.58:8080\//, '');
    return convertToJpgUrl(relativePath);
  }

  if (rawPath.startsWith('https://')) {
    return rawPath;
  }

  const parts = rawPath.split('/');
  const fileName = parts.pop();
  const path = parts.join('/') + (parts.length ? '/' : '');
  const dotIndex = fileName.lastIndexOf('.');
  const baseName = dotIndex !== -1 ? fileName.substring(0, dotIndex) : fileName;

  return `https://moon-oh.com/image-proxy/${path}thumbnail_${baseName}.jpg`;
}

// Filter out policy-violating items (tobacco, prescription drugs, weapons, adult, counterfeit, etc.)
function isPolicyViolatingItem(title, description, categoryName) {
  const t = (title + " " + description + " " + categoryName).toLowerCase();
  
  // 1. Tobacco & Nicotine Products (strictly prohibited)
  if (t.includes("marlboro") || t.includes("tobacco") || t.includes("cigarette") || t.includes("cigar") || t.includes("vape") || t.includes("nicotine") || t.includes("cbd") || t.includes("e-cig")) {
    return true;
  }
  
  // 2. Prescription Drugs, Pet Pharmaceuticals & Medical Devices
  if (t.includes("cosequin") || t.includes("prescription") || t.includes("pharmaceutical") || t.includes("antibiotic") || t.includes("cpap") || t.includes("syringe") || t.includes("needle")) {
    return true;
  }

  // 3. Weapons, Ammunition & Explosives
  if (t.includes("gun") || t.includes("rifle") || t.includes("pistol") || t.includes("firearm") || t.includes("ammo") || t.includes("bullet") || t.includes("knife") || t.includes("sword") || t.includes("weapon") || t.includes("explosive") || t.includes("firework") || t.includes("pepper spray")) {
    // Exceptions for toys or kitchen knives might be needed, but broad filter is safer for GMC compliance.
    if (!t.includes("toy") && !t.includes("water gun") && !t.includes("kitchen knife") && !t.includes("chef knife")) {
      return true;
    }
  }

  // 4. Adult Content & Inappropriate Content
  if (t.includes("porn") || t.includes("sex toy") || t.includes("vibrator") || t.includes("dildo") || t.includes("erotic") || t.includes("fetish")) {
    return true;
  }

  // 5. Counterfeit & Fake Goods
  if (t.includes("fake") || t.includes("replica") || t.includes("knockoff") || t.includes("counterfeit") || t.includes("clone")) {
    return true;
  }

  // 6. Alcohol
  if (t.includes("alcohol") || t.includes("liquor") || t.includes("whiskey") || t.includes("vodka") || t.includes("rum") || t.includes("beer") || t.includes("wine")) {
    // Exclude wine glasses or racks
    if (!t.includes("glass") && !t.includes("rack") && !t.includes("cooler") && !t.includes("opener")) {
      return true;
    }
  }

  // 7. Live Animals
  if (t.includes("live animal") || t.includes("puppy for sale") || t.includes("kitten for sale")) {
    return true;
  }

  return false;
}

// Map Moonoh categories and product title to exact Google Product Category strings
function getGoogleCategory(categoryName, title) {
  const cat = (categoryName || '').toLowerCase();
  const t = (title || '').toLowerCase();

  // 1. Skincare Cleansers & Cosmetics (prevent prescription drug misclassification)
  if (t.includes('cleanser') || t.includes('toner') || t.includes('serum') || t.includes('moisturizer') || t.includes('cream') || t.includes('mask') || cat.includes('beauty')) {
    return 'Health & Beauty > Skincare > Facial Cleansers';
  }
  // 2. Camera & Optical Accessories (lenses, filters, tripods, etc.)
  if (t.includes('lens') || t.includes('filter') || t.includes('tripod') || t.includes('camera') || cat.includes('camera')) {
    return 'Electronics > Cameras & Optics > Camera & Optic Accessories';
  }
  // 3. Musical Instruments & Accessories
  if (t.includes('zither') || t.includes('gayageum') || t.includes('keyboard') || t.includes('piano') || t.includes('guitar') || t.includes('instrument') || t.includes('flute') || t.includes('violin') || t.includes('drum')) {
    return 'Arts & Entertainment > Hobbies & Creative Arts > Musical Instruments';
  }
  // 4. Books & Magazines
  if (t.includes('book') || t.includes('novel') || t.includes('textbook') || t.includes('magazine') || t.includes('manual')) {
    return 'Media > Books';
  }
  // 5. Visual Arts & Collectibles
  if (t.includes('painting') || t.includes('artwork') || t.includes('sculpture') || t.includes('kaws') || t.includes('figurine') || t.includes('collectible') || t.includes('souvenir') || cat.includes('antique')) {
    return 'Arts & Entertainment > Visual Arts';
  }
  // 6. Clothing & Apparel
  if (cat.includes('women') || cat.includes('men') || cat.includes('clothing') || cat.includes('fashion') || cat.includes('skirt') || cat.includes('shirt') || cat.includes('pants') || cat.includes('dress') || cat.includes('jacket') || cat.includes('coat') || cat.includes('sweater') || cat.includes('hoodie') || cat.includes('top') || cat.includes('vest') || cat.includes('beanie') || cat.includes('cap') || cat.includes('socks')) {
    return 'Apparel & Accessories > Clothing';
  }
  // 7. Shoes
  if (cat.includes('shoe') || cat.includes('boot') || cat.includes('sneaker') || cat.includes('heel') || cat.includes('sandal') || cat.includes('loafer') || t.includes('shoes') || t.includes('sneakers')) {
    return 'Apparel & Accessories > Shoes';
  }
  // 8. Handbags & Bags
  if (cat.includes('bag') || cat.includes('luggage') || cat.includes('purse') || cat.includes('backpack') || cat.includes('wallet') || cat.includes('pouch') || cat.includes('clutch') || t.includes('backpack') || t.includes('tote') || t.includes('clutch') || t.includes('bag')) {
    return 'Apparel & Accessories > Handbags, Wallets & Cases';
  }
  // 9. Jewelry & Watches
  if (cat.includes('jewelry') || cat.includes('necklace') || cat.includes('ring') || cat.includes('bracelet') || cat.includes('earring') || cat.includes('watch') || t.includes('ring') || t.includes('necklace') || t.includes('watch')) {
    return 'Apparel & Accessories > Jewelry';
  }
  // 10. Electronics & Appliances
  if (cat.includes('electronic') || cat.includes('phone') || cat.includes('laptop') || cat.includes('computer') || cat.includes('tablet') || t.includes('iphone') || t.includes('ipad') || t.includes('airpods') || t.includes('tv') || t.includes('ssd') || t.includes('headphone') || t.includes('speaker') || t.includes('monitor') || t.includes('kettle') || t.includes('iron') || t.includes('vacuum') || t.includes('curling') || t.includes('cooker')) {
    return 'Electronics';
  }
  // 11. Furniture
  if (cat.includes('furniture') || cat.includes('sofa') || cat.includes('chair') || cat.includes('table') || cat.includes('desk') || cat.includes('bed') || cat.includes('shelf') || cat.includes('drawer') || cat.includes('nightstand') || t.includes('table') || t.includes('chair') || t.includes('desk') || t.includes('shelf')) {
    return 'Furniture';
  }
  // 12. Toys & Games
  if (cat.includes('toy') || cat.includes('game') || cat.includes('kids') || cat.includes('baby') || cat.includes('child') || t.includes('figure') || t.includes('toy') || t.includes('puzzle') || t.includes('mat')) {
    return 'Toys & Games';
  }
  // 13. Sporting Goods
  if (cat.includes('sport') || cat.includes('fitness') || cat.includes('gym') || cat.includes('outdoor') || t.includes('golf') || t.includes('racket') || t.includes('ball') || t.includes('roller')) {
    return 'Sporting Goods';
  }
  // 14. Home & Garden
  if (cat.includes('kitchen') || cat.includes('cookware') || cat.includes('appliance') || cat.includes('home') || cat.includes('diy') || t.includes('mug') || t.includes('cup') || t.includes('lamp') || t.includes('rod') || t.includes('candle')) {
    return 'Home & Garden';
  }
  // 15. Animals & Pet Supplies
  if (cat.includes('pet') || cat.includes('dog') || cat.includes('cat') || t.includes('dog') || t.includes('cat') || t.includes('treat') || t.includes('leash') || t.includes('harness')) {
    return 'Animals & Pet Supplies';
  }

  return 'Apparel & Accessories';
}

// Auto-extract required Google Merchant fashion attributes: age_group, gender, color, size
function extractFashionAttributes(title, categoryName) {
  const t = (title || '').toLowerCase();
  
  // Age Group
  let ageGroup = "adult";
  if (t.includes('kids') || t.includes('baby') || t.includes('child') || t.includes('toddler') || t.includes('infant') || t.includes('youth')) {
    ageGroup = "kids";
  }

  // Gender
  let gender = "unisex";
  if (t.includes('women') || t.includes('womens') || t.includes('female') || t.includes('lady') || t.includes('ladies')) {
    gender = "female";
  } else if (t.includes('men') || t.includes('mens') || t.includes('male') || t.includes('man')) {
    gender = "male";
  }

  // Color
  let color = "Multicolor";
  const colors = ["black", "white", "gray", "grey", "blue", "red", "green", "yellow", "brown", "pink", "purple", "orange", "silver", "gold", "beige", "navy", "tan", "coral", "cream"];
  for (const c of colors) {
    if (t.includes(c)) {
      color = c.charAt(0).toUpperCase() + c.slice(1);
      break;
    }
  }

  // Size
  let size = "Regular";
  const sizeMatch = t.match(/\b(size\s*[:\s]*([0-9\.\s\/a-z]+)|xs|s|m|l|xl|xxl|2xl|3xl|[0-9]+(?:\.[0-9]+)?\s*(?:us|uk|eu)?)\b/i);
  if (sizeMatch) {
    size = sizeMatch[0].toUpperCase();
  }

  return { ageGroup, gender, color, size };
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

let cachedXml = null;
let cacheTimestamp = 0;
const CACHE_DURATION_MS = 3600000;

async function buildFeed() {
  let feedItems = [];

  try {
    const res = await fetch("https://moon-oh.com/api/items", {
      signal: AbortSignal.timeout(10000)
    });
    if (res.ok) {
      const items = await res.json();
      if (Array.isArray(items)) {
        items.forEach(item => {
          if (!item) return;
          const itemNo = item.no || item.id;
          const itemTitle = item.title || "Secondhand Item";
          const description = item.description || itemTitle;
          const categoryName = item.categoryName || item.category || "General";
          const rawLocStr = item.location || item.townName || "NYC, NY";
          const realPrice = item.price || 0;
          const rawPhotoPath = item.photo || item.image || "";

          if (isPolicyViolatingItem(itemTitle, description, categoryName)) return;

          const imageUrl = convertToJpgUrl(rawPhotoPath);
          const productUrl = generateSlug(itemTitle, rawLocStr, itemNo);
          const googleCategory = getGoogleCategory(categoryName, itemTitle);
          const fashionAttr = extractFashionAttributes(itemTitle, categoryName);

          let townDisplay = rawLocStr || "New York, NY";
          if (townDisplay.includes(',')) {
            const parts = townDisplay.split(',').map(p => p.trim());
            townDisplay = parts.slice(0, 2).join(', ');
          }

          feedItems.push({
            id: `moonoh-${itemNo}`,
            title: itemTitle,
            description: description,
            link: productUrl,
            imageUrl: imageUrl,
            price: realPrice,
            categoryName: categoryName,
            googleCategory: googleCategory,
            fashionAttr: fashionAttr,
            condition: "used",
            availability: "in_stock",
            brand: "Moonoh",
            location: townDisplay
          });
        });
      }
    }
  } catch (e) {
    console.warn("Backend fetch warning in merchant-feed.mjs:", e.message);
  }

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
    if (!item.imageUrl) continue;
    const priceVal = parseFloat(item.price) || 0;
    const priceStr = priceVal > 0 ? `${priceVal.toFixed(2)} USD` : "1.00 USD";

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
      <g:age_group>${escapeXml(item.fashionAttr.ageGroup)}</g:age_group>
      <g:gender>${escapeXml(item.fashionAttr.gender)}</g:gender>
      <g:color>${escapeXml(item.fashionAttr.color)}</g:color>
      <g:size>${escapeXml(item.fashionAttr.size)}</g:size>
      <g:shipping>
        <g:country>US</g:country>
        <g:service>Local Pickup &amp; Neighborhood Delivery</g:service>
        <g:price>0.00 USD</g:price>
        <g:min_handling_time>0</g:min_handling_time>
        <g:max_handling_time>1</g:max_handling_time>
        <g:min_transit_time>0</g:min_transit_time>
        <g:max_transit_time>2</g:max_transit_time>
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
    cacheTimestamp = now;

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
    if (cachedXml) {
      return new Response(cachedXml, {
        status: 200,
        headers: { "Content-Type": "application/rss+xml; charset=UTF-8" }
      });
    }
    const nowRss = new Date().toUTCString();
    const fallbackRss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
  <channel>
    <title>Moonoh Marketplace</title>
    <link>https://moon-oh.com</link>
    <description>Local Secondhand Marketplace</description>
    <lastBuildDate>${nowRss}</lastBuildDate>
  </channel>
</rss>`;
    return new Response(fallbackRss, {
      status: 200,
      headers: { "Content-Type": "application/rss+xml; charset=UTF-8" }
    });
  }
};

export const config = {
  path: "/merchant-feed.xml"
};
