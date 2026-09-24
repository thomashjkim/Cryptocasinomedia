#!/usr/bin/env python3
"""
Automated publisher for staged articles using articles_db.py:
1. Reads data/staged_articles.json
2. Sequentially appends each article via articles_db.append_article()
3. Runs scripts/pre_render.py
4. Runs scripts/update_sitemap.py (updates sitemaps, news 48h, rss, llms.txt, llms-full.txt)
5. Runs scripts/verify_site.py
"""
import os, sys, json, subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STAGED_JSON = os.path.join(DATA_DIR, "staged_articles.json")

sys.path.insert(0, SCRIPTS_DIR)
from articles_db import append_article, verify_immutability, load_articles

def publish():
    if not os.path.exists(STAGED_JSON):
        print(f"Error: {STAGED_JSON} does not exist.")
        sys.exit(1)
        
    with open(STAGED_JSON, "r", encoding="utf-8") as f:
        staged = json.load(f)
        
    current_articles = load_articles()
    existing_ids = {a['id'] for a in current_articles}
    
    # We want article 1 to be newest, so append in reverse order (art 3, art 2, art 1)
    to_add = [a for a in staged if a['id'] not in existing_ids]
    if not to_add:
        print("All staged articles already published.")
        return
        
    for art in reversed(to_add):
        art_clean = {k: v for k, v in art.items() if k not in ["imageFileName"]}
        print(f"Appending article: {art_clean['title']}")
        append_article(art_clean)
        
    valid, count = verify_immutability()
    print(f"[1/4] Master Articles verified: total {count} articles immutable.")
    
    # 2. Run pre_render.py
    print("[2/4] Running scripts/pre_render.py...")
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "pre_render.py")], check=True)
    
    # 3. Run update_sitemap.py
    print("[3/4] Running scripts/update_sitemap.py...")
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "update_sitemap.py")], check=True)
    
    # 4. Run verify_site.py
    print("[4/4] Running scripts/verify_site.py...")
    subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "verify_site.py")], check=True)
    
    print("\nALL STAGED ARTICLES SUCCESSFULLY PUBLISHED AND VERIFIED!")

if __name__ == "__main__":
    publish()
