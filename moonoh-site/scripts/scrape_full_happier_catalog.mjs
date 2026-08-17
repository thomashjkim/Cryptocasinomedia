import { spawn } from 'child_process';
import fs from 'fs';

async function scrapeFullCatalog() {
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
    console.log('Navigating to https://shop.happiergrocery.com/shop ...');
    await call('Page.navigate', { url: 'https://shop.happiergrocery.com/shop' });
    await new Promise(r => setTimeout(r, 8000));

    console.log('Scrolling down to trigger infinite scroll queries...');
    for (let i = 0; i < 20; i++) {
      await call('Runtime.evaluate', { expression: 'window.scrollTo(0, document.body.scrollHeight);' });
      await new Promise(r => setTimeout(r, 2000));
      process.stdout.write((i + 1) + ' ');
    }
    console.log('\nFinished scrolling. Extracting all product cards...');

    const evalRes = await call('Runtime.evaluate', {
      expression: `(() => {
        const results = [];
        const cards = Array.from(document.querySelectorAll('a[href*="/product/"]'));
        for (const card of cards) {
          const href = card.href;
          const text = card.innerText.trim();
          const img = card.querySelector('img');
          const imgSrc = img ? img.src : '';
          const imgAlt = img ? img.alt : '';
          results.push({ href, text, imgSrc, imgAlt });
        }
        return JSON.stringify(results);
      })()`
    });

    const items = JSON.parse(evalRes.result?.value || '[]');
    console.log('Total card elements extracted: ' + items.length);
    fs.writeFileSync('scripts/happier_full_raw.json', JSON.stringify(items, null, 2));

    ws.close();
    chrome.kill();
  };
}

scrapeFullCatalog().catch(console.error);
