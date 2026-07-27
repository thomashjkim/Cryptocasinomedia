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
    print("Medium page not found in Chrome tabs!")
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
    return {
        url: window.location.href,
        title: document.title,
        hasUserMenu: !!document.querySelector('[aria-label="User menu"], [data-testid="user-avatar"], img[alt="Go to profile"]'),
        bodyTextLength: document.body.innerText.length
    };
})()
"""

res = send_command("Runtime.evaluate", {"expression": eval_js, "returnByValue": True})
print(json.dumps(res, indent=2))
ws.close()
