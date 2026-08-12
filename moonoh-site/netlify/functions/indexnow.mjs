import { realFoodRescueItems } from './food-rescue-items.mjs';

export default async (req, context) => {
  const host = "moon-oh.com";
  const key = "4b0a388c30674918af2d3a180e35a053";
  const keyLocation = `https://${host}/${key}.txt`;

  const urlList = [
    `https://${host}/`,
    `https://${host}/explore`,
    `https://${host}/explore/brooklyn`,
    `https://${host}/sitemap.xml`,
    `https://${host}/sitemap-food-rescue.xml`
  ];

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
        urlList.push(`https://${host}/item/${cleanTitle}-brooklyn-ny-ext-${item.id}`);
      }
    });
  }

  const payload = {
    host: host,
    key: key,
    keyLocation: keyLocation,
    urlList: urlList
  };

  let bingStatus = 0;
  try {
    const res = await fetch("https://api.indexnow.org/indexnow", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify(payload)
    });
    bingStatus = res.status;
  } catch (e) {
    console.error("IndexNow ping error:", e);
  }

  return new Response(JSON.stringify({
    success: true,
    bingStatus: bingStatus,
    pingedUrlsCount: urlList.length,
    keyLocation: keyLocation
  }), {
    status: 200,
    headers: { "Content-Type": "application/json; charset=utf-8" }
  });
};
