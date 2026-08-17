import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update tab placeholders and search state variables in explore.html
search_js_block = '''
    // Phase 3C: Explore Search & Sort State
    let currentSearchQuery = '';
    let currentSortOption = 'recommended';
    let searchDebounceTimer = null;

    const tabPlaceholders = {
      'moonoh': 'Search Moonoh listings',
      'foodrescue': 'Search food rescue items',
      'localshops': 'Search local shops',
      'marketplaces': 'Search marketplace listings',
      'others': 'Search marketplace listings'
    };

    function normalizeSearchText(str) {
      if (!str) return '';
      return String(str)
        .toLowerCase()
        .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '')
        .replace(/[^a-z0-9\\s]/g, ' ')
        .replace(/\\s+/g, ' ')
        .trim();
    }

    function getItemSearchText(item) {
      if (item._cachedSearchText) return item._cachedSearchText;
      const fields = [
        item.title || '',
        item.brand || '',
        item.badgeName || '',
        item.store_name || '',
        item.sourceName || '',
        item.category || item.categoryName || '',
        item.location || item.townName || item.rawTown || '',
        item.description || item.moonoh_summary || ''
      ];
      item._cachedSearchText = normalizeSearchText(fields.join(' '));
      return item._cachedSearchText;
    }

    function updateSearchUI() {
      const searchInput = document.getElementById('explore-search-input');
      const searchClearBtn = document.getElementById('explore-search-clear');
      const sortSelect = document.getElementById('explore-sort-select');

      if (searchInput) {
        searchInput.placeholder = tabPlaceholders[activeSource] || 'Search items in this tab';
        searchInput.value = currentSearchQuery;
      }
      if (searchClearBtn) {
        searchClearBtn.style.display = currentSearchQuery ? 'flex' : 'none';
      }
      if (sortSelect) {
        sortSelect.value = currentSortOption;
      }
    }

    function syncUrlAndSeo() {
      try {
        const urlObj = new URL(window.location.href);
        if (currentSearchQuery) {
          urlObj.searchParams.set('q', currentSearchQuery);
        } else {
          urlObj.searchParams.delete('q');
        }

        if (currentSortOption && currentSortOption !== 'recommended') {
          urlObj.searchParams.set('sort', currentSortOption);
        } else {
          urlObj.searchParams.delete('sort');
        }

        const newUrlStr = urlObj.pathname + (urlObj.search ? urlObj.search : '');
        window.history.replaceState({ q: currentSearchQuery, sort: currentSortOption, source: activeSource }, '', newUrlStr);

        const hasSearchOrSort = urlObj.searchParams.has('q') || urlObj.searchParams.has('sort');
        let robotsMeta = document.querySelector('meta[name="robots"]');
        if (robotsMeta) {
          robotsMeta.setAttribute('content', hasSearchOrSort ? 'noindex, follow' : 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1');
        }
      } catch (e) {}
    }

    function clearSearch() {
      const prevQuery = currentSearchQuery;
      currentSearchQuery = '';
      const searchInput = document.getElementById('explore-search-input');
      if (searchInput) searchInput.value = '';
      const searchClearBtn = document.getElementById('explore-search-clear');
      if (searchClearBtn) searchClearBtn.style.display = 'none';

      if (prevQuery && typeof gtag === 'function') {
        gtag('event', 'search_clear', {
          previous_search_term: prevQuery,
          active_tab: activeSource
        });
      }

      applyFilters();
    }
'''

