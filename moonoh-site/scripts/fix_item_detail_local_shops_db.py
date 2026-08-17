import re

print("=" * 80)
print("🔧 FIXING LOCAL SHOPS DB IN netlify/functions/item-detail.mjs")
print("=" * 80)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add top imports if not present
top_imports = '''import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const currentDir = path.dirname(fileURLToPath(import.meta.url));

function getLocalShopsDb() {
  try {
    const jsonPath = path.join(currentDir, '../../local_shops_data.json');
    if (fs.existsSync(jsonPath)) {
      return JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    }
  } catch (e) {}
  try {
    const jsonPathAlt = path.join(process.cwd(), 'local_shops_data.json');
    if (fs.existsSync(jsonPathAlt)) {
      return JSON.parse(fs.readFileSync(jsonPathAlt, 'utf8'));
    }
  } catch (e) {}
  return { shops: {}, products: [] };
}
'''

if 'function getLocalShopsDb' not in code:
    code = top_imports + '\n' + code

# 2. Replace hardcoded const localShopsDb = {...}; with const localShopsDb = getLocalShopsDb();
code = re.sub(
    r'const localShopsDb = \{"shops":[\s\S]*?\};\n\s*if \(localProductMatch\)',
    'const localShopsDb = getLocalShopsDb();\n      if (localProductMatch)',
    code
)

# Also check for any other occurrences
code = re.sub(
    r'const localShopsDb = \{"shops":[\s\S]*?\};',
    'const localShopsDb = getLocalShopsDb();',
    code
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Saved netlify/functions/item-detail.mjs with dynamic getLocalShopsDb()")
