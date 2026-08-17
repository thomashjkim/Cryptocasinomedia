import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HTML Markup for explore-sort-wrap
old_sort_markup = '''          <!-- 100% Plain Text Sort Selector (No button border, no pill box) -->
          <div class="explore-sort-wrap" style="display: inline-flex; align-items: center; gap: 4px; font-size: 13px; color: #4B5563;">
            <label for="explore-sort-select" style="font-weight: 500; cursor: pointer;">Sort:</label>
            <div style="position: relative; display: inline-flex; align-items: center;">
              <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; -moz-appearance: none; background: transparent; border: none; padding: 0 16px 0 2px; font-size: 13.5px; font-weight: 700; color: #111827; cursor: pointer; outline: none; box-shadow: none; font-family: inherit; line-height: 1;">
                <option value="relevance">Relevance</option>
                <option value="newest">Newest</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
              </select>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 0; pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>'''

new_sort_markup = '''          <!-- 100% Seamless Plain Text Sort Selector (Exact same font size, weight 400, color & perfect vertical alignment) -->
          <div class="explore-sort-wrap" style="display: inline-flex; align-items: center; gap: 4px; font-size: 13.5px; font-weight: 400; color: #4B5563; line-height: 1;">
            <label for="explore-sort-select" style="font-size: 13.5px; font-weight: 400; color: #4B5563; margin: 0; padding: 0; line-height: 1; cursor: pointer; white-space: nowrap;">Sort:</label>
            <div style="position: relative; display: inline-flex; align-items: center;">
              <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; -moz-appearance: none; background: transparent; border: none; padding: 0 14px 0 2px; margin: 0; font-size: 13.5px; font-weight: 400; color: #4B5563; cursor: pointer; outline: none; box-shadow: none; font-family: inherit; line-height: 1; vertical-align: baseline;">
                <option value="relevance">Relevance</option>
                <option value="newest">Newest</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
              </select>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 0; pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>'''

if old_sort_markup in html:
    html = html.replace(old_sort_markup, new_sort_markup)
    print("✅ Replaced sort markup in explore.html")
else:
    # Use regex replacement if whitespace differed
    pattern = r'<div class="explore-sort-wrap"[\s\S]*?<\/div>\s*<\/div>'
    html = re.sub(pattern, new_sort_markup, html, count=1)
    print("✅ Replaced sort markup via regex in explore.html")

# 2. Add complete CSS rules to remove focus boxes / outlines and ensure perfect alignment
css_rules = '''
    /* Sort: Perfect Typography, Alignment & Zero Focus Outline */
    .explore-sort-wrap {
      display: inline-flex !important;
      align-items: center !important;
      gap: 4px !important;
      font-size: 13.5px !important;
      font-weight: 400 !important;
      color: #4B5563 !important;
      line-height: 1 !important;
    }
    .explore-sort-wrap label {
      font-size: 13.5px !important;
      font-weight: 400 !important;
      color: #4B5563 !important;
      margin: 0 !important;
      padding: 0 !important;
      line-height: 1 !important;
      cursor: pointer !important;
    }
    #explore-sort-select {
      appearance: none !important;
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      outline: none !important;
      font-size: 13.5px !important;
      font-weight: 400 !important;
      color: #4B5563 !important;
      font-family: inherit !important;
      line-height: 1 !important;
      padding: 0 14px 0 2px !important;
      margin: 0 !important;
      cursor: pointer !important;
      -webkit-tap-highlight-color: transparent !important;
    }
    #explore-sort-select:focus,
    #explore-sort-select:active,
    #explore-sort-select:focus-visible,
    #explore-sort-select:hover {
      outline: none !important;
      border: none !important;
      box-shadow: none !important;
      background: transparent !important;
      color: #111827 !important;
    }
    .explore-sort-wrap:hover label,
    .explore-sort-wrap:hover svg {
      color: #111827 !important;
      stroke: #111827 !important;
    }
'''

# Insert css_rules before </style>
html = html.replace('</style>', css_rules + '\n  </style>')

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Applied Sort CSS and typography updates to explore.html")
