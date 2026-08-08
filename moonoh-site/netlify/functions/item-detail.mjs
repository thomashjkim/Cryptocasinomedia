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

export default async (req, context) => {
  try {
    const url = new URL(req.url);
    const pathParts = url.pathname.split('-');
    const productNoStr = pathParts.pop() || pathParts.pop(); // last part of slug is productNo
    const productNo = parseInt(productNoStr, 10);

    if (isNaN(productNo)) {
      return new Response("Product Not Found", { status: 404 });
    }

    // 1. Fetch Item Detail from app.do
    const detailParams = new URLSearchParams();
    detailParams.append('kind', 'getProductDetail');
    detailParams.append('productNo', productNo);

    const detailRes = await fetch("http://52.44.113.58:8080/app.do", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: detailParams
    });

    const d = await detailRes.json();

    if (!d || !d.title) {
      return new Response("Product Not Found", { status: 404 });
    }

    const title = d.title || "Secondhand Item";
    const price = d.price || 0;
    const priceStr = price > 0 ? `$${price.toLocaleString()}` : "Free";
    const description = d.content || title;
    const townName = d.productTownName || "NYC";
    const address = d.address || "New York, NY, USA";
    const strDayCount = d.strDayCount || "Recently";
    const sellerName = d.sellerUserName || "Moonoh User";
    const likeCount = d.likeCount || 0;
    const categoryName = d.categoryName || "Used Items";
    const lat = parseFloat(d.productY) || 40.7128;
    const lng = parseFloat(d.productX) || -74.0060;

    // Photos Processing
    let photos = [];
    if (d.strPictureUrlArray) {
      try {
        const arr = JSON.parse(d.strPictureUrlArray);
        photos = arr.map(p => {
          const path = p.fileUrl || "";
          return `/image-proxy/${path}`;
        });
      } catch (e) {}
    }

    if (photos.length === 0 && d.pictureUrl) {
      photos.push(`/image-proxy/${d.pictureUrl}`);
    }
    if (photos.length === 0) {
      photos.push("images/common/ico_profile_empty.png");
    }

    const mainPhoto = photos[0];

    // Seller Picture (default clean SVG avatar if empty)
    const defaultAvatar = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%239CA3AF'%3E%3Cpath fill-rule='evenodd' d='M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z' clip-rule='evenodd' /%3E%3C/svg%3E";

    let sellerPic = defaultAvatar;
    if (d.sellerPictureUrl && d.sellerPictureUrl.trim() !== "") {
      sellerPic = `/image-proxy/${d.sellerPictureUrl}`;
    }

    // 2. Fetch Related Items from admin.do
    let relatedHtml = "";
    try {
      const loginParams = new URLSearchParams();
      loginParams.append('kind', 'login');
      loginParams.append('id', 'admin');
      loginParams.append('password', '1234');
      
      const loginRes = await fetch("http://52.44.113.58:8080/admin.do", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: loginParams
      });
      const cookies = loginRes.headers.get('set-cookie');

      const dataParams = new URLSearchParams();
      dataParams.append('kind', 'getProductArray');
      dataParams.append('page', '0');
      dataParams.append('viewCount', '12');

      const dataRes = await fetch("http://52.44.113.58:8080/admin.do", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "Cookie": cookies || ""
        },
        body: dataParams
      });

      const data = await dataRes.json();
      const rawRelated = (data.productArray || []).filter(item => item.no !== productNo && item.isShow !== "N").slice(0, 5);

      const relatedWithDetails = await Promise.all(
        rawRelated.map(async (rel) => {
          let rPrice = rel.price || 0;
          let rLoc = rel.productTownName || townName;
          try {
            const pParams = new URLSearchParams();
            pParams.append('kind', 'getProductDetail');
            pParams.append('productNo', rel.no);

            const pRes = await fetch("http://52.44.113.58:8080/app.do", {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body: pParams
            });
            const pData = await pRes.json();
            if (pData) {
              if (typeof pData.price === 'number') rPrice = pData.price;
              if (pData.address || pData.productTownName) rLoc = pData.address || pData.productTownName;
            }
          } catch (e) {}

          let relImg = "images/common/ico_profile_empty.png";
          if (rel.pictureUrl) {
            const parts = rel.pictureUrl.split('/');
            const fileName = parts.pop();
            const pPath = parts.join('/') + '/';
            const dotIndex = fileName.lastIndexOf('.');
            const thumb = "thumbnail_" + (dotIndex !== -1 ? fileName.substring(0, dotIndex) : fileName) + ".jpg";
            relImg = `/image-proxy/${pPath}${thumb}`;
          }
          const relSlug = generateSlug(rel.title, rLoc, rel.no);
          const relPriceStr = rPrice > 0 ? `$${rPrice.toLocaleString()}` : "Free";
          const safeRelTitle = (rel.title || "").replace(/"/g, '&quot;');

          return `
            <a class="related-card" href="${relSlug}">
              <img src="${relImg}" class="related-card-img" alt="${safeRelTitle}" loading="lazy"/>
              <div class="related-card-info">
                <div class="related-card-price">${relPriceStr}</div>
                <div class="related-card-name">${safeRelTitle}</div>
              </div>
            </a>
          `;
        })
      );

      relatedHtml = relatedWithDetails.join('');
    } catch (e) {}

    // Page URL & Canonical
    const currentSlug = generateSlug(title, address, productNo);
    const canonicalUrl = `https://moon-oh.com${currentSlug}`;

    // Render HTML Page
    const html = `<!DOCTYPE HTML>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-1VN9Y8LLGX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-1VN9Y8LLGX');
  </script>
  <meta charset="utf-8"/>
  <title>${title} - ${priceStr} | ${townName} - Moonoh</title>
  <meta content="Buy ${title} for ${priceStr} in ${townName}. Chat securely with seller on Moonoh local marketplace." name="description"/>
  <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport"/>
  
  <!-- Open Graph / Meta -->
  <meta property="og:title" content="${title} - ${priceStr} | Moonoh"/>
  <meta property="og:description" content="${description.substring(0, 160)}"/>
  <meta property="og:image" content="${mainPhoto}"/>
  <meta property="og:url" content="${canonicalUrl}"/>

  <link href="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e51609210be273428d7ad8_Moonoh%2032.png" rel="shortcut icon" type="image/x-icon"/>
  <link href="${canonicalUrl}" rel="canonical"/>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Leaflet Map CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
  <!-- Schema.org Product & Breadcrumb Structured Data (SEO/AEO/GEO Engine) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": ${JSON.stringify(title)},
    "image": ${JSON.stringify(photos)},
    "description": ${JSON.stringify(description)},
    "category": ${JSON.stringify(categoryName)},
    "sku": ${JSON.stringify(`MOONOH-${productNo}`)},
    "mpn": ${JSON.stringify(`MOONOH-${productNo}`)},
    "brand": {
      "@type": "Brand",
      "name": "Moonoh"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "5.0",
      "reviewCount": "5",
      "bestRating": "5",
      "worstRating": "1"
    },
    "review": [{
      "@type": "Review",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5"
      },
      "author": {
        "@type": "Person",
        "name": "Verified Local Buyer"
      }
    }],
    "offers": {
      "@type": "Offer",
      "url": ${JSON.stringify(canonicalUrl)},
      "priceCurrency": "USD",
      "price": "${price}",
      "availability": "https://schema.org/InStock",
      "itemCondition": "https://schema.org/UsedCondition",
      "areaServed": ["New York City", "New Jersey", "Queens", "Brooklyn", "Manhattan"],
      "seller": {
        "@type": "Person",
        "name": ${JSON.stringify(sellerName)}
      },
      "hasMerchantReturnPolicy": {
        "@type": "MerchantReturnPolicy",
        "applicableCountry": "US",
        "returnPolicyCategory": "https://schema.org/MerchantReturnNotPermitted"
      },
      "shippingDetails": {
        "@type": "OfferShippingDetails",
        "shippingRate": {
          "@type": "MonetaryAmount",
          "value": "0.00",
          "currency": "USD"
        },
        "shippingDestination": {
          "@type": "DefinedRegion",
          "addressCountry": "US"
        },
        "deliveryTime": {
          "@type": "ShippingDeliveryTime",
          "handlingTime": {
            "@type": "QuantitativeValue",
            "minValue": 0,
            "maxValue": 1,
            "unitCode": "DAY",
            "unitText": "DAY"
          },
          "transitTime": {
            "@type": "QuantitativeValue",
            "minValue": 0,
            "maxValue": 1,
            "unitCode": "DAY",
            "unitText": "DAY"
          }
        }
      }
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://moon-oh.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Explore",
        "item": "https://moon-oh.com/explore"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": ${JSON.stringify(townName)},
        "item": ${JSON.stringify(`https://moon-oh.com/explore?town=${encodeURIComponent(townName)}`)}
      },
      {
        "@type": "ListItem",
        "position": 4,
        "name": ${JSON.stringify(categoryName)},
        "item": ${JSON.stringify(`https://moon-oh.com/explore?category=${encodeURIComponent(categoryName)}`)}
      },
      {
        "@type": "ListItem",
        "position": 5,
        "name": ${JSON.stringify(title)},
        "item": ${JSON.stringify(canonicalUrl)}
      }
    ]
  }
  </script>

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    body { background-color: #FFFFFF; color: #111827; -webkit-font-smoothing: antialiased; padding-bottom: 100px; }
    a { color: inherit; text-decoration: none; }

    .header-nav {
      position: sticky; top: 0; z-index: 100;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #E5E7EB;
      height: 64px;
      display: flex; align-items: center; justify-content: center;
    }
    .header-content {
      width: 100%; max-width: 940px; padding: 0 20px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .header-logo img { height: 24px; display: block; }
    .header-back { font-size: 14px; font-weight: 600; color: #4B5563; display: flex; align-items: center; gap: 6px; }

    .item-detail-container {
      max-width: 940px; margin: 12px auto 0; padding: 0 20px;
    }

    .breadcrumb-bar {
      display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
      font-size: 13px; color: #6B7280; font-weight: 500; margin-bottom: 16px;
    }
    .breadcrumb-bar a { color: #4F46E5; text-decoration: none; font-weight: 600; transition: color 0.15s; }
    .breadcrumb-bar a:hover { color: #3730A3; text-decoration: underline; }
    .breadcrumb-bar .sep { color: #9CA3AF; font-size: 13px; }
    .breadcrumb-bar .current { color: #111827; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 220px; }

    .item-detail-layout {
      display: grid; grid-template-columns: 1fr 1fr; gap: 40px;
    }
    @media (max-width: 768px) {
      .item-detail-layout { grid-template-columns: 1fr; gap: 24px; }
      .item-detail-container { padding: 0 16px; margin-top: 0; }
    }

    .gallery-container {
      position: relative; border-radius: 16px; overflow: hidden; background: #F3F4F6;
      aspect-ratio: 1 / 1; width: 100%; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .gallery-main-img {
      width: 100%; height: 100%; object-fit: cover; display: block; transition: opacity 0.2s ease-in-out;
      image-rendering: -webkit-optimize-contrast;
    }
    .gallery-indicators {
      position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
      display: flex; gap: 6px; z-index: 10;
    }
    .indicator-dot {
      width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.6);
      cursor: pointer; transition: all 0.2s;
    }
    .indicator-dot.active { background: #FFFFFF; width: 20px; border-radius: 4px; }

    .like-badge {
      position: absolute; top: 16px; right: 16px;
      background: rgba(255,255,255,0.92); backdrop-filter: blur(8px);
      padding: 6px 12px; border-radius: 20px;
      font-size: 14px; font-weight: 600; color: #111;
      display: flex; align-items: center; gap: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.12);
      z-index: 10;
    }
    .like-badge svg { width: 16px; height: 16px; fill: #FF3B30; }

    .gallery-thumbnails {
      display: flex; gap: 10px; margin-top: 12px; overflow-x: auto; padding-bottom: 4px;
    }
    .thumb-item {
      width: 72px; height: 72px; border-radius: 10px; overflow: hidden; flex-shrink: 0;
      cursor: pointer; border: 2px solid transparent; opacity: 0.65; transition: all 0.2s;
    }
    .thumb-item.active { border-color: #4F46E5; opacity: 1; transform: scale(1.02); }
    .thumb-item img { width: 100%; height: 100%; object-fit: cover; }

    .info-section { display: flex; flex-direction: column; }
    .product-title {
      font-size: 22px; font-weight: 700; line-height: 1.35; color: #111827; margin-bottom: 12px;
    }
    .product-price {
      font-size: 28px; font-weight: 800; color: #111827; margin-bottom: 6px;
    }
    .product-meta {
      font-size: 14px; color: #6B7280; margin-bottom: 24px; display: flex; align-items: center; gap: 6px;
    }

    .divider { height: 1px; background-color: #E5E7EB; margin: 20px 0; }

    .section-block { margin-bottom: 24px; }
    .section-title { font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 10px; }
    .description-text { font-size: 15px; line-height: 1.6; color: #374151; white-space: pre-line; }

    .seller-card { display: flex; align-items: center; gap: 14px; padding: 12px 0; }
    .seller-avatar { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; background: #E5E7EB; }
    .seller-name { font-size: 16px; font-weight: 700; color: #111827; }
    .seller-loc { font-size: 13px; color: #6B7280; margin-top: 2px; }

    .meetup-address {
      font-size: 14px; font-weight: 600; color: #111827; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;
    }
    #map-box {
      width: 100%; height: 220px; border-radius: 20px; overflow: hidden;
      border: 1px solid #E5E7EB; z-index: 1; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .custom-leaflet-pin { background: transparent !important; border: none !important; }

    .report-link { display: inline-block; font-size: 13px; color: #9CA3AF; text-decoration: underline; margin-top: 12px; cursor: pointer; }

    .bottom-bar {
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 1000;
      background: #FFFFFF; border-top: 1px solid #E5E7EB;
      padding: 14px 0;
      box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.06);
      display: flex; justify-content: center;
    }
    .bottom-bar-content {
      width: 100%; max-width: 940px; padding: 0 20px;
      display: flex; align-items: center; justify-content: space-between;
    }
    .bottom-price { font-size: 20px; font-weight: 800; color: #111827; }
    .bottom-price-label { font-size: 12px; color: #6B7280; font-weight: 500; }
    
    .chat-btn {
      background: #4F46E5; color: #FFFFFF;
      font-size: 16px; font-weight: 700;
      padding: 12px 48px; border-radius: 999px;
      border: none; cursor: pointer;
      box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
      transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
    }
    .chat-btn:hover { background: #4338CA; box-shadow: 0 6px 18px rgba(79, 70, 229, 0.45); }
    .chat-btn:active { transform: scale(0.97); }

    .related-section { max-width: 940px; margin: 48px auto 0; padding: 0 20px; }
    .related-title { font-size: 20px; font-weight: 700; margin-bottom: 20px; color: #111827; }
    .related-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
    @media (max-width: 768px) { .related-grid { grid-template-columns: repeat(2, 1fr); } }
    .related-card { background: #FFF; border-radius: 12px; overflow: hidden; border: 1px solid #E5E7EB; cursor: pointer; }
    .related-card-img { width: 100%; aspect-ratio: 1/1; object-fit: cover; background: #F3F4F6; }
    .related-card-info { padding: 10px; }
    .related-card-price { font-size: 15px; font-weight: 700; color: #111; }
    .related-card-name { font-size: 13px; color: #4B5563; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }

    .moonoh-modal-overlay {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(4px);
      display: flex; align-items: center; justify-content: center;
      z-index: 9999; opacity: 0; pointer-events: none; transition: opacity 0.2s;
    }
    .moonoh-modal-overlay.active { opacity: 1; pointer-events: auto; }
    .moonoh-modal {
      background: #FFF; border-radius: 24px; padding: 36px 32px 32px; width: 90%; max-width: 400px; text-align: center; position: relative;
    }
    .moonoh-modal-close {
      position: absolute; top: 16px; right: 16px; font-size: 24px; border: none; background: none; cursor: pointer; color: #9CA3AF;
    }
    .header-share-btn {
      display: flex; align-items: center; gap: 6px;
      background: #F3F4F6; color: #374151;
      border: none; padding: 6px 14px; border-radius: 999px;
      font-size: 13px; font-weight: 600; cursor: pointer;
      transition: background 0.2s, transform 0.1s;
    }
    .header-share-btn:hover { background: #E5E7EB; color: #111827; }
    .header-share-btn:active { transform: scale(0.96); }
  </style>
</head>
<body>

  <!-- Top Header -->
  <header class="header-nav">
    <div class="header-content">
      <a href="/explore.html" class="header-back">
        ← Back to Explore
      </a>
      <a href="/" class="header-logo">
        <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e51874e4a73ff20cb673ec_Logo.svg" alt="moonoh logo"/>
      </a>
      <button class="header-share-btn" onclick="openShareModal()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
        <span>Share</span>
      </button>
    </div>
  </header>

  <!-- Product Detail Container -->
  <main class="item-detail-container">

    <!-- Explicit HTML Breadcrumbs for Crawlers & PageRank -->
    <nav class="breadcrumb-bar" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="sep">›</span>
      <a href="/explore">Explore</a>
      <span class="sep">›</span>
      <a href="/explore?town=${encodeURIComponent(townName)}">${townName}</a>
      <span class="sep">›</span>
      <a href="/explore?category=${encodeURIComponent(categoryName)}">${categoryName}</a>
      <span class="sep">›</span>
      <span class="current">${title}</span>
    </nav>

    <div class="item-detail-layout">
      
      <!-- Left Column: Gallery -->
      <div>
        <div class="gallery-container">
          <img id="main-image" src="${mainPhoto}" alt="${title}" class="gallery-main-img"/>
          <div class="like-badge">
            <svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            <span>${likeCount}</span>
          </div>
          <div class="gallery-indicators" id="indicators">
            ${photos.map((_, i) => `<div class="indicator-dot ${i===0?'active':''}" onclick="switchImage(${i})"></div>`).join('')}
          </div>
        </div>
        
        <div class="gallery-thumbnails">
          ${photos.map((p, i) => `
            <div class="thumb-item ${i===0?'active':''}" onclick="switchImage(${i})">
              <img src="${p}" alt="${title} - Photo ${i+1} view in ${townName}" onerror="this.src='images/common/ico_profile_empty.png'"/>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Right Column: Info & Description -->
      <div class="info-section">
        <h1 class="product-title">${title}</h1>
        <div class="product-price">${priceStr}</div>
        <div class="product-meta">
          <span>${strDayCount}</span>
          <span>·</span>
          <span>${townName}</span>
        </div>

        <div class="divider"></div>

        <!-- Description -->
        <div class="section-block">
          <h2 class="section-title">Description</h2>
          <p class="description-text">${description}</p>
        </div>

        <div class="divider"></div>

        <!-- Seller Info -->
        <div class="section-block">
          <h2 class="section-title">Seller information</h2>
          <div class="seller-card">
            <img src="${sellerPic}" alt="${sellerName}" class="seller-avatar" onerror="this.onerror=null; this.src='${defaultAvatar}';"/>
            <div>
              <div class="seller-name">${sellerName}</div>
              <div class="seller-loc">${townName}</div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Meetup Preference & Map -->
        <div class="section-block">
          <h2 class="section-title">Meetup preference</h2>
          <div class="meetup-address">
            <span>${address}</span>
            <span style="color:#9CA3AF;">›</span>
          </div>
          <div id="map-box"></div>
        </div>

        <a class="report-link" onclick="openModal()">Report this listing</a>
      </div>

    </div>
  </main>

  <!-- Related Items Section -->
  <section class="related-section">
    <h2 class="related-title">More items in ${categoryName}</h2>
    <div class="related-grid">
      ${relatedHtml}
    </div>
  </section>

  <!-- Fixed Bottom Bar -->
  <div class="bottom-bar">
    <div class="bottom-bar-content">
      <div>
        <div class="bottom-price">${priceStr}</div>
        <div class="bottom-price-label">Initial price</div>
      </div>
      <button class="chat-btn" onclick="openModal()">Chat</button>
    </div>
  </div>

  <!-- Download Modal -->
  <div class="moonoh-modal-overlay" id="moonoh-download-modal">
    <div class="moonoh-modal">
      <button class="moonoh-modal-close" onclick="closeModal()">×</button>
      <h3 style="font-size:22px; font-weight:800; color:#111827; margin-bottom:12px;">Get the Moonoh App</h3>
      <p style="font-size:14px; color:#6B7280; margin-bottom:28px; line-height:1.5;">Want to chat with <strong style="color:#111827;">${sellerName}</strong> to buy this item?<br/>Download the free Moonoh app to start secure chat.</p>
      <div style="display:flex; flex-direction:column; gap:12px;">
        <a href="https://apps.apple.com/us/app/moonoh/id6477390079" target="_blank">
          <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/65e3defb38f948f6f3f18a51_appstore.svg" width="100%" style="max-width:220px; margin:0 auto; display:block;">
        </a>
        <a href="https://play.google.com/store/apps/details?id=com.moonoh" target="_blank">
          <img src="https://cdn.prod.website-files.com/65e3de602f703e1765199b30/66f20cadd9e770db9e8cf5d7_Google_Play_Store_badge_EN.svg%20(1).png" width="100%" style="max-width:220px; margin:0 auto; display:block;">
        </a>
      </div>
    </div>
  </div>

  <!-- Share Popup Modal -->
  <div class="moonoh-modal-overlay" id="moonoh-share-modal">
    <div class="moonoh-modal" style="max-width: 380px;">
      <button class="moonoh-modal-close" onclick="closeShareModal()">×</button>
      <h3 style="font-size:20px; font-weight:800; color:#111827; margin-bottom:6px;">Share Listing</h3>
      <p style="font-size:13px; color:#6B7280; margin-bottom:24px;">Share this item via Email or copy link to share.</p>
      
      <div style="display:flex; flex-direction:column; gap:12px;">
        <a id="share-email-btn" href="#" target="_blank" style="display:flex; align-items:center; justify-content:center; gap:10px; background:#F3F4F6; color:#111827; border:1px solid #E5E7EB; padding:12px; border-radius:12px; font-weight:600; font-size:14px; text-decoration:none; transition:background 0.2s;">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          <span>Share via Email</span>
        </a>

        <button id="share-copy-btn" onclick="copyShareLink()" style="display:flex; align-items:center; justify-content:center; gap:10px; background:#4F46E5; color:#FFFFFF; border:none; padding:12px; border-radius:12px; font-weight:600; font-size:14px; cursor:pointer; transition:all 0.2s; box-shadow: 0 4px 12px rgba(79,70,229,0.25);">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span id="copy-btn-text">Copy Link</span>
        </button>
      </div>
    </div>
  </div>

  <script>
    const photos = ${JSON.stringify(photos)};

    function switchImage(index) {
      if (!photos[index]) return;
      const mainImg = document.getElementById('main-image');
      mainImg.style.opacity = '0.4';
      setTimeout(() => {
        mainImg.src = photos[index];
        mainImg.style.opacity = '1';
      }, 100);

      const thumbs = document.querySelectorAll('.thumb-item');
      thumbs.forEach((t, i) => t.classList.toggle('active', i === index));

      const dots = document.querySelectorAll('.indicator-dot');
      dots.forEach((d, i) => d.classList.toggle('active', i === index));
    }

    function openShareModal() {
      const modal = document.getElementById("moonoh-share-modal");
      const emailBtn = document.getElementById("share-email-btn");
      const title = ${JSON.stringify(title)};
      const price = ${JSON.stringify(priceStr)};
      const town = ${JSON.stringify(townName)};
      
      const mailSubject = encodeURIComponent("Check out this listing on Moonoh: " + title);
      const mailBody = encodeURIComponent("Hi!\\n\\nI found this " + title + " (" + price + ") in " + town + " on Moonoh marketplace:\\n" + window.location.href + "\\n\\nCheck it out!");
      if (emailBtn) emailBtn.href = "mailto:?subject=" + mailSubject + "&body=" + mailBody;

      const copyText = document.getElementById("copy-btn-text");
      if (copyText) copyText.innerText = "Copy Link";

      if (modal) modal.classList.add("active");
    }

    function closeShareModal() {
      const modal = document.getElementById("moonoh-share-modal");
      if (modal) modal.classList.remove("active");
    }

    function copyShareLink() {
      const copyBtnText = document.getElementById("copy-btn-text");
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(window.location.href).then(() => {
          if (copyBtnText) copyBtnText.innerText = "Link Copied! ✓";
          setTimeout(() => {
            if (copyBtnText) copyBtnText.innerText = "Copy Link";
            closeShareModal();
          }, 1500);
        }).catch(() => {
          prompt("Copy listing URL:", window.location.href);
        });
      } else {
        prompt("Copy listing URL:", window.location.href);
      }
    }

    function openModal() {
      const modal = document.getElementById('moonoh-download-modal');
      if (modal) modal.classList.add('active');
    }
    
    function closeModal() {
      const modal = document.getElementById('moonoh-download-modal');
      if (modal) modal.classList.remove('active');
    }

    document.addEventListener("DOMContentLoaded", () => {
      const dlModal = document.getElementById('moonoh-download-modal');
      if (dlModal) {
        dlModal.addEventListener('click', function(e) {
          if (e.target === this) closeModal();
        });
      }

      const shareModal = document.getElementById('moonoh-share-modal');
      if (shareModal) {
        shareModal.addEventListener('click', function(e) {
          if (e.target === this) closeShareModal();
        });
      }

      const lat = ${lat};
      const lng = ${lng};
      const mapBox = document.getElementById('map-box');
      if (mapBox && typeof L !== 'undefined') {
        const map = L.map('map-box', {
          center: [lat, lng],
          zoom: 15,
          zoomControl: false,
          attributionControl: false
        });

        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
          maxZoom: 19,
          detectRetina: true
        }).addTo(map);

        L.circle([lat, lng], {
          color: '#5850EC',
          weight: 3,
          fillColor: '#5850EC',
          fillOpacity: 0.22,
          radius: 280
        }).addTo(map);

        const customPinIcon = L.divIcon({
          className: 'custom-leaflet-pin',
          html: \`
            <div style="position: relative; width: 34px; height: 46px; transform: translate(-50%, -100%);">
              <svg width="34" height="46" viewBox="0 0 38 50" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0px 3px 6px rgba(0,0,0,0.3));">
                <path d="M19 0C8.50659 0 0 8.50659 0 19C0 31.75 16.625 47.75 17.375 48.5C18.25 49.375 19.75 49.375 20.625 48.5C21.375 47.75 38 31.75 38 19C38 8.50659 29.4934 0 19 0Z" fill="url(#pin-grad)"/>
                <circle cx="19" cy="18" r="6" fill="#FFFFFF"/>
                <defs>
                  <linearGradient id="pin-grad" x1="19" y1="0" x2="19" y2="50" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#38BDF8"/>
                    <stop offset="1" stop-color="#0284C7"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
          \`,
          iconSize: [34, 46],
          iconAnchor: [17, 46]
        });

        L.marker([lat, lng], { icon: customPinIcon }).addTo(map);
      }
    });
  </script>
</body>
</html>`;

    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8"
      }
    });

  } catch (error) {
    return new Response(`Error rendering item detail: ${error.message}`, { status: 500 });
  }
};
