import re

print("=" * 80)
print("🏙️ ELIMINATING ALL 'NYC' HARDCODED STRINGS IN FRONTENDS & SSR")
print("=" * 80)

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp = f.read()

# Replace local shop mapping in explore.html
exp = re.sub(
    r"townName:\s*p\.availability_context\s*\|\|\s*\(p\.store_city\s*\?[^:]+:\s*'NYC'\),\s*rawTown:\s*'NYC',\s*location:\s*'NYC',",
    "townName: p.location || (p.shop_id === 'happier-grocery' || p.shop_id === 'pop-up-grocer' ? 'Manhattan, NY' : 'Brooklyn, NY'),\n            rawTown: p.location || (p.shop_id === 'happier-grocery' || p.shop_id === 'pop-up-grocer' ? 'Manhattan, NY' : 'Brooklyn, NY'),\n            location: p.location || (p.shop_id === 'happier-grocery' || p.shop_id === 'pop-up-grocer' ? 'Manhattan, NY' : 'Brooklyn, NY'),",
    exp
)

exp = exp.replace("location: raw.location || raw.townName || 'NYC',", "location: raw.location || raw.townName || 'Manhattan, NY',")
exp = exp.replace("const rawLoc = item.location || item.rawTown || 'NYC';", "const rawLoc = item.location || item.rawTown || 'Manhattan, NY';")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp)
print("✅ Updated explore.html (no more 'NYC' defaults for local shops or fallback items)")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(
    r"location:\s*p\.availability_context\s*\|\|\s*\(p\.store_city\s*\?[^:]+:\s*'NYC'\),\s*rawTown:\s*'NYC',",
    "location: p.location || (p.shop_id === 'happier-grocery' || p.shop_id === 'pop-up-grocer' ? 'Manhattan, NY' : 'Brooklyn, NY'),\n              rawTown: p.location || (p.shop_id === 'happier-grocery' || p.shop_id === 'pop-up-grocer' ? 'Manhattan, NY' : 'Brooklyn, NY'),",
    idx
)

idx = idx.replace("const itemLocation = item.location || item.townName || 'NYC';", "const itemLocation = item.location || item.townName || 'Manhattan, NY';")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("✅ Updated index.html")

# 3. Update netlify/functions/explore.mjs
with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    exp_mjs = f.read()

exp_mjs = exp_mjs.replace("townName || item.location || 'NYC'", "townName || item.location || 'Manhattan, NY'")
exp_mjs = exp_mjs.replace("'NYC, NY'", "'Manhattan, NY'")

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(exp_mjs)
print("✅ Updated explore.mjs")
