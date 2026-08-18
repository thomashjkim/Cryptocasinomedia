import fs from 'fs';

// Update verify_all_breadcrumb_cases.mjs to dynamically use live product slugs
const scriptPath = 'scripts/verify_all_breadcrumb_cases.mjs';
let code = fs.readFileSync(scriptPath, 'utf8');

const dynamicCasesBlock = `  const localDb = JSON.parse(fs.readFileSync('./local_shops_data.json', 'utf8'));
  const prods = localDb.products || [];
  const seyProd = prods.find(p => p.shop_id === 'sey-coffee');
  const popProd = prods.find(p => p.shop_id === 'pop-up-grocer');
  const fgsProd = prods.find(p => p.shop_id === 'front-general-store');
  const saltProd = prods.find(p => p.shop_id === 'salter-house');

  const testCases = [
    {
      sourceType: "Local Shop (SEY Coffee)",
      url: \`https://moon-oh.com/local-product/sey-coffee/\${seyProd ? seyProd.slug : 'coffee'}\`,
      expectedTab: "/explore?source=localshops",
      expectedRegion: "/explore?source=localshops&area=Brooklyn%2C%20NY",
      expectedCategory: "/explore?source=localshops&area=Brooklyn%2C%20NY&category=coffee-pantry",
      expectedShop: "/local-shops/sey-coffee",
      targetCategoryUrl: "https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY&category=coffee-pantry"
    },
    {
      sourceType: "Local Shop (Pop Up Grocer)",
      url: \`https://moon-oh.com/local-product/pop-up-grocer/\${popProd ? popProd.slug : 'prind'}\`,
      expectedTab: "/explore?source=localshops",
      expectedRegion: "/explore?source=localshops&area=Manhattan%2C%20NY",
      expectedCategory: "/explore?source=localshops&area=Manhattan%2C%20NY&category=coffee-pantry",
      expectedShop: "/local-shops/pop-up-grocer",
      targetCategoryUrl: "https://moon-oh.com/explore?source=localshops&area=Manhattan%2C%20NY&category=coffee-pantry"
    },
    {
      sourceType: "Local Shop (Front General Store)",
      url: \`https://moon-oh.com/local-product/front-general-store/\${fgsProd ? fgsProd.slug : 'vintage'}\`,
      expectedTab: "/explore?source=localshops",
      expectedRegion: "/explore?source=localshops&area=Brooklyn%2C%20NY",
      expectedCategory: "/explore?source=localshops&area=Brooklyn%2C%20NY&category=vintage-fashion",
      expectedShop: "/local-shops/front-general-store",
      targetCategoryUrl: "https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY&category=vintage-fashion"
    },
    {
      sourceType: "Local Shop (Salter House)",
      url: \`https://moon-oh.com/local-product/salter-house/\${saltProd ? saltProd.slug : 'soap'}\`,
      expectedTab: "/explore?source=localshops",
      expectedRegion: "/explore?source=localshops&area=Brooklyn%2C%20NY",
      expectedCategory: "/explore?source=localshops&area=Brooklyn%2C%20NY&category=home-objects",
      expectedShop: "/local-shops/salter-house",
      targetCategoryUrl: "https://moon-oh.com/explore?source=localshops&area=Brooklyn%2C%20NY&category=home-objects"
    },
    {
      sourceType: "Food Rescue (Kim'C Market)",
      url: "https://moon-oh.com/item/woorimil-wheat-egg-cookie-sell-by-sale-brooklyn-ny-ext-kimc-8141248626941",
      expectedTab: "/explore?source=foodrescue",
      expectedRegion: "/explore?source=foodrescue&area=Brooklyn%2C%20NY",
      expectedCategory: "/explore?source=foodrescue&area=Brooklyn%2C%20NY&category=food-groceries",
      targetCategoryUrl: "https://moon-oh.com/explore?source=foodrescue&area=Brooklyn%2C%20NY&category=food-groceries"
    },
    {
      sourceType: "Marketplace (Karrot Item)",
      url: "https://moon-oh.com/item/petmate-replendish-25-gallon-pet-waterer-manhattan-ny-ext-karrot-i9753yxh6ayn",
      expectedTab: "/explore?source=marketplaces",
      expectedRegion: "/explore?source=marketplaces&area=Manhattan%2C%20NY",
      expectedCategory: "/explore?source=marketplaces&area=Manhattan%2C%20NY&category=pet-supplies",
      targetCategoryUrl: "https://moon-oh.com/explore?source=marketplaces&area=Manhattan%2C%20NY&category=pet-supplies"
    },
    {
      sourceType: "Moonoh Listing (No. 855)",
      url: "https://moon-oh.com/item/khadlaj-island-dreams-the-bronx-ny-855",
      expectedTab: "/explore?source=moonoh",
      expectedRegion: "/explore?source=moonoh&area=The%20Bronx%2C%20NY",
      expectedCategory: "/explore?source=moonoh&area=The%20Bronx%2C%20NY&category=sports-leisure",
      targetCategoryUrl: "https://moon-oh.com/explore?source=moonoh&area=The%20Bronx%2C%20NY&category=sports-leisure"
    },
    {
      sourceType: "Moonoh Listing (No. 851)",
      url: "https://moon-oh.com/item/oura-ring-4-size-9-brand-new-in-fhe-box-brooklyn-ny-851",
      expectedTab: "/explore?source=moonoh",
      expectedRegion: "/explore?source=moonoh&area=Brooklyn%2C%20NY",
      expectedCategory: "/explore?source=moonoh&area=Brooklyn%2C%20NY&category=electronics",
      targetCategoryUrl: "https://moon-oh.com/explore?source=moonoh&area=Brooklyn%2C%20NY&category=electronics"
    }
  ];`;

// Replace testCases block
code = code.replace(/const testCases = \[[\s\S]*?\n  \];/, dynamicCasesBlock);
fs.writeFileSync(scriptPath, code, 'utf8');
console.log("✅ Updated verify_all_breadcrumb_cases.mjs with dynamic product slugs");

// Also update validate_all_10_user_issues.mjs
const valPath = 'scripts/validate_all_10_user_issues.mjs';
let valCode = fs.readFileSync(valPath, 'utf8');
valCode = valCode.replace(
  "new Request('https://moon-oh.com/local-product/sey-coffee/oma-plot')",
  "new Request(`https://moon-oh.com/local-product/sey-coffee/${seyProd ? seyProd.slug : 'coffee'}`)"
);
if (!valCode.includes('const localDb = JSON.parse')) {
  valCode = valCode.replace('async function runAudit() {', 'async function runAudit() {\n  const localDb = JSON.parse(fs.readFileSync("./local_shops_data.json", "utf8"));\n  const prods = localDb.products || [];\n  const seyProd = prods.find(p => p.shop_id === "sey-coffee");');
}
fs.writeFileSync(valPath, valCode, 'utf8');
console.log("✅ Updated validate_all_10_user_issues.mjs with dynamic product slugs");
