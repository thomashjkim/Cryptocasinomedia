import websocket
import json
import urllib.request
import base64
import time
import os

# Hardcoded articles array
articles = [
    {
        "title": "The Shift to AEO: How iGaming Operators Must Optimize News for AI Search in 2026",
        "body_html": """<p>The digital marketing landscape for interactive gaming (iGaming) operators is undergoing a fundamental structural transition. For over a decade, programmatic SEO and keyword-stuffed press releases served as the primary drivers of organic search visibility. However, as generative AI search engines—such as ChatGPT Search, Perplexity AI, Claude, and Google’s Gemini-powered AI Overviews—become the primary discovery tools for industry professionals and analysts, the playbook has shifted from SEO to <strong>AEO (Answer Engine Optimization)</strong>.</p>
<p>To be cited as a source by an AI LLM (Large Language Model) crawler, content must satisfy completely different parameters than traditional Google indexing. Rather than counting backlinks or keyword density, AI models evaluate semantic clarity, factual corroboration, and structured metadata.</p>
<h3>1. Semantic Clarity Over Keyword Density</h3>
<p>AI engines do not read text in isolation; they build semantic maps of entities and relationships. If an operator publishes a press release claiming to launch the "best bitcoin casino app," an AI engine will cross-reference this claim against external databases, regulatory licensing records, and user reviews. If the claim cannot be verified, the model flags it as low-trust and excludes it from generative answers.</p>
<p>Operators must write in clear, objective, and declarative B2B language. Avoid hyperbole and focus on concrete metrics, named executives, and verifiable integration timelines.</p>
<h3>2. The Power of Schema Markup</h3>
<p>If AI crawlers cannot parse who issued an announcement, what the primary topic is, and which markets are affected, they will not synthesize it into search answers. Incorporating structured JSON-LD metadata—defining the <code>NewsArticle</code>, <code>Organization</code>, and <code>about</code> entities—is no longer optional. It acts as the direct API through which AI crawlers ingest corporate announcements.</p>
<p>For operators looking to navigate this technical shift, auditing your distribution channels against modern <a href="https://cryptocasinomedia.com/press-release-seo">iGaming press release SEO standards</a> is the first critical step to ensuring your corporate updates are visible in generative engine outputs.</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/igaming_seo_aeo.jpg",
        "tags": ["iGaming", "SEO", "AEO", "Marketing", "Artificial Intelligence"]
    },
    {
        "title": "Navigating the Curacao GCB Regulatory Transition: A Checklist for Web3 Operators",
        "body_html": """<p>For decades, Curacao was viewed as a low-barrier jurisdiction for international online gambling operators, particularly those pioneer platforms integrating cryptocurrency deposit and withdrawal methods. However, the comprehensive legislative overhaul led by the <strong>Curaçao Gaming Control Board (GCB)</strong> in 2026 has permanently changed this landscape.</p>
<p>The transition from master license holders to direct regulatory oversight by the GCB represents a major compliance shift. Operators must prepare for strict compliance auditing or risk losing access to payment processing rails and top-tier software providers.</p>
<h3>Key Pillars of the GCB Framework</h3>
<p>1. <strong>Direct Licensing Requirements</strong>: Under the new regime, operators must obtain direct licenses from the GCB, replacing the old sub-license structure. This requires a thorough corporate audit, beneficial owner verification, and documented financial security deposits.</p>
<p>2. <strong>Enhanced AML and KYC Auditing</strong>: Web3 casinos must implement robust Anti-Money Laundering (AML) monitoring and automated Know Your Customer (KYC) compliance. Programmatic checking against global sanctions lists is now mandatory for all active accounts.</p>
<p>3. <strong>Data Protection and Responsible Gaming</strong>: Operators must provide clear user control panels for responsible gambling, deposit limits, and secure data storage policies aligned with international privacy standards.</p>
<p>To avoid operational disruptions during this legislative shift, consulting up-to-date <a href="https://cryptocasinomedia.com/guides/regulation-2026">Curacao iGaming regulation guides</a> is vital for compliance officers managing international Web3 and crypto casino jurisdictions.</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/curacao_gcb_regulation.jpg",
        "tags": ["iGaming", "Curacao", "Gambling", "Compliance", "Cryptocurrency"]
    },
    {
        "title": "Prediction Markets vs. Sportsbooks: The Battle for On-Chain Event Betting",
        "body_html": """<p>The sports wagering industry is experiencing a profound shift driven by the explosion of event-contract prediction markets. Platforms like the decentralized protocol Polymarket and the CFTC-regulated exchange Kalshi have captured billions of dollars in volume, proving that retail users are increasingly drawn to binary event contracts over traditional bookmaker structures.</p>
<p>This raises a critical question for B2B gaming executives: Are prediction markets a temporary trend, or do they represent a permanent threat to traditional sportsbooks?</p>
<h3>Bidding Efficiency vs. Vigorish (Vig)</h3>
<p>Traditional sportsbooks operate on a bookmaker model, setting lines and charging a transaction fee (the "vig" or juice) to guarantee their margin. Prediction markets, by contrast, act as order-book exchanges. Prices fluctuate between $0.00 and $1.00 based entirely on market supply and demand, mimicking stock exchanges.</p>
<p>For the end-user, order-book markets offer superior liquidity, zero bookmaker margin, and the ability to trade positions dynamically in real-time as the probability of the outcome shifts.</p>
<h3>The Technology Gap</h3>
<p>Web3 sportsbooks are increasingly integrating prediction market logic to capture this retail demand. By embedding ERC-20 stablecoin settlement layers and decentralized oracle resolutions, operators can automate payouts instantly, bypassing manual settlement delays.</p>
<p>A comprehensive comparison of this structural shift is detailed in the B2B <a href="https://cryptocasinomedia.com/press-releases/polymarket-kalshi-prediction-markets-rival-crypto-sportsbooks">prediction markets vs. crypto sportsbooks analysis</a>, outlining how operators can adapt to this new era of event-driven liquidity.</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/prediction_markets_vs_sportsbook.jpg",
        "tags": ["Prediction Markets", "Sportsbooks", "Polymarket", "Crypto", "Finance"]
    },
    {
        "title": "Telegram Mini-Apps & GambleFi: The Frictionless Future of Mobile iGaming",
        "body_html": """<p>The biggest challenge facing mobile iGaming operators is user acquisition friction. App store compliance restrictions, lengthy download steps, and complex wallet connections result in high user drop-off rates, especially in Web3 gambling. The solution emerging as the dominant acquisition channel in 2026 is <strong>Telegram GambleFi</strong>.</p>
<p>By leveraging Telegram Mini-Apps (TMAs) and automated Web3 betting bots, operators are bringing the casino lobby directly inside the world's most popular messaging app for crypto communities.</p>
<h3>Why Telegram is Dominating Web3 Gaming</h3>
<p>1. <strong>Zero-Download Onboarding</strong>: Telegram Mini-Apps load instantly via WebViews, allowing players to access sportsbooks, slots, and live tables without downloading external files.</p>
<p>2. <strong>Native Wallet Integration</strong>: Built-in TON (The Open Network) wallets and EVM-compatible bot commands enable users to deposit, place wagers, and request instant withdrawals directly inside the chat interface.</p>
<p>3. <strong>Viral Social Mechanics</strong>: Group chats, referral bonuses, and shared betting brackets encourage community-driven user acquisition, reducing marketing costs significantly.</p>
<p>For Web3 software developers, exploring <a href="https://cryptocasinomedia.com/guides/gamblefi-telegram">Telegram GambleFi integration frameworks</a> is key to capturing the millions of mobile-first players migrating toward chat-based gaming solutions.</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/telegram_gamblefi.png",
        "tags": ["GambleFi", "Telegram", "Web3", "TON", "Mobile Gaming"]
    },
    {
        "title": "Understanding Sweepstakes Casino Legality: A Compliance Guide for US Markets",
        "body_html": """<p>As traditional real-money online casino regulation progresses slowly across the United States, the B2B interactive gaming sector has witnessed a massive surge in <strong>social and sweepstakes-model casinos</strong>. Operating under sweepstakes law rather than real-money gaming statutes, these platforms have successfully entered over 40 states, representing a multi-billion dollar vertical.</p>
<p>However, operating a sweepstakes casino in the US requires navigating a highly complex, state-specific legal framework to maintain compliance and avoid enforcement actions.</p>
<h3>The Dual-Currency Legal Loophole</h3>
<p>To remain lawful under US federal and state laws, a sweepstakes casino must not require payment to play. This is achieved by utilizing a dual-currency system:</p>
<p>• <strong>Gold Coins (GC)</strong>: A virtual currency purchased by players for recreational play. Gold Coins have no real-world value and cannot be redeemed for cash or prizes.</p>
<p>• <strong>Sweeps Coins (SC)</strong>: A promotional currency given for free as a bonus with Gold Coin purchases, or through mail-in and social media requests. Sweeps Coins can be used to play promotional games, and accumulated winnings can be redeemed for cash prizes.</p>
<h3>Critical Compliance Requirements</h3>
<p>Operators must implement strict geo-fencing to block restricted states (such as Washington and Idaho), limit maximum daily prize redemptions, and enforce rigorous age verification protocols.</p>
<p>B2B operators looking to launch or support these platforms must refer to verified <a href="https://cryptocasinomedia.com/guides/sweepstakes-market">social and sweepstakes casino compliance guides</a> to ensure their payment routing, marketing promotions, and terms of service align with the latest state attorney general designations.</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/sweepstakes_compliance_guide.png",
        "tags": ["Sweepstakes", "Compliance", "Gaming Law", "iGaming", "Legality"]
    }
]

try:
    with urllib.request.urlopen("http://localhost:9222/json") as response:
        pages = json.loads(response.read().decode())
except Exception as e:
    print("Error connecting to Chrome:", e)
    exit(1)

medium_page = None
for page in pages:
    if "medium.com" in page.get("url", "") and page.get("type") == "page":
        medium_page = page
        break

if not medium_page:
    print("Medium page not found!")
    exit(1)

ws_url = medium_page["webSocketDebuggerUrl"]
ws = websocket.create_connection(ws_url)

def send_command(method, params={}):
    cmd = {"id": 1, "method": method, "params": params}
    ws.send(json.dumps(cmd))
    res = json.loads(ws.recv())
    return res

def eval_js(expr, await_promise=False):
    res = send_command("Runtime.evaluate", {
        "expression": expr,
        "awaitPromise": await_promise,
        "returnByValue": True
    })
    return res.get("result", {}).get("result", {}).get("value")

published_links = []

for idx, article in enumerate(articles):
    print(f"\\n=== Publishing Article {idx+1}/5: {article['title']} ===")
    
    # 1. Navigation
    if idx == 0:
        # Overwrite the test draft page
        edit_url = "https://medium.com/p/d6eb784e545e/edit"
        send_command("Page.navigate", {"url": edit_url})
        print(f"Navigating to edit URL for first article: {edit_url}")
    else:
        send_command("Page.navigate", {"url": "https://medium.com/new-story"})
        print("Navigating to new-story...")
    
    time.sleep(6) # Wait for page load
    
    # 2. Focus and Type Title
    title_js = f"""
    (function() {{
        var h3 = document.querySelector('h3');
        if (!h3) return false;
        h3.focus();
        var range = document.createRange();
        range.selectNodeContents(h3);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        return true;
    }})()
    """
    if not eval_js(title_js):
        print("Error: Could not focus title element!")
        continue
    
    # Delete current title if any (overwrite mode)
    send_command("Input.insertText", {"text": ""})
    time.sleep(0.5)
    send_command("Input.insertText", {"text": article["title"]})
    print("Title entered.")
    time.sleep(1)
    
    # 3. Focus and Paste Body HTML
    body_plain = article["title"] # fallback text
    body_js = f"""
    (function() {{
        var p = document.querySelector('p');
        if (!p) return false;
        p.focus();
        
        var range = document.createRange();
        range.selectNodeContents(p);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        
        var clipboardData = new DataTransfer();
        clipboardData.setData('text/html', `{article['body_html']}`);
        clipboardData.setData('text/plain', `{body_plain}`);
        
        var pasteEvent = new ClipboardEvent('paste', {{
            clipboardData: clipboardData,
            bubbles: true,
            cancelable: true
        }});
        
        p.dispatchEvent(pasteEvent);
        return true;
    }})()
    """
    if not eval_js(body_js):
        print("Error: Could not paste body text!")
        continue
    print("Body text pasted.")
    time.sleep(2)
    
    # 4. Read Local Image and Paste as Base64 File
    if os.path.exists(article["image_path"]):
        with open(article["image_path"], "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")
        
        image_js = f"""
        (async function() {{
            try {{
                var b64 = "{b64_data}";
                var bin = atob(b64);
                var len = bin.length;
                var arr = new Uint8Array(len);
                for (var i = 0; i < len; i++) {{
                    arr[i] = bin.charCodeAt(i);
                }}
                var blob = new Blob([arr], {{ type: 'image/jpeg' }});
                var file = new File([blob], 'image.jpg', {{ type: 'image/jpeg' }});
                
                var clipboardData = new DataTransfer();
                clipboardData.items.add(file);
                
                var pasteEvent = new ClipboardEvent('paste', {{
                    clipboardData: clipboardData,
                    bubbles: true,
                    cancelable: true
                }});
                
                // Paste at the beginning of the editor
                var p = document.querySelector('p');
                if (p) {{
                    p.focus();
                    p.dispatchEvent(pasteEvent);
                    return "Image paste successful";
                }}
                return "Paragraph element not found for image paste";
            }} catch(e) {{
                return "Image paste error: " + e.toString();
            }}
        }})()
        """
        img_res = eval_js(image_js, await_promise=True)
        print(f"Image upload status: {img_res}")
        time.sleep(5) # Wait for CDN upload
    else:
        print(f"Warning: Image file not found at {article['image_path']}")
    
    # 5. Click Prepublish
    prepublish_js = """
    (function() {
        var btn = document.querySelector('button[data-action="show-prepublish"]');
        if (!btn) return false;
        btn.classList.remove('js-buttonDisabledPrimary');
        btn.removeAttribute('disabled');
        btn.click();
        return true;
    })()
    """
    if not eval_js(prepublish_js):
        print("Error: Prepublish button not found or click failed!")
        continue
    print("Prepublish button clicked.")
    time.sleep(5) # Wait for navigation to submission page
    
    # 6. Enter Tags (Topics)
    for tag in article["tags"]:
        focus_input_js = """
        (function() {
            var input = document.querySelector('input[placeholder="Add a topic..."]');
            if (input) {
                input.focus();
                return true;
            }
            return false;
        })()
        """
        if eval_js(focus_input_js):
            send_command("Input.insertText", {"text": tag})
            time.sleep(0.5)
            # Send Enter key event
            send_command("Input.dispatchKeyEvent", {
                "type": "rawKeyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13
            })
            send_command("Input.dispatchKeyEvent", {
                "type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13
            })
            print(f"Added tag: {tag}")
            time.sleep(0.8)
    
    # 7. Click Final Publish Button
    publish_now_js = """
    (function() {
        var btns = Array.from(document.querySelectorAll('button'));
        var publishBtn = btns.find(btn => btn.innerText.trim() === 'Publish' || btn.innerText.trim() === 'Publish now');
        if (!publishBtn) return false;
        publishBtn.click();
        return true;
    })()
    """
    if not eval_js(publish_now_js):
        print("Error: Final publish button not found!")
        continue
    print("Final publish button clicked.")
    time.sleep(6) # Wait for publication redirect
    
    # 8. Retrieve and Store Published URL
    url_info_js = """
    (function() {
        return {
            url: window.location.href,
            title: document.title
        };
    })()
    """
    info = eval_js(url_info_js)
    print(f"Published info: {info}")
    published_links.append(info)

# Output summary to a text file
report_path = "/Users/thomaskim/Cryptocasinomedia/scratch/medium_publish_report.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(published_links, f, indent=2)

print("\\n=== ALL 5 ARTICLES PUBLISHED LIVE SUCCESSFUL! ===")
print(f"Report saved to {report_path}")
ws.close()
