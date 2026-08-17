import re

# 1. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

# Add mixer script before </head> or before custom scripts
if '<script src="/js/local-products-mixer.js"></script>' not in exp_html:
    exp_html = exp_html.replace('</head>', '  <script src="/js/local-products-mixer.js"></script>\n</head>')
    print("✅ Added local-products-mixer.js to explore.html head")

# Add #local-filter-container after #filter-container
local_filter_markup = '''      <div class="filter-container" id="local-filter-container" style="display:none;">
        <button class="filter-pill active" data-local-cat="All">All</button>
        <button class="filter-pill" data-local-cat="Vintage & Fashion">Vintage & Fashion</button>
        <button class="filter-pill" data-local-cat="Home & Objects">Home & Objects</button>
        <button class="filter-pill" data-local-cat="Coffee & Pantry">Coffee & Pantry</button>
        <button class="filter-pill" data-local-cat="Gifts & Culture">Gifts & Culture</button>
      </div>'''

if 'id="local-filter-container"' not in exp_html:
    exp_html = exp_html.replace('</div>\n\n      <!-- Food Rescue Informational Banner', '</div>\n\n' + local_filter_markup + '\n\n      <!-- Food Rescue Informational Banner')
    print("✅ Added #local-filter-container to explore.html")

# Update JS in explore.html
old_preload_local = '''    async function preloadLocalShopsItems() {
      if (localShopsItemsList.length > 0) return;
      try {
        const res = await fetch('/local_shops_data.json');
        if (res.ok) {
          const data = await res.json();
          localShopsItemsList = (data.products || []).map(p => ({
            id: p.id,
            no: p.id,
            title: p.title,
            price: p.current_price,
            photo: p.image_source_url,
            image: p.image_source_url,
            townName: p.availability_context || 'NYC',
            rawTown: 'NYC',
            location: 'NYC',
            category: p.moonoh_category || 'Grocery',
            categoryName: p.moonoh_category || 'Grocery',
            source: p.shop_id,
            shop_id: p.shop_id,
            badgeName: p.brand || (data.shops && data.shops[p.shop_id] ? data.shops[p.shop_id].name : 'Local Shop'),
            url: `/local-product/${p.shop_id}/${p.slug}`
          }));
          if (activeSource === 'localshops') applyFilters(getActiveCategoryKeyword());
        }
      } catch (e) {}
    }'''

new_preload_local = '''    let localShopsRawData = null;
    let activeLocalCategory = 'All';

    async function preloadLocalShopsItems() {
      try {
        if (!localShopsRawData) {
          const res = await fetch('/local_shops_data.json');
          if (res.ok) {
            localShopsRawData = await res.json();
          }
        }
        if (localShopsRawData) {
          const rawProds = localShopsRawData.products || [];
          const shops = localShopsRawData.shops || {};
          const balanced = (typeof getBalancedLocalProducts === 'function')
            ? getBalancedLocalProducts(rawProds, { category: activeLocalCategory, context: 'explore-local' })
            : rawProds;

          localShopsItemsList = balanced.map(p => ({
            id: p.id,
            no: p.id,
            title: p.title,
            price: p.current_price,
            photo: p.image_source_url,
            image: p.image_source_url,
            townName: p.availability_context || (p.store_city ? `${p.store_city}, ${p.store_state}` : 'NYC'),
            rawTown: 'NYC',
            location: 'NYC',
            category: p.primary_category || p.moonoh_category || 'General',
            categoryName: p.primary_category || p.moonoh_category || 'General',
            source: p.shop_id,
            shop_id: p.shop_id,
            badgeName: p.brand || (shops[p.shop_id] ? shops[p.shop_id].name : 'Local Shop'),
            url: `/local-product/${p.shop_id}/${p.slug}`
          }));
          if (activeSource === 'localshops') applyFilters(getActiveCategoryKeyword());
        }
      } catch (e) {
        console.error("Error loading local shops:", e);
      }
    }'''

if old_preload_local in exp_html:
    exp_html = exp_html.replace(old_preload_local, new_preload_local)
    print("✅ Updated preloadLocalShopsItems in explore.html")
else:
    print("⚠️ preloadLocalShopsItems pattern mismatch in explore.html")

# Update switchSource in explore.html for local-filter-container
old_switch = '''      const filterContainer = document.getElementById("filter-container");
      if (filterContainer) {
        filterContainer.style.display = (source === 'foodrescue' || source === 'localshops') ? 'none' : 'flex';
      }'''

new_switch = '''      const filterContainer = document.getElementById("filter-container");
      const localFilterContainer = document.getElementById("local-filter-container");
      if (filterContainer) {
        filterContainer.style.display = (source === 'foodrescue' || source === 'localshops') ? 'none' : 'flex';
      }
      if (localFilterContainer) {
        localFilterContainer.style.display = source === 'localshops' ? 'flex' : 'none';
      }'''

if old_switch in exp_html:
    exp_html = exp_html.replace(old_switch, new_switch)
    print("✅ Updated switchSource for localFilterContainer in explore.html")

