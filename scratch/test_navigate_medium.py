import websocket
import json
import urllib.request
import time

# Try to open a new tab first
try:
    with urllib.request.urlopen("http://localhost:9222/json/new") as response:
        new_tab = json.loads(response.read().decode())
        print("Successfully opened new tab:", new_tab)
except Exception as e:
    print("Could not open new tab directly, reading existing list...", e)

try:
    with urllib.request.urlopen("http://localhost:9222/json") as response:
        pages = json.loads(response.read().decode())
except Exception as e:
    print("Error connecting to Chrome:", e)
    exit(1)

print("Pages list:")
print(json.dumps(pages, indent=2))

target_page = None
for page in pages:
    if page.get("type") == "page":
        target_page = page
        break

if not target_page:
    print("No active page found!")
    exit(1)

ws_url = target_page["webSocketDebuggerUrl"]
ws = websocket.create_connection(ws_url)

def send_command(method, params={}):
    cmd = {"id": 1, "method": method, "params": params}
    ws.send(json.dumps(cmd))
    res = json.loads(ws.recv())
    return res

print("Navigating to Medium...")
send_command("Page.navigate", {"url": "https://medium.com"})
time.sleep(6)

eval_js = """
(function() {
    return {
        url: window.location.href,
        title: document.title,
        bodyLength: document.body ? document.body.innerText.length : 0,
        hasUserMenu: !!document.querySelector('button[aria-label="user-menu"]') || !!document.querySelector('img[alt="cryptocasinomedia"]')
    };
})()
"""

res = send_command("Runtime.evaluate", {"expression": eval_js, "returnByValue": True})
print("State:", json.dumps(res["result"]["result"]["value"], indent=2))
ws.close()
