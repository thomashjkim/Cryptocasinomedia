/**
 * Moonoh Local Products Deterministic Mixer
 * Balances representation across local NYC shops without letting large inventories dominate.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.getBalancedLocalProducts = factory().getBalancedLocalProducts;
  }
}(typeof self !== 'undefined' ? self : this, function () {

  function getBalancedLocalProducts(products, options = {}) {
    const {
      limit = Infinity,
      context = 'default',
      dateKey = null,
      maxConsecutivePerStore = 2,
      category = 'All'
    } = options;

    if (!Array.isArray(products) || products.length === 0) return [];

    let pool = products;
    if (category && category !== 'All') {
      pool = products.filter(p => {
        const cat = p.primary_category || p.moonoh_category || p.category || p.categoryName;
        return cat === category;
      });
    }
    if (pool.length === 0) return [];

    const storeMap = new Map();
    for (const p of pool) {
      const sId = p.shop_id || p.source || 'other';
      if (!storeMap.has(sId)) {
        storeMap.set(sId, []);
      }
      storeMap.get(sId).push(p);
    }

    // 1. Internal Store Sorting:
    // Priority: 1. source_published_at, 2. source_created_at, 3. source_updated_at, 4. source_order, 5. source_product_id
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

    // 2. Deterministic Seed from America/New_York date + context
    let nyDate = dateKey;
    if (!nyDate) {
      try {
        const nyFormatter = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' });
        nyDate = nyFormatter.format(new Date()); // 'YYYY-MM-DD'
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

    // 3. Round-Robin Queue Drain with maxConsecutivePerStore constraint
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

  return { getBalancedLocalProducts };
}));
