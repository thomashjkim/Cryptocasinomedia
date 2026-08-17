import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Restore exact Kim'C Market green banner in explore.html
kimc_banner = '''      <!-- Food Rescue Informational Banner (Compact Category Pill Bar Size, Kim'C Market Green) -->
      <div id="food-rescue-banner" style="display:none; background:#E6F5F0; border:1px solid #99D6C4; border-radius:9999px; padding:4px 16px; margin-bottom:24px; min-height:42px; box-sizing:border-box; align-items:center; justify-content:space-between; gap:12px;">
        <div style="display:flex; align-items:center; gap:8px; overflow:hidden; white-space:nowrap;">
          <span style="background:#006853; color:#fff; font-weight:700; font-size:12px; padding:3px 10px; border-radius:9999px; display:inline-flex; align-items:center; gap:4px; flex-shrink:0;">🌱 Kim'C Market</span>
          <span style="font-size:13px; color:#006853; font-weight:600; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;">Peak quality Korean foods near sell-by date at special discounts</span>
        </div>
        <a href="https://kimcmarket.com/blogs/korean-food-blog/understanding-sell-by-dates" target="_blank" rel="noopener noreferrer" style="display:inline-flex; align-items:center; gap:4px; background:#006853; color:#ffffff; font-weight:700; font-size:12px; padding:5px 14px; border-radius:9999px; text-decoration:none; white-space:nowrap; flex-shrink:0;">
          Sell-By Guide ↗
        </a>
      </div>'''

banner_pattern = r'<div id="food-rescue-banner"[\s\S]*?<\/div>\s*<\/div>'
html = re.sub(banner_pattern, kimc_banner, html, count=1)

# 2. Perfect Zero-Gap Sort Selector Overlay
new_sort_bar = '''<!-- 4. Result Count & Right-Aligned Pure Text Sort Row -->
      <div class="results-sort-bar" style="display: flex; align-items: center; justify-content: space-between; margin: 16px 0 20px 0; width: 100%; box-sizing: border-box;">
        <div id="explore-results-label" style="font-size: 13.5px; font-weight: 600; color: #374151; white-space: nowrap;">
        </div>
        <div class="explore-sort-wrap" style="display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; margin-left: auto;">
          <span style="font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; user-select: none;">Sort:</span>
          <div class="sort-overlay-wrap" style="position: relative; display: inline-flex; align-items: center; cursor: pointer; line-height: 1.2;">
            <span id="sort-current-text" style="font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; white-space: nowrap;">Newest</span>
            <svg class="sort-caret-icon" width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-left: 4px; pointer-events: none; display: inline-block; vertical-align: middle;"><polyline points="6 9 12 15 18 9"/></svg>
            <select id="explore-sort-select" aria-label="Sort products" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; -webkit-appearance: none; appearance: none; margin: 0; padding: 0; font-size: 13px; border: none; outline: none;">
              <option value="newest">Newest</option>
              <option value="relevance">Relevance</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
            </select>
          </div>
        </div>
      </div>'''

bar_pattern = r'<!-- 4\. Result Count[\s\S]*?(?=<div class="item-grid" id="moonoh-item-grid">)'
html = re.sub(bar_pattern, new_sort_bar + '\n      ', html, count=1)

# 3. Update JS in explore.html to keep #sort-current-text in sync
sync_sort_text = '''
    function updateSortText() {
      const select = document.getElementById('explore-sort-select');
      const textEl = document.getElementById('sort-current-text');
      if (select && textEl) {
        const selectedOption = select.options[select.selectedIndex];
        textEl.textContent = selectedOption ? selectedOption.text : 'Newest';
      }
    }
'''

# Replace updateSortWidth with updateSortText
html = re.sub(r'function updateSortWidth\(\)\s*\{[\s\S]*?\}', sync_sort_text, html)

# Hook updateSortText on select change and in applyFilters / initAll
html = html.replace('updateSortWidth();', 'updateSortText();')
html = html.replace('updateSortWidth()', 'updateSortText()')

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Restored original Kim'C Market green banner and implemented zero-gap Sort overlay")
