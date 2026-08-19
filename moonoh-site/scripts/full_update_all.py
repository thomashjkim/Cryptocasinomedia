import json, datetime, os, re
from collections import Counter

TODAY = datetime.date.today().isoformat()
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DOMAIN = "https://moon-oh.com"

print(f"=== FULL UPDATE ALL === {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ─── STEP 1: moonoh-items-data.mjs ───
print("\n[1/5] Syncing moonoh-items-data.mjs from data.json...")
with open(os.path.join(BASE, "data.json"), "r", encoding="utf-8") as f:
    moonoh_data = json.load(f)
moonoh_data.sort(key=lambda x: x.get("postedAt", 0), reverse=True)
mjs_content = (
    f"// Live Moonoh Items Dataset ({len(moonoh_data)} visible items, sorted by postedAt DESC)\n"
    f"// Last synced: {TODAY}\n"
    "export const realMoonohItems = " + json.dumps(moonoh_data, ensure_ascii=False, indent=2) + ";\n"
)
with open(os.path.join(BASE, "netlify/functions/moonoh-items-data.mjs"), "w", encoding="utf-8") as f:
    f.write(mjs_content)
print(f"  OK: {len(moonoh_data)} items, newest=No.{moonoh_data[0]['no']}")

# ─── STEP 2: Fix local_shops_data.json ───
print("\n[2/5] Fixing local_shops_data.json (image + summary fields)...")
shops_path = os.path.join(BASE, "local_shops_data.json")
with open(shops_path, "r", encoding="utf-8") as f:
    shops_raw = json.load(f)
products = shops_raw.get("products", [])
fixed = 0
for p in products:
    if not p.get("image"):
        img = p.get("image_source_url") or p.get("primary_image_url", "")
        if img:
            p["image"] = img
            p["photo"] = img
            fixed += 1
    if not p.get("photo") and p.get("image"):
        p["photo"] = p["image"]
    if not p.get("moonoh_summary") and p.get("title"):
        shop_name = p.get("store_name") or p.get("shop_id", "").replace("-", " ").title()
        brand = p.get("brand", "")
        cat = p.get("primary_category") or p.get("moonoh_category", "")
        loc = p.get("location") or p.get("store_city", "New York")
        price = p.get("current_price") or p.get("price")
        price_str = f"${price}" if price else ""
        title = p["title"]
        p["moonoh_summary"] = f"{title}{' by ' + brand if brand else ''} {price_str} – at {shop_name}, {loc}.{(' ' + cat + '.') if cat else ''}"
        fixed += 1
shops_raw["products"] = products
with open(shops_path, "w", encoding="utf-8") as f:
    json.dump(shops_raw, f, ensure_ascii=False, separators=(",", ":"))
print(f"  OK: {len(products)} products, {fixed} fields fixed")

# ─── STEP 3: Regenerate all sitemaps ───
print("\n[3/5] Regenerating sitemaps...")

def write_sitemap(path, urls, changefreq="weekly", priority="0.7"):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        if isinstance(url, str):
            loc, prio, freq = url, priority, changefreq
        else:
            loc = url.get("loc", "")
            prio = url.get("priority", priority)
            freq = url.get("changefreq", changefreq)
        if not loc:
            continue
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    lines.append("</urlset>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(urls)

# sitemap-moonoh.xml
moonoh_urls = []
for item in moonoh_data:
    up = item.get("url", f"/item/item-{item['no']}")
    loc = up if up.startswith("http") else f"{SITE_DOMAIN}{up}"
    moonoh_urls.append({"loc": loc, "priority": "0.8", "changefreq": "daily"})
n = write_sitemap(os.path.join(BASE, "sitemap-moonoh.xml"), moonoh_urls)
print(f"  sitemap-moonoh.xml: {n}")

# sitemap-marketplace.xml
karrot_path = os.path.join(BASE, "scraped_karrot_500.json")
ext_mjs_path = os.path.join(BASE, "netlify/functions/external-items.mjs")
with open(karrot_path, "r", encoding="utf-8") as f:
    karrot_items = json.load(f)
marketplace_urls = []
for item in karrot_items:
    u = item.get("external_url") or item.get("canonical_url") or item.get("url", "")
    if u:
        marketplace_urls.append({"loc": u, "priority": "0.6", "changefreq": "weekly"})
with open(ext_mjs_path, "r", encoding="utf-8") as f:
    ext_content = f.read()
hk_urls = re.findall(r'"external_url"\s*:\s*"(https://[^"]*heykorean[^"]*)"', ext_content)
for u in hk_urls:
    marketplace_urls.append({"loc": u, "priority": "0.6", "changefreq": "weekly"})
n = write_sitemap(os.path.join(BASE, "sitemap-marketplace.xml"), marketplace_urls)
print(f"  sitemap-marketplace.xml: {n} (Karrot:{len(karrot_items)}, HeyKorean:{len(hk_urls)})")

# sitemap-local-products.xml
local_urls = []
for p in products:
    sid = p.get("shop_id", "")
    slug = p.get("slug", "")
    if sid and slug:
        local_urls.append({"loc": f"{SITE_DOMAIN}/local-product/{sid}/{slug}", "priority": "0.7", "changefreq": "weekly"})
n = write_sitemap(os.path.join(BASE, "sitemap-local-products.xml"), local_urls)
print(f"  sitemap-local-products.xml: {n}")

# sitemap-food-rescue.xml
food_mjs = os.path.join(BASE, "netlify/functions/food-rescue-items.mjs")
food_urls = []
if os.path.exists(food_mjs):
    with open(food_mjs, "r", encoding="utf-8") as f:
        fc = f.read()
    for slug in re.findall(r'"slug"\s*:\s*"([^"]+)"', fc):
        food_urls.append({"loc": f"{SITE_DOMAIN}/food-rescue/{slug}", "priority": "0.6", "changefreq": "weekly"})
if not food_urls:
    food_urls = [{"loc": f"{SITE_DOMAIN}/food-rescue/kimc-item-{i}", "priority": "0.6", "changefreq": "weekly"} for i in range(1, 16)]
n = write_sitemap(os.path.join(BASE, "sitemap-food-rescue.xml"), food_urls)
print(f"  sitemap-food-rescue.xml: {n}")

# sitemap-shops.xml
shop_ids = ["front-general-store","sey-coffee","salter-house","mirth-vintage","big-night","pop-up-grocer","happier-grocery"]
shop_urls = [{"loc": f"{SITE_DOMAIN}/shop/{s}", "priority": "0.8", "changefreq": "monthly"} for s in shop_ids]
n = write_sitemap(os.path.join(BASE, "sitemap-shops.xml"), shop_urls)
print(f"  sitemap-shops.xml: {n}")

# sitemap-pages.xml
boroughs = ["manhattan","brooklyn","queens","bronx","staten-island","flushing","bayside","astoria","bergen","hudson"]
categories = ["electronics","furniture","fashion","free","sports","beauty","kids"]
page_urls = [
    {"loc": f"{SITE_DOMAIN}/", "priority": "1.0", "changefreq": "daily"},
    {"loc": f"{SITE_DOMAIN}/explore", "priority": "0.9", "changefreq": "daily"},
    {"loc": f"{SITE_DOMAIN}/about", "priority": "0.5", "changefreq": "monthly"},
    {"loc": f"{SITE_DOMAIN}/local-shops", "priority": "0.8", "changefreq": "weekly"},
    {"loc": f"{SITE_DOMAIN}/food-rescue", "priority": "0.7", "changefreq": "weekly"},
    {"loc": f"{SITE_DOMAIN}/marketplaces", "priority": "0.7", "changefreq": "daily"},
]
for b in boroughs:
    page_urls.append({"loc": f"{SITE_DOMAIN}/explore/{b}", "priority": "0.7", "changefreq": "daily"})
for c in categories:
    page_urls.append({"loc": f"{SITE_DOMAIN}/explore/{c}", "priority": "0.7", "changefreq": "daily"})
for b in boroughs:
    for c in categories:
        page_urls.append({"loc": f"{SITE_DOMAIN}/explore/{b}/{c}", "priority": "0.6", "changefreq": "weekly"})
n = write_sitemap(os.path.join(BASE, "sitemap-pages.xml"), page_urls)
print(f"  sitemap-pages.xml: {n}")

# sitemap.xml (master mirror = moonoh)
write_sitemap(os.path.join(BASE, "sitemap.xml"), moonoh_urls)

# sitemap-index.xml
all_sm = ["sitemap-moonoh.xml","sitemap-marketplace.xml","sitemap-local-products.xml",
          "sitemap-food-rescue.xml","sitemap-shops.xml","sitemap-pages.xml"]
idx_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for sm in all_sm:
    idx_lines.append(f'  <sitemap><loc>{SITE_DOMAIN}/{sm}</loc><lastmod>{TODAY}</lastmod></sitemap>')
idx_lines.append("</sitemapindex>")
with open(os.path.join(BASE, "sitemap-index.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(idx_lines) + "\n")
print(f"  sitemap-index.xml: {len(all_sm)} entries")

# ─── STEP 4: llms.txt ───
print("\n[4/5] Updating llms.txt...")
total_moonoh = len(moonoh_data)
total_local = len(products)
total_karrot = len(karrot_items)
total_heykorean = len(hk_urls)
total_food = len(food_urls)
grand_total = total_moonoh + total_local + total_karrot + total_heykorean + total_food
total_urls_count = len(moonoh_urls)+len(marketplace_urls)+len(local_urls)+len(food_urls)+len(shop_urls)+len(page_urls)

borough_map = {"manhattan":"Manhattan","brooklyn":"Brooklyn","queens":"Queens","bronx":"Bronx",
               "the bronx":"Bronx","staten island":"Staten Island","flushing":"Flushing",
               "bayside":"Bayside","astoria":"Astoria","bergen":"Bergen County, NJ",
               "fort lee":"Bergen County, NJ","palisades":"Bergen County, NJ",
               "jersey city":"Hudson County, NJ","hoboken":"Hudson County, NJ","hudson":"Hudson County, NJ"}
bc = Counter()
for item in moonoh_data:
    loc = (item.get("rawTown") or item.get("townName") or item.get("location") or "").lower()
    matched = False
    for key, label in borough_map.items():
        if key in loc:
            bc[label] += 1
            matched = True
            break
    if not matched:
        bc["Other NYC"] += 1

cat_counts = Counter(item.get("categoryName") or item.get("category") or "General" for item in moonoh_data)
priced = [x["price"] for x in moonoh_data if isinstance(x.get("price"), (int,float)) and x["price"] > 0]
avg_p = sum(priced)/len(priced) if priced else 0
newest = moonoh_data[0]
newest_dt = datetime.datetime.fromtimestamp(newest.get("postedAt",0)/1000, datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")

per_shop = Counter(p.get("shop_id","") for p in products)

llms = f"""# Moonoh.com — Local Marketplace for NYC & NJ Communities
# AI/LLM Context File — Last updated: {TODAY}
# Format: https://llmstxt.org

> Moonoh.com is a curated secondhand and local marketplace discovery platform serving NYC and NJ communities.

## Platform Overview

- **Domain**: https://moon-oh.com
- **Coverage**: NYC (all 5 boroughs) + Bergen County NJ + Hudson County NJ
- **Last full data sync**: {TODAY}

## Data Summary

| Source | Items | Notes |
|--------|-------|-------|
| Moonoh (moon-oh.com) | {total_moonoh:,} | Live secondhand, newest No.{newest['no']} |
| Local Boutique Shops | {total_local:,} | FGS, SEY Coffee, Salter House, Mirth Vintage, Big Night, Pop Up Grocer |
| Karrot NYC | {total_karrot:,} | Peer-to-peer listings |
| HeyKorean Marketplace | {total_heykorean:,} | Korean-American community |
| Kim'C Market Food Rescue | {total_food:,} | Near sell-by Korean foods |
| **TOTAL** | **{grand_total:,}** | **{total_urls_count:,} indexed URLs** |

## Moonoh Detail

- Newest: No.{newest['no']} "{newest['title']}" ({newest_dt})
- Price: ${min(priced) if priced else 0:.0f}–${max(priced) if priced else 0:.0f} avg ${avg_p:.0f}
- Free items: {sum(1 for x in moonoh_data if x.get('price',0)==0)}

### By Borough
{chr(10).join(f'- {b}: {c}' for b,c in sorted(bc.items(), key=lambda x:-x[1]))}

### Top Categories
{chr(10).join(f'- {cat}: {cnt}' for cat,cnt in cat_counts.most_common(10))}

## Local Shops

| Shop | Products |
|------|----------|
| Front General Store | {per_shop.get('front-general-store',0)} |
| SEY Coffee | {per_shop.get('sey-coffee',0)} |
| Salter House | {per_shop.get('salter-house',0)} |
| Mirth Vintage | {per_shop.get('mirth-vintage',0)} |
| Big Night | {per_shop.get('big-night',0)} |
| Pop Up Grocer | {per_shop.get('pop-up-grocer',0)} |

## Sitemaps

- https://moon-oh.com/sitemap-index.xml
- https://moon-oh.com/sitemap-moonoh.xml ({len(moonoh_urls)} URLs)
- https://moon-oh.com/sitemap-marketplace.xml ({len(marketplace_urls)} URLs)
- https://moon-oh.com/sitemap-local-products.xml ({len(local_urls)} URLs)
- https://moon-oh.com/sitemap-food-rescue.xml ({len(food_urls)} URLs)
- https://moon-oh.com/sitemap-shops.xml ({len(shop_urls)} URLs)
- https://moon-oh.com/sitemap-pages.xml ({len(page_urls)} URLs)

## Sort Logic

- Default: Newest (postedAt DESC, real timestamp from backend)
- Relevance: title exact(+100), starts-with(+60), contains(+40), token: title(+25) brand(+15) category(+10) location(+5) description(+3)
- Price: ascending / descending
"""
with open(os.path.join(BASE, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(llms)
print(f"  OK: {grand_total:,} items, {total_urls_count:,} URLs")

# ─── STEP 5: Sort karrot by postedAt ───
print("\n[5/5] Sorting scraped_karrot_500.json by postedAt...")
karrot_items.sort(key=lambda x: x.get("postedAt", 0), reverse=True)
with open(karrot_path, "w", encoding="utf-8") as f:
    json.dump(karrot_items, f, ensure_ascii=False, separators=(",", ":"))
print(f"  OK: {len(karrot_items)} items sorted")

print(f"\n{'='*50}")
print(f"GRAND TOTAL: {grand_total:,} items | {total_urls_count:,} indexed URLs")
print(f"{'='*50}")
