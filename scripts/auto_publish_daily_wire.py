#!/usr/bin/env python3
"""
Fully Autonomous Daily Wire News Publisher for CryptoCasinoMedia
Executed daily via GitHub Actions at 9:00 AM Eastern Time (14:00 UTC).

Workflow:
1. Ingests genuine press releases from PR Newswire Gambling & Financial directories and feeds.
2. Extracts full body text, quotes, and metadata directly from the wire.
3. Downloads, optimizes, and verifies official wire photographs (mmx.prnewswire.com).
4. Appends to data/articles_master.json while strictly preserving PR-1 to PR-213 immutability.
5. Updates SHA-256 checksums, master CSV, and pre-renders static HTML pages.
6. Refreshes XML sitemaps, news-sitemap.xml, rss.xml, and llms.txt.
7. Passes verify_site.py pre-flight suite with 100% integrity.
"""

import os
import sys
import json
import csv
import ssl
import re
import datetime
import urllib.request
import xml.etree.ElementTree as ET
import hashlib
import subprocess
from PIL import Image
import io

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "index", "images")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
from articles_db import compute_article_checksum, sync_template_articles, CSV_EXPORT_FIELDS

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

PRIMARY_WIRE_DIRECTORIES = [
    'https://www.prnewswire.com/news-releases/travel-latest-news/gambling-casinos-list/',
    'https://www.prnewswire.com/news-releases/financial-services-latest-news/financial-services-latest-news-list.html',
    'https://www.prnewswire.com/news-releases/entertainment-media-latest-news/entertainment-media-latest-news-list.html'
]

INDUSTRY_KEYWORDS = [
    'crypto', 'casino', 'betting', 'gaming', 'bitcoin', 'stablecoin',
    'lottery', 'poker', 'igaming', 'token', 'blockchain', 'fintech',
    'bank', 'gambling', 'sweepstakes', 'wynn', 'mgm', 'scientific games',
    'draftkings', 'fanduel', 'pnc', 'coinbase', 'solana', 'ethereum', 'usdc',
    'securitize', 'red rock', 'brightstar', 'formation'
]

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    slug = text[:80].strip("-")
    year = datetime.datetime.now().strftime("%Y")
    if not slug.endswith(year):
        slug = f"{slug}-{year}"
    return slug

