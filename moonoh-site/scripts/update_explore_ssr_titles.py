with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    exp_mjs = f.read()

exp_mjs = exp_mjs.replace(
    'pageTitle = "NYC Food Waste Rescue & Grocery Deals | Moonoh";',
    'pageTitle = "NYC Food Waste Rescue & Sustainable Groceries | Moonoh";'
)

exp_mjs = exp_mjs.replace(
    'pageTitle = "NYC & NJ Community Marketplace Feed | Moonoh";',
    'pageTitle = "NYC & NJ Local Community Marketplace Feed | Moonoh";'
)

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(exp_mjs)

print("✅ Updated explore.mjs SSR titles to ensure 50-60 characters")