# 2. Comprehensive applyFilters() implementation
new_apply_filters = '''    function applyFilters(categorySlug = null) {
      const targetSlug = categorySlug || getActiveCategoryKeyword() || 'all';
      let filtered = [];

      // 1. Tab Scope Pool
      if (activeSource === 'foodrescue') {
        filtered = [...foodRescueItemsList];
      } else if (activeSource === 'localshops') {
        if (localShopsRawData) {
          const rawProds = localShopsRawData.products || [];
          const shops = localShopsRawData.shops || {};
          let catPool = rawProds;
          if (activeLocalCategory && activeLocalCategory !== 'All') {
            catPool = rawProds.filter(p => (p.primary_category || p.moonoh_category || '') === activeLocalCategory);
          }
          filtered = catPool.map(p => ({
            id: p.id,
            no: p.id,
            title: p.title,
            brand: p.brand,
            price: p.current_price,
            photo: p.image_source_url,
            image: p.image_source_url,
            townName: p.availability_context || (p.store_city ? `${p.store_city}, ${p.store_state}` : 'NYC'),
            rawTown: 'NYC',
            location: 'NYC',
            category: p.primary_category || p.moonoh_category || 'General',
            categoryName: p.primary_category || p.moonoh_category || 'General',
            primary_category: p.primary_category || p.moonoh_category || 'General',
            source: p.shop_id,
            shop_id: p.shop_id,
            badgeName: p.brand || (shops[p.shop_id] ? shops[p.shop_id].name : 'Local Shop'),
            url: `/local-product/${p.shop_id}/${p.slug}`,
            source_published_at: p.source_published_at,
            source_created_at: p.source_created_at,
            source_updated_at: p.source_updated_at,
            source_order: p.source_order,
            source_product_id: p.source_product_id,
            moonoh_summary: p.moonoh_summary
          }));
        } else {
          filtered = [...localShopsItemsList];
        }
      } else if (activeSource === 'marketplaces' || activeSource === 'others') {
        filtered = externalItemsList.length > 0 ? [...externalItemsList] : allItems.filter(i => i.source === 'karrot' || i.source === 'heykorean' || i.source === 'external' || String(i.url || '').includes('-ext-'));
      } else {
        // Moonoh tab
        const moonohInAll = allItems.filter(isStrictMoonoh);
        filtered = moonohInAll.length > 0 ? [...moonohInAll] : (moonohItemsList.length > 0 ? [...moonohItemsList] : [...allItems]);
      }

      // 2. Location filter
      if (activeTown && boroughKeywords[activeTown]) {
        const kws = boroughKeywords[activeTown];
        filtered = filtered.filter(item => {
          if (item.source === 'kimc') return true;
          const locStr = ((item.rawTown || '') + ' ' + (item.location || '')).toLowerCase();
          return kws.some(kw => locStr.includes(kw));
        });
      }

      // 3. Category filter (for non-local tabs)
      if (activeSource !== 'localshops') {
        if (targetSlug === 'free') {
          filtered = filtered.filter(item => {
            if (!item) return false;
            const p = item.price !== undefined ? item.price : (item.current_price !== undefined ? item.current_price : null);
            if (p === 0 || p === '0' || p === 'Free' || p === 'free') return true;
            const num = parseFloat(p);
            return !isNaN(num) && num === 0;
          });
        } else if (targetSlug && targetSlug !== 'all') {
          filtered = filtered.filter(item => matchesCategory(item.category || item.categoryName, item.title, targetSlug));
        }
      }

      // 4. Search query filter
      if (currentSearchQuery) {
        const queryTokens = normalizeSearchText(currentSearchQuery).split(' ').filter(Boolean);
        if (queryTokens.length > 0) {
          filtered = filtered.filter(item => {
            const target = getItemSearchText(item);
            return queryTokens.every(token => target.includes(token));
          });
        }
      }

      // 5. Sorting
      if (currentSortOption === 'recommended') {
        if (activeSource === 'localshops') {
          if (typeof getBalancedLocalProducts === 'function') {
            filtered = getBalancedLocalProducts(filtered, { context: 'explore-local' });
          }
        } else {
          filtered.sort((a, b) => {
            const numA = (typeof a.postedAt === 'number' && a.postedAt > 0) ? a.postedAt : (typeof a.no === 'number' ? a.no : (parseInt(String(a.id || '').replace(/\\D/g, ''), 10) || 0));
            const numB = (typeof b.postedAt === 'number' && b.postedAt > 0) ? b.postedAt : (typeof b.no === 'number' ? b.no : (parseInt(String(b.id || '').replace(/\\D/g, ''), 10) || 0));
            return numB - numA;
          });
        }
      } else if (currentSortOption === 'newest') {
        filtered.sort((a, b) => {
          const dateA = a.source_published_at ? new Date(a.source_published_at).getTime() : (a.postedAt ? new Date(a.postedAt).getTime() : null);
          const dateB = b.source_published_at ? new Date(b.source_published_at).getTime() : (b.postedAt ? new Date(b.postedAt).getTime() : null);
          if (dateA !== null && dateB !== null) return dateB - dateA;
          if (dateA !== null && dateB === null) return -1;
          if (dateA === null && dateB !== null) return 1;
          return 0;
        });
      } else if (currentSortOption === 'price-asc') {
        filtered.sort((a, b) => {
          const priceA = (typeof a.price === 'number' && a.price > 0) ? a.price : ((typeof a.current_price === 'number' && a.current_price > 0) ? a.current_price : null);
          const priceB = (typeof b.price === 'number' && b.price > 0) ? b.price : ((typeof b.current_price === 'number' && b.current_price > 0) ? b.current_price : null);
          if (priceA !== null && priceB !== null) return priceA - priceB;
          if (priceA !== null && priceB === null) return -1;
          if (priceA === null && priceB !== null) return 1;
          return 0;
        });
      } else if (currentSortOption === 'price-desc') {
        filtered.sort((a, b) => {
          const priceA = (typeof a.price === 'number' && a.price > 0) ? a.price : ((typeof a.current_price === 'number' && a.current_price > 0) ? a.current_price : null);
          const priceB = (typeof b.price === 'number' && b.price > 0) ? b.price : ((typeof b.current_price === 'number' && b.current_price > 0) ? b.current_price : null);
          if (priceA !== null && priceB !== null) return priceB - priceA;
          if (priceA !== null && priceB === null) return -1;
          if (priceA === null && priceB !== null) return 1;
          return 0;
        });
      } else if (currentSortOption === 'name-asc') {
        filtered.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
      }

      currentFiltered = filtered;
      visibleCount = 40;
      renderGrid(currentFiltered);
      updateLocationCount(filtered.length);
      updateResultsLabel(filtered.length);
      updateSearchUI();
      syncUrlAndSeo();
    }

    function updateResultsLabel(count) {
      const labelEl = document.getElementById('explore-results-label');
      if (!labelEl) return;
      if (currentSearchQuery) {
        const safeQuery = currentSearchQuery.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        labelEl.innerHTML = `${count} ${count === 1 ? 'result' : 'results'} for “<strong>${safeQuery}</strong>”`;
      } else {
        labelEl.textContent = `${count} items`;
      }
    }'''