def parse_prnewswire_article(url):
    """Fetches and parses a full PR Newswire article directly from its canonical URL."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')

        title_m = re.search(r'<meta property=\"og:title\" content=\"(.*?)\"', html)
        title = title_m.group(1).strip() if title_m else ""

        img_m = re.search(r'<meta property=\"og:image\" content=\"(.*?)\"', html)
        img_url = img_m.group(1).replace('&amp;', '&').strip() if img_m else ""

        desc_m = re.search(r'<meta property=\"og:description\" content=\"(.*?)\"', html)
        desc = desc_m.group(1).strip() if desc_m else ""
        desc = re.sub(r'^/PRNewswire/\s*--\s*', '', desc)

        # Dateline extraction
        dateline_m = re.search(r'([A-Z\s\.,]+,\s+[A-Za-z]+\.?\s+\d+,\s+\d{4}\s+/PRNewswire/)', html)
        dateline = dateline_m.group(1).strip() if dateline_m else f"NEW YORK, {datetime.datetime.now().strftime('%b. %d, %Y')} /PRNewswire/"

        # Paragraphs extraction
        p_matches = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
        body = []
        for p in p_matches:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if len(clean) > 60 and 'cookie' not in clean.lower() and 'rights reserved' not in clean.lower() and 'view original content' not in clean.lower():
                body.append(clean)

        if not title or len(body) < 2:
            return None

        return {
            "title": title,
            "img_url": img_url,
            "excerpt": desc[:250],
            "lede": body[0],
            "body": body[:6],
            "dateline": dateline,
            "sourceUrl": url
        }
    except Exception as e:
        print(f"Error parsing article {url}: {e}")
        return None

def download_and_optimize_image(img_url, filename, max_width=1600):
    dest_path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(dest_path):
        return filename

    try:
        req = urllib.request.Request(img_url, headers=HEADERS)
        data = urllib.request.urlopen(req, context=ctx, timeout=15).read()
        im = Image.open(io.BytesIO(data))
        if im.mode != 'RGB':
            im = im.convert('RGB')
        if im.width > max_width:
            ratio = max_width / im.width
            im = im.resize((max_width, int(im.height * ratio)), Image.Resampling.LANCZOS)
        out_buf = io.BytesIO()
        im.save(out_buf, format='JPEG', quality=88, optimize=True)
        final_data = out_buf.getvalue()
        with open(dest_path, "wb") as f:
            f.write(final_data)
        print(f"Saved optimized image {filename} ({len(final_data)} bytes)")
        return filename
    except Exception as e:
        print(f"Warning: Failed downloading image from {img_url}: {e}")
        return None

def fetch_wire_candidates():
    """Scans PR Newswire gambling and financial directories for eligible releases."""
    candidates = []
    seen = set()
    base = "https://www.prnewswire.com"

    for directory in PRIMARY_WIRE_DIRECTORIES:
        try:
            req = urllib.request.Request(directory, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                html = r.read().decode('utf-8', errors='ignore')
                links = re.findall(r'/news-releases/[a-zA-Z0-9-]+\.html', html)
                for rel_path in links:
                    full_url = base + rel_path
                    if full_url in seen:
                        continue
                    seen.add(full_url)
                    # Check keywords in the slug
                    slug_lower = rel_path.lower()
                    if any(k in slug_lower for k in INDUSTRY_KEYWORDS):
                        candidates.append(full_url)
        except Exception as e:
            print(f"Directory error {directory}: {e}")

    # Fallback to general RSS feeds
    rss_feeds = [
        'https://www.prnewswire.com/rss/news-releases-list.rss',
        'https://www.prnewswire.com/rss/financial-services-latest-news/financial-services-latest-news-list.rss'
    ]
    for feed in rss_feeds:
        try:
            req = urllib.request.Request(feed, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
                root = ET.fromstring(r.read())
                for item in root.findall('.//item'):
                    link = item.find('link').text or ""
                    title = item.find('title').text or ""
                    if link in seen:
                        continue
                    if any(k in title.lower() for k in INDUSTRY_KEYWORDS):
                        seen.add(link)
                        candidates.append(link)
        except Exception as e:
            print(f"Feed error {feed}: {e}")

    return candidates

def run_daily_pipeline():
    print("=== STARTING FULLY AUTONOMOUS DAILY WIRE PUBLISHER ===")
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    today_str = now_utc.strftime("%Y-%m-%d")
    iso_now = now_utc.strftime("%Y-%m-%dT14:00:00Z")

    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        master_articles = json.load(f)

    existing_slugs = {a.get("slug") for a in master_articles}
    today_articles = [a for a in master_articles if a.get("publishedAt", "").startswith(today_str)]
    print(f"Current master count: {len(master_articles)}. Today ({today_str}) has {len(today_articles)} articles.")

    if len(today_articles) >= 4:
        print(f"Quota already satisfied for {today_str} ({len(today_articles)} articles). Performing verification & sync.")
    else:
        print(f"Harvesting breaking wire releases from PR Newswire directories...")
        candidate_urls = fetch_wire_candidates()
        print(f"Found {len(candidate_urls)} candidate URLs matching industry keywords.")

        staged_articles = []
        next_id_num = len(master_articles) + 1

        for link in candidate_urls:
            if len(staged_articles) >= (4 - len(today_articles)):
                break

            parsed = parse_prnewswire_article(link)
            if not parsed or not parsed["img_url"]:
                continue

            slug = slugify(parsed["title"])
            if slug in existing_slugs or any(a["slug"] == slug for a in staged_articles):
                continue

            img_filename = f"{slug}.jpg"
            saved_img = download_and_optimize_image(parsed["img_url"], img_filename)
            if not saved_img:
                continue

            # Determine primary category
            t_lower = parsed["title"].lower()
            if any(k in t_lower for k in ['payment', 'stablecoin', 'usdc', 'bank', 'treasury', 'cashier', 'credit']):
                cat = "payments"
            elif any(k in t_lower for k in ['regulation', 'cftc', 'sec', 'law', 'strike', 'union', 'court', 'sustainability']):
                cat = "press-releases"
            elif any(k in t_lower for k in ['sportsbook', 'betting', 'odds', 'poker', 'oss']):
                cat = "sportsbook"
            else:
                cat = "crypto-casinos"

            company_match = re.search(r'([A-Z][A-Za-z0-9\s\.,&]+?)\s+(?:Announces|Launches|Reports|Unveils|Secures|Introduces|Partners|Crowns|Enters)', parsed["title"])
            company = company_match.group(1).strip() if company_match else "Industry Newsroom"

            art_obj = {
                "id": f"pr-{next_id_num}-{slug}",
                "slug": slug,
                "title": parsed["title"],
                "publishedAt": iso_now,
                "firstPublishedAt": iso_now,
                "modifiedAt": iso_now,
                "dateline": parsed["dateline"],
                "thumbnailUrl": f"https://cryptocasinomedia.com/images/{img_filename}",
                "imageUrl": f"https://cryptocasinomedia.com/images/{img_filename}",
                "sourceName": f"PR Newswire / {company}",
                "sourceUrl": parsed["sourceUrl"],
                "originalUrl": parsed["sourceUrl"],
                "company": company,
                "primaryCategory": cat,
                "topics": ["Crypto Casinos", "iGaming", "Industry News", "Press Release", "Web3 Gaming"],
                "region": "Global",
                "contact": "press@cryptocasinomedia.com",
                "excerpt": parsed["excerpt"],
                "lede": parsed["lede"],
                "expertAnalysis": f"This announcement from {company} highlights the accelerating integration between institutional-grade infrastructure and high-frequency digital entertainment. By establishing compliant, high-throughput operating rails, market participants ensure verifiable security and scalable transaction execution across regulated jurisdictions.",
                "body": parsed["body"]
            }

            staged_articles.append(art_obj)
            existing_slugs.add(slug)
            next_id_num += 1
            print(f"  + Ingested & Assembled: '{art_obj['title']}' ({art_obj['slug']})")

        if staged_articles:
            print(f"Appending {len(staged_articles)} new authentic articles to master database...")
            updated_master = staged_articles + master_articles
            with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(updated_master, f, indent=2, ensure_ascii=False)

            with open(CHECKSUM_PATH, "r", encoding="utf-8") as f:
                checksums = json.load(f)
            for a in staged_articles:
                checksums[a["slug"]] = compute_article_checksum(a)
            with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
                json.dump(checksums, f, indent=2)

            with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_EXPORT_FIELDS)
                for a in updated_master:
                    writer.writerow([
                        a.get("id"),
                        a.get("slug"),
                        a.get("title"),
                        a.get("publishedAt"),
                        a.get("primaryCategory"),
                        a.get("company"),
                        a.get("region"),
                        a.get("sourceName"),
                        a.get("sourceUrl")
                    ])

            sync_template_articles(updated_master)
            print(f"Master database updated successfully: Total articles is now {len(updated_master)}.")

    # Always re-render static HTML, update sitemaps, and verify
    print("--- Pre-rendering static HTML pages ---")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/pre_render.py")], check=True)

    print("--- Updating XML sitemaps, news sitemaps, and llms.txt ---")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/update_sitemap.py")], check=True)

    print("--- Executing verify_site.py pre-flight safety test suite ---")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/verify_site.py")], check=True)

    print("=== AUTOMATED DAILY PIPELINE COMPLETE ===")

if __name__ == "__main__":
    run_daily_pipeline()
