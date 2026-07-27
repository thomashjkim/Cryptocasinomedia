import websocket
import json
import urllib.request
import time

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

# Print raw result for debugging
eval_js = """
(async function() {
    var btn = document.querySelector('button[data-action="show-prepublish"]');
    if (!btn) return "Publish button not found";
    
    btn.classList.remove('js-buttonDisabledPrimary');
    btn.removeAttribute('disabled');
    btn.click();
    
    await new Promise(r => setTimeout(r, 3000));
    
    var elements = Array.from(document.querySelectorAll('button, a, [role="button"], input')).map(el => ({
        tag: el.tagName,
        text: el.innerText || el.textContent || el.value,
        placeholder: el.getAttribute('placeholder'),
        class: el.className,
        action: el.getAttribute('data-action')
    }));
    
    return {
        clicked: true,
        elements: elements.filter(el => el.text.toLowerCase().includes('publish') || el.action === 'publish-post' || el.placeholder)
    };
})()
"""

res = send_command("Runtime.evaluate", {
    "expression": eval_js,
    "awaitPromise": True,
    "returnByValue": True
})
print("Raw response:", json.dumps(res, indent=2))
ws.close()
