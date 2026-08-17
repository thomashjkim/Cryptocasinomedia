import re

print("=" * 80)
print("🔧 ADDING LOCAL 5 CATEGORY FILTERS TO HOME (index.html)")
print("=" * 80)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add #local-filter-container markup after #filter-container
local_filter_markup = '''      <!-- Local Shops 5 Category Filters -->
      <div class="filter-container" id="local-filter-container" style="display: none;">
        <button class="filter-pill active" data-local-cat="All">All</button>
        <button class="filter-pill" data-local-cat="Vintage & Fashion">Vintage &amp; Fashion</button>
        <button class="filter-pill" data-local-cat="Home & Objects">Home &amp; Objects</button>
        <button class="filter-pill" data-local-cat="Coffee & Pantry">Coffee &amp; Pantry</button>
        <button class="filter-pill" data-local-cat="Gifts & Culture">Gifts &amp; Culture</button>
      </div>'''

if 'id="local-filter-container"' not in html:
    html = html.replace('</div>\n      <!-- Food Rescue Informational Banner', f'</div>\n{local_filter_markup}\n      <!-- Food Rescue Informational Banner')
    print("✅ Inserted #local-filter-container into index.html")

# 2. Update switchSource in index.html to toggle #local-filter-container
old_switch_display = '''        const filterContainer = document.getElementById("filter-container");
        if (filterContainer) {
          filterContainer.style.display = (source === 'foodrescue' || source === 'localshops') ? 'none' : 'flex';
        }'''

new_switch_display = '''        const filterContainer = document.getElementById("filter-container");
        const localFilterContainer = document.getElementById("local-filter-container");
        if (filterContainer) {
          filterContainer.style.display = (source === 'foodrescue' || source === 'localshops') ? 'none' : 'flex';
        }
        if (localFilterContainer) {
          localFilterContainer.style.display = (source === 'localshops') ? 'flex' : 'none';
        }'''

if old_switch_display in html:
    html = html.replace(old_switch_display, new_switch_display)
    print("✅ Updated switchSource display logic in index.html")

# 3. Add local category filter event handling and activeLocalCategory state
old_preload = '''    let localShopsRawData = null;
    async function preloadLocalShopsOnIndex() {'''

new_preload = '''    let localShopsRawData = null;
    let activeLocalCategory = 'All';

    // Local category pill click listener
    document.addEventListener('DOMContentLoaded', () => {
      const localPills = document.querySelectorAll('#local-filter-container .filter-pill');
      localPills.forEach(pill => {
        pill.addEventListener('click', () => {
          localPills.forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          activeLocalCategory = pill.getAttribute('data-local-cat') || 'All';
          const locSelect = document.getElementById('location-select');
          filterAndRender(locSelect ? locSelect.value.toLowerCase() : '', null);
        });
      });
    });

    async function preloadLocalShopsOnIndex() {'''

if old_preload in html:
    html = html.replace(old_preload, new_preload)
    print("✅ Added local category click listeners in index.html")

# 4. Update filterAndRender to filter local items by activeLocalCategory
old_filter_local = '''        else if (activeSource === 'localshops') pool = localShopsItemsList;'''

new_filter_local = '''        else if (activeSource === 'localshops') {
          pool = localShopsItemsList;
          if (activeLocalCategory && activeLocalCategory !== 'All') {
            pool = pool.filter(item => {
              const itemCat = (item.moonoh_category || item.category || '').toLowerCase();
              const target = activeLocalCategory.toLowerCase();
              return itemCat === target || itemCat.includes(target);
            });
          }
        }'''

if old_filter_local in html:
    html = html.replace(old_filter_local, new_filter_local)
    print("✅ Updated filterAndRender with activeLocalCategory in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Saved index.html with full Local 5 category filtering support!")
