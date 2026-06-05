import urllib.request
import re
import time

KEYWORDS = {
    "crypto-casinos": ["casino", "roulette", "blackjack", "poker", "slot-machine"],
    "sportsbook": ["stadium", "sports-betting", "soccer-field", "basketball-betting"],
    "payments": ["bitcoin", "ethereum", "cryptocurrency", "gold-coins"],
    "regulation": ["gavel", "law-books", "courtroom", "scales-of-justice"],
    "sweepstakes": ["arcade", "gold-coins", "slot-machine", "mobile-gaming"],
    "guides": ["infographic-chart", "notebook-pen", "study-guide", "tutorial"]
}

def scrape_keyword(keyword):
    url = f"https://unsplash.com/s/photos/{keyword}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error scraping {keyword}: {e}")
        return []
        
    # Match patterns like: images.unsplash.com/photo-1596838132731-3301c3fd4317 or href="/photos/XXXXXX"
    # Let's search for photo-XXXXXXXXXXXXX
    matches = re.findall(r"photo-([a-zA-Z0-9\-]+)", html)
    # Remove duplicates and preserve order
    seen = set()
    unique_ids = []
    for m in matches:
        if m not in seen and len(m) > 10:  # Unsplash IDs are typically 10-15 chars, photo IDs have hyphen-separated components
            seen.add(m)
            unique_ids.append(m)
    return unique_ids

def verify_photo(photo_id):
    url = f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&q=80&w=800"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status == 200
    except Exception:
        return False

def main():
    results = {}
    for category, kw_list in KEYWORDS.items():
        print(f"Scraping category: {category}...")
        cat_ids = []
        for kw in kw_list:
            ids = scrape_keyword(kw)
            print(f"  Keyword '{kw}': found {len(ids)} candidates.")
            cat_ids.extend(ids)
            time.sleep(1) # politely sleep
            
        # Deduplicate candidates
        cat_ids = list(dict.fromkeys(cat_ids))
        
        # Verify active images
        verified = []
        print(f"  Verifying {len(cat_ids)} unique candidates...")
        for pid in cat_ids[:35]: # test first 35
            if verify_photo(pid):
                verified.append(pid)
                if len(verified) >= 20: # we want around 20 verified unique images per category
                    break
        print(f"  Category '{category}' verified {len(verified)} images.")
        results[category] = verified
        
    print("\n--- FINAL RESULTS ---")
    import pprint
    pprint.pprint(results)

if __name__ == "__main__":
    main()
