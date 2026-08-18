import json

urls = [
    # Rule 114 Fixed Pages
    "https://moon-oh.com/fraud-prevention",
    "https://moon-oh.com/terms",
    "https://moon-oh.com/privacy",
    "https://moon-oh.com/explore",
    "https://moon-oh.com/about",
    "https://moon-oh.com/contact",
    "https://moon-oh.com/press",
    "https://moon-oh.com/disclaimer",
    "https://moon-oh.com/facebook-marketplace-alternative-nyc",
    "https://moon-oh.com/explore/local-shops",
    "https://moon-oh.com/explore/food-rescue",
    "https://moon-oh.com/explore/marketplaces",
    
    # 7 Local Shop Pages
    "https://moon-oh.com/local-shops/sey-coffee",
    "https://moon-oh.com/local-shops/front-general-store",
    "https://moon-oh.com/local-shops/mirth-vintage",
    "https://moon-oh.com/local-shops/salter-house",
    "https://moon-oh.com/local-shops/big-night",
    "https://moon-oh.com/local-shops/happier-grocery",
    "https://moon-oh.com/local-shops/pop-up-grocer",

    # Key Regional Hubs
    "https://moon-oh.com/explore/manhattan",
    "https://moon-oh.com/explore/brooklyn",
    "https://moon-oh.com/explore/queens",
    "https://moon-oh.com/explore/bronx",
    "https://moon-oh.com/explore/staten-island",
    "https://moon-oh.com/explore/bergen-county-nj",
    "https://moon-oh.com/explore/hudson-county-nj",

    # Key Category Hubs
    "https://moon-oh.com/explore/furniture",
    "https://moon-oh.com/explore/electronics",
    "https://moon-oh.com/explore/womens-fashion",
    "https://moon-oh.com/explore/mens-fashion",
    "https://moon-oh.com/explore/home-garden",
    "https://moon-oh.com/explore/food-groceries",
    "https://moon-oh.com/explore/sports-leisure",
    "https://moon-oh.com/explore/baby-kids",
    "https://moon-oh.com/explore/jewelry-watches",
    "https://moon-oh.com/explore/luggages-bags"
]

# Add Latest Moonoh visible products
try:
    with open("data.json", "r", encoding="utf-8") as f:
        moonoh_data = json.load(f)
        for item in moonoh_data[:30]:
            if item.get("url"):
                urls.append(f"https://moon-oh.com{item['url']}")
except Exception as e:
    pass

# Add Local Shop products
try:
    with open("local_shops_data.json", "r", encoding="utf-8") as f:
        local_db = json.load(f)
        for p in (local_db.get("products") or [])[:30]:
            if p.get("shop_id") and p.get("slug"):
                urls.append(f"https://moon-oh.com/local-product/{p['shop_id']}/{p['slug']}")
except Exception as e:
    pass

# Remove duplicates while preserving order
seen = set()
unique_urls = []
for u in urls:
    if u not in seen:
        seen.add(u)
        unique_urls.append(u)

# Limit to top 100
final_100 = unique_urls[:100]

with open("bing_submit_urls.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_100) + "\n")

print(f"✅ Generated {len(final_100)} URLs in bing_submit_urls.txt")
