import websocket
import json
import urllib.request

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

eval_js = """
(function() {
    var elements = Array.from(document.querySelectorAll('button, a, [role="button"]')).map(el => ({
        tag: el.tagName,
        text: el.innerText || el.textContent,
        id: el.id,
        class: el.className,
        testid: el.getAttribute('data-testid') || el.getAttribute('data-action')
    }));
    // Filter elements containing "Publish" or similar
    return elements.filter(el => el.text.toLowerCase().includes('publish') || el.text.toLowerCase().includes('publish now') || el.testid === 'publish-button');
})()
"""

res = send_command("Runtime.evaluate", {"expression": eval_js, "returnByValue": True})
print(json.dumps(res["result"]["result"]["value"], indent=2))
ws.close()
