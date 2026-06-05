import os
import sys

scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(scripts_dir, "scripts"))

try:
    from update_articles import articles_data
    from generate_daily_news import select_unique_image, write_to_update_articles
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

used_urls = set()
updated_articles = []

for article in articles_data:
    category = article.get("primaryCategory", "guides")
    chosen_url = select_unique_image(category, used_urls)
    
    article["thumbnailUrl"] = chosen_url
    used_urls.add(chosen_url)
    updated_articles.append(article)

write_to_update_articles(updated_articles)
print(f"SUCCESS: Migrated {len(updated_articles)} articles with 100% unique relevant images using fallback chain!")
