import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HTML Markup in explore.html
# Search field markup & Sort bar markup
search_and_sort_markup = '''      <!-- 3. Search Bar Container -->
      <div class="explore-search-wrap" id="explore-search-wrap" style="margin: 0 0 16px 0; width: 100%; box-sizing: border-box;">
        <div class="explore-search-inner" style="position: relative; display: flex; align-items: center; width: 100%;">
          <svg class="explore-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; left: 16px; pointer-events: none;">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" id="explore-search-input" class="explore-search-input" placeholder="Search Moonoh listings" aria-label="Search listings in current tab" style="width: 100%; height: 46px; padding: 0 42px 0 46px; border: 1.5px solid #E5E7EB; border-radius: 9999px; font-size: 15px; color: #111827; background: #FFFFFF; outline: none; transition: border-color 0.2s, box-shadow 0.2s; box-sizing: border-box;" />
          <button id="explore-search-clear" class="explore-search-clear" aria-label="Clear search keyword" style="display: none; position: absolute; right: 12px; width: 28px; height: 28px; border: none; background: #E5E7EB; color: #4B5563; cursor: pointer; border-radius: 50%; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; padding: 0; line-height: 1;">
            ✕
          </button>
        </div>
      </div>'''

results_and_sort_markup = '''      <!-- 5. Results Count & Sort Bar -->
      <div class="explore-results-sort-bar" id="explore-results-sort-bar" style="display: flex; align-items: center; justify-content: space-between; margin: 0 0 16px 0; gap: 12px; flex-wrap: wrap;">
        <div id="explore-results-label" style="font-size: 14px; font-weight: 600; color: #374151;">
        </div>
        <div class="explore-sort-wrap" style="display: flex; align-items: center; gap: 8px; margin-left: auto;">
          <label for="explore-sort-select" style="font-size: 13px; font-weight: 600; color: #6B7280;">Sort:</label>
          <div style="position: relative; display: inline-flex; align-items: center;">
            <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; background: #FFFFFF; border: 1.5px solid #E5E7EB; border-radius: 9999px; padding: 8px 32px 8px 14px; font-size: 13px; font-weight: 600; color: #1F2937; cursor: pointer; min-height: 44px; min-width: 145px; outline: none; box-sizing: border-box;">
              <option value="recommended">Recommended</option>
              <option value="newest">Newest</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
              <option value="name-asc">Name: A–Z</option>
            </select>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 12px; pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
      </div>'''

# Place search bar right after source-segment-wrap's parent (explore-controls-wrap)
if 'id="explore-search-wrap"' not in html:
    pattern_after_tabs = r'(</div>\s*<!-- \/explore-controls-wrap -->|</div>\s*<div class="filter-container" id="filter-container">)'
    html = re.sub(r'(\s*<div class="filter-container" id="filter-container">)', r'\n\n' + search_and_sort_markup + r'\1', html, count=1)
    print("✅ Inserted explore-search-wrap before filter-container")

# Place results and sort bar right before #moonoh-item-grid
if 'id="explore-results-sort-bar"' not in html:
    html = html.replace('<div class="item-grid" id="moonoh-item-grid">', results_and_sort_markup + '\n\n      <div class="item-grid" id="moonoh-item-grid">')
    print("✅ Inserted explore-results-sort-bar before moonoh-item-grid")

# CSS Focus style for search input
focus_style = '''
    .explore-search-input:focus {
      border-color: #4F46E5 !important;
      box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }
    .explore-search-input:focus-visible {
      outline: 2px solid #4F46E5 !important;
    }
    #explore-sort-select:focus {
      border-color: #4F46E5 !important;
      box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }
'''
if '.explore-search-input:focus' not in html:
    html = html.replace('</style>', focus_style + '\n  </style>')
    print("✅ Added search and sort CSS styles")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved explore.html markup")
