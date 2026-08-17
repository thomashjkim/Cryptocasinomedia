import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testMirthDetailButton() {
  const req = new Request("https://moon-oh.com/local-product/mirth-vintage/60s-lace-skirt-set");
  const resp = await itemDetailHandler(req);
  const body = await resp.text();
  
  console.log("Status:", resp.status);
  const hasBlackBtn = body.includes("background:#000000") || body.includes("background: #000000") || body.includes("btnBgColor = \"#000000\"") || body.includes("#000000");
  console.log("Has #000000 in rendered HTML:", hasBlackBtn);
  
  const m = body.match(/class="chat-btn"[^>]*style="([^"]*)"/);
  if (m) {
    console.log("Chat/View button inline style:", m[1]);
  }
  
  const bannerMatch = body.match(/🛒 <strong>Mirth Vintage<\/strong>/);
  console.log("Has Mirth banner:", !!bannerMatch);
}

testMirthDetailButton();
