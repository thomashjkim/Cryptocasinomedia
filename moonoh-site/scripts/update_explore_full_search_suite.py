import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Layout Markup in explore.html
controls_markup = '''      <!-- Controls Bar (Desktop 1 row, Mobile 2 rows) -->
      <div class="explore-controls-container" id="explore-controls-container" style="margin: 0 0 16px 0; width: 100%; box-sizing: border-box;">
        <div class="explore-controls-row-top" style="display: flex; align-items: center; gap: 12px; width: 100%; flex-wrap: wrap;">
          <!-- Search Input -->
          <div class="explore-search-inner" style="position: relative; display: flex; align-items: center; flex: 1; min-width: 220px; box-sizing: border-box;">
            <svg class="explore-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; left: 14px; pointer-events: none;">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" id="explore-search-input" class="explore-search-input" placeholder="Search in Moonoh" aria-label="Search listings in current tab" style="width: 100%; height: 46px; padding: 0 42px 0 42px; border: 1.5px solid #E5E7EB; border-radius: 9999px; font-size: 14px; color: #111827; background: #FFFFFF; outline: none; transition: border-color 0.2s, box-shadow 0.2s; box-sizing: border-box;" />
            <button id="explore-search-clear" class="explore-search-clear" aria-label="Clear search keyword" style="display: none; position: absolute; right: 8px; width: 30px; height: 30px; border: none; background: #E5E7EB; color: #4B5563; cursor: pointer; border-radius: 50%; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; padding: 0; line-height: 1;">
              ✕
            </button>
          </div>

          <!-- Controls Sub-Row (Results count, Sort, Clear Filters) -->
          <div class="explore-controls-subrow" style="display: flex; align-items: center; gap: 10px; justify-content: space-between; flex-wrap: nowrap;">
            <div id="explore-results-label" style="font-size: 13px; font-weight: 600; color: #374151; white-space: nowrap;">
            </div>
            <div class="explore-sort-wrap" style="display: flex; align-items: center; gap: 6px;">
              <label for="explore-sort-select" style="font-size: 12px; font-weight: 600; color: #6B7280; white-space: nowrap;">Sort:</label>
              <div style="position: relative; display: inline-flex; align-items: center;">
                <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; background: #FFFFFF; border: 1.5px solid #E5E7EB; border-radius: 9999px; padding: 6px 28px 6px 12px; font-size: 13px; font-weight: 600; color: #1F2937; cursor: pointer; min-height: 44px; min-width: 115px; outline: none; box-sizing: border-box;">
                  <option value="relevance">Relevance</option>
                  <option value="newest">Newest</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                </select>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 10px; pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
              </div>
            </div>
            <!-- Clear Filters Button -->
            <button id="btn-clear-all-filters" class="btn-clear-all-filters" aria-label="Clear all active filters" style="display: none; align-items: center; justify-content: center; height: 44px; padding: 0 14px; background: #F3F4F6; color: #374151; font-size: 12px; font-weight: 700; border: 1px solid #E5E7EB; border-radius: 9999px; cursor: pointer; white-space: nowrap; transition: background 0.2s;">
              Clear Filters
            </button>
          </div>
        </div>
      </div>'''

# Replace old explore-search-wrap and explore-results-sort-bar
html = re.sub(r'<!-- 3\. Search Bar Container -->[\s\S]*?<!-- \/explore-search-wrap -->|<!-- 3\. Search Bar Container -->[\s\S]*?</div>\s*</div>\s*</div>', '', html)
html = re.sub(r'<!-- 5\. Results Count & Sort Bar -->[\s\S]*?</div>\s*</div>\s*</div>', '', html)
html = re.sub(r'<div class="explore-search-wrap"[\s\S]*?<\/div>\s*<\/div>', '', html)
html = re.sub(r'<div class="explore-results-sort-bar"[\s\S]*?<\/div>\s*<\/div>', '', html)
html = re.sub(r'<div class="explore-controls-container"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>', '', html)

# Insert clean controls_markup right above filter-container
html = re.sub(r'(\s*<div class="filter-container" id="filter-container">)', r'\n\n' + controls_markup + r'\1', html, count=1)

# Add Responsive CSS styles
responsive_css = '''
    /* Explore Controls Bar Styling */
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
    .btn-clear-all-filters:hover {
      background: #E5E7EB !important;
    }

    @media (max-width: 475px) {
      .explore-controls-row-top {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 8px !important;
      }
      .explore-search-inner {
        width: 100% !important;
        min-width: 100% !important;
      }
      .explore-controls-subrow {
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
      }
      #explore-sort-select {
        min-width: 110px !important;
        font-size: 12px !important;
      }
      .btn-clear-all-filters {
        padding: 0 10px !important;
        font-size: 11px !important;
        height: 44px !important;
      }
    }
'''

if '/* Explore Controls Bar Styling */' not in html:
    html = html.replace('</style>', responsive_css + '\n  </style>')

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ Saved explore.html markup and responsive CSS")
