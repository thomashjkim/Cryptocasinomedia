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

eval_js = """
(async function() {
    try {
        var res = await fetch('http://localhost:8080/index/images/igaming_seo_aeo.jpg');
        var blob = await res.blob();
        var file = new File([blob], 'igaming_seo_aeo.jpg', { type: 'image/jpeg' });
        
        var clipboardData = new DataTransfer();
        clipboardData.items.add(file);
        
        var pasteEvent = new ClipboardEvent('paste', {
            clipboardData: clipboardData,
            bubbles: true,
            cancelable: true
        });
        
        var p = document.querySelector('p');
        if (!p) return "Paragraph not found";
        p.focus();
        p.dispatchEvent(pasteEvent);
        return "Image paste dispatched successfully!";
    } catch(e) {
        return "Error: " + e.toString();
    }
})()
"""

res = send_command("Runtime.evaluate", {
    "expression": eval_js,
    "awaitPromise": True,
    "returnByValue": True
})
print(res["result"]["result"]["value"])
ws.close()
