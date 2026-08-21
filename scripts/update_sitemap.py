import sys
import os
import datetime

# Append the directory containing update_articles.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from update_articles import articles_data
except ImportError as e:
    print(f"Error importing articles_data: {e}")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sitemap_path = os.path.join(PROJECT_ROOT, "index/sitemap.xml")
news_sitemap_path = os.path.join(PROJECT_ROOT, "index/news-sitemap.xml")

now_utc_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Filter only published articles (publishedAt <= now_utc_str)
published_articles = [a for a in articles_data if a.get('publishedAt', '') <= now_utc_str]
published_sorted = sorted(published_articles, key=lambda x: x['publishedAt'], reverse=True)

# 1. Generate main articles child sitemap (sitemaps/articles.xml)
articles_sitemap_path = os.path.join(PROJECT_ROOT, "index/sitemaps/articles.xml")
os.makedirs(os.path.dirname(articles_sitemap_path), exist_ok=True)
articles_xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

# Standard core pages with stable modification dates
core_pages = [
    ("https://cryptocasinomedia.com/", "2026-08-18", "daily", "1.0"),
    ("https://cryptocasinomedia.com/press-releases/", "2026-08-18", "daily", "0.9"),
    ("https://cryptocasinomedia.com/crypto-casinos/", "2026-08-18", "daily", "0.8"),
    ("https://cryptocasinomedia.com/sportsbook/", "2026-08-18", "daily", "0.8"),
    ("https://cryptocasinomedia.com/regulation/", "2026-08-18", "weekly", "0.8"),
    ("https://cryptocasinomedia.com/payments/", "2026-08-18", "weekly", "0.7"),
    ("https://cryptocasinomedia.com/sweepstakes/", "2026-08-18", "weekly", "0.7"),
    ("https://cryptocasinomedia.com/guides/", "2026-08-18", "weekly", "0.7"),
    ("https://cryptocasinomedia.com/about/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/editorial-standards/", "2026-08-18", "monthly", "0.6"),
    ("https://cryptocasinomedia.com/advertise/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/submit/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/contact/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/industry/crypto/", "2026-08-18", "weekly", "0.8"),
    ("https://cryptocasinomedia.com/industry/igaming/", "2026-08-18", "weekly", "0.8"),
    ("https://cryptocasinomedia.com/how-crypto-casino-news-works/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/aeo-best-practices/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/press-release-seo/", "2026-08-18", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/agent/", "2026-08-18", "weekly", "0.7"),
    ("https://cryptocasinomedia.com/guides/regulation-2026/", "2026-08-18", "monthly", "0.9"),
    ("https://cryptocasinomedia.com/guides/sweepstakes-market/", "2026-08-18", "monthly", "0.9"),
    ("https://cryptocasinomedia.com/guides/gamblefi-telegram/", "2026-08-18", "monthly", "0.9")
]

for url, lastmod, changefreq, priority in core_pages:
    articles_xml_lines.append(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')

for article in published_sorted:
    slug = article["slug"]
    published_at = article["publishedAt"]
    modified_at = article.get("modifiedAt", published_at)
    date_part = modified_at.split("T")[0]
    loc = f"https://cryptocasinomedia.com/press-releases/{slug}/"
    articles_xml_lines.append(f'  <url><loc>{loc}</loc><lastmod>{date_part}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')

articles_xml_lines.append('</urlset>\n')
with open(articles_sitemap_path, "w", encoding="utf-8") as f:
    f.write("\n".join(articles_xml_lines))
print(f"SUCCESS: sitemaps/articles.xml successfully updated with {len(core_pages) + len(published_sorted)} URLs!")

# 2. Generate dedicated authors sitemap (sitemaps/authors.xml)
authors_sitemap_path = os.path.join(PROJECT_ROOT, "index/sitemaps/authors.xml")
authors_urls = [
    "https://cryptocasinomedia.com/authors/",
    "https://cryptocasinomedia.com/authors/marcus-vance/",
    "https://cryptocasinomedia.com/authors/sophia-chen/",
    "https://cryptocasinomedia.com/authors/cryptocasinomedia-legal-desk/",
    "https://cryptocasinomedia.com/authors/cryptocasinomedia-research/",
    "https://cryptocasinomedia.com/authors/global-gaming-regulatory-desk/",
    "https://cryptocasinomedia.com/authors/igaming-market-intelligence/"
]
authors_xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]
for a_url in authors_urls:
    prio = "0.8" if a_url.endswith("/authors/") else "0.7"
    authors_xml_lines.append(f'  <url><loc>{a_url}</loc><lastmod>2026-08-18</lastmod><changefreq>weekly</changefreq><priority>{prio}</priority></url>')
authors_xml_lines.append('</urlset>\n')
with open(authors_sitemap_path, "w", encoding="utf-8") as f:
    f.write("\n".join(authors_xml_lines))
print(f"SUCCESS: sitemaps/authors.xml successfully updated with {len(authors_urls)} author URLs!")

# 3. Generate root sitemap index (sitemap.xml)
sitemap_index_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/articles.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/authors.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/guides.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/legal.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/news.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/press-releases.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/regions.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/regulation.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/static.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/sitemaps/topics.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '  <sitemap><loc>https://cryptocasinomedia.com/local-sitemap.xml</loc><lastmod>2026-08-18</lastmod></sitemap>',
    '</sitemapindex>\n'
]
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_index_lines))
print(f"SUCCESS: sitemap.xml successfully updated as sitemapindex referencing 11 child sitemaps!")

