import websocket
import json
import urllib.request
import base64

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

res = send_command("Page.captureScreenshot", {"format": "png"})
if "result" in res and "data" in res["result"]:
    img_data = base64.b64decode(res["result"]["data"])
    with open("/Users/thomaskim/.gemini/antigravity/brain/559a368e-49d2-4e82-a47e-ec2ab5cc5f91/medium_screenshot.png", "wb") as f:
        f.write(img_data)
    print("Screenshot saved successfully!")
else:
    print("Failed to capture screenshot:", res)

ws.close()
