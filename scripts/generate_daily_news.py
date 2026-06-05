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

# Expanded pools of high-quality verified Unsplash image URLs per category to guarantee uniqueness and relevance.
# These pools exclude any generic/corporate portraits and irrelevant images.
IMAGE_POOLS = {
    "crypto-casinos": [
        "https://images.unsplash.com/photo-1596838132731-3301c3fd4317?auto=format&fit=crop&q=80&w=800", # roulette wheel
        "https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&q=80&w=800", # casino dice chips
        "https://images.unsplash.com/photo-1606167668584-78701c57f13d?auto=format&fit=crop&q=80&w=800", # roulette wheel close up
        "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=800", # golden dice
        "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?auto=format&fit=crop&q=80&w=800", # neon casino lights
        "https://images.unsplash.com/photo-1609501676725-7186f017a4b7?auto=format&fit=crop&q=80&w=800", # card dealer
        "https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&q=80&w=800", # party dice
        "https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?auto=format&fit=crop&q=80&w=800", # gold tokens
        "https://images.unsplash.com/photo-1541256996761-85df2efaa164?auto=format&fit=crop&q=80&w=800", # colored dice
        "https://images.unsplash.com/photo-1542224566-6e85f2e6772f?auto=format&fit=crop&q=80&w=800", # dice board game
        "https://images.unsplash.com/photo-1594122230689-45899d9e6f69?auto=format&fit=crop&q=80&w=800", # roulette wheel
        "https://images.unsplash.com/photo-1601987177651-8edfe6c20009?auto=format&fit=crop&q=80&w=800", # blackjack table
        "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&q=80&w=800"  # neon slots
    ],
    "sportsbook": [
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&q=80&w=800", # soccer ball grass
        "https://images.unsplash.com/photo-1518063319789-7217e6706b04?auto=format&fit=crop&q=80&w=800", # stadium field
        "https://images.unsplash.com/photo-1544377193-33dcf4d68fb5?auto=format&fit=crop&q=80&w=800", # stadium lights
        "https://images.unsplash.com/photo-1529900748604-07564a03e7a6?auto=format&fit=crop&q=80&w=800", # soccer players
        "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&q=80&w=800", # basketball net
        "https://images.unsplash.com/photo-1505250469679-203ad9ced0cb?auto=format&fit=crop&q=80&w=800", # tennis wagers
        "https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?auto=format&fit=crop&q=80&w=800", # basketball
        "https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?auto=format&fit=crop&q=80&w=800", # swimming race
        "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&q=80&w=800", # stadium track
        "https://images.unsplash.com/photo-1595030044556-acfaa61edc0f?auto=format&fit=crop&q=80&w=800", # soccer cleats field
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&q=80&w=800"  # gym barbell
    ],
    "regulation": [
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&q=80&w=800", # gavel
        "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&q=80&w=800", # law books
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&q=80&w=800", # scales of justice
        "https://images.unsplash.com/photo-1505664194779-8beaceb93744?auto=format&fit=crop&q=80&w=800", # court gavel
        "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&q=80&w=800", # pillars court
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=800", # document audit
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&q=80&w=800", # business audit
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&q=80&w=800", # terms reading
        "https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?auto=format&fit=crop&q=80&w=800"  # regulatory meeting table
    ],
    "payments": [
        "https://images.unsplash.com/photo-1516245834210-c4c142787335?auto=format&fit=crop&q=80&w=800", # bitcoin motherboard
        "https://images.unsplash.com/photo-1621761191319-c6fb62004040?auto=format&fit=crop&q=80&w=800", # eth coin
        "https://images.unsplash.com/photo-1622630998477-20aa696ecb05?auto=format&fit=crop&q=80&w=800", # DeFi coins
        "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?auto=format&fit=crop&q=80&w=800", # gold coins stack
        "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?auto=format&fit=crop&q=80&w=800", # blockchain
        "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?auto=format&fit=crop&q=80&w=800", # bitcoin macro
        "https://images.unsplash.com/photo-1624555130581-1d9cca783bc0?auto=format&fit=crop&q=80&w=800", # gold coins stack 2
        "https://images.unsplash.com/photo-1634704784915-aacf363b021f?auto=format&fit=crop&q=80&w=800", # ether symbol
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=800", # data charts nodes
        "https://images.unsplash.com/photo-1642104704074-907c0698cbd9?auto=format&fit=crop&q=80&w=800", # NFT crypto display
        "https://images.unsplash.com/photo-1518156677180-95a2893f3e9f?auto=format&fit=crop&q=80&w=800", # finance chart
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&q=80&w=800", # safety vault
        "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&q=80&w=800", # mobile pay crypto scan
        "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&q=80&w=800"  # coin growth
    ],
    "sweepstakes": [
        "https://images.unsplash.com/photo-1560253023-3ec5d502959f?auto=format&fit=crop&q=80&w=800", # mobile play
        "https://images.unsplash.com/photo-1553481187-be93c21490a9?auto=format&fit=crop&q=80&w=800", # arcade cabinet
        "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&q=80&w=800", # esports gaming
        "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&q=80&w=800", # keyboard neon
        "https://images.unsplash.com/photo-1566241440091-ec10de8db2e1?auto=format&fit=crop&q=80&w=800", # mobile game
        "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&q=80&w=800", # gaming room
        "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&q=80&w=800", # monitor gamer
        "https://images.unsplash.com/photo-1551103782-8ab07afd45c1?auto=format&fit=crop&q=80&w=800", # joystick arcade
        "https://images.unsplash.com/photo-1542751110-97646eb5f202?auto=format&fit=crop&q=80&w=800", # gaming desk setup
        "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?auto=format&fit=crop&q=80&w=800", # cyberpunk neon gamer
        "https://images.unsplash.com/photo-1627856013091-fed6e4e30025?auto=format&fit=crop&q=80&w=800", # vr headset social play
        "https://images.unsplash.com/photo-1614294149010-950b698f72c0?auto=format&fit=crop&q=80&w=800", # slot reels
        "https://images.unsplash.com/photo-1538097304804-2a1b932466a9?auto=format&fit=crop&q=80&w=800"  # slot screen
    ],
    "guides": [
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&q=80&w=800", # search tutorial
        "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&q=80&w=800", # books study guides
        "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&q=80&w=800", # calendar planning
        "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&q=80&w=800", # code guide
        "https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&q=80&w=800", # html learning
        "https://images.unsplash.com/photo-1511193311914-0346f16efe90?auto=format&fit=crop&q=80&w=800", # billiards logic strategy
        "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&q=80&w=800", # course notes
        "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?auto=format&fit=crop&q=80&w=800", # support guide help
        "https://images.unsplash.com/photo-1518495973542-4542c06a5843?auto=format&fit=crop&q=80&w=800", # reading online guide
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&q=80&w=800", # writing tips notes
        "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?auto=format&fit=crop&q=80&w=800", # taking exam guide
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&q=80&w=800"  # learning presentation
    ]
}