# Update applyFilters in explore.html to avoid re-sorting balanced local shops
old_apply_local = '''      if (activeSource === 'foodrescue') {
        filtered = foodRescueItemsList;
      } else if (activeSource === 'localshops') {
        filtered = localShopsItemsList;
      }'''

new_apply_local = '''      if (activeSource === 'foodrescue') {
        filtered = foodRescueItemsList;
      } else if (activeSource === 'localshops') {
        if (localShopsRawData) {
          const rawProds = localShopsRawData.products || [];
          const shops = localShopsRawData.shops || {};
          const balanced = (typeof getBalancedLocalProducts === 'function')
            ? getBalancedLocalProducts(rawProds, { category: activeLocalCategory, context: 'explore-local' })
            : rawProds;

          localShopsItemsList = balanced.map(p => ({
            id: p.id,
            no: p.id,
            title: p.title,
            price: p.current_price,
            photo: p.image_source_url,
            image: p.image_source_url,
            townName: p.availability_context || (p.store_city ? `${p.store_city}, ${p.store_state}` : 'NYC'),
            rawTown: 'NYC',
            location: 'NYC',
            category: p.primary_category || p.moonoh_category || 'General',
            categoryName: p.primary_category || p.moonoh_category || 'General',
            source: p.shop_id,
            shop_id: p.shop_id,
            badgeName: p.brand || (shops[p.shop_id] ? shops[p.shop_id].name : 'Local Shop'),
            url: `/local-product/${p.shop_id}/${p.slug}`
          }));
        }
        filtered = localShopsItemsList;
        currentFiltered = filtered;
        visibleCount = 40;
        renderGrid(currentFiltered);
        updateLocationCount(filtered.length);
        return;
      }'''

if old_apply_local in exp_html:
    exp_html = exp_html.replace(old_apply_local, new_apply_local)
    print("✅ Updated applyFilters for localshops in explore.html")

# Add click event listener for local filter pills
local_pills_event = '''    // Local filter pill clicks
    document.querySelectorAll('#local-filter-container .filter-pill').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('#local-filter-container .filter-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeLocalCategory = btn.getAttribute('data-local-cat') || 'All';
        applyFilters();
      });
    });
'''

if 'activeLocalCategory = btn.getAttribute' not in exp_html:
    exp_html = exp_html.replace('preloadMoonohItems();', 'preloadMoonohItems();\n' + local_pills_event)
    print("✅ Added local filter pill click handler in explore.html")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp_html)
print("Saved explore.html")


# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

if '<script src="/js/local-products-mixer.js"></script>' not in idx_html:
    idx_html = idx_html.replace('</head>', '  <script src="/js/local-products-mixer.js"></script>\n</head>')
    print("✅ Added local-products-mixer.js to index.html head")

old_idx_preload = '''      async function preloadLocalShopsOnIndex() {
        if (localShopsItemsList.length > 0) return;
        try {
          const res = await fetch('/local_shops_data.json');
          if (res.ok) {
            const data = await res.json();
            localShopsItemsList = (data.products || []).map(p => ({
              id: p.id,
              no: p.id,
              title: p.title,
              price: p.current_price,
              image: p.image_source_url,
              photo: p.image_source_url,
              location: p.availability_context || 'NYC',
              rawTown: 'NYC',
              category: p.moonoh_category || 'Grocery',
              categoryName: p.moonoh_category || 'Grocery',
              source: p.shop_id,
              badgeName: p.brand || 'Local Shop',
              url: `/local-product/${p.shop_id}/${p.slug}`
            }));
          }
        } catch (e) {}
      }'''

new_idx_preload = '''      async function preloadLocalShopsOnIndex() {
        if (localShopsItemsList.length > 0) return;
        try {
          const res = await fetch('/local_shops_data.json');
          if (res.ok) {
            const data = await res.json();
            const rawProds = data.products || [];
            const shops = data.shops || {};
            const balanced = (typeof getBalancedLocalProducts === 'function')
              ? getBalancedLocalProducts(rawProds, { context: 'home' })
              : rawProds;

            localShopsItemsList = balanced.map(p => ({
              id: p.id,
              no: p.id,
              title: p.title,
              price: p.current_price,
              image: p.image_source_url,
              photo: p.image_source_url,
              location: p.availability_context || (p.store_city ? `${p.store_city}, ${p.store_state}` : 'NYC'),
              rawTown: 'NYC',
              category: p.primary_category || p.moonoh_category || 'General',
              categoryName: p.primary_category || p.moonoh_category || 'General',
              source: p.shop_id,
              badgeName: p.brand || (shops[p.shop_id] ? shops[p.shop_id].name : 'Local Shop'),
              url: `/local-product/${p.shop_id}/${p.slug}`
            }));
          }
        } catch (e) {}
      }'''

if old_idx_preload in idx_html:
    idx_html = idx_html.replace(old_idx_preload, new_idx_preload)
    print("✅ Updated preloadLocalShopsOnIndex in index.html")
else:
    print("⚠️ preloadLocalShopsOnIndex pattern mismatch in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)
print("Saved index.html")
