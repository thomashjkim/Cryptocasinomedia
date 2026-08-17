import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function testDebug() {
  const req = new Request("https://moon-oh.com/local-product/sey-coffee/oma-plot");
  try {
    const resp = await itemDetailHandler(req);
    const body = await resp.text();
    console.log("Status:", resp.status);
    if (resp.status !== 200) {
      console.log("Body error:", body);
    }
  } catch (e) {
    console.error("Caught error:", e);
  }
}

testDebug();
