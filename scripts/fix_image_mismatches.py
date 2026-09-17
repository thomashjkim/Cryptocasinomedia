#!/usr/bin/env python3
"""
Fix visually verified image mismatches in articles_master.json.
Sports images on non-sportsbook articles must be replaced with thematic assets.
"""

import json
import hashlib
import csv
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "index/index.html.template")

BASE_URL = "https://cryptocasinomedia.com/images/"

# Visually verified remappings (slug -> correct image filename)
REMAPPINGS = {
    # Was: ccm_003.jpg (Argentina vs Spain soccer match) -> WRONG for crypto-casino
    "bitcoin-halving-crypto-casino-impact-june-2026": "ccm_011.jpg",
    # Was: ccm_031.jpg (NFL American football) -> WRONG for payments
    "fast-payout-online-casinos-blockchain-standards-2026": "ccm_037.jpg",
    # Was: bluff_gamblefi_21m_funding.png (soccer boot kicking ball) -> WRONG for crypto-casino
    "gamblefi-growth-decentralized-casinos-profit-sharing-2026": "ccm_087.jpg",
    # Was: ccm_036.jpg (NFL football live sports betting room) -> WRONG for crypto-casino
    "high-roller-crypto-casinos-bitcoin-whales-2026": "ccm_044.jpg",
    # Was: chumba_sweeps_casino_bonus.png (FIFA World Cup Trophy & ball!) -> WRONG for sweepstakes
    "list-of-online-casinos-usa-for-real-money-players-2026": "ccm_077.jpg",
    # Was: ccm_081.jpg (World Cup fan zone betting) -> WRONG for sweepstakes
    "sweepstakes-bonus-portal-launch-usa-2026": "ccm_079.jpg",
    # Was: uae_vara_enforcement.jpg (children in Africa!) -> WRONG for UAE regulation
    "uae-vara-crypto-casino-enforcement-proof-of-reserves-mandatory-2026": "uae_vara_crypto_enforcement.jpg",
}

CSV_EXPORT_FIELDS = [
    'id', 'slug', 'title', 'publishedAt', 'firstPublishedAt', 'modifiedAt',
    'dateline', 'thumbnailUrl', 'sourceName', 'sourceUrl', 'company',
    'primaryCategory', 'region', 'contact', 'excerpt', 'boilerplate'
]

def compute_article_checksum(a):
    immutable_str = f"{a.get('id')}|{a.get('slug')}|{a.get('title')}|{a.get('publishedAt')}|{a.get('dateline')}|{a.get('thumbnailUrl')}|{a.get('company')}|{a.get('sourceUrl')}"
    return hashlib.sha256(immutable_str.encode('utf-8')).hexdigest()


def main():
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"Loaded {len(articles)} articles")
    
    # Verify images exist before applying
    images_dir = os.path.join(PROJECT_ROOT, "index/images")
    for slug, img_file in REMAPPINGS.items():
        img_path = os.path.join(images_dir, img_file)
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")
        print(f"  [OK] {img_file} exists ({os.path.getsize(img_path):,} bytes)")

    print("\nApplying remappings...")
    changed = 0
    for a in articles:
        slug = a.get("slug")
        if slug in REMAPPINGS:
            new_img = REMAPPINGS[slug]
            new_url = BASE_URL + new_img
            old_url = a.get("thumbnailUrl")
            a["thumbnailUrl"] = new_url
            a["imageUrl"] = new_url
            print(f"  FIXED: {slug}")
            print(f"    OLD: {old_url}")
            print(f"    NEW: {new_url}")
            changed += 1

    print(f"\n{changed} articles updated")

    # Save master JSON
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print("Saved articles_master.json")

    # Recompute checksums for ALL articles (thumbnailUrl is in checksum)
    checksums = {}
    for a in articles:
        checksums[a["slug"]] = compute_article_checksum(a)
    with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2)
    print(f"Recomputed checksums for {len(checksums)} articles -> articles_checksum.json")

    # Update CSV
    with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_EXPORT_FIELDS, extrasaction='ignore')
        writer.writeheader()
        for item in articles:
            writer.writerow(item)
    print("Updated articles_master.csv")

    # Sync to template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = f.read()

    start_marker = "const ARTICLES = ["
    end_marker = "];\n\n        // ============================================================================\n        // 2. COMPONENT RENDERERS"
    start_pos = tpl.find(start_marker)
    end_pos = tpl.find(end_marker, start_pos)

    if start_pos == -1 or end_pos == -1:
        m = re.search(r'const ARTICLES = \[.*?\];', tpl, re.DOTALL)
        if not m:
            raise ValueError("Could not locate const ARTICLES in index.html.template")
        start_pos = m.start()
        end_pos = m.end() - 2

    articles_js = json.dumps(articles, indent=8, ensure_ascii=False)
    new_tpl = tpl[:start_pos] + "const ARTICLES = " + articles_js + ";" + tpl[end_pos + 2:]

    with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(new_tpl)
    print("Synced index/index.html.template")

    print("\nDone. Run pre_render.py next.")


if __name__ == "__main__":
    main()
