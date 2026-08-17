import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update results-sort-bar markup: Remove clear filters button and right-align Sort
new_bar_markup = '''      <!-- 4. Result Count & Right-Aligned Plain Text Sort Row -->
      <div class="results-sort-bar" style="display: flex; align-items: center; justify-content: space-between; margin: 16px 0 20px 0; width: 100%; box-sizing: border-box;">
        <div id="explore-results-label" style="font-size: 13.5px; font-weight: 600; color: #374151; white-space: nowrap;">
        </div>
        <div class="explore-sort-wrap" style="display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; margin-left: auto;">
          <span style="font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; user-select: none;">Sort:</span>
          <div style="position: relative; display: inline-flex; align-items: center;">
            <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; -moz-appearance: none; background: transparent; border: none; outline: none; box-shadow: none; font-size: 13px; font-weight: 400; color: #4B5563; font-family: inherit; line-height: 1.2; padding: 0 12px 0 2px; margin: 0; cursor: pointer; -webkit-tap-highlight-color: transparent; width: auto;">
              <option value="newest">Newest</option>
              <option value="relevance">Relevance</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
            </select>
            <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
      </div>'''

pattern = r'<div class="results-sort-bar"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>'
html = re.sub(pattern, new_bar_markup, html, count=1)

# 2. In JS, guard any clearAllBtn references safely
html = html.replace(
    'const clearAllBtn = document.getElementById(\'btn-clear-all-filters\');',
    '// Clear filters button removed'
)
html = html.replace(
    'if (clearAllBtn) {\n        clearAllBtn.style.display = hasActiveFilters ? \'inline-flex\' : \'none\';\n      }',
    '// Clear filters display logic removed'
)
html = html.replace(
    'const clearAllBtnEl = document.getElementById(\'btn-clear-all-filters\');',
    '// Clear filters button removed'
)
html = html.replace(
    'if (clearAllBtnEl) {\n      clearAllBtnEl.addEventListener(\'click\', clearAllFilters);\n    }',
    '// Clear filters listener removed'
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Removed Clear Filters button and right-aligned Sort in explore.html")
