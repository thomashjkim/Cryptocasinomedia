import mixerPkg from '../js/local-products-mixer.js';
import { realKarrotItems, realHeyKoreanItems } from '../netlify/functions/external-items.mjs';

const { getBalancedMarketplaceProducts } = mixerPkg;

const allItems = [...realKarrotItems, ...realHeyKoreanItems];
console.log(`Total Marketplace Items: ${allItems.length} (${realKarrotItems.length} Karrot, ${realHeyKoreanItems.length} HeyKorean)`);

const mixed12 = getBalancedMarketplaceProducts(allItems, { limit: 12, context: 'explore-marketplace' });
const mixed24 = getBalancedMarketplaceProducts(allItems, { limit: 24, context: 'explore-marketplace' });

console.log('\n--- First 12 Items Distribution ---');
const dist12 = {};
mixed12.forEach((i, idx) => {
  dist12[i.source] = (dist12[i.source] || 0) + 1;
  console.log(`  #${idx+1}: [${i.source.toUpperCase()}] ${i.title.substring(0, 35)} ($${i.price}) in ${i.rawTown}`);
});
console.log('Count:', dist12);

console.log('\n--- First 24 Items Distribution ---');
const dist24 = {};
mixed24.forEach(i => dist24[i.source] = (dist24[i.source] || 0) + 1);
console.log('Count:', dist24);

// Max consecutive
let maxConsec = 0, curr = 0, prev = null;
for (const item of mixed24) {
  if (item.source === prev) curr++;
  else { curr = 1; prev = item.source; }
  if (curr > maxConsec) maxConsec = curr;
}
console.log(`\nMax consecutive same platform: ${maxConsec} (Expected <= 2)`);

if (dist12['karrot'] < 5 || dist12['heykorean'] < 5 || maxConsec > 2) {
  throw new Error('❌ Marketplace mixing test failed!');
}
console.log('✅ Marketplace 50:50 Balanced Mixing Verified Successfully!');
