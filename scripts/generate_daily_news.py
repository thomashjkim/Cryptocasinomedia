import os
import sys
import json
import datetime
import urllib.request
import urllib.error

# Add current scripts directory to sys.path to load local modules
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(scripts_dir)

try:
    from update_articles import articles_data
except ImportError as e:
    print(f"Error: Could not import articles_data from update_articles.py: {e}")
    sys.exit(1)

# Expanded pools of high-quality verified Unsplash image URLs per category to guarantee uniqueness
IMAGE_POOLS = {
    "crypto-casinos": [
        "https://images.unsplash.com/photo-1596838132731-3301c3fd4317?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1606167668584-78701c57f13d?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1570649236495-42fa5fe3c48b?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1605809831853-4117905d0d41?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1596838132646-c73db2f664df?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1511193311914-0346f16efe90?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1609501676725-7186f017a4b7?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?auto=format&fit=crop&q=80&w=800"
    ],
    "sportsbook": [
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1505250469679-203ad9ced0cb?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1518063319789-7217e6706b04?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1541252260730-0412e8e2108e?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1599447421416-3414500d18a5?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1579952362224-d986950002a4?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1519766304817-4f37bda74a27?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1540747737956-37872404f802?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?auto=format&fit=crop&q=80&w=800"
    ],
    "regulation": [
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1505664194779-8bebcb95c553?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1521791136364-72864c003222?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1447069387593-a5de0862481e?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&q=80&w=800"
    ],
    "payments": [
        "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1563013544-824ae1d704d3?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1601597111158-2fceff270190?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1616077168079-7e09a677fb2c?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1516245834210-c4c142787335?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1621761191319-c6fb62004040?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1622630998477-20aa696ecb05?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1629339942248-47d49e0855d6?auto=format&fit=crop&q=80&w=800"
    ],
    "sweepstakes": [
        "https://images.unsplash.com/photo-1541256996761-85df2efaa164?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1612287230202-1bf1d85d1bdf?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1560253023-3ec5d502959f?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1553481187-be93c21490a9?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1566241440091-ec10de8db2e1?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1551103782-8ab07afd45c1?auto=format&fit=crop&q=80&w=800"
    ],
    "guides": [
        "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&q=80&w=800",
        "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?auto=format&fit=crop&q=80&w=800"
    ]
}

def select_unique_image(category, existing_urls):
    pool = IMAGE_POOLS.get(category, IMAGE_POOLS.get("guides"))
    unused = [url for url in pool if url not in existing_urls]
    if unused:
        return unused[0]
    all_unused = []
    for cat, urls in IMAGE_POOLS.items():
        for url in urls:
            if url not in existing_urls and url not in all_unused:
                all_unused.append(url)
    if all_unused:
        return all_unused[0]
    return pool[0]


