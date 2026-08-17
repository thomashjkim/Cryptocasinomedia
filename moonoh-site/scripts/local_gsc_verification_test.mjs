// Comprehensive Local Verification Test for GSC & GMC Cleanup

async function runVerification() {
  console.log("=================================================");
  console.log("  Moonoh GSC & GMC Technical Cleanup Local Tests ");
  console.log("=================================================\n");

  const itemMod = await import('../netlify/functions/item-detail.mjs');
  const exploreMod = await import('../netlify/functions/explore.mjs');
  const imageMod = await import('../netlify/functions/image-proxy.mjs');
  const merchantMod = await import('../netlify/functions/merchant-feed.mjs');

  const tests = [
    {
      name: "1. Current Moonoh C2C Item",
      url: "https://moon-oh.com/item/osaka-souvenir-pen-lightweight-with-osaka-keychain-queens-ny-849",
      handler: itemMod.default,
      validate: (res, text) => {
        const title = text.match(/<title>(.*?)<\/title>/)?.[1];
        const h1 = text.match(/<h1[^>]*>(.*?)<\/h1>/)?.[1];
        const hasMsgSeller = text.includes("Open App to Message Seller") || text.includes("Chat with Seller in App");
        const hasNoFakeReturn = !text.includes("hasMerchantReturnPolicy");
        const hasNoFakeShip = !text.includes('"value": "0.00"');
        console.log(`   Status: ${res.status} | Title: ${title}`);
        console.log(`   H1: ${h1}`);
        console.log(`   CTA reflects messaging: ${hasMsgSeller}`);
        console.log(`   Omitted fake C2C return policy: ${hasNoFakeReturn}`);
        console.log(`   Omitted fake free delivery schema: ${hasNoFakeShip}`);
        return res.status === 200 && hasMsgSeller && hasNoFakeReturn && hasNoFakeShip;
      }
    },
    {
      name: "2. Existing External Kim'C Market Item",
      url: "https://moon-oh.com/item/salmon-chips-4-flavors-sell-by-sale-brooklyn-ny-ext-kimc-9334042001661",
      handler: itemMod.default,
      validate: (res, text) => {
        const title = text.match(/<title>(.*?)<\/title>/)?.[1];
        const hasStoreCTA = text.includes("View on Kim&#39;C Market") || text.includes("View on Kim'C Market");
        const hasNoShippingSchema = !text.includes("shippingDetails") && !text.includes("hasMerchantReturnPolicy");
        const hasMerchantHandledText = text.includes("Shipping, returns, and checkout are handled by");
        console.log(`   Status: ${res.status} | Title: ${title}`);
        console.log(`   CTA points to original store: ${hasStoreCTA}`);
        console.log(`   Removed shippingDetails & return policy from JSON-LD: ${hasNoShippingSchema}`);
        console.log(`   UI displays merchant handling notice: ${hasMerchantHandledText}`);
        return res.status === 200 && hasStoreCTA && hasNoShippingSchema && hasMerchantHandledText;
      }
    },
    {
      name: "3. Existing Local Product Page",
      url: "https://moon-oh.com/local-product/big-night/small-round-tray",
      handler: itemMod.default,
      validate: (res, text) => {
        const title = text.match(/<title>(.*?)<\/title>/)?.[1];
        const hasBigNightCTA = text.includes("View on Big Night");
        console.log(`   Status: ${res.status} | Title: ${title}`);
        console.log(`   CTA points to Big Night store: ${hasBigNightCTA}`);
        return res.status === 200 && hasBigNightCTA;
      }
    },
    {
      name: "4. /explore Root Hub",
      url: "https://moon-oh.com/explore",
      handler: exploreMod.default,
      validate: (res, text) => {
        const h1 = text.match(/<h1[^>]*>(.*?)<\/h1>/)?.[1];
        const hasItemList = text.includes('"@type": "ItemList"') || text.includes('"@type":"ItemList"');
        console.log(`   Status: ${res.status} | H1: ${h1}`);
        console.log(`   Has ItemList schema: ${hasItemList}`);
        return res.status === 200 && !!h1 && hasItemList;
      }
    },
    {
      name: "5. Filter / Query Variant Canonicalization",
      url: "https://moon-oh.com/explore?category=Furniture&town=brooklyn",
      handler: exploreMod.default,
      validate: (res, text) => {
        const canonical = text.match(/<link rel="canonical" href="(.*?)"\/>/)?.[1];
        console.log(`   Status: ${res.status} | Canonical target: ${canonical}`);
        return res.status === 200 && canonical === "https://moon-oh.com/explore/brooklyn/furniture";
      }
    },
    {
      name: "6. Old Item Slug 301 Redirect",
      url: "https://moon-oh.com/item/mr-potato-head-mug-downtown-manhattan-209",
      handler: itemMod.default,
      validate: (res) => {
        const loc = res.headers.get("location");
        console.log(`   Status: ${res.status} | 301 Location: ${loc}`);
        return res.status === 301 && loc === "https://moon-oh.com/item/mr-potato-head-mug-manhattan-ny-209";
      }
    },
    {
      name: "7. Permanently Deleted Item",
      url: "https://moon-oh.com/item/downtown-brooklyn-sublet-16-w-19th-st-new-york-ny-10011-usa-",
      handler: itemMod.default,
      validate: (res, text) => {
        console.log(`   Status: ${res.status} (Controlled 404 for deleted listing)`);
        return res.status === 404;
      }
    },
    {
      name: "8. Image Proxy / Missing Asset Handling",
      url: "https://moon-oh.com/image-proxy/temp/1761780597453/IMG_5052.HEIC",
      handler: imageMod.default,
      validate: (res, text) => {
        console.log(`   Status: ${res.status} | X-Robots-Tag: ${res.headers.get("x-robots-tag")}`);
        return res.status === 200 || res.status === 404;
      }
    },
    {
      name: "9. Malformed Template Placeholder URL",
      url: "https://moon-oh.com/item/invalid-template-${article.slug}",
      handler: itemMod.default,
      validate: (res, text) => {
        console.log(`   Status: ${res.status} (Controlled 404 for malformed template)`);
        return res.status === 404;
      }
    },
    {
      name: "10. Category/Location Combo Page (Soft 404 Fix)",
      url: "https://moon-oh.com/explore/manhattan/food-groceries",
      handler: exploreMod.default,
      validate: (res, text) => {
        const h1 = text.match(/<h1[^>]*>(.*?)<\/h1>/)?.[1];
        const hasItems = text.includes("item-card");
        console.log(`   Status: ${res.status} | H1: ${h1} | Has items: ${hasItems}`);
        return res.status === 200 && !!h1 && hasItems;
      }
    },
    {
      name: "11. Google Merchant Center Feed Check",
      url: "https://moon-oh.com/merchant-feed.xml",
      handler: merchantMod.default,
      validate: (res, text) => {
        const hasZeroCheckoutItems = !text.includes("<item>") && text.includes("<channel>");
        console.log(`   Status: ${res.status} | Content-Type: ${res.headers.get("content-type")}`);
        console.log(`   Zero C2C web-checkout items in feed: ${hasZeroCheckoutItems}`);
        return res.status === 200 && hasZeroCheckoutItems;
      }
    }
  ];

  let passed = 0;
  for (const t of tests) {
    console.log(`\n▶ Testing: ${t.name}`);
    try {
      const res = await t.handler(new Request(t.url), {});
      const text = await res.text();
      const ok = t.validate(res, text);
      if (ok) {
        console.log(`   ✅ PASS`);
        passed++;
      } else {
        console.log(`   ❌ FAIL`);
      }
    } catch (e) {
      console.log(`   ❌ ERROR: ${e.message}`);
    }
  }

  console.log(`\n=================================================`);
  console.log(`  Test Results: ${passed} / ${tests.length} Passed`);
  console.log(`=================================================\n`);
  return passed === tests.length;
}

runVerification().then(success => {
  process.exit(success ? 0 : 1);
});
