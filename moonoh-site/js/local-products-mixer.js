/**
 * Moonoh Local & Marketplace Products Deterministic Mixer
 * Balances representation across local NYC shops and external marketplace platforms (Karrot & HeyKorean)
 * without letting any single shop or platform dominate the feed.
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    const exports = factory();
    root.getBalancedLocalProducts = exports.getBalancedLocalProducts;
    root.getBalancedMarketplaceProducts = exports.getBalancedMarketplaceProducts;
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

    // Internal Store Sorting
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

    // Deterministic Seed
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

    const result = [];
    let lastStore = null;
    let consecutiveCount = 0;
    const totalItems = pool.length;

    while (result.length < totalItems && result.length < limit) {
      let progressMade = false;

      for (const store of rotatedStores) {
        const queue = queues.get(store);
        if (!queue || queue.length === 0) continue;

        if (store === lastStore && consecutiveCount >= maxConsecutivePerStore) {
          const otherStoresAvailable = Array.from(queues.entries()).some(([s, q]) => s !== store && q.length > 0);
          if (otherStoresAvailable) {
            continue;
          }
        }

        const item = queue.shift();
        result.push(item);
        progressMade = true;

        if (store === lastStore) {
          consecutiveCount++;
        } else {
          lastStore = store;
          consecutiveCount = 1;
        }

        if (result.length >= limit) break;
      }

      if (!progressMade) {
        for (const queue of queues.values()) {
          while (queue.length > 0 && result.length < limit) {
            result.push(queue.shift());
          }
        }
        break;
      }
    }

    return result;
  }

  function getBalancedMarketplaceProducts(products, options = {}) {
    const {
      limit = Infinity,
      context = 'default',
      dateKey = null,
      maxConsecutivePerPlatform = 2
    } = options;

    if (!Array.isArray(products) || products.length === 0) return [];

    // Separate into platforms (karrot vs heykorean vs other)
    const platformMap = new Map();
    for (const p of products) {
      let plat = (p.source || p.sourceName || 'other').toLowerCase();
      if (plat.includes('karrot')) plat = 'karrot';
      else if (plat.includes('heykorean')) plat = 'heykorean';
      else plat = 'other';

      if (!platformMap.has(plat)) {
        platformMap.set(plat, []);
      }
      platformMap.get(plat).push(p);
    }

    // Sort internal platform queues strictly by authentic posting recency
    for (const [plat, items] of platformMap.entries()) {
      items.sort((a, b) => {
        const aDate = a.postedAt ? new Date(a.postedAt).getTime() : (a.source_published_at ? new Date(a.source_published_at).getTime() : (typeof a.no === 'number' ? a.no : 0));
        const bDate = b.postedAt ? new Date(b.postedAt).getTime() : (b.source_published_at ? new Date(b.source_published_at).getTime() : (typeof b.no === 'number' ? b.no : 0));
        if (aDate !== bDate) return bDate - aDate;
        return String(a.id || '').localeCompare(String(b.id || ''));
      });
    }

    // Deterministic rotation seed
    let nyDate = dateKey;
    if (!nyDate) {
      try {
        const nyFormatter = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' });
        nyDate = nyFormatter.format(new Date());
      } catch (e) {
        nyDate = new Date().toISOString().split('T')[0];
      }
    }

    let seedStr = `${nyDate}:${context}:marketplace`;
    let seedHash = 0;
    for (let i = 0; i < seedStr.length; i++) {
      seedHash = ((seedHash << 5) - seedHash) + seedStr.charCodeAt(i);
      seedHash |= 0;
    }
    const positiveSeed = Math.abs(seedHash);

    const platformKeys = Array.from(platformMap.keys()).sort();
    const startIndex = positiveSeed % platformKeys.length;
    const rotatedPlatforms = [...platformKeys.slice(startIndex), ...platformKeys.slice(0, startIndex)];

    const queues = new Map();
    for (const plat of rotatedPlatforms) {
      queues.set(plat, [...platformMap.get(plat)]);
    }

    const result = [];
    let lastPlatform = null;
    let consecutiveCount = 0;
    const totalItems = products.length;

    while (result.length < totalItems && result.length < limit) {
      let progressMade = false;

      for (const plat of rotatedPlatforms) {
        const queue = queues.get(plat);
        if (!queue || queue.length === 0) continue;

        if (plat === lastPlatform && consecutiveCount >= maxConsecutivePerPlatform) {
          const otherAvailable = Array.from(queues.entries()).some(([otherPlat, otherQ]) => otherPlat !== plat && otherQ.length > 0);
          if (otherAvailable) {
            continue;
          }
        }

        const item = queue.shift();
        result.push(item);
        progressMade = true;

        if (plat === lastPlatform) {
          consecutiveCount++;
        } else {
          lastPlatform = plat;
          consecutiveCount = 1;
        }

        if (result.length >= limit) break;
      }

      if (!progressMade) {
        for (const queue of queues.values()) {
          while (queue.length > 0 && result.length < limit) {
            result.push(queue.shift());
          }
        }
        break;
      }
    }

    return result;
  }

  return {
    getBalancedLocalProducts,
    getBalancedMarketplaceProducts
  };
}));
