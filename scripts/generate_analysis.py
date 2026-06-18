import sys
import os
import json
import anthropic
from dotenv import load_dotenv

# Add current dir to path to import update_articles
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from update_articles import articles_data

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

JSON_FILE = os.path.join(DATA_DIR, "expert_analysis.json")

def load_analysis():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_analysis(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_analysis(article):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""You are a B2B iGaming industry expert writing for CryptoCasinoMedia.
Write a 2-paragraph "Expert Analysis" for the following press release.
Do NOT summarize the press release. Instead, provide "Original Information Gain": add unique market context, regulatory implications, or industry insight about why this matters to operators, investors, or B2B professionals.
Do not use introductory phrases like "Here is an analysis". Just output the two paragraphs of analysis directly.
Use a highly professional, journalistic tone in English.

Title: {article['title']}
Topics: {', '.join(article['topics'])}
Excerpt: {article['excerpt']}
Lede: {article.get('lede', '')}
"""
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Error generating for {article['slug']}: {e}")
        return None

def main():
    if not ANTHROPIC_API_KEY:
        print("Error: ANTHROPIC_API_KEY not found.")
        return

    analysis_data = load_analysis()
    new_generated = 0
    
    print(f"Total articles found: {len(articles_data)}")
    
    for article in articles_data:
        slug = article['slug']
        if slug not in analysis_data:
            print(f"Generating analysis for: {slug}")
            result = generate_analysis(article)
            if result:
                analysis_data[slug] = result
                save_analysis(analysis_data)
                new_generated += 1
                print("  ✓ Success")
            else:
                print("  ✗ Failed")
        else:
            pass # Already exists
            
    print(f"\nDone! Generated {new_generated} new analyses.")

if __name__ == "__main__":
    main()
