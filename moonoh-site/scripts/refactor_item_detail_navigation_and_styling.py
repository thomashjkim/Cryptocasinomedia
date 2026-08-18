import re

print("=" * 80)
print("🛠️ STEP 6: REFACTORING ITEM DETAIL NAVIGATION, RESPONSIVE CTA & BREADCRUMBS")
print("=" * 80)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update CTA button CSS for mobile
responsive_btn_css = '''
    .cta-btn-main {
      width: 100%;
      box-sizing: border-box;
      border: none;
      padding: 14px 16px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 15px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      text-decoration: none;
      white-space: nowrap;
      transition: opacity 0.2s, transform 0.1s;
    }
    .cta-btn-main:hover { opacity: 0.92; }
    .cta-btn-main:active { transform: scale(0.98); }
    @media (max-width: 480px) {
      .cta-btn-main {
        font-size: 13.5px !important;
        padding: 12px 10px !important;
        white-space: nowrap !important;
        letter-spacing: -0.2px !important;
      }
      .cta-btn-main span {
        white-space: nowrap !important;
      }
    }
'''

if '.cta-btn-main' not in code:
    code = code.replace('</style>', f'{responsive_btn_css}\n</style>')

# 2. Fix the CTA button markup in item-detail.mjs
code = re.sub(
    r'<a href="\$\{externalUrl\}" target="_blank" rel="noopener noreferrer" onclick="[^"]*"  style="width:100%;[^"]*"',
    r'<a href="${externalUrl}" target="_blank" rel="noopener noreferrer" onclick="if(typeof gtag===\'function\')gtag(\'event\',\'click_external_source\',{item_id:\'${productNo}\',item_name:${JSON.stringify(title)},source:\'${externalSource}\',store_name:\'${sourceDisplayName}\',destination_url:\'${externalUrl}\'});" class="cta-btn-main" style="background:${btnBgColor}; color:${btnTextColor || \'#FFFFFF\'};"',
    code
)

# 3. Ensure priceStr formatting never outputs "Check price at retailer" for local shops
code = code.replace(
    'priceStr = price > 0 ? (price % 1 !== 0 ? `$${price.toFixed(2)}` : `$${Math.round(price).toLocaleString()}`) : "Check price at retailer";',
    'priceStr = price > 0 ? (price % 1 !== 0 ? `$${price.toFixed(2)}` : `$${Math.round(price).toLocaleString()}`) : (price === 0 ? "Free" : `$${price}`);'
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Saved netlify/functions/item-detail.mjs with responsive CTA buttons and clean pricing")
