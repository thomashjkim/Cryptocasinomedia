import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the Search Bar completely
search_bar_pattern = r'<!-- 2\. Scoped Search Bar[\s\S]*?<\/div>\s*<\/div>'
html = re.sub(search_bar_pattern, '', html)

# 2. Perfect Sort inline styling
old_sort_pattern = r'<div class="explore-sort-wrap"[\s\S]*?<\/div>\s*<\/div>'
new_sort_html = '''<div class="explore-sort-wrap" style="display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2;">
            <span style="font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; user-select: none;">Sort:</span>
            <div style="position: relative; display: inline-flex; align-items: center;">
              <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; -moz-appearance: none; background: transparent; border: none; outline: none; box-shadow: none; font-size: 13px; font-weight: 400; color: #4B5563; font-family: inherit; line-height: 1.2; padding: 0 13px 0 0; margin: 0; cursor: pointer; -webkit-tap-highlight-color: transparent; width: auto;">
                <option value="newest">Newest</option>
                <option value="relevance">Relevance</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
              </select>
              <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>'''

html = re.sub(old_sort_pattern, new_sort_html, html, count=1)

# 3. Clean CSS for explore-sort-wrap & explore-sort-select
sort_css_clean = '''
    /* Sort: Perfect Baseline & Zero Outline */
    .explore-sort-wrap {
      display: inline-flex !important;
      align-items: center !important;
      gap: 4px !important;
      font-size: 13px !important;
      font-weight: 400 !important;
      color: #4B5563 !important;
      line-height: 1.2 !important;
      vertical-align: middle !important;
    }
    .explore-sort-wrap span {
      font-size: 13px !important;
      font-weight: 400 !important;
      color: #4B5563 !important;
      line-height: 1.2 !important;
    }
    #explore-sort-select {
      appearance: none !important;
      -webkit-appearance: none !important;
      -moz-appearance: none !important;
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      outline: none !important;
      font-size: 13px !important;
      font-weight: 400 !important;
      color: #4B5563 !important;
      font-family: inherit !important;
      line-height: 1.2 !important;
      padding: 0 13px 0 0 !important;
      margin: 0 !important;
      cursor: pointer !important;
      width: auto !important;
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
'''

# Replace old sort CSS in <style>
html = re.sub(r'\/\* Sort: Perfect Typography[\s\S]*?(?=<\/style>)', sort_css_clean + '\n  ', html, count=1)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Removed search bar and perfected Sort inline alignment in explore.html")