FALLBACK_CHAINS = {
    "crypto-casinos": ["sweepstakes", "payments"],
    "sportsbook": ["crypto-casinos", "sweepstakes"],
    "regulation": ["payments", "crypto-casinos"],
    "payments": ["crypto-casinos", "sweepstakes"],
    "sweepstakes": ["crypto-casinos", "payments"],
    "guides": ["crypto-casinos", "sweepstakes", "payments"]
}

def select_unique_image(category, existing_urls):
    # 1. Try primary category pool
    pool = IMAGE_POOLS.get(category, IMAGE_POOLS.get("guides"))
    unused = [url for url in pool if url not in existing_urls]
    if unused:
        return unused[0]
        
    # 2. Try fallback chain categories
    chain = FALLBACK_CHAINS.get(category, [])
    for fallback_cat in chain:
        fallback_pool = IMAGE_POOLS.get(fallback_cat, [])
        unused_fallback = [url for url in fallback_pool if url not in existing_urls]
        if unused_fallback:
            return unused_fallback[0]
            
    # 3. Global sweep: try ANY category's pool to guarantee uniqueness
    for other_cat, other_pool in IMAGE_POOLS.items():
        unused_global = [url for url in other_pool if url not in existing_urls]
        if unused_global:
            return unused_global[0]
            
    # 4. Ultimate fallback: if completely ran out of all unique images, return pool[0]
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
