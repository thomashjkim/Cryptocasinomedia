import { spawn } from 'child_process';

async function testLiveViewports() {
  console.log('=== TESTING LIVE PRODUCTION VIEWPORT RESPONSIVENESS ON HTTPS://MOON-OH.COM ===\n');

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
      { name: 'Tablet 768px', width: 768, height: 1024 },
      { name: 'Desktop 1440px', width: 1440, height: 900 }
    ];

    const testPages = [
      'https://moon-oh.com/explore',
      'https://moon-oh.com/local-product/happier-grocery/lasso-watermelon-lime-gelatin-cups'
    ];

    for (const pageUrl of testPages) {
      console.log(`Checking page: ${pageUrl}`);
      for (const vp of viewports) {
        await call('Emulation.setDeviceMetricsOverride', {
          width: vp.width,
          height: vp.height,
          deviceScaleFactor: 2,
          mobile: vp.width < 1000
        });

        await call('Page.navigate', { url: pageUrl });
        await new Promise(r => setTimeout(r, 2500));

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
        const pass = !res.hasOverflow;
        console.log(`  ${vp.name} (${vp.width}x${vp.height}) => docWidth=${res.docWidth}, innerWidth=${res.innerWidth}, Overflow=${res.hasOverflow ? 'YES (FAIL)' : 'NO (PASS)'} [${pass ? '✅' : '❌'}]`);
      }
      console.log('--------------------------------------------------');
    }

    ws.close();
    chrome.kill();
    console.log('\n✅ All live viewport responsiveness tests completed!');
  };
}

testLiveViewports().catch(console.error);
