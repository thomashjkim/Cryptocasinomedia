import urllib.request
import json
import re
import time

def extract_remix_context(html):
    # Find window.__remixContext = {...}
    start_idx = html.find('window.__remixContext =')
    if start_idx == -1:
        return None
    json_start = html.find('{', start_idx)
    # Match balanced braces
    brace_count = 0
    in_string = False
    escape = False
    for i in range(json_start, len(html)):
        c = html[i]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if not in_string:
            if c == '{':
                brace_count += 1
            elif c == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_str = html[json_start:i+1]
                    try:
                        return json.loads(json_str)
                    except Exception as e:
                        print(f"JSON parse error: {e}")
                        return None
    return None

def fetch_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
            ctx = extract_remix_context(html)
            if ctx:
                loader = ctx.get('state', {}).get('loaderData', {}).get('routes/($lang).buy-sell.all', {})
                return loader.get('articles', [])
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return []

print("Fetching Karrot articles...")
all_articles = {}

# 1. Main buy-sell page
arts = fetch_page('https://us.karrotmarket.com/buy-sell/')
for a in arts:
    all_articles[a['nodeId']] = a
print(f"Main page: {len(arts)} articles, unique: {len(all_articles)}")

# 2. Category & Keyword pages
keywords = [
    'furniture', 'table', 'chair', 'sofa', 'lamp', 'desk',
    'electronics', 'keyboard', 'monitor', 'camera', 'speaker',
    'women', 'dress', 'jacket', 'shoes', 'boots', 'bag',
    'kitchen', 'plant', 'pot', 'mug', 'plate',
    'baby', 'kids', 'toy', 'stroller',
    'pet', 'dog', 'cat', 'carrier',
    'bike', 'fitness', 'book', 'art', 'mirror', 'rug'
]

for kw in keywords:
    if len(all_articles) >= 150:
        break
    time.sleep(0.5)
    arts = fetch_page(f'https://us.karrotmarket.com/buy-sell/all/?search={kw}')
    for a in arts:
        all_articles[a['nodeId']] = a
    print(f"Keyword '{kw}': got {len(arts)}, total unique: {len(all_articles)}")

print(f"\nTotal harvested authentic Karrot articles: {len(all_articles)}")

with open('scraped_karrot_raw.json', 'w', encoding='utf-8') as f:
    json.dump(list(all_articles.values()), f, ensure_ascii=False, indent=2)
print("Saved scraped_karrot_raw.json")
