#!/usr/bin/env python3
"""
update_archive_images.py
Maps rich, category-specific, bespoke editorial images from index/images/ 
to all 1,000 historical wire archive articles in data/articles_archive_1000.json,
completely eliminating repetitive placeholder thumbnails.
"""

import os
import json
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_JSON = os.path.join(PROJECT_ROOT, "data", "articles_archive_1000.json")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "index", "images")

if not os.path.exists(ARCHIVE_JSON):
    print(f"Error: {ARCHIVE_JSON} not found!")
    exit(1)

with open(ARCHIVE_JSON, "r", encoding="utf-8") as f:
    articles = json.load(f)

# Collect all valid image filenames from index/images/ excluding og-image.jpg
all_imgs = [
    f for f in os.listdir(IMAGES_DIR)
    if f.endswith(('.jpg', '.png', '.webp')) and f != 'og-image.jpg'
]

# Categorize images by relevance
img_pools = {
    'crypto-casinos': [],
    'sportsbook': [],
    'payments': [],
    'regulation': [],
    'sweepstakes': []
}

for img in all_imgs:
    low = img.lower()
    if any(k in low for k in ['sport', 'bet', 'odds', 'wager', 'poker', 'acr', 'esport', 'thunderpick', 'racing', 'draftking', 'betmgm', 'bet365', 'espn', 'messi', 'football', 'tennis']):
        img_pools['sportsbook'].append(img)
    if any(k in low for k in ['pay', 'usdc', 'usde', 'solana', 'settle', 'cashier', 'wallet', 'treasury', 'stable', 'deposit', 'trc20', 'bank', 'fintech', 'arbitrum', 'orbit', 'eth', 'bitcoin', 'token', 'binance', 'bybit', 'chain']):
        img_pools['payments'].append(img)
    if any(k in low for k in ['reg', 'mica', 'sec', 'cftc', 'curacao', 'ukgc', 'malta', 'mga', 'gcb', 'complian', 'licens', 'law', 'court', 'hearing', 'jurisdiction', 'fatf', 'vara', 'state', 'policy']):
        img_pools['regulation'].append(img)
    if any(k in low for k in ['sweep', 'social', 'chumba', 'fliff', 'tracker', 'stakeus', 'luckyland']):
        img_pools['sweepstakes'].append(img)
    if any(k in low for k in ['casino', 'stake', 'roobet', 'rollbit', 'bc_game', 'bcgame', 'pragmatic', 'slot', 'gamble', 'game', 'spin', 'wsm', 'lucky_block', 'tg_casino', 'megadice', 'shuffle', 'soft2bet', 'aristocrat']):
        img_pools['crypto-casinos'].append(img)

# Combine with ccm_ general editorial images for maximum variety
ccm_imgs = sorted([img for img in all_imgs if img.startswith('ccm_')])

for cat in img_pools:
    specific = sorted(list(set(img_pools[cat])))
    combined = []
    c_idx = 0
    for s in specific:
        combined.append(s)
        if c_idx < len(ccm_imgs) and len(combined) % 3 == 0:
            combined.append(ccm_imgs[c_idx])
            c_idx += 1
    while c_idx < len(ccm_imgs):
        combined.append(ccm_imgs[c_idx])
        c_idx += 1
    img_pools[cat] = combined

# Counters per category to cycle through the pools
cat_counters = {cat: 0 for cat in img_pools}

# Direct company matching
for article in articles:
    company = article.get('company', '')
    cat = article.get('primaryCategory', 'crypto-casinos')
    if cat not in img_pools:
        cat = 'crypto-casinos'
    
    # Try exact company match first
    slug_company = re.sub(r'[^a-z0-9]', '', company.lower())
    company_match = [
        img for img in all_imgs 
        if slug_company and slug_company in re.sub(r'[^a-z0-9]', '', img.lower())
    ]
    
    if company_match:
        # Pick from company matches using article id hash
        chosen_img = company_match[abs(hash(article['id'])) % len(company_match)]
    else:
        # Pick next image in the category pool
        pool = img_pools[cat]
        idx = cat_counters[cat] % len(pool)
        chosen_img = pool[idx]
        cat_counters[cat] += 1
    
    img_url = f"https://cryptocasinomedia.com/images/{chosen_img}"
    article['thumbnailUrl'] = img_url
    article['imageUrl'] = img_url

with open(ARCHIVE_JSON, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

print(f"Successfully updated all {len(articles)} archive articles with diverse editorial images!")
for cat, count in cat_counters.items():
    print(f"  {cat}: cycled {count} articles across {len(img_pools[cat])} unique images")
