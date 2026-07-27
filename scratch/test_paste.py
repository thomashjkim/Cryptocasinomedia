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
(function() {
    var p = document.querySelector('p');
    if (!p) return "Paragraph not found";
    p.focus();
    
    var range = document.createRange();
    range.selectNodeContents(p);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    
    var clipboardData = new DataTransfer();
    clipboardData.setData('text/html', 'This is a test of <a href="https://cryptocasinomedia.com/press-release-seo">iGaming press release SEO standards</a> within the paragraph.');
    clipboardData.setData('text/plain', 'This is a test of iGaming press release SEO standards within the paragraph.');
    
    var pasteEvent = new ClipboardEvent('paste', {
        clipboardData: clipboardData,
        bubbles: true,
        cancelable: true
    });
    
    p.dispatchEvent(pasteEvent);
    return "Paste event dispatched";
})()
"""

res = send_command("Runtime.evaluate", {"expression": eval_js, "returnByValue": True})
print(res["result"]["result"]["value"])
ws.close()