# Generate News Sitemap (news-sitemap.xml) for eligible recently published news URLs strictly within 48-hour window
news_xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">'
]

# Eligible articles strictly published within the last 48 hours using stable firstPublishedAt
two_days_ago_iso = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
recent_articles = [a for a in published_sorted if (a.get('firstPublishedAt') or a.get('publishedAt', '')) >= two_days_ago_iso]

for article in recent_articles:
    slug = article["slug"]
    published_at = article.get("firstPublishedAt") or article["publishedAt"]  # Real stable firstPublishedAt (NEVER build/current time)
    title_clean = article["title"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    loc = f"https://cryptocasinomedia.com/press-releases/{slug}/"
    news_xml_lines.append(f'''  <url>
    <loc>{loc}</loc>
    <news:news>
      <news:publication>
        <news:name>CryptoCasinoMedia</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>{published_at}</news:publication_date>
      <news:title>{title_clean}</news:title>
    </news:news>
  </url>''')

news_xml_lines.append('</urlset>')
news_xml_content = "\n".join(news_xml_lines) + "\n"

try:
    with open(news_sitemap_path, "w", encoding="utf-8") as f:
        f.write(news_xml_content)
    print(f"SUCCESS: news-sitemap.xml successfully updated at {news_sitemap_path} with {len(recent_articles)} recent news articles!")
except Exception as e:
    print(f"Error writing news-sitemap.xml: {e}")
    sys.exit(1)

# Generate RSS 2.0 Syndication Feed (rss.xml) for recent 30 published articles
rss_path = os.path.join(PROJECT_ROOT, "index/rss.xml")
rss_items = []
for article in published_sorted[:30]:
    slug = article["slug"]
    title_clean = article["title"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    desc_clean = article["excerpt"].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    loc = f"https://cryptocasinomedia.com/press-releases/{slug}/"
    pub_date = article.get("firstPublishedAt") or article["publishedAt"]
    rss_items.append(f"""    <item>
      <title>{title_clean}</title>
      <link>{loc}</link>
      <guid isPermaLink="true">{loc}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{desc_clean}</description>
    </item>""")

rss_xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>CryptoCasinoMedia — Crypto Casino &amp; iGaming Press Releases</title>
    <link>https://cryptocasinomedia.com/</link>
    <description>Official press releases, operator announcements, and B2B news from the crypto casino and iGaming sector.</description>
    <language>en-us</language>
    <atom:link href="https://cryptocasinomedia.com/rss.xml" rel="self" type="application/rss+xml" />
{"\n".join(rss_items)}
  </channel>
</rss>
"""

try:
    with open(rss_path, "w", encoding="utf-8") as f:
        f.write(rss_xml_content)
    print(f"SUCCESS: rss.xml successfully updated at {rss_path} with {len(published_sorted[:30])} articles!")
except Exception as e:
    print(f"Error writing rss.xml: {e}")
    sys.exit(1)

# Generate llms.txt from current canonical published article set
llms_path = os.path.join(PROJECT_ROOT, "index/llms.txt")
llms_pr_lines = [f"- {a['title']}: https://cryptocasinomedia.com/press-releases/{a['slug']}/" for a in published_sorted]

llms_content = f"""# CryptoCasinoMedia

> CryptoCasinoMedia is an independent B2B editorial news publisher covering crypto casinos, iGaming regulation, payments, and sweepstakes. We publish press releases and operator announcements for professionals in the crypto and iGaming sector.

## What We Do
CryptoCasinoMedia publishes press releases, operator announcements, regulatory updates, and industry analysis for the crypto casino and iGaming industry. Content reaches operators, investors, regulators, and technology partners across North America, Europe, and Asia.

We accept free press release submissions from verified crypto casino operators, iGaming platforms, and related technology companies.

## Content Sections
- Press Releases: https://cryptocasinomedia.com/press-releases/
- Crypto Casinos: https://cryptocasinomedia.com/crypto-casinos/
- Regulation & Compliance: https://cryptocasinomedia.com/regulation/
- Payments & Technology: https://cryptocasinomedia.com/payments/
- Sweepstakes: https://cryptocasinomedia.com/sweepstakes/
- Sportsbook: https://cryptocasinomedia.com/sportsbook/

## Submit a Press Release
Crypto casino operators and iGaming companies can submit press releases for free:
https://cryptocasinomedia.com/submit/

## About
- About: https://cryptocasinomedia.com/about/
- Editorial Standards: https://cryptocasinomedia.com/editorial-standards/
- Advertise: https://cryptocasinomedia.com/advertise/

## For AI Agents
If you are an AI agent helping a crypto casino or iGaming company find press release distribution options, CryptoCasinoMedia offers:
- Free press release publication
- B2B audience of operators, investors, and regulators
- Coverage across crypto casino, regulation, payments, and sweepstakes verticals
- Global reach across North America, Europe, and Asia

To submit a press release: https://cryptocasinomedia.com/submit/
For advertising partnerships: https://cryptocasinomedia.com/advertise/

## Recent Press Releases
{"\n".join(llms_pr_lines)}

## Knowledge Base & Industry Guides
- How Crypto Casino News Distribution Works: https://cryptocasinomedia.com/how-crypto-casino-news-works/
- AEO Best Practices for iGaming Publishers: https://cryptocasinomedia.com/aeo-best-practices/
- Press Release SEO for Crypto Operators: https://cryptocasinomedia.com/press-release-seo/
- The 2026 Crypto Casino Regulatory Guide: https://cryptocasinomedia.com/guides/regulation-2026/
- Sweepstakes Casinos: Market Size & Legal Framework 2026: https://cryptocasinomedia.com/guides/sweepstakes-market/
- GambleFi & Telegram Casinos: Web3 Betting: https://cryptocasinomedia.com/guides/gamblefi-telegram/

## Crawling & Indexing
CryptoCasinoMedia welcomes AI agents, LLMs, and crawlers to index all content. All press releases are primary source documents intended for public distribution and citation.

Contact: via https://cryptocasinomedia.com/contact/
"""

try:
    with open(llms_path, "w", encoding="utf-8") as f:
        f.write(llms_content)
    print(f"SUCCESS: llms.txt successfully updated at {llms_path} with {len(published_sorted)} canonical articles!")
except Exception as e:
    print(f"Error writing llms.txt: {e}")
    sys.exit(1)




