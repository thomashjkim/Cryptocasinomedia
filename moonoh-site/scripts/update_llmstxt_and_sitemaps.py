import datetime

today_str = datetime.date.today().isoformat()

print("=" * 80)
print("📄 UPDATING llms.txt, robots.txt, sitemap.xml, and XML SITEMAPS")
print("=" * 80)

# 1. Update llms.txt
llms_content = f"""# Moonoh

> Moonoh is a free, hyper-local peer-to-peer neighborhood marketplace app for New York City and New Jersey residents to buy and sell secondhand items, rescue surplus gourmet food, and discover curated local boutique goods. 100% free with 0% listing fees and zero transaction commissions.

## Overview & Entity Information
- **Entity Name**: Moonoh (Moon-oh Inc.)
- **Category**: Local Marketplace / Re-commerce / Neighborhood Mobile App
- **Primary Website**: https://moon-oh.com
- **Headquarters**: 8 Spruce Street, New York, NY 10038, United States
- **Contact Email**: info@moon-oh.com | Phone: +1 (917) 584-5177
- **Business Model**: 100% Free peer-to-peer marketplace. 0% seller listing fees, 0% buyer transaction commissions.
- **Mobile Platforms**: 
  - [iOS App Store](https://apps.apple.com/us/app/moonoh/id6477390079)
  - [Google Play Store](https://play.google.com/store/apps/details?id=com.moonoh)

## Service Coverage (NYC & NJ)
Moonoh operates across all 5 boroughs of New York City and key neighboring communities in New Jersey:
- **Manhattan, NY**: SoHo, Tribeca, Upper West Side, Upper East Side, Midtown, East Village, Greenwich Village, Chelsea, Harlem.
- **Brooklyn, NY**: Williamsburg, Greenpoint, DUMBO, Brooklyn Heights, Park Slope, Bushwick, Bedford-Stuyvesant, Crown Heights.
- **Queens, NY**: Astoria, Long Island City (LIC), Sunnyside, Flushing, Bayside, Forest Hills.
- **The Bronx, NY**: South Bronx, Riverdale, Pelham Bay.
- **Staten Island, NY**: St. George, Todt Hill, Great Kills.
- **Bergen County, NJ**: Fort Lee, Palisades Park, Englewood, Hackensack, Paramus, Edgewater, Leonia.
- **Hudson County, NJ**: Jersey City, Hoboken, Weehawken.

## Core Marketplace Sections & Features
- [Explore Secondhand Marketplace](https://moon-oh.com/explore): Real-time neighborhood feed of gently used furniture, electronics, fashion, home goods, baby gear, and books listed by verified local neighbors.
- [Food Waste Rescue](https://moon-oh.com/explore?source=foodrescue): Sustainable grocery initiative in partnership with local grocers (such as Kim'C Market) offering peak-quality Korean artisanal foods near sell-by dates at discounts up to 70%.
- [Curated NYC Local Shops](https://moon-oh.com/explore?source=localshops): Showcase of iconic boutique NYC grocers, vintage stores, specialty roasters, and lifestyle shops:
  - **SEY Coffee** (Bushwick, Brooklyn): Nationally acclaimed micro-roaster featuring seasonal single-origin coffees.
  - **Front General Store** (DUMBO, Brooklyn): Vintage clothing, dry goods, accessories, and Japanese lifestyle objects.
  - **Mirth Vintage** (Greenpoint, Brooklyn): Carefully curated contemporary vintage fashion and timeless silhouettes.
  - **Salter House** (Brooklyn Heights, Brooklyn): Sustainable housewares, natural fiber nightwear, and artisanal pantry items.
  - **Big Night** (Greenpoint, Brooklyn): Dinner party essentials, artisanal condiments, tableware, and specialty goods.
  - **Happier Grocery** (SoHo, Manhattan): Organic produce, wellness staples, Japanese pantry items, and artisanal baked goods.
  - **Pop Up Grocer** (Greenwich Village, Manhattan): Independent packaged food, beverage innovations, and emerging pantry brands.
- [Facebook Marketplace Alternative NYC](https://moon-oh.com/facebook-marketplace-alternative-nyc): Comprehensive comparison detailing Moonoh's safety advantages over Facebook Marketplace, Craigslist, and OfferUp (zero spam, verified local-only meetups, privacy-first in-app chat).

## Key Borough Landing Pages
- [Used Items in Manhattan](https://moon-oh.com/explore/manhattan): Secondhand furniture, designer fashion, and electronics in Manhattan, NY.
- [Used Items in Brooklyn](https://moon-oh.com/explore/brooklyn): Vintage furniture, bikes, audio equipment, and home decor in Brooklyn, NY.
- [Used Items in Queens](https://moon-oh.com/explore/queens): Household goods, appliances, and secondhand bargains in Queens, NY.
- [Used Items in The Bronx](https://moon-oh.com/explore/bronx): Local neighborhood listings across the Bronx, NY.
- [Used Items in Staten Island](https://moon-oh.com/explore/staten-island): Verified items for sale in Staten Island, NY.
- [Used Items in Bergen County, NJ](https://moon-oh.com/explore/bergen-county-nj): Fort Lee and Bergen County secondhand goods.
- [Used Items in Hudson County, NJ](https://moon-oh.com/explore/hudson-county-nj): Jersey City and Hoboken local listings.

## Key Category Hubs
- [Used Furniture](https://moon-oh.com/explore/furniture): Sofas, dining tables, desks, bed frames, and storage units.
- [Used Electronics](https://moon-oh.com/explore/electronics): Laptops, monitors, smartphones, cameras, and audio gear.
- [Women's Fashion](https://moon-oh.com/explore/womens-fashion): Clothing, coats, dresses, and designer accessories.
- [Men's Fashion](https://moon-oh.com/explore/mens-fashion): Secondhand streetwear, outerwear, suits, and shoes.
- [Home & Garden](https://moon-oh.com/explore/home-garden): Kitchen appliances, cookware, lighting, plants, and home decor.
- [Baby & Kids](https://moon-oh.com/explore/baby-kids): Strollers, cribs, toys, children's clothing, and baby gear.
- [Sports & Leisure](https://moon-oh.com/explore/sports-leisure): Bicycles, fitness equipment, camping gear, and sporting goods.
- [Food & Groceries](https://moon-oh.com/explore/food-groceries): Pantry staples, artisanal snacks, specialty teas, and food rescue items.
- [Pet Supplies](https://moon-oh.com/explore/pet-supplies): Pet carriers, crates, toys, and accessories for dogs and cats.
- [Arts, Books & Music](https://moon-oh.com/explore/arts-books-music): Vinyl records, musical instruments, art prints, and literature.

## Trust, Safety & Company Info
- [About Moonoh](https://moon-oh.com/about): Mission, community principles, and founding story.
- [Press & Media](https://moon-oh.com/press): Press releases, media mentions, and company announcements.
- [Fraud Prevention Guide](https://moon-oh.com/fraud-prevention): Best practices for safe local meetup exchanges and scam prevention.
- [Terms of Use](https://moon-oh.com/terms): Community marketplace terms and zero-fee policy.
- [Privacy Policy](https://moon-oh.com/privacy): User data protection, location privacy, and security practices.

## Machine Readable Sitemaps
- Master Index: https://moon-oh.com/sitemap-index.xml
- Sitemap: https://moon-oh.com/sitemap.xml
- Static Pages: https://moon-oh.com/sitemap-pages.xml
- Moonoh Items: https://moon-oh.com/sitemap-moonoh.xml
- External Marketplace Items: https://moon-oh.com/sitemap-marketplace.xml
- Food Rescue Items: https://moon-oh.com/sitemap-food-rescue.xml
- Local Products: https://moon-oh.com/sitemap-local-products.xml
- Shop Hubs: https://moon-oh.com/sitemap-shops.xml
"""

