import re

print("=" * 80)
print("📱 INCREASING PHOTO & PRICE SPACING BY 4PX ON MOBILE VIEW (<=475PX)")
print("=" * 80)

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

target_exp = '''    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-img-wrap {
        margin-bottom: 0px !important;
      }'''

replacement_exp = '''    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-img-wrap {
        margin-bottom: 4px !important;
      }'''

if target_exp in exp_html:
    exp_html = exp_html.replace(target_exp, replacement_exp)
    with open('explore.html', 'w', encoding='utf-8') as f:
        f.write(exp_html)
    print("✅ Updated explore.html: Set mobile photo-to-price margin-bottom to 4px")
else:
    print("⚠️ Target block not found in explore.html, applying regex")
    exp_html = re.sub(
        r'(@media\s*\(max-width:\s*479px\)\s*\{[\s\S]*?\.item-card-img-wrap\s*\{\s*margin-bottom:\s*)0px(\s*!important;)',
        r'\g<1>4px\g<2>',
        exp_html
    )
    with open('explore.html', 'w', encoding='utf-8') as f:
        f.write(exp_html)
    print("✅ Applied regex replacement to explore.html")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

target_idx = '''    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-img-wrap {
        margin-bottom: 0px !important;
      }'''

replacement_idx = '''    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-img-wrap {
        margin-bottom: 4px !important;
      }'''

if target_idx in idx_html:
    idx_html = idx_html.replace(target_idx, replacement_idx)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html)
    print("✅ Updated index.html: Set mobile photo-to-price margin-bottom to 4px")
else:
    print("⚠️ Target block not found in index.html, applying regex")
    idx_html = re.sub(
        r'(@media\s*\(max-width:\s*479px\)\s*\{[\s\S]*?\.item-card-img-wrap\s*\{\s*margin-bottom:\s*)0px(\s*!important;)',
        r'\g<1>4px\g<2>',
        idx_html
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html)
    print("✅ Applied regex replacement to index.html")
