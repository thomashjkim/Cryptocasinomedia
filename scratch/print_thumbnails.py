import os
import sys

scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(scripts_dir, "scripts"))

try:
    from update_articles import articles_data
except ImportError as e:
    print(f"Error importing articles_data: {e}")
    sys.exit(1)

for art in articles_data:
    print(f"[{art['id']}] Category: {art['primaryCategory']} | Image: {art['thumbnailUrl']}")
    print(f"      Title: {art['title']}")
