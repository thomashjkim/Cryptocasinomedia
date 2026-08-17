import fs from 'fs';

const rawDb = JSON.parse(fs.readFileSync('local_shops_data.json', 'utf8'));

export function getBalancedLocalProducts(products, options = {}) {
  const {
    limit = Infinity,
    context = 'default',
    dateKey = null,
    maxConsecutivePerStore = 2,
    category = 'All'
  } = options;

  let pool = products;
  if (category && category !== 'All') {
    pool = products.filter(p => {
      const cat = p.primary_category || p.moonoh_category || p.category || p.categoryName;
      return cat === category;
    });
  }
  if (!pool || pool.length === 0) return [];

  const storeMap = new Map();
  for (const p of pool) {
    const sId = p.shop_id || p.source || 'other';
    if (!storeMap.has(sId)) {
      storeMap.set(sId, []);
    }
    storeMap.get(sId).push(p);
  }

  // Internal store sort
  for (const [sId, items] of storeMap.entries()) {
    items.sort((a, b) => {
      const aPub = a.source_published_at ? new Date(a.source_published_at).getTime() : 0;
      const bPub = b.source_published_at ? new Date(b.source_published_at).getTime() : 0;
      if (aPub !== bPub) return bPub - aPub;

      const aCre = a.source_created_at ? new Date(a.source_created_at).getTime() : 0;
      const bCre = b.source_created_at ? new Date(b.source_created_at).getTime() : 0;
      if (aCre !== bCre) return bCre - aCre;

      const aUpd = a.source_updated_at ? new Date(a.source_updated_at).getTime() : 0;
      const bUpd = b.source_updated_at ? new Date(b.source_updated_at).getTime() : 0;
      if (bUpd !== aUpd) return bUpd - aUpd;

      const aOrd = Number(a.source_order) || 0;
      const bOrd = Number(b.source_order) || 0;
      if (aOrd !== bOrd) return aOrd - bOrd;

      return String(a.source_product_id || a.id).localeCompare(String(b.source_product_id || b.id));
    });
  }

  let nyDate = dateKey;
  if (!nyDate) {
    try {
      const nyFormatter = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' });
      nyDate = nyFormatter.format(new Date());
    } catch (e) {
      nyDate = new Date().toISOString().split('T')[0];
    }
  }

  let seedStr = `${nyDate}:${context}`;
  let seedHash = 0;
  for (let i = 0; i < seedStr.length; i++) {
    seedHash = ((seedHash << 5) - seedHash) + seedStr.charCodeAt(i);
    seedHash |= 0;
  }
  const positiveSeed = Math.abs(seedHash);

  const storeKeys = Array.from(storeMap.keys()).sort();
  const startIndex = positiveSeed % storeKeys.length;
  const rotatedStores = [...storeKeys.slice(startIndex), ...storeKeys.slice(0, startIndex)];

  const queues = new Map();
  for (const s of rotatedStores) {
    queues.set(s, [...storeMap.get(s)]);
  }

  const result = [];
  let lastStore = null;
  let consecutiveCount = 0;

  while (result.length < limit) {
    let anyAddedInRound = false;

    for (const s of rotatedStores) {
      if (result.length >= limit) break;
      const queue = queues.get(s);
      if (!queue || queue.length === 0) continue;

      if (lastStore === s && consecutiveCount >= maxConsecutivePerStore) {
        const otherAvailable = rotatedStores.find(other => other !== s && queues.get(other)?.length > 0);
        if (otherAvailable) {
          continue;
        }
      }

      const item = queue.shift();
      result.push(item);
      anyAddedInRound = true;

      if (lastStore === s) {
        consecutiveCount++;
      } else {
        lastStore = s;
        consecutiveCount = 1;
      }
    }

    if (!anyAddedInRound) {
      const remainingStores = rotatedStores.filter(s => queues.get(s)?.length > 0);
      if (remainingStores.length === 0) break;
      for (const s of remainingStores) {
        if (result.length >= limit) break;
        const queue = queues.get(s);
        if (queue && queue.length > 0) {
          result.push(queue.shift());
          lastStore = s;
        }
      }
    }
  }

  return result;
}

// Test runner
function test() {
  console.log("=== Testing getBalancedLocalProducts ===");
  const products = rawDb.products;
  console.log(`Total Products: ${products.length}`);

  // 1. Test Home Context
  const homeResults1 = getBalancedLocalProducts(products, { context: 'home', limit: 24 });
  const homeResults2 = getBalancedLocalProducts(products, { context: 'home', limit: 24 });
  console.log(`Home Deterministic Same Day: ${JSON.stringify(homeResults1.map(i => i.id)) === JSON.stringify(homeResults2.map(i => i.id))}`);

  // Check consecutive count
  let maxConsecutive = 0;
  let currConsecutive = 0;
  let prevShop = null;
  for (const item of homeResults1) {
    if (item.shop_id === prevShop) {
      currConsecutive++;
    } else {
      currConsecutive = 1;
      prevShop = item.shop_id;
    }
    if (currConsecutive > maxConsecutive) maxConsecutive = currConsecutive;
  }
  console.log(`Max Consecutive in Home First 24: ${maxConsecutive} (<= 2: ${maxConsecutive <= 2})`);

  // Source Distribution First 12 & First 24 in Home
  const dist12 = {};
  homeResults1.slice(0, 12).forEach(i => dist12[i.shop_id] = (dist12[i.shop_id] || 0) + 1);
  console.log("Home First 12 Distribution:", dist12);

  const dist24 = {};
  homeResults1.slice(0, 24).forEach(i => dist24[i.shop_id] = (dist24[i.shop_id] || 0) + 1);
  console.log("Home First 24 Distribution:", dist24);

  // 2. Test Explore Local Context
  const exploreResults = getBalancedLocalProducts(products, { context: 'explore-local', limit: 24 });
  const expDist12 = {};
  exploreResults.slice(0, 12).forEach(i => expDist12[i.shop_id] = (expDist12[i.shop_id] || 0) + 1);
  console.log("\nExplore-Local First 12 Distribution:", expDist12);

  const expDist24 = {};
  exploreResults.slice(0, 24).forEach(i => expDist24[i.shop_id] = (expDist24[i.shop_id] || 0) + 1);
  console.log("Explore-Local First 24 Distribution:", expDist24);

  // 3. Test Category Filtering
  const categories = ['Vintage & Fashion', 'Home & Objects', 'Coffee & Pantry', 'Gifts & Culture'];
  console.log("\nCategory Counts in DB & Filter Test:");
  for (const cat of categories) {
    const catItems = getBalancedLocalProducts(products, { category: cat, limit: 1000 });
    console.log(`  ${cat}: ${catItems.length} items (100% match: ${catItems.every(i => i.primary_category === cat)})`);
  }
}

test();
