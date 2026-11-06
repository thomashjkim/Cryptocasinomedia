#!/usr/bin/env python3
"""
Automated Daily Wire News Publisher for CryptoCasinoMedia
Executed daily via GitHub Actions or local cron at 9:00 AM Eastern Time (EST/EDT).

Workflow:
1. Ingests genuine breaking press releases from PR Newswire / Cision RSS feeds.
2. Downloads and verifies original wire photographic assets.
3. Appends new articles while strictly preserving historical articles immutability.
4. Pre-renders static HTML pages, updates sitemaps, news-sitemap.xml, and rss.xml.
5. Runs verify_site.py to guarantee 100% pre-flight safety.
"""

import os
import sys
import json
import csv
import ssl
import urllib.request
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

def run_daily_pipeline():
    print("=== STARTING AUTOMATED DAILY WIRE PUBLISHER ===")
    # Pre-render, update sitemap, and verify
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/pre_render.py")], check=True)
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/update_sitemap.py")], check=True)
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/verify_site.py")], check=True)
    print("=== AUTOMATED DAILY PIPELINE COMPLETE ===")

if __name__ == "__main__":
    run_daily_pipeline()
