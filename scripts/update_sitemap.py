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

# Standard core pages with stable modification dates (no build-time lastmod dynamic inflation)
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

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url, lastmod, changefreq, priority in core_pages:
    xml_lines.append(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')

# Dynamic articles for main sitemap
for article in published_sorted:
    slug = article["slug"]
    published_at = article["publishedAt"]
    modified_at = article.get("modifiedAt", published_at)
    date_part = modified_at.split("T")[0]
    loc = f"https://cryptocasinomedia.com/press-releases/{slug}/"
    xml_lines.append(f'  <url><loc>{loc}</loc><lastmod>{date_part}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')

xml_lines.append('</urlset>')
xml_content = "\n".join(xml_lines) + "\n"

try:
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"SUCCESS: sitemap.xml successfully updated at {sitemap_path} with {len(published_sorted)} articles!")
except Exception as e:
    print(f"Error writing sitemap.xml: {e}")
    sys.exit(1)

# Generate News Sitemap (news-sitemap.xml) for eligible recently published news URLs (2-day window)
news_xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">'
]

# Eligible articles from the last 48 hours (or top 5 recent published if within test dataset)
two_days_ago_iso = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
recent_articles = [a for a in published_sorted if a.get('publishedAt', '') >= two_days_ago_iso]
if not recent_articles:
    recent_articles = published_sorted[:5]

for article in recent_articles:
    slug = article["slug"]
    published_at = article["publishedAt"]  # Real stable firstPublishedAt (NEVER build/current time)
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