def get_next_date():
    # Detect the date of the latest article in our database
    dates = []
    for art in articles_data:
        try:
            dt = datetime.datetime.strptime(art["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            dates.append(dt)
        except Exception:
            pass
    if dates:
        latest = max(dates)
        # The next day's date
        next_day = latest + datetime.timedelta(days=1)
        return next_day
    return datetime.datetime.utcnow()

def serialize_articles(articles):
    # Formats the articles array to standard, readable Python code blocks matching update_articles.py
    lines = ["articles_data = ["]
    for i, art in enumerate(articles):
        art_lines = ["  {"]
        art_lines.append(f'    "id": {json.dumps(art["id"])},')
        art_lines.append(f'    "slug": {json.dumps(art["slug"])},')
        art_lines.append(f'    "originalUrl": {json.dumps(art["originalUrl"])},')
        art_lines.append(f'    "title": {json.dumps(art["title"])},')
        art_lines.append(f'    "publishedAt": {json.dumps(art["publishedAt"])},')
        art_lines.append(f'    "sourceName": {json.dumps(art["sourceName"])},')
        art_lines.append(f'    "thumbnailUrl": {json.dumps(art["thumbnailUrl"])},')
        art_lines.append(f'    "dateline": {json.dumps(art["dateline"])},')
        art_lines.append(f'    "lede": {json.dumps(art["lede"])},')
        
        body_json = ",\n".join([f'      {json.dumps(p)}' for p in art["body"]])
        art_lines.append(f'    "body": [\n{body_json}\n    ],')
        
        art_lines.append(f'    "topics": {json.dumps(art["topics"])},')
        art_lines.append(f'    "primaryCategory": {json.dumps(art["primaryCategory"])},')
        art_lines.append(f'    "company": {json.dumps(art["company"])},')
        art_lines.append(f'    "region": {json.dumps(art["region"])},')
        art_lines.append(f'    "contact": {json.dumps(art["contact"])},')
        art_lines.append(f'    "excerpt": {json.dumps(art["excerpt"])}')
        art_lines.append("  }")
        
        item_str = "\n".join(art_lines)
        if i < len(articles) - 1:
            item_str += ","
        lines.append(item_str)
    lines.append("]")
    return "\n".join(lines)

def write_to_update_articles(updated_articles_data):
    # Overwrites update_articles.py with the updated list of articles
    file_path = os.path.join(scripts_dir, "update_articles.py")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_marker = "articles_data = ["
    end_marker = "\n\ndef main():"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Error: Could not locate articles_data start in update_articles.py")
        sys.exit(1)
        
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("Error: Could not locate main() landmark in update_articles.py")
        sys.exit(1)
        
    serialized = serialize_articles(updated_articles_data)
    
    new_content = content[:start_idx] + serialized + content[end_idx:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"SUCCESS: update_articles.py successfully updated with {len(updated_articles_data)} articles!")

def generate_mock_articles(next_date):
    # Generates 5 high-quality mock press releases if the Gemini API Key is missing (useful for testing)
    import random
    existing_urls = {art["thumbnailUrl"] for art in articles_data if "thumbnailUrl" in art}
    
    companies = ["Stake.com", "BC.GAME", "Rollbit", "Roobet", "Curacao Gaming Board", "MGA", "Coinbase Commerce", "Tether"]
    categories = ["crypto-casinos", "sportsbook", "regulation", "payments", "sweepstakes", "guides"]
    regions = ["Europe", "USA", "Global", "Asia", "Latin America"]
    
    date_str = next_date.strftime("%Y-%m-%d")
    date_iso = next_date.strftime("%Y-%m-%dT09:00:00Z")
    dateline_str = next_date.strftime("%B %d, %Y").replace(" 0", " ")
    
    new_articles = []
    for offset in range(5):
        category = random.choice(categories)
        company = random.choice(companies)
        region = random.choice(regions)
        
        art_id = f"pr-{len(articles_data) + offset + 1}"
        slug = f"automated-press-release-{art_id}-{date_str}"
        title = f"{company} Announces Major {category.replace('-', ' ').title()} Expansion in {region} for Q2 2026"
        
        body = [
            f"{company} has officially announced a new strategic roadmap targeting the {category.replace('-', ' ')} sector in {region}. The initiative aims to align platform compliance with upcoming global standards and meet growing customer demands.",
            "The expansion features upgraded transaction processing, enabling players to execute deposit and withdrawal requests via native blockchain rails in seconds. By deploying layer-2 scaling solutions, transaction friction is reduced to near-zero.",
            f"“We are thrilled to launch this new phase of our expansion,” said a {company} communications officer. “By combining blockchain efficiency with regulatory safety, we believe this rollout sets a new benchmark for players in {region}.”",
            "Technical audits have been completed by third-party smart contract verifiers to ensure the safety of developer endpoints and user assets. The updates will begin rolling out across active markets immediately.",
            "As digital asset regulations tighten globally, operators prioritize robust KYC/AML frameworks. This upgrade ensures full compliance with local financial authorities while maintaining standard user privacy parameters."
        ]
        
        # Select unique unused image
        thumbnail = select_unique_image(category, existing_urls)
        existing_urls.add(thumbnail)
        
        new_articles.append({
            "id": art_id,
            "slug": slug,
            "originalUrl": f"https://cryptocasinomedia.com/press-releases/{slug}",
            "title": title,
            "publishedAt": date_iso,
            "sourceName": company,
            "thumbnailUrl": thumbnail,
            "dateline": f"LONDON, UK, {dateline_str[:3]}. {next_date.day}, {next_date.year}",
            "lede": body[0],
            "body": body,
            "topics": [category.replace('-', ' ').title(), company, region],
            "primaryCategory": category,
            "company": company,
            "region": region,
            "contact": f"press@{company.lower().replace('.com', '')}.io",
            "excerpt": f"{company} expands its {category.replace('-', ' ')} service suite in {region} with updated speed and security protocols."
        })
        
    return new_articles

def generate_ai_articles(api_key, next_date):
    # Generates 5 unique press releases using the Gemini API in JSON mode
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    
    date_str = next_date.strftime("%Y-%m-%d")
    date_iso = next_date.strftime("%Y-%m-%dT09:00:00Z")
    dateline_str = next_date.strftime("%b. %d, %Y").replace(" 0", " ") # e.g. Jun. 2, 2026
    
    prompt = f"""
Generate exactly 5 unique, realistic B2B press releases/news articles for the news publisher "CryptoCasinoMedia" as of the publish date {date_iso} (Dateline string should be e.g. "LONDON, UK, {dateline_str}").
The articles should focus on crypto casinos, sportsbooks, iGaming regulation, blockchain payments, or sweepstakes in 2026.
Include a variety of companies: Stake, BC.GAME, Rollbit, Roobet, Curacao Gaming Control Board, MGA, Flutter Entertainment, Coinbase, or similar major players.

You MUST use ONLY the following image URLs for the "thumbnailUrl" field based on the article theme:
- Crypto Casinos theme: "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&q=80&w=800"
- Sportsbook/Sports: "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&q=80&w=800"
- Payments/Stablecoins: "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?auto=format&fit=crop&q=80&w=800"
- Regulation/Legal: "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=800"
- Guides/Tutorials: "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&q=80&w=800"
- Sweepstakes/Social Casinos: "https://images.unsplash.com/photo-1541256996761-85df2efaa164?auto=format&fit=crop&q=80&w=800"
- Tech/AI: "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?auto=format&fit=crop&q=80&w=800"
- Corporate/Offices: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&q=80&w=800"
- Esports: "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=800"

Format the output strictly as a JSON array of 5 objects matching the following schema. Do NOT wrap it in any code blocks except returning valid JSON:
[
  {{
    "slug": "url-friendly-slug-excluding-dates-or-ids",
    "originalUrl": "https://cryptocasinomedia.com/press-releases/slug",
    "title": "Compelling B2B headline...",
    "publishedAt": "{date_iso}",
    "sourceName": "The publishing brand/company",
    "thumbnailUrl": "Choose from the allowed list above",
    "dateline": "CITY, COUNTRY, {dateline_str}",
    "lede": "1-2 sentence lead paragraph matching body[0] exactly...",
    "body": [
      "Lede paragraph (1-2 sentences)...",
      "Detail paragraph 2...",
      "Paragraph 3 with a quote starting with “ and ending with ” from a company executive...",
      "Detail paragraph 4...",
      "Closing paragraph 5..."
    ],
    "topics": ["Topic1", "Topic2", "Topic3"],
    "primaryCategory": "One of: crypto-casinos, sportsbook, regulation, payments, sweepstakes, guides",
    "company": "Company Name",
    "region": "Global, Europe, USA, Asia, or Latin America",
    "contact": "press@company.com",
    "excerpt": "Brief 1-2 sentence description summarizing the news."
  }}
]
"""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print("Calling Gemini API to generate daily articles...")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode('utf-8')
            res_json = json.loads(res_data)
            
            # Extract content from response structure
            content_text = res_json['candidates'][0]['content']['parts'][0]['text']
            new_articles = json.loads(content_text.strip())
            
            # Post-process to inject IDs and unique thumbnails incrementally
            existing_urls = {art["thumbnailUrl"] for art in articles_data if "thumbnailUrl" in art}
            for offset, art in enumerate(new_articles):
                art["id"] = f"pr-{len(articles_data) + offset + 1}"
                # Ensure publishedAt and originalUrl conform
                art["publishedAt"] = date_iso
                art["originalUrl"] = f"https://cryptocasinomedia.com/press-releases/{art['slug']}"
                if "lede" not in art:
                    art["lede"] = art["body"][0]
                
                # Assign a unique unused image
                category = art.get("primaryCategory", "guides")
                unique_img = select_unique_image(category, existing_urls)
                art["thumbnailUrl"] = unique_img
                existing_urls.add(unique_img)
                
            return new_articles
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error calling Gemini API: {e.code} - {e.read().decode('utf-8')}")
        raise e
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise e

def update_llms_txt(new_articles):
    # Adds the 5 new articles to the top of the Recent Press Releases section of llms.txt
    llms_path = os.path.join(os.path.dirname(scripts_dir), "index/llms.txt")
    if not os.path.exists(llms_path):
        print(f"Warning: llms.txt not found at {llms_path}")
        return
        
    with open(llms_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    recent_header_idx = -1
    for idx, line in enumerate(lines):
        if "## Recent Press Releases" in line:
            recent_header_idx = idx
            break
            
    if recent_header_idx == -1:
        print("Warning: '## Recent Press Releases' header not found in llms.txt")
        return
        
    # Format the new entries
    new_entries = []
    for art in new_articles:
        entry = f"- {art['title']}: https://cryptocasinomedia.com/press-releases/{art['slug']}\n"
        new_entries.append(entry)
        
    # Insert new entries right below the header line (recent_header_idx + 1)
    updated_lines = lines[:recent_header_idx + 1] + new_entries + lines[recent_header_idx + 1:]
    
    with open(llms_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)
    print("SUCCESS: llms.txt successfully updated with new article references!")

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    next_date = get_next_date()
    
    print(f"Target Date for Daily Run: {next_date.strftime('%Y-%m-%d')}")
    
    if not api_key:
        print("WARNING: GEMINI_API_KEY env variable not found. Running in MOCK content generator mode...")
        new_articles = generate_mock_articles(next_date)
    else:
        try:
            new_articles = generate_ai_articles(api_key, next_date)
        except Exception as e:
            print(f"Failed to generate AI articles. Falling back to MOCK mode... Error: {e}")
            new_articles = generate_mock_articles(next_date)
            
    # Print summary of generated articles
    print(f"Generated {len(new_articles)} new articles:")
    for art in new_articles:
        print(f"  [{art['id']}] {art['title']} (Category: {art['primaryCategory']}, Image: {art['thumbnailUrl']})")
        
    # Merge and update update_articles.py
    updated_articles_data = articles_data + new_articles
    write_to_update_articles(updated_articles_data)
    
    # Update llms.txt reference lists
    update_llms_txt(new_articles)
    
    # Run build pipeline
    print("Executing site compiler and pre-rendering build...")
    import subprocess
    res_build = subprocess.run([sys.executable, os.path.join(scripts_dir, "update_articles.py")], capture_output=True, text=True)
    if res_build.returncode != 0:
        print(f"Compilation error:\n{res_build.stderr}")
        sys.exit(res_build.returncode)
    print(res_build.stdout.strip())
    
    print("Daily news update generation completed successfully!")

if __name__ == "__main__":
    main()
