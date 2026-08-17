import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean HTML Template for Item Feed Controls
controls_markup = '''      <!-- 1. Top Primary Controls Row: Location Select & Primary 4-Tab Switcher -->
      <div class="location-bar" style="display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; width: 100%; box-sizing: border-box;">
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

        <span class="location-count" id="location-count" style="display: none;"></span>

        <!-- Primary 4-Tab Segment Switcher -->
        <div class="source-segment-wrap" id="source-segment-wrap" style="flex-shrink: 0; margin-left: auto;">
          <button class="source-tab-btn active" id="tab-source-moonoh" data-source="moonoh">Moonoh</button>
          <button class="source-tab-btn tab-foodrescue" id="tab-source-foodrescue" data-source="foodrescue">Food Rescue</button>
          <button class="source-tab-btn" id="tab-source-localshops" data-source="localshops">Local</button>
          <button class="source-tab-btn" id="tab-source-marketplaces" data-source="marketplaces">Marketplaces</button>
        </div>
      </div>

      <!-- 2. Scoped Search Bar (Sub-item directly under selected tab, Airbnb style) -->
      <div class="explore-search-bar-row" style="margin: 0 auto 20px auto; width: 100%; max-width: 680px; box-sizing: border-box;">
        <div class="explore-search-inner" style="position: relative; display: flex; align-items: center; width: 100%; border: 1.5px solid #E5E7EB; border-radius: 9999px; background: #FFFFFF; box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: border-color 0.2s, box-shadow 0.2s;">
          <svg class="explore-search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="position: absolute; left: 16px; pointer-events: none;">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" id="explore-search-input" class="explore-search-input" placeholder="Search in Moonoh" aria-label="Search listings in current tab" style="width: 100%; height: 44px; padding: 0 44px 0 46px; border: none; border-radius: 9999px; font-size: 14px; color: #111827; background: transparent; outline: none; box-sizing: border-box;" />
          <button id="explore-search-clear" class="explore-search-clear" aria-label="Clear search keyword" style="display: none; position: absolute; right: 10px; width: 26px; height: 26px; border: none; background: #F3F4F6; color: #4B5563; cursor: pointer; border-radius: 50%; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; padding: 0; line-height: 1;">
            ✕
          </button>
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

      <!-- 3. Standard Category Filters (Moonoh & Marketplaces) -->
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
          <span id="filter-pill-more-text">More</span> <svg class="filter-more-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
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

      <!-- 4. Result Count & Plain Text Sort Row -->
      <div class="results-sort-bar" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 16px 0 20px 0; width: 100%; box-sizing: border-box;">
        <div id="explore-results-label" style="font-size: 13.5px; font-weight: 600; color: #374151; white-space: nowrap;">
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
          <!-- 100% Plain Text Sort Selector (No button border, no pill box) -->
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
          </div>
          <!-- Clear Filters Link / Minimal Button -->
          <button id="btn-clear-all-filters" class="btn-clear-all-filters" aria-label="Clear all active filters" style="display: none; align-items: center; justify-content: center; height: 32px; padding: 0 12px; background: #F3F4F6; color: #4F46E5; font-size: 12px; font-weight: 700; border: 1px solid #E0E7FF; border-radius: 9999px; cursor: pointer; white-space: nowrap; transition: background 0.2s;">
            Clear Filters
          </button>
        </div>
      </div>
'''

# Replace controls block in explore.html
pattern = r'(?:<!-- 1\. Top Integrated Row: Location[\s\S]*?|<!-- Location Dropdown & Source Toggle Row -->[\s\S]*?)(?=<div class="item-grid" id="moonoh-item-grid">)'
html = re.sub(pattern, controls_markup + '\n      ', html, count=1)

# 2. Add More Button and Sort styles in CSS
css_updates = '''
    /* Scoped Search, More Categories & Plain Text Sort Styling */
    .explore-search-inner:focus-within {
      border-color: #4F46E5 !important;
      box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }
    .filter-container .filter-pill-extra {
      display: none;
    }
    .filter-container.is-expanded .filter-pill-extra {
      display: inline-flex !important;
    }
    #explore-sort-select {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      outline: none !important;
    }
    #explore-sort-select:focus {
      outline: none !important;
      box-shadow: none !important;
    }
    .btn-clear-all-filters:hover {
      background: #EEF2FF !important;
    }

    @media (max-width: 520px) {
      .location-bar {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
      }
      .location-select-wrap {
        width: 100% !important;
      }
      .location-select-wrap select {
        width: 100% !important;
      }
      .source-segment-wrap {
        width: 100% !important;
        display: flex !important;
        justify-content: space-between !important;
        overflow-x: auto !important;
        margin-left: 0 !important;
      }
      .source-tab-btn {
        flex: 1 !important;
        text-align: center !important;
        padding: 8px 4px !important;
        font-size: 12px !important;
      }
      .results-sort-bar {
        margin: 10px 0 16px 0 !important;
      }
    }
'''

# Replace old Explore Controls Bar Styling in <style>
html = re.sub(r'\/\* (?:Option 1|Explore Controls Bar).*?\*\/[\s\S]*?(?=<\/style>)', css_updates + '\n  ', html, count=1)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Updated explore.html markup and CSS hierarchy")
