import sys
import os

# Append the directory containing update_articles.py to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from update_articles import articles_data
except ImportError as e:
    print(f"Error importing articles_data: {e}")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sitemap_path = os.path.join(PROJECT_ROOT, "index/sitemap.xml")

import datetime

today_date = datetime.date.today().isoformat()

# Standard core pages with dynamic build date
core_pages = [
    ("https://cryptocasinomedia.com/", today_date, "daily", "1.0"),
    ("https://cryptocasinomedia.com/press-releases/", today_date, "daily", "0.9"),
    ("https://cryptocasinomedia.com/crypto-casinos/", today_date, "daily", "0.8"),
    ("https://cryptocasinomedia.com/sportsbook/", today_date, "daily", "0.8"),
    ("https://cryptocasinomedia.com/regulation/", today_date, "weekly", "0.8"),
    ("https://cryptocasinomedia.com/payments/", today_date, "weekly", "0.7"),
    ("https://cryptocasinomedia.com/sweepstakes/", today_date, "weekly", "0.7"),
    ("https://cryptocasinomedia.com/guides/", today_date, "weekly", "0.7"),
    ("https://cryptocasinomedia.com/about/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/editorial-standards/", "2026-08-11", "monthly", "0.6"),
    ("https://cryptocasinomedia.com/advertise/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/submit/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/contact/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/industry/crypto/", today_date, "weekly", "0.8"),
    ("https://cryptocasinomedia.com/industry/igaming/", today_date, "weekly", "0.8"),
    ("https://cryptocasinomedia.com/how-crypto-casino-news-works/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/aeo-best-practices/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/press-release-seo/", "2026-08-11", "monthly", "0.7"),
    ("https://cryptocasinomedia.com/agent/", today_date, "weekly", "0.7"),
    ("https://cryptocasinomedia.com/guides/regulation-2026/", today_date, "monthly", "0.9"),
    ("https://cryptocasinomedia.com/guides/sweepstakes-market/", today_date, "monthly", "0.9"),
    ("https://cryptocasinomedia.com/guides/gamblefi-telegram/", today_date, "monthly", "0.9")
]

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url, lastmod, changefreq, priority in core_pages:
    xml_lines.append(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')

# Dynamic articles
for article in articles_data:
    slug = article["slug"]
    published_at = article["publishedAt"]
    # Get YYYY-MM-DD from YYYY-MM-DDTHH:MM:SSZ
    date_part = published_at.split("T")[0]
    loc = f"https://cryptocasinomedia.com/press-releases/{slug}/"
    xml_lines.append(f'  <url><loc>{loc}</loc><lastmod>{date_part}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>')

xml_lines.append('</urlset>')
xml_content = "\n".join(xml_lines) + "\n"

try:
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    print(f"SUCCESS: sitemap.xml successfully updated at {sitemap_path} with {len(articles_data)} articles!")
except Exception as e:
    print(f"Error writing sitemap.xml: {e}")
    sys.exit(1)
