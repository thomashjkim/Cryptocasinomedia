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

  return `/item/${cleanTitle}-${locSlug}-${productNo}`;
}

// Global in-memory cache for serverless instance reuse
let globalCachedItems = null;
let lastCacheTimestamp = 0;
const CACHE_DURATION_MS = 5 * 60 * 1000; // 5 minutes cache

async function buildFullItemList() {
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
  const rawItems = (data && data.productArray) ? data.productArray.filter(item => item && item.isShow === "Y") : [];
  
  const chunkSize = 80;
  const resultItems = [];
  
  for (let i = 0; i < rawItems.length; i += chunkSize) {
    const chunk = rawItems.slice(i, i + chunkSize);
    const chunkResults = await Promise.all(
      chunk.map(async (item) => {
        let realPrice = item.price || 0;
        let realLocation = item.productTownName ? `1mi · ${item.productTownName}` : "1mi · NYC";
        let rawLocStr = item.productTownName || "";
        let rawTown = item.productTownName || "";
        
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
          
          if (detailData) {
            if (typeof detailData.price === 'number') {
              realPrice = detailData.price;
            }
            if (detailData.productTownName) {
              rawTown = detailData.productTownName;
            }
            const addr = detailData.address || detailData.productTownName || "";
            if (addr) {
              rawLocStr = addr;
              const parts = addr.split(',').map(p => p.trim());
              if (parts.length >= 4) {
                realLocation = `1mi · ${parts[1]}, ${parts[2].split(' ')[0]}`;
              } else if (parts.length >= 3) {
                realLocation = `1mi · ${parts[0]}, ${parts[1].split(' ')[0]}`;
              } else {
                realLocation = `1mi · ${addr}`;
              }
            }
          }
        } catch (e) {}
        
        let img_url = "images/common/ico_profile_empty.png";
        if (item.pictureUrl) {
          const parts = item.pictureUrl.split('/');
          const fileName = parts.pop();
          const path = parts.join('/') + '/';
          const dotIndex = fileName.lastIndexOf('.');
          const thumbnailName = "thumbnail_" + (dotIndex !== -1 ? fileName.substring(0, dotIndex) : fileName) + ".jpg";
          img_url = `/image-proxy/${path}${thumbnailName}`;
        }
        
        const slug = generateSlug(item.title, rawLocStr, item.no);
        
        return {
          no: item.no,
          title: item.title || "",
          price: realPrice,
          location: realLocation,
          rawTown: rawTown,
          image: img_url,
          category: item.categoryName || "",
          url: slug
        };
      })
    );
    resultItems.push(...chunkResults);
  }
  
  globalCachedItems = resultItems;
  lastCacheTimestamp = Date.now();
  return resultItems;
}

export default async (req, context) => {
  const now = Date.now();
  
  // Fast path: Return cached items instantly
  if (globalCachedItems && globalCachedItems.length > 0) {
    if ((now - lastCacheTimestamp) > CACHE_DURATION_MS) {
      buildFullItemList().catch(() => {}); // refresh in background
    }
    return new Response(JSON.stringify(globalCachedItems), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "public, max-age=60, s-maxage=120"
      }
    });
  }

  try {
    const fetchPromise = buildFullItemList();
    const timeoutPromise = new Promise(resolve => setTimeout(() => resolve(null), 1200));
    const items = await Promise.race([fetchPromise, timeoutPromise]);
    
    if (items) {
      return new Response(JSON.stringify(items), {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Cache-Control": "public, max-age=60, s-maxage=120"
        }
      });
    }
    
    // Fast fallback if live 636 HTTP calls take > 1.2s
    fetchPromise.catch(() => {});
    return new Response(JSON.stringify(globalCachedItems || []), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });
  } catch (error) {
    return new Response(JSON.stringify(globalCachedItems || []), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      }
    });
  }
};

export const config = {
  path: "/api/items"
};
