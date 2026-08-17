import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

correct_markup = '''      <!-- Controls Bar (Desktop 1 row, Mobile 2 rows) -->
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
      </div>

      <!-- Food Rescue Informational Banner -->
      <div id="food-rescue-banner" style="display: none; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 12px 16px; margin-bottom: 20px; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="font-size: 20px;">🥗</span>
          <div>
            <strong style="color: #1E40AF; font-size: 14px;">Fight Food Waste with Local Partner Stores</strong>
            <p style="margin: 0; font-size: 13px; color: #3B82F6;">Near-expiration artisanal groceries up to 50% off. Sourced directly from Kim'C Market.</p>
          </div>
        </div>
      </div>

      <!-- Standard Category Filters (Moonoh & Marketplaces) -->
      <div class="filter-container" id="filter-container">
        <button class="filter-pill active">All</button>
        <button class="filter-pill">Free</button>
        <button class="filter-pill">Furniture</button>
        <button class="filter-pill">Electronics &amp; Appliances</button>
        <button class="filter-pill">Men's fashion</button>
        <button class="filter-pill">Women's fashion</button>
        <button class="filter-pill">Shoes</button>
        <button class="filter-pill">Baby &amp; kids</button>
        
        <!-- Folded Extra Categories -->
        <button class="filter-pill filter-pill-extra">Food &amp; Groceries</button>
        <button class="filter-pill filter-pill-extra">Home, garden &amp; DIY</button>
        <button class="filter-pill filter-pill-extra">Jewelry &amp; watches</button>
        <button class="filter-pill filter-pill-extra">Luggages &amp; bags</button>
        <button class="filter-pill filter-pill-extra">Health &amp; beauty</button>
        <button class="filter-pill filter-pill-extra">Antiques &amp; collections</button>
        <button class="filter-pill filter-pill-extra">Arts, books, music, movies &amp; tickets</button>
        <button class="filter-pill filter-pill-extra">Pet supplies</button>
        <button class="filter-pill filter-pill-extra">Sublets</button>
        <button class="filter-pill filter-pill-extra">Sports &amp; leisure</button>
        <button class="filter-pill filter-pill-extra">Toys &amp; Games</button>
        <button class="filter-pill filter-pill-extra">Other</button>

        <button class="filter-pill-more" id="filter-pill-more" aria-expanded="false" aria-label="Show more categories">
          More <svg class="filter-more-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
      </div>

      <!-- Local Shops 5 Category Filters -->
      <div class="filter-container" id="local-filter-container" style="display: none;">
        <button class="filter-pill active" data-local-cat="All">All</button>
        <button class="filter-pill" data-local-cat="Vintage & Fashion">Vintage &amp; Fashion</button>
        <button class="filter-pill" data-local-cat="Home & Objects">Home &amp; Objects</button>
        <button class="filter-pill" data-local-cat="Coffee & Pantry">Coffee &amp; Pantry</button>
        <button class="filter-pill" data-local-cat="Gifts & Culture">Gifts &amp; Culture</button>
      </div>
'''

# Find the spot between `</div>\s*</div>\s*<div class="item-grid"`
html = re.sub(r'(<\/div>\s*<\/div>\s*)(<div class="item-grid" id="moonoh-item-grid">)', r'\1\n' + correct_markup + r'\n      \2', html, count=1)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Correctly structured explore.html controls and category filters")
