import itemDetailHandler from '../netlify/functions/item-detail.mjs';

async function checkRedirects() {
  const req1 = new Request("https://moon-oh.com/item/khadlaj-island-dreams-manhattan-ny-855");
  const resp1 = await itemDetailHandler(req1);
  console.log("855 Redirect ->", resp1.headers.get('Location'));

  const req2 = new Request("https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-malverne-ny-ext-karrot-i9753yxh6ayn");
  const resp2 = await itemDetailHandler(req2);
  console.log("Karrot Redirect ->", resp2.headers.get('Location'));
}

checkRedirects();
