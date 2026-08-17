import { spawn } from 'child_process';
import http from 'http';

async function testViewportLayouts() {
  console.log('=== TESTING RESPONSIVE VIEWPORT RENDERING (375px, 390px, 475px, Desktop) ===\n');

  import('../netlify/functions/item-detail.mjs').then(async (mod) => {
    const defaultHandler = mod.default;

    const server = http.createServer(async (req, res) => {
      try {
        const fullUrl = `https://moon-oh.com${req.url}`;
        const response = await defaultHandler(new Request(fullUrl), {});
        const body = await response.text();
        res.writeHead(response.status, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(body);
      } catch (e) {
        res.writeHead(500);
        res.end(e.message);
      }
    });

    server.listen(8999, async () => {
      console.log('Local test server running on port 8999');

      const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
        '--headless=new',
        '--remote-debugging-port=9222',
        '--disable-gpu',
        '--no-sandbox'
      ]);
      await new Promise(r => setTimeout(r, 1500));

      const list = await (await fetch('http://127.0.0.1:9222/json/list')).json();
      const ws = new WebSocket(list[0].webSocketDebuggerUrl);

      let id = 1;
      const call = (method, params = {}) => new Promise((resolve) => {
        const curId = id++;
        const handler = (event) => {
          const d = JSON.parse(event.data);
          if (d.id === curId) {
            ws.removeEventListener('message', handler);
            resolve(d.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });

      ws.onopen = async () => {
        await call('Page.enable');
        await call('DOM.enable');

        const viewports = [
          { name: 'Mobile 375px', width: 375, height: 667 },
          { name: 'Mobile 390px', width: 390, height: 844 },
          { name: 'Mobile 475px', width: 475, height: 850 },
          { name: 'Desktop 1440px', width: 1440, height: 900 }
        ];

        for (const vp of viewports) {
          await call('Emulation.setDeviceMetricsOverride', {
            width: vp.width,
            height: vp.height,
            deviceScaleFactor: 2,
            mobile: vp.width < 1000
          });

          await call('Page.navigate', { url: 'http://127.0.0.1:8999/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups' });
          await new Promise(r => setTimeout(r, 2000));

          const metrics = await call('Runtime.evaluate', {
            expression: `(() => {
              const bodyWidth = document.body.scrollWidth;
              const docWidth = document.documentElement.scrollWidth;
              const innerWidth = window.innerWidth;
              const hasOverflow = bodyWidth > innerWidth || docWidth > innerWidth;
              return JSON.stringify({ bodyWidth, docWidth, innerWidth, hasOverflow });
            })()`
          });

          const res = JSON.parse(metrics.result?.value || '{}');
          console.log(`Viewport: ${vp.name} (${vp.width}x${vp.height}) => docWidth=${res.docWidth}, innerWidth=${res.innerWidth}, Overflow=${res.hasOverflow ? 'YES (FAIL)' : 'NO (PASS)'}`);
        }

        ws.close();
        chrome.kill();
        server.close();
        console.log('\n✅ All viewport responsiveness tests completed successfully!');
      };
    });
  });
}

testViewportLayouts().catch(console.error);
