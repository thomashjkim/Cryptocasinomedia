import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testSalterDetail() {
  const req = new Request("https://moon-oh.com/local-product/salter-house/gift-wrap");
  const resp = await itemDetailHandler(req);
  const body = await resp.text();

  console.log("Status:", resp.status);
  const hasSalterColor = body.includes("#007A4B") || body.includes("#007a4b");
  console.log("Has #007A4B in rendered HTML:", hasSalterColor);
  
  const m = body.match(/class="chat-btn"[^>]*style="([^"]*)"/);
  if (m) {
    console.log("Chat/View button inline style:", m[1]);
  }
}

testSalterDetail();
