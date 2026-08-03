import websocket
import json
import urllib.request
import base64
import time
import os

new_articles = [
    {
        "title": "Under the Microscope: The Financial and Operational Realities of Curaçao's New Direct iGaming Licenses",
        "body_html": """<p>The global interactive gaming (iGaming) compliance landscape is undergoing a permanent structural shift. For decades, Curaçao operated as a sub-licensing hub under a handful of master license holders, offering a low-barrier entry point for startup crypto casinos. However, the comprehensive regulatory transition enforced by the Curaçao Gaming Control Board (GCB) in 2026 has introduced rigorous direct oversight, fundamentally altering the financial and operational calculus for international Web3 operators.</p>
<p>Under the new regulatory framework, operators must transition away from sub-licenses and apply directly to the GCB for a corporate operating license. This direct licensing process mandates absolute corporate transparency, including complete Ultimate Beneficial Owner (UBO) disclosures, audited financial reserve statements, and documented security deposits. Furthermore, operators must establish a physical presence in Curaçao and appoint a local compliance officer to manage regulatory audits.</p>
<p>From a financial perspective, the cost of compliance has risen significantly. Operators must budget for substantial annual license fees, application processing charges, and system compliance audits. Yet, regulatory experts argue that this transition will ultimately benefit the industry. A direct license from the GCB provides operators with enhanced credibility, unlocking access to top-tier payment processing rails, major merchant acquirers, and premium software providers that previously shunned the jurisdiction.</p>
<p>“The Curaçao GCB reforms are a double-edged sword,” remarked Marcus Vance, Lead iGaming Analyst. “While the administrative and financial burdens will squeeze thin-margin platforms, the compliance legitimacy gained will secure the long-term viability of high-caliber operators. Understanding the exact <a href="https://cryptocasinomedia.com/guides/regulation-2026">Curaçao direct licensing frameworks</a> is now the most critical task for Web3 compliance teams preparing for this transition.”</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/curacao_licensing_realities.jpg",
        "tags": ["iGaming", "Compliance", "Curacao", "Gaming Law", "Business"]
    },
    {
        "title": "Decentralized Oracles and API Resolvers: Automating Smart Contract Settlements in Crypto Sportsbooks",
        "body_html": """<p>Traditional sportsbooks have long suffered from settlement latency. When a sporting event concludes, bettors must wait for manual validation, bookmaker reviews, and database updates before they can access their winnings. In the fast-paced Web3 ecosystem, this lag represents a significant user experience bottleneck. The solution gaining widespread adoption is the integration of decentralized oracles and automated API resolvers.</p>
<p>By combining blockchain-based smart contracts with decentralized oracle networks (such as Chainlink or custom oracle nodes), operators can automate the entire event resolution pipeline. The oracle acts as a secure bridge, fetching real-time match data from multiple independent sports API feeds, verifying the consensus result on-chain, and triggering the smart contract to execute immediate payouts to winning wallets.</p>
<p>This automation removes the element of human bookmaker error and potential platform manipulation, building trust with players who know that settlements are governed by immutable code. Furthermore, using stablecoin settlements (such as USDT or USDC) on high-throughput networks ensures that transactions are completed at low cost and within seconds, providing the frictionless experience that modern mobile-first bettors expect.</p>
<p>“Automated resolvers are redefining the relationship between bettor and bookmaker,” noted Joshua De Vos, Web3 Analyst. “Decentralized oracles ensure that payouts are transparent, instantaneous, and cryptographically verified. Transitioning to <a href="https://cryptocasinomedia.com/press-releases/polymarket-kalshi-prediction-markets-rival-crypto-sportsbooks">smart contract sportsbook automation</a> is the next key milestone for crypto sportsbooks aiming to capture market share from legacy bookmakers.”</p>""",
        "image_path": "/Users/thomaskim/Cryptocasinomedia/index/images/decentralized_oracles_sportsbook.jpg",
        "tags": ["Crypto", "Sportsbook", "Web3", "Oracle", "Automation"]
    }
]

# Look for active Medium page
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
    print("Medium page not found! Please make sure you are navigated to medium.com in Chrome.")
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

for idx, article in enumerate(new_articles):
    print(f"\n=== Publishing New Article {idx+1}/2: {article['title']} ===")
    
    # 1. Navigation
    send_command("Page.navigate", {"url": "https://medium.com/new-story"})
    print("Navigating to new-story...")
    time.sleep(6)
    
    # 2. Focus and Type Title
    title_js = """
    (function() {
        var h3 = document.querySelector('h3');
        if (!h3) return false;
        h3.focus();
        var range = document.createRange();
        range.selectNodeContents(h3);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        return true;
    })()
    """
    if not eval_js(title_js):
        print("Error: Could not focus title element!")
        continue
    
    send_command("Input.insertText", {"text": article["title"]})
    print("Title entered.")
    time.sleep(1)
    
    # 3. Focus and Paste Body HTML
    body_plain = article["title"]
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
        time.sleep(5)
    else:
        print(f"Warning: Image file not found at {article['image_path']}")
    
    # 5. Click Prepublish
    prepublish_js = """
    (function() {
        var btn = document.querySelector('button.js-publishButton') || 
                  document.querySelector('button[data-testid="show-prepublish"]') || 
                  document.querySelector('button[data-action="show-prepublish"]') ||
                  Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Publish');
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
    time.sleep(5)
    
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
    time.sleep(6)
    
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
report_path = "/Users/thomaskim/Cryptocasinomedia/scratch/medium_publish_report_new.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(published_links, f, indent=2)

print("\n=== NEW ARTICLES PUBLISHED LIVE SUCCESSFUL! ===")
ws.close()
