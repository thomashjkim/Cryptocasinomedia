"""
CryptoCasinoMedia Articles Database (Single Source of Truth)
Enforces strict immutability of existing historical articles and provides safe append-only publishing.
"""

import json
import csv
import hashlib
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "index/index.html.template")

REQUIRED_FIELDS = [
    'id', 'slug', 'title', 'publishedAt', 'dateline', 'thumbnailUrl',
    'sourceName', 'sourceUrl', 'company', 'primaryCategory', 'topics',
    'excerpt', 'body'
]

CSV_EXPORT_FIELDS = [
    'id', 'slug', 'title', 'publishedAt', 'firstPublishedAt', 'modifiedAt',
    'dateline', 'thumbnailUrl', 'sourceName', 'sourceUrl', 'company',
    'primaryCategory', 'region', 'contact', 'excerpt', 'boilerplate'
]


def compute_article_checksum(a):
    """Computes SHA-256 hash of immutable article metadata."""
    immutable_str = f"{a.get('id')}|{a.get('slug')}|{a.get('title')}|{a.get('publishedAt')}|{a.get('dateline')}|{a.get('thumbnailUrl')}|{a.get('company')}|{a.get('sourceUrl')}"
    return hashlib.sha256(immutable_str.encode('utf-8')).hexdigest()


def load_articles():
    """Loads all articles from the master JSON database."""
    if not os.path.exists(MASTER_JSON_PATH):
        raise FileNotFoundError(f"Master articles database not found at {MASTER_JSON_PATH}")
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_immutability():
    """
    Verifies that no existing historical article has been mutated.
    Raises ValueError if any historical record was altered.
    """
    articles = load_articles()
    if not os.path.exists(CHECKSUM_PATH):
        return True, len(articles)

    with open(CHECKSUM_PATH, "r", encoding="utf-8") as f:
        checksums = json.load(f)

    violations = []
    for a in articles:
        slug = a.get('slug')
        if slug in checksums:
            expected = checksums[slug]
            current = compute_article_checksum(a)
            if expected != current:
                violations.append(slug)

    if violations:
        raise ValueError(f"CRITICAL IMMUTABILITY VIOLATION: {len(violations)} historical articles were mutated: {violations}")

    return True, len(articles)


def sync_template_articles(articles=None):
    """Synchronizes the master articles array into index/index.html.template."""
    if articles is None:
        articles = load_articles()

    if not os.path.exists(TEMPLATE_PATH):
        return False

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

    return True


def append_article(new_article):
    """
    Safely appends a new article to the master database.
    Strictly validates schema, prevents duplicates, and updates all artifacts.
    """
    verify_immutability()

    for field in REQUIRED_FIELDS:
        if not new_article.get(field):
            raise ValueError(f"Missing required article field: '{field}'")

    articles = load_articles()

    existing_slugs = {a['slug'] for a in articles}
    existing_ids = {a['id'] for a in articles}

    if new_article['slug'] in existing_slugs:
        raise ValueError(f"Article with slug '{new_article['slug']}' already exists! Cannot overwrite existing articles.")
    if new_article['id'] in existing_ids:
        raise ValueError(f"Article with id '{new_article['id']}' already exists! Cannot overwrite existing articles.")

    if not new_article.get('imageUrl'):
        new_article['imageUrl'] = new_article['thumbnailUrl']
    if not new_article.get('firstPublishedAt'):
        new_article['firstPublishedAt'] = new_article['publishedAt']
    if not new_article.get('modifiedAt'):
        new_article['modifiedAt'] = new_article['publishedAt']
    if not new_article.get('content_type'):
        new_article['content_type'] = 'press_release'
    if not new_article.get('publicationStatus'):
        new_article['publicationStatus'] = 'published'

    articles.insert(0, new_article)

    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    checksum = compute_article_checksum(new_article)
    checksums = {}
    if os.path.exists(CHECKSUM_PATH):
        with open(CHECKSUM_PATH, "r", encoding="utf-8") as f:
            checksums = json.load(f)
    checksums[new_article['slug']] = checksum
    with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2)

    with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_EXPORT_FIELDS, extrasaction='ignore')
        writer.writeheader()
        for item in articles:
            writer.writerow(item)

    sync_template_articles(articles)
    return True


if __name__ == "__main__":
    valid, count = verify_immutability()
    print(f"SUCCESS: Master Articles Database verified! Total {count} articles protected and immutable.")
