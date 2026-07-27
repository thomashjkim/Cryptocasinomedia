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

# Focus and select title
send_command("Runtime.evaluate", {
    "expression": """
        var h3 = document.querySelector('h3');
        h3.focus();
        var range = document.createRange();
        range.selectNodeContents(h3);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    """
})

# Type title
send_command("Input.insertText", {"text": "Test Article Title"})
time.sleep(1)

# Focus and select paragraph
send_command("Runtime.evaluate", {
    "expression": """
        var p = document.querySelector('p');
        p.focus();
        var range = document.createRange();
        range.selectNodeContents(p);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    """
})

# Type body text
send_command("Input.insertText", {"text": "This is the body text of the article with a backlink: https://cryptocasinomedia.com/press-release-seo."})

print("Typing complete!")
ws.close()
