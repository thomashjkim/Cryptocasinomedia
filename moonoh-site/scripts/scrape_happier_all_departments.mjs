import { spawn } from 'child_process';
import fs from 'fs';

async function scrapeAllHappier() {
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

    const urls = [
      'https://shop.happiergrocery.com/shop',
      'https://shop.happiergrocery.com/shop?departmentID=GROCERY',
      'https://shop.happiergrocery.com/shop?departmentID=PREPARED_FOODS',
      'https://shop.happiergrocery.com/shop?departmentID=SNACKS',
      'https://shop.happiergrocery.com/shop?departmentID=PANTRY',
      'https://shop.happiergrocery.com/shop?departmentID=DRINKS',
      'https://shop.happiergrocery.com/shop?departmentID=MERCHANDISE'
    ];

    const allProducts = new Map();

    for (const u of urls) {
      console.log('Navigating to:', u);
      await call('Page.navigate', { url: u });
      await new Promise(r => setTimeout(r, 6000));

      for (let s = 0; s < 8; s++) {
        await call('Runtime.evaluate', { expression: 'window.scrollBy(0, 1500);' });
        await new Promise(r => setTimeout(r, 1200));
      }

      const evalRes = await call('Runtime.evaluate', {
        expression: `(() => {
          const res = [];
          const cards = Array.from(document.querySelectorAll('a[href*="/product/"]'));
          for (const card of cards) {
            const href = card.href;
            const text = card.innerText.trim();
            const img = card.querySelector('img');
            const imgSrc = img ? img.src : '';
            const imgAlt = img ? img.alt : '';
            if (href && text && imgSrc) {
              res.push({ href, text, imgSrc, imgAlt });
            }
          }
          return JSON.stringify(res);
        })()`
      });

      const items = JSON.parse(evalRes.result?.value || '[]');
      console.log('  Found ' + items.length + ' cards');
      for (const item of items) {
        const idMatch = item.href.match(/\/product\/([a-f0-9]+)/i);
        if (idMatch) {
          const prodId = idMatch[1];
          if (!allProducts.has(prodId)) {
            allProducts.set(prodId, item);
          }
        }
      }
    }

    console.log('Total unique products collected: ' + allProducts.size);
    fs.writeFileSync('scripts/happier_scraped_unique.json', JSON.stringify(Array.from(allProducts.values()), null, 2));

    ws.close();
    chrome.kill();
  };
}

scrapeAllHappier().catch(console.error);
