import { spawn } from 'child_process';

async function run() {
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
    await call('Page.navigate', { url: 'https://shop.happiergrocery.com/product/69f4b7f336470545e58ee629' });
    await new Promise(r => setTimeout(r, 6000));

    const evalRes = await call('Runtime.evaluate', {
      expression: `(() => {
        const text = document.body.innerText;
        const imgs = Array.from(document.querySelectorAll('img')).map(i => ({ src: i.src, alt: i.alt }));
        const links = Array.from(document.querySelectorAll('a')).map(a => a.href);
        return JSON.stringify({ imgs, text: text.slice(0, 1000) });
      })()`
    });

    console.log('EXTRACTED DATA:\n', evalRes.result.value);

    ws.close();
    chrome.kill();
  };
}

run().catch(console.error);
