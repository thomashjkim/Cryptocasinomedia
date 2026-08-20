import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { realFoodRescueItems } from '../netlify/functions/food-rescue-items.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Standard Quantile Helper (NIST / R-type 7)
function getStandardQuantile(sortedArr, q) {
  if (!sortedArr || sortedArr.length === 0) return 0;
  if (sortedArr.length === 1) return sortedArr[0];
  const pos = (sortedArr.length - 1) * q;
  const base = Math.floor(pos);
  const rest = pos - base;
  if (sortedArr[base + 1] !== undefined) {
    return Math.round((sortedArr[base] + rest * (sortedArr[base + 1] - sortedArr[base])) * 100) / 100;
  }
  return sortedArr[base];
}

async function recordDailySnapshot() {
  const rootDir = path.resolve(__dirname, '..');
  const dataDir = path.resolve(rootDir, 'data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  const snapshotFile = path.resolve(dataDir, 'historical_market_snapshots.json');

  const moonohItems = JSON.parse(fs.readFileSync(path.resolve(rootDir, 'data.json'), 'utf8'));
  const externalData = JSON.parse(fs.readFileSync(path.resolve(rootDir, 'real_external_items.json'), 'utf8'));
  const localData = JSON.parse(fs.readFileSync(path.resolve(rootDir, 'local_shops_data.json'), 'utf8'));
  const foodData = realFoodRescueItems || [];

  const extItems = [...(externalData.karrot || []), ...(externalData.heykorean || [])];
  const shopItems = localData.products || [];

  const allItems = [];

  moonohItems.forEach(i => {
    allItems.push({
      id: i.id || i.no,
      title: i.title,
      price: i.price,
      location: i.location || i.townName || 'Manhattan, NY',
      category: i.categoryName || i.category || 'General',
      source: 'moonoh'
    });
  });

  extItems.forEach(i => {
    allItems.push({
      id: i.id || i.no,
      title: i.title,
      price: i.price,
      location: i.location || i.townName || 'NYC',
      category: i.category || 'General',
      source: i.source || 'external'
    });
  });

  const nhMap = {
    'Greenpoint': 'Brooklyn, NY', 'Bushwick': 'Brooklyn, NY',
    'DUMBO': 'Brooklyn, NY', 'Brooklyn Heights': 'Brooklyn, NY',
    'SoHo': 'Manhattan, NY', 'Greenwich Village': 'Manhattan, NY',
    'Williamsburg': 'Brooklyn, NY', 'Astoria': 'Queens, NY'
  };

  shopItems.forEach(p => {
    const shop = (localData.shops && localData.shops[p.shop_id]) || {};
    const loc = nhMap[shop.neighborhood] || p.location || shop.location || 'Brooklyn, NY';
    allItems.push({
      id: p.id,
      title: p.title,
      price: p.current_price,
      location: loc,
      category: p.primary_category || p.moonoh_category || 'General',
      source: p.shop_id || 'local-shop'
    });
  });

  foodData.forEach(i => {
    allItems.push({
      id: i.id,
      title: i.title,
      price: i.price,
      location: 'Brooklyn, NY',
      category: i.categoryName || 'Food & Groceries',
      source: 'kimc'
    });
  });

  const todayStr = new Date().toISOString().split('T')[0];
  console.log(`[Snapshot] Capturing daily market pulse for ${todayStr} across ${allItems.length} live items...`);

  const regions = {
    'manhattan': ['manhattan', 'soho', 'harlem', 'upper east', 'upper west', 'midtown', 'chelsea', 'east village', 'tribeca', 'financial district'],
    'brooklyn': ['brooklyn', 'williamsburg', 'bushwick', 'greenpoint', 'park slope', 'dumbo', 'cobble hill', 'bed stuy'],
    'queens': ['queens', 'astoria', 'flushing', 'bayside', 'long island city', 'lic', 'forest hills', 'sunnyside']
  };

  const categories = ['furniture', 'electronics', 'womens-fashion', 'home-garden', 'food-groceries'];

  const dailyRecords = {};

  for (const [rSlug, kws] of Object.entries(regions)) {
    const rItems = allItems.filter(item => {
      const loc = (item.location || '').toLowerCase();
      return kws.some(kw => loc.includes(kw));
    });

    const prices = rItems.map(i => {
      const num = typeof i.price === 'number' ? i.price : parseFloat(i.price);
      return (!isNaN(num) && num > 0) ? num : null;
    }).filter(p => p !== null).sort((a, b) => a - b);

    const freeCount = rItems.filter(i => {
      const p = i.price;
      return p === 0 || p === '0' || p === 'Free' || p === 'free';
    }).length;

    dailyRecords[rSlug] = {
      active_listings: rItems.length,
      median_price: getStandardQuantile(prices, 0.5),
      p25_price: getStandardQuantile(prices, 0.25),
      p75_price: getStandardQuantile(prices, 0.75),
      free_items: freeCount,
      categories: {}
    };

    for (const cat of categories) {
      const cItems = rItems.filter(item => {
        const text = ((item.category || '') + ' ' + (item.title || '')).toLowerCase();
        return text.includes(cat) || (cat === 'furniture' && (text.includes('sofa') || text.includes('chair') || text.includes('table') || text.includes('bed') || text.includes('desk')));
      });

      const cPrices = cItems.map(i => {
        const num = typeof i.price === 'number' ? i.price : parseFloat(i.price);
        return (!isNaN(num) && num > 0) ? num : null;
      }).filter(p => p !== null).sort((a, b) => a - b);

      dailyRecords[rSlug].categories[cat] = {
        active_listings: cItems.length,
        median_price: getStandardQuantile(cPrices, 0.5),
        p25_price: getStandardQuantile(cPrices, 0.25),
        p75_price: getStandardQuantile(cPrices, 0.75)
      };
    }
  }

  let existingSnapshots = {};
  if (fs.existsSync(snapshotFile)) {
    try {
      existingSnapshots = JSON.parse(fs.readFileSync(snapshotFile, 'utf8'));
    } catch (e) {
      existingSnapshots = {};
    }
  }

  existingSnapshots[todayStr] = dailyRecords;
  fs.writeFileSync(snapshotFile, JSON.stringify(existingSnapshots, null, 2), 'utf8');

  console.log(`[Snapshot] Successfully recorded daily pulse for ${todayStr} to ${snapshotFile}`);
}

recordDailySnapshot();
