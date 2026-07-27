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

# Focus topic input and add tags, then click Publish button
eval_js = """
(async function() {
    var input = document.querySelector('input[placeholder="Add a topic..."]');
    if (input) {
        input.focus();
    }
    return "Topic input focused";
})()
"""

send_command("Runtime.evaluate", {"expression": eval_js})
time.sleep(1)

# Type tag "iGaming" and press Enter
send_command("Input.insertText", {"text": "iGaming"})
time.sleep(0.5)
# Press Enter key (CDP key events)
# KeyDown
send_command("Input.dispatchKeyEvent", {
    "type": "rawKeyDown",
    "key": "Enter",
    "code": "Enter",
    "windowsVirtualKeyCode": 13
})
# KeyUp
send_command("Input.dispatchKeyEvent", {
    "type": "keyUp",
    "key": "Enter",
    "code": "Enter",
    "windowsVirtualKeyCode": 13
})
time.sleep(1)

# Now click the final Publish button
eval_js_click = """
(function() {
    var btns = Array.from(document.querySelectorAll('button'));
    var publishBtn = btns.find(btn => btn.innerText.trim() === 'Publish');
    if (!publishBtn) return "Publish button not found";
    publishBtn.click();
    return "Publish button clicked";
})()
"""

res = send_command("Runtime.evaluate", {"expression": eval_js_click, "returnByValue": True})
print(res["result"]["result"]["value"])

time.sleep(5)

# Check final URL
eval_js_final = """
(function() {
    return {
        url: window.location.href,
        title: document.title
    };
})()
"""
res_final = send_command("Runtime.evaluate", {"expression": eval_js_final, "returnByValue": True})
print("Final state:", json.dumps(res_final["result"]["result"]["value"], indent=2))

ws.close()