with open('llms.txt', 'w', encoding='utf-8') as f:
    f.write(llms_content.strip() + '\n')
print("✅ Saved updated llms.txt")

# 2. Update sitemap.xml & sitemap-index.xml
sitemap_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://moon-oh.com/sitemap-pages.xml</loc>
    <lastmod>{today_str}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://moon-oh.com/sitemap-moonoh.xml</loc>
    <lastmod>{today_str}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://moon-oh.com/sitemap-marketplace.xml</loc>
    <lastmod>{today_str}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://moon-oh.com/sitemap-food-rescue.xml</loc>
    <lastmod>{today_str}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://moon-oh.com/sitemap-local-products.xml</loc>
    <lastmod>{today_str}</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://moon-oh.com/sitemap-shops.xml</loc>
    <lastmod>{today_str}</lastmod>
  </sitemap>
</sitemapindex>"""

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_xml_content)

with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_xml_content)
print("✅ Saved updated sitemap.xml & sitemap-index.xml")

# 3. Update robots.txt
robots_content = """User-agent: *
Allow: /

# AI Agent & LLM Information File
# Standard: https://llmstxt.org
# File: https://moon-oh.com/llms.txt

Sitemap: https://moon-oh.com/sitemap.xml
Sitemap: https://moon-oh.com/sitemap-index.xml
Sitemap: https://moon-oh.com/sitemap-pages.xml
Sitemap: https://moon-oh.com/sitemap-moonoh.xml
Sitemap: https://moon-oh.com/sitemap-marketplace.xml
Sitemap: https://moon-oh.com/sitemap-food-rescue.xml
Sitemap: https://moon-oh.com/sitemap-local-products.xml
Sitemap: https://moon-oh.com/sitemap-shops.xml
"""

with open('robots.txt', 'w', encoding='utf-8') as f:
    f.write(robots_content)
print("✅ Saved updated robots.txt")