# Replace old applyFilters block in explore.html
old_apply_pattern = r'function applyFilters\(categorySlug = null\) \{[\s\S]*?updateLocationCount\(filtered\.length\);\s*\}'
html = re.sub(old_apply_pattern, lambda m: new_apply_filters, html, count=1)

# Add search_js_block before applyFilters
if 'let currentSearchQuery =' not in html:
    html = html.replace('function applyFilters(', search_js_block + '\n\n    function applyFilters(')
    print("✅ Inserted search & sort JS state block")

# 3. Update renderGrid to handle empty search state with "Clear search" button
if 'No items found for' not in html:
    html = re.sub(r'grid\.innerHTML = \'<p style="text-align:center; color:#888; padding:40px; grid-column:1\/-1;">No items found\.</p>\';\s*return;', lambda m: new_empty_grid, html, count=1)
    print("✅ Updated renderGrid empty state with Clear search button")

# 4. Wire up Search Input, Clear Button, Sort Select and URL initialization
event_wiring = '''
    // Phase 3C Event Listeners & URL Initializer
    const searchInputEl = document.getElementById('explore-search-input');
    const searchClearEl = document.getElementById('explore-search-clear');
    const sortSelectEl = document.getElementById('explore-sort-select');

    if (searchInputEl) {
      searchInputEl.addEventListener('input', (e) => {
        const val = e.target.value;
        if (searchClearEl) searchClearEl.style.display = val ? 'flex' : 'none';

        if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
          currentSearchQuery = val.trim();
          if (currentSearchQuery && typeof gtag === 'function') {
            gtag('event', 'search', {
              search_term: currentSearchQuery,
              active_tab: activeSource,
              result_count: currentFiltered.length
            });
          }
          applyFilters();
        }, 200);
      });

      searchInputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          clearSearch();
        } else if (e.key === 'Enter') {
          if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
          currentSearchQuery = searchInputEl.value.trim();
          applyFilters();
        }
      });
    }

    if (searchClearEl) {
      searchClearEl.addEventListener('click', clearSearch);
    }

    if (sortSelectEl) {
      sortSelectEl.addEventListener('change', (e) => {
        currentSortOption = e.target.value;
        if (typeof gtag === 'function') {
          gtag('event', 'sort_change', {
            sort_value: currentSortOption,
            active_tab: activeSource,
            result_count: currentFiltered.length
          });
        }
        applyFilters();
      });
    }

    // Handle browser popstate
    window.addEventListener('popstate', (e) => {
      try {
        const params = new URLSearchParams(window.location.search);
        currentSearchQuery = params.get('q') || '';
        currentSortOption = params.get('sort') || 'recommended';
        updateSearchUI();
        applyFilters();
      } catch (err) {}
    });

    // Parse initial URL query params on load
    try {
      const initialParams = new URLSearchParams(window.location.search);
      if (initialParams.has('q')) {
        currentSearchQuery = initialParams.get('q') || '';
      }
      if (initialParams.has('sort')) {
        currentSortOption = initialParams.get('sort') || 'recommended';
      }
      updateSearchUI();
    } catch (err) {}
'''

if '// Phase 3C Event Listeners' not in html:
    html = html.replace('// Local filter pill clicks', event_wiring + '\n\n    // Local filter pill clicks')
    print("✅ Added search and sort event wiring and initial URL sync")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved explore.html with search & sort features")
