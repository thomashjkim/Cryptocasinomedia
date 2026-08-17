import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean results-sort-bar markup
bar_pattern = r'<!-- 4\. Result Count[\s\S]*?(?=<div class="item-grid" id="moonoh-item-grid">)'
clean_bar = '''<!-- 4. Result Count & Right-Aligned Plain Text Sort Row -->
      <div class="results-sort-bar" style="display: flex; align-items: center; justify-content: space-between; margin: 16px 0 20px 0; width: 100%; box-sizing: border-box;">
        <div id="explore-results-label" style="font-size: 13.5px; font-weight: 600; color: #374151; white-space: nowrap;">
        </div>
        <div class="explore-sort-wrap" style="display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; margin-left: auto;">
          <span style="font-size: 13px; font-weight: 400; color: #4B5563; line-height: 1.2; user-select: none;">Sort:</span>
          <div style="position: relative; display: inline-flex; align-items: center;">
            <select id="explore-sort-select" aria-label="Sort products" onchange="if(typeof updateSortWidth==='function')updateSortWidth();" style="appearance: none; -webkit-appearance: none; -moz-appearance: none; background: transparent; border: none; outline: none; box-shadow: none; font-size: 13px; font-weight: 400; color: #4B5563; font-family: inherit; line-height: 1.2; padding: 0 12px 0 2px; margin: 0; cursor: pointer; -webkit-tap-highlight-color: transparent;">
              <option value="newest">Newest</option>
              <option value="relevance">Relevance</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
            </select>
            <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
      </div>
'''

html = re.sub(bar_pattern, clean_bar + '\n      ', html, count=1)

# 2. Add updateSortWidth function and call it in applyFilters & initAll
update_width_func = '''
    function updateSortWidth() {
      const select = document.getElementById('explore-sort-select');
      if (!select) return;
      const selectedOption = select.options[select.selectedIndex];
      const txt = selectedOption ? selectedOption.text : '';
      const temp = document.createElement('span');
      temp.style.visibility = 'hidden';
      temp.style.position = 'absolute';
      temp.style.fontSize = '13px';
      temp.style.fontWeight = '400';
      temp.style.fontFamily = getComputedStyle(select).fontFamily || 'sans-serif';
      temp.textContent = txt;
      document.body.appendChild(temp);
      const textWidth = Math.ceil(temp.getBoundingClientRect().width);
      document.body.removeChild(temp);
      select.style.width = (textWidth + 14) + 'px';
    }
'''

if 'function updateSortWidth' not in html:
    html = html.replace('function updateSearchUI() {', update_width_func + '\n    function updateSearchUI() {')

# Hook updateSortWidth inside updateSearchUI and sort change listener
html = html.replace('sortSelect.value = currentSortOption;', 'sortSelect.value = currentSortOption;\n        updateSortWidth();')

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Applied tight dynamic width and clean right-aligned sort bar")
