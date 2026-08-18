import re

print("=" * 80)
print("📍 STEP 4: REMOVING FORT LEE DROPDOWN OPTION & CONSOLIDATING TO BERGEN COUNTY, NJ")
print("=" * 80)

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_code = f.read()

# Remove Fort Lee option
exp_code = exp_code.replace('<option value="Fort Lee">Fort Lee, NJ</option>\n', '')
exp_code = exp_code.replace('<option value="Fort Lee">Fort Lee, NJ</option>', '')

# Update regionKeywords
exp_code = re.sub(
    r"'Fort Lee':\s*\[[^\]]+\],\s*",
    "",
    exp_code
)
exp_code = re.sub(
    r"'Bergen':\s*\[[^\]]+\],",
    "'Bergen': ['bergen', 'hackensack', 'paramus', 'fort lee', 'fortlee', 'englewood', 'teaneck', 'palisades', 'palisades park', 'fair lawn', 'garfield', 'ridgewood', 'rutherford', 'edgewater', 'leonia', 'cliffside park'],",
    exp_code
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp_code)
print("✅ Updated explore.html (Fort Lee removed from dropdown, consolidated into Bergen County)")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_code = f.read()

idx_code = idx_code.replace('<option value="Fort Lee">Fort Lee, NJ</option>\n', '')
idx_code = idx_code.replace('<option value="Fort Lee">Fort Lee, NJ</option>', '')

idx_code = re.sub(
    r"'Fort Lee':\s*\[[^\]]+\],\s*",
    "",
    idx_code
)
idx_code = re.sub(
    r"'Bergen':\s*\[[^\]]+\],",
    "'Bergen': ['bergen', 'hackensack', 'paramus', 'fort lee', 'fortlee', 'englewood', 'teaneck', 'palisades', 'palisades park', 'fair lawn', 'garfield', 'ridgewood', 'rutherford', 'edgewater', 'leonia', 'cliffside park'],",
    idx_code
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_code)
print("✅ Updated index.html (Fort Lee removed from dropdown, consolidated into Bergen County)")

# 3. Update netlify/functions/explore.mjs
with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    fn_exp = f.read()

fn_exp = fn_exp.replace('<option value="Fort Lee">Fort Lee, NJ</option>\n', '')
fn_exp = fn_exp.replace('<option value="Fort Lee">Fort Lee, NJ</option>', '')

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(fn_exp)
print("✅ Updated netlify/functions/explore.mjs")
