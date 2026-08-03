import websocket
import json
import urllib.request

try:
    with urllib.request.urlopen("http://localhost:9222/json/version") as response:
        info = json.loads(response.read().decode())
except Exception as e:
    print("Error connecting to Chrome version endpoint:", e)
    exit(1)

browser_ws_url = info["webSocketDebuggerUrl"]
print("Browser WebSocket URL:", browser_ws_url)

ws = websocket.create_connection(browser_ws_url)

def send_command(method, params={}):
    cmd = {"id": 1, "method": method, "params": params}
    ws.send(json.dumps(cmd))
    res = json.loads(ws.recv())
    return res

# Open medium.com
print("Opening Medium tab via Target.createTarget...")
res = send_command("Target.createTarget", {"url": "https://medium.com"})
print("Result:", json.dumps(res, indent=2))
ws.close()
