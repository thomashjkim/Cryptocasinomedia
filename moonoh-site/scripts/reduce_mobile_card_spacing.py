import re

print("=" * 80)
print("📱 REDUCING MOBILE CARD IMAGE-TO-PRICE SPACING BY -8PX")
print("=" * 80)

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp = f.read()

# Replace general card spacing
old_general_css = """.item-card-img-wrap {
      width: 100% !important;
      max-width: 100% !important;
      height: 0 !important;
      padding-bottom: 100% !important;
      position: relative !important;
      border-radius: 12px !important;
      overflow: hidden !important;
      background-color: #F3F4F6 !important;
      margin-bottom: 8px !important;
      display: block !important;
    }"""

new_general_css = """.item-card-img-wrap {
      width: 100% !important;
      max-width: 100% !important;
      height: 0 !important;
      padding-bottom: 100% !important;
      position: relative !important;
      border-radius: 12px !important;
      overflow: hidden !important;
      background-color: #F3F4F6 !important;
      margin-bottom: 2px !important;
      display: block !important;
    }"""

if old_general_css in exp:
    exp = exp.replace(old_general_css, new_general_css)

# Replace mobile card spacing in explore.html
old_mobile_css = """    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-image,
      .item-card-img {
        margin-bottom: 6px !important;
      }
      .item-card-content,
      .item-card-info {
        padding-top: 4px !important;
        margin-top: 4px !important;
      }
      .item-card-price {
        font-size: 20px !important;
        font-weight: 800 !important;
      }
    }"""

new_mobile_css = """    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-img-wrap {
        margin-bottom: 0px !important;
      }
      .item-card-image,
      .item-card-img {
        margin-bottom: 0px !important;
      }
      .item-card-content,
      .item-card-info {
        padding: 0 2px 0 2px !important;
        margin-top: 0px !important;
      }
      .item-card-price {
        font-size: 18px !important;
        font-weight: 800 !important;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
      }
    }"""

if old_mobile_css in exp:
    exp = exp.replace(old_mobile_css, new_mobile_css)
else:
    # Use regex replacement
    exp = re.sub(
        r'@media \(max-width: 479px\) \{[\s\S]*?\.item-card-price \{[\s\S]*?\}[\s\S]*?\}',
        new_mobile_css.strip(),
        exp
    )

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp)
print("✅ Updated explore.html mobile card spacing")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

if old_general_css in idx:
    idx = idx.replace(old_general_css, new_general_css)

old_idx_mobile = """    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
    }"""

new_idx_mobile = """    @media (max-width: 479px) {
      .item-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
      .item-card-img-wrap {
        margin-bottom: 0px !important;
      }
      .item-card-image,
      .item-card-img {
        margin-bottom: 0px !important;
      }
      .item-card-content,
      .item-card-info {
        padding: 0 2px 0 2px !important;
        margin-top: 0px !important;
      }
      .item-card-price {
        font-size: 18px !important;
        font-weight: 800 !important;
        margin-top: 0px !important;
        margin-bottom: 2px !important;
      }
    }"""

if old_idx_mobile in idx:
    idx = idx.replace(old_idx_mobile, new_idx_mobile)
else:
    idx = re.sub(
        r'@media \(max-width: 479px\) \{\s*\.item-grid \{\s*grid-template-columns: repeat\(2, 1fr\);\s*gap: 12px;\s*\}\s*\}',
        new_idx_mobile.strip(),
        idx
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("✅ Updated index.html mobile card spacing")
