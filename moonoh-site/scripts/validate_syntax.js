const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('=== RUNNING MOONOH ZERO-SYNTAX-ERROR GATE ===');

const htmlFiles = [
  'moonoh-site/explore.html',
  'moonoh-site/index.html'
];

const mjsFiles = [
  'moonoh-site/netlify/functions/explore.mjs',
  'moonoh-site/netlify/functions/reports.mjs',
  'moonoh-site/netlify/functions/items.mjs',
  'moonoh-site/netlify/functions/external-items.mjs',
  'moonoh-site/netlify/functions/food-rescue-items.mjs'
];

let hasError = false;

for (const relPath of htmlFiles) {
  const fullPath = path.resolve(__dirname, '../../', relPath);
  if (!fs.existsSync(fullPath)) continue;

  const content = fs.readFileSync(fullPath, 'utf8');
  const matches = [...content.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  matches.forEach((m, idx) => {
    const typeMatch = m[0].match(/type=[\"']([^\"']+)[\"']/i);
    const scriptType = typeMatch ? typeMatch[1] : 'javascript';
    if (scriptType.includes('json') || scriptType.includes('ld+json')) {
      try {
        JSON.parse(m[1]);
      } catch (e) {
        console.error(`❌ [${relPath}] Script #${idx+1} (${scriptType}) JSON ERROR:`, e.message);
        hasError = true;
      }
    } else {
      try {
        new Function(m[1]);
      } catch (e) {
        console.error(`❌ [${relPath}] Script #${idx+1} (JS) SYNTAX ERROR:`, e.message);
        hasError = true;
      }
    }
  });
}

for (const relPath of mjsFiles) {
  const fullPath = path.resolve(__dirname, '../../', relPath);
  if (!fs.existsSync(fullPath)) continue;
  try {
    execSync(`node --check ${fullPath}`, { stdio: 'pipe' });
  } catch (e) {
    console.error(`❌ [${relPath}] MJS SYNTAX ERROR:`, e.stderr ? e.stderr.toString() : e.message);
    hasError = true;
  }
}

if (hasError) {
  console.error('\n🚨 SYNTAX VALIDATION FAILED! CANNOT PROCEED.');
  process.exit(1);
} else {
  console.log('✅ ALL SCRIPTS & HTML/MJS FILES PASSED ZERO-SYNTAX-ERROR GATE.');
  process.exit(0);
}
