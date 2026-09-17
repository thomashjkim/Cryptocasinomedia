"""
CryptoCasinoMedia Articles Adapter
Loads the protected master articles dataset from data/articles_master.json.
This file is protected against accidental overwrites.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from articles_db import load_articles

articles_data = load_articles()

if __name__ == "__main__":
    print(f"Loaded {len(articles_data)} articles from protected master database.")
