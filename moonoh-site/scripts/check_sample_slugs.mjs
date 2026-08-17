import { realMoonohItems } from '../netlify/functions/moonoh-items-data.mjs';
import { realFoodRescueItems } from '../netlify/functions/food-rescue-items.mjs';

function getSlug(title, loc, no) {
  let clean = (title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
  if (clean.length > 50) clean = clean.substring(0, 50).replace(/-$/, '');
  const locSlug = (loc || 'nyc').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
  return `${clean}-${locSlug}-${no}`;
}

const m = realMoonohItems[0];
console.log("Moonoh item 1 URL: https://moon-oh.com/item/" + getSlug(m.title, m.townName, m.no));

const f = realFoodRescueItems[0];
let cleanF = (f.title || 'item').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').replace(/-+/g, '-');
if (cleanF.length > 50) cleanF = cleanF.substring(0, 50).replace(/-$/, '');
const locF = (f.location || 'nyc').toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
console.log(`Food rescue item 1 URL: https://moon-oh.com/item/${cleanF}-${locF}-ext-${f.id}`);
