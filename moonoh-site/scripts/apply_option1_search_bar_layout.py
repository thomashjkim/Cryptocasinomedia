import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. New Markup for Option 1
option1_markup = '''      <!-- 1. Top Integrated Row: Location, Compact Search & 4-Tab Switcher -->
      <div class="top-nav-search-bar" style="display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; width: 100%; box-sizing: border-box;">
        <!-- Location Select (Left) -->
        <div class="location-select-wrap" style="flex-shrink: 0;">
          <select id="location-select" aria-label="Select location">
            <option value="">New York area (All)</option>
            <optgroup label="NYC Boroughs">
              <option value="Manhattan">Manhattan, NY</option>
              <option value="Queens">Queens, NY (All)</option>
              <option value="Flushing">&nbsp;&nbsp;• Flushing</option>
              <option value="Bayside">&nbsp;&nbsp;• Bayside</option>
              <option value="Astoria">&nbsp;&nbsp;• Astoria</option>
              <option value="Brooklyn">Brooklyn, NY</option>
              <option value="Bronx">The Bronx, NY</option>
              <option value="Staten Island">Staten Island, NY</option>
            </optgroup>
            <optgroup label="New Jersey">
              <option value="Fort Lee">Fort Lee, NJ</option>
              <option value="Bergen">Bergen County, NJ</option>
              <option value="Hudson">Hudson County, NJ</option>
            </optgroup>
          </select>
          <svg class="location-select-caret" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </div>

        <!-- Compact Search Input (Center - Max Width 380px on Desktop) -->
        <div class="explore-search-wrap" style="flex: 1; max-width: 380px; min-width: 220px; box-sizing: border-box;">
          <div class="explore-search-inner" style="position: relative; display: flex; align-items: center; width: 100%;">
            <svg class="explore-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; left: 14px; pointer-events: none;">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" id="explore-search-input" class="explore-search-input" placeholder="Search in Moonoh" aria-label="Search listings in current tab" style="width: 100%; height: 42px; padding: 0 38px 0 38px; border: 1.5px solid #E5E7EB; border-radius: 9999px; font-size: 13.5px; color: #111827; background: #FFFFFF; outline: none; transition: border-color 0.2s, box-shadow 0.2s; box-sizing: border-box;" />
            <button id="explore-search-clear" class="explore-search-clear" aria-label="Clear search keyword" style="display: none; position: absolute; right: 8px; width: 26px; height: 26px; border: none; background: #E5E7EB; color: #4B5563; cursor: pointer; border-radius: 50%; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; padding: 0; line-height: 1;">
              ✕
            </button>
          </div>
        </div>

        <!-- Source Segment Switcher (Right) -->
        <div class="source-segment-wrap" id="source-segment-wrap" style="flex-shrink: 0; margin-left: auto;">
          <button class="source-tab-btn active" id="tab-source-moonoh" data-source="moonoh">Moonoh</button>
          <button class="source-tab-btn tab-foodrescue" id="tab-source-foodrescue" data-source="foodrescue">Food Rescue</button>
          <button class="source-tab-btn" id="tab-source-localshops" data-source="localshops">Local</button>
          <button class="source-tab-btn" id="tab-source-marketplaces" data-source="marketplaces">Marketplaces</button>
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

      <!-- Results Count, Sort & Clear Filters Sub-Row -->
      <div class="results-sort-bar" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 12px 0 20px 0; width: 100%; box-sizing: border-box;">
        <div id="explore-results-label" style="font-size: 13.5px; font-weight: 600; color: #374151; white-space: nowrap;">
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          <div class="explore-sort-wrap" style="display: flex; align-items: center; gap: 6px;">
            <label for="explore-sort-select" style="font-size: 12px; font-weight: 600; color: #6B7280; white-space: nowrap;">Sort:</label>
            <div style="position: relative; display: inline-flex; align-items: center;">
              <select id="explore-sort-select" aria-label="Sort products" style="appearance: none; -webkit-appearance: none; background: #FFFFFF; border: 1.5px solid #E5E7EB; border-radius: 9999px; padding: 6px 28px 6px 12px; font-size: 13px; font-weight: 600; color: #1F2937; cursor: pointer; min-height: 40px; min-width: 115px; outline: none; box-sizing: border-box;">
                <option value="relevance">Relevance</option>
                <option value="newest">Newest</option>
                <option value="price-asc">Price: Low to High</option>
                <option value="price-desc">Price: High to Low</option>
              </select>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#4B5563" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; right: 10px; pointer-events: none;"><polyline points="6 9 12 15 18 9"/></svg>
            </div>
          </div>
          <!-- Clear Filters Button -->
          <button id="btn-clear-all-filters" class="btn-clear-all-filters" aria-label="Clear all active filters" style="display: none; align-items: center; justify-content: center; height: 40px; padding: 0 14px; background: #F3F4F6; color: #374151; font-size: 12px; font-weight: 700; border: 1px solid #E5E7EB; border-radius: 9999px; cursor: pointer; white-space: nowrap; transition: background 0.2s;">
            Clear Filters
          </button>
        </div>
      </div>
'''

# Replace from location-bar down to right before moonoh-item-grid
pattern = r'<!-- Location Dropdown & Source Toggle Row -->[\s\S]*?(?=<div class="item-grid" id="moonoh-item-grid">)'
html = re.sub(pattern, option1_markup + '\n      ', html, count=1)

# 2. Update CSS for Option 1
option1_css = '''
    /* Option 1: Top Navigation, Search & Controls Responsive Styling */
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

    @media (max-width: 860px) {
      .top-nav-search-bar {
        gap: 12px !important;
      }
      .top-nav-search-bar .explore-search-wrap {
        width: 100% !important;
        max-width: 100% !important;
        order: 3 !important; /* Move search below location and tabs on tablet */
      }
      .top-nav-search-bar .source-segment-wrap {
        margin-left: auto !important;
      }
    }

    @media (max-width: 520px) {
      .top-nav-search-bar {
        gap: 10px !important;
      }
      .top-nav-search-bar .location-select-wrap {
        width: 100% !important;
      }
      .top-nav-search-bar .location-select-wrap select {
        width: 100% !important;
      }
      .top-nav-search-bar .source-segment-wrap {
        width: 100% !important;
        display: flex !important;
        justify-content: space-between !important;
        overflow-x: auto !important;
        order: 2 !important;
      }
      .top-nav-search-bar .source-tab-btn {
        flex: 1 !important;
        text-align: center !important;
        padding: 8px 4px !important;
        font-size: 12px !important;
      }
      .top-nav-search-bar .explore-search-wrap {
        order: 3 !important;
      }
      .results-sort-bar {
        margin: 8px 0 16px 0 !important;
        flex-wrap: wrap !important;
      }
      #explore-sort-select {
        min-width: 105px !important;
        font-size: 12px !important;
      }
      .btn-clear-all-filters {
        padding: 0 10px !important;
        font-size: 11px !important;
      }
    }
'''

# Replace old Explore Controls Bar Styling
html = re.sub(r'\/\* Explore Controls Bar Styling \*\/[\s\S]*?(?=<\/style>)', option1_css + '\n  ', html, count=1)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Applied Option 1 layout & responsive CSS to explore.html")
