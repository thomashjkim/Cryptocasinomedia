#!/usr/bin/env python3
"""
Publishes 6 real PR Newswire, GlobeNewswire, and Business Wire releases for November 4, 2026.
Updates articles_master.json, articles_checksum.json, articles_master.csv,
index.html.template, pre-renders static HTML, and runs pre-flight verification.
"""

import os
import sys
import json
import csv
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
from articles_db import compute_article_checksum, sync_template_articles, verify_immutability, CSV_EXPORT_FIELDS

# Import the 6 prepared Nov 4 articles
scratch_script = os.path.join(PROJECT_ROOT, ".gemini/antigravity/brain/559a368e-49d2-4e82-a47e-ec2ab5cc5f91/scratch/prepare_nov4_articles.py")
if not os.path.exists(scratch_script):
    # Fallback to local import if needed
    import importlib.util
    spec = importlib.util.spec_from_file_location("prepare_nov4", os.path.expanduser("~/.gemini/antigravity/brain/559a368e-49d2-4e82-a47e-ec2ab5cc5f91/scratch/prepare_nov4_articles.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    nov4_articles = mod.nov4_articles
else:
    import importlib.util
    spec = importlib.util.spec_from_file_location("prepare_nov4", scratch_script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    nov4_articles = mod.nov4_articles

def main():
    print("=== PUBLISHING NOVEMBER 4, 2026 WIRE BATCH ===")
    verify_immutability()
    print("  [PASS] Immutability verified before ingestion.")

    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    existing_slugs = {a["slug"] for a in articles}
    added_count = 0

    for art in nov4_articles:
        if art["slug"] in existing_slugs:
            print(f"  [SKIP] Article already exists: {art['slug']}")
            continue

        # Standardize URLs and fields
        slug = art["slug"]
        art["thumbnailUrl"] = f"https://cryptocasinomedia.com/images/{slug}.jpg"
        art["imageUrl"] = f"https://cryptocasinomedia.com/images/{slug}.jpg"
        art["content_type"] = "press_release"
        art["publicationStatus"] = "published"

        articles.append(art)
        added_count += 1
        print(f"  [ADD] {art['title'][:70]}...")

    # Sort strictly by publishedAt descending
    articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
    print(f"  Total articles in database: {len(articles)} (Added {added_count})")

    # 1. Save master JSON
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"  [SAVED] {MASTER_JSON_PATH}")

    # 2. Update checksums
    checksums = {}
    for a in articles:
        checksums[a["slug"]] = compute_article_checksum(a)
    with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2, ensure_ascii=False)
    print(f"  [UPDATED] {CHECKSUM_PATH} with {len(checksums)} entries.")

    # 3. Export to CSV
    with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_EXPORT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for a in articles:
            row = {k: a.get(k, "") for k in CSV_EXPORT_FIELDS}
            if isinstance(row.get("topics"), list):
                row["topics"] = "; ".join(row["topics"])
            writer.writerow(row)
    print(f"  [EXPORTED] {MASTER_CSV_PATH}")

    # 4. Sync template
    sync_template_articles(articles)
    print(f"  [SYNCED] index/index.html.template")

    # 5. Pre-render all pages
    print("\n--- Running Pre-Render Pipeline ---")
    res = subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/pre_render.py")], check=True)
    if res.returncode != 0:
        raise RuntimeError("pre_render.py failed")

    # 6. Verify pre-flight suite
    print("\n--- Running Pre-Flight Verification Suite ---")
    res = subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/verify_site.py")], check=True)
    if res.returncode != 0:
        raise RuntimeError("verify_site.py failed")

    print("\n=== SUCCESS: NOVEMBER 4, 2026 BATCH PUBLISHED & VERIFIED! ===")

if __name__ == "__main__":
    main()
