import { spawn } from 'child_process';
import fs from 'fs';

async function scrapeHappierCatalog() {
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
    await call('Page.navigate', { url: 'https://shop.happiergrocery.com/shop' });
    console.log('Navigated to /shop, waiting 8 seconds...');
    await new Promise(r => setTimeout(r, 8000));

    // Scroll down multiple times to load items
    for (let i = 0; i < 8; i++) {
      await call('Runtime.evaluate', { expression: 'window.scrollBy(0, 1500);' });
      await new Promise(r => setTimeout(r, 1500));
    }

    const evalRes = await call('Runtime.evaluate', {
      expression: `(() => {
        const items = [];
        const links = Array.from(document.querySelectorAll('a[href*="/product/"]'));
        for (const a of links) {
          const href = a.href;
          const img = a.querySelector('img');
          const title = a.innerText.trim();
          if (href && (img || title)) {
            items.push({
              href,
              imgSrc: img ? img.src : '',
              imgAlt: img ? img.alt : '',
              text: title
            });
          }
        }
        return JSON.stringify(items);
      })()`
    });

    const items = JSON.parse(evalRes.result.value || '[]');
    console.log('Found ' + items.length + ' product links on /shop!');
    fs.writeFileSync('scripts/scraped_happier_raw.json', JSON.stringify(items, null, 2));

    ws.close();
    chrome.kill();
  };
}

scrapeHappierCatalog().catch(console.error);
