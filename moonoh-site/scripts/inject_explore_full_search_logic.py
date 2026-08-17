import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the entire search & filtering JavaScript block in explore.html
full_search_logic = '''
    // =========================================================================
    // Phase 3D/3C: Scoped Tab Search, Sort, Filters & URL State Management
    // =========================================================================
    let currentSearchQuery = '';
    let currentSortOption = 'newest';
    let userHasExplicitSort = false;
    let searchDebounceTimer = null;

    const tabPlaceholders = {
      'moonoh': 'Search in Moonoh',
      'foodrescue': 'Search food rescue',
      'localshops': 'Search in Local',
      'marketplaces': 'Search in Marketplaces',
      'others': 'Search in Marketplaces'
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
        item.source || '',
        item.category || item.categoryName || item.primary_category || '',
        item.location || item.townName || item.rawTown || '',
        item.description || item.moonoh_summary || ''
      ];
      item._cachedSearchText = normalizeSearchText(fields.join(' '));
      return item._cachedSearchText;
    }

    function calculateRelevanceScore(item, queryTokens, fullQueryNorm) {
      let score = 0;
      const titleNorm = normalizeSearchText(item.title || '');
      const brandNorm = normalizeSearchText(item.brand || item.store_name || item.badgeName || '');
      const catNorm = normalizeSearchText(item.category || item.categoryName || item.primary_category || '');
      const locNorm = normalizeSearchText(item.location || item.townName || item.rawTown || '');
      const descNorm = normalizeSearchText(item.description || item.moonoh_summary || '');

      if (titleNorm === fullQueryNorm) score += 100;
      else if (titleNorm.startsWith(fullQueryNorm)) score += 60;
      else if (titleNorm.includes(fullQueryNorm)) score += 40;

      for (const token of queryTokens) {
        if (titleNorm.includes(token)) score += 25;
        if (brandNorm.includes(token)) score += 15;
        if (catNorm.includes(token)) score += 10;
        if (locNorm.includes(token)) score += 5;
        if (descNorm.includes(token)) score += 3;
      }
      return score;
    }

    function updateSearchUI() {
      const searchInput = document.getElementById('explore-search-input');
      const searchClearBtn = document.getElementById('explore-search-clear');
      const sortSelect = document.getElementById('explore-sort-select');
      const clearAllBtn = document.getElementById('btn-clear-all-filters');

      if (searchInput) {
        searchInput.placeholder = tabPlaceholders[activeSource] || 'Search in this tab';
        searchInput.value = currentSearchQuery;
      }
      if (searchClearBtn) {
        searchClearBtn.style.display = currentSearchQuery ? 'flex' : 'none';
      }
      if (sortSelect) {
        sortSelect.value = currentSortOption;
      }

      // Check if any filter is active (search query, category !== 'all', or non-default sort)
      const currentCat = getActiveCategoryKeyword();
      const isLocalCatActive = (activeSource === 'localshops' && activeLocalCategory !== 'All');
      const isNormalCatActive = (activeSource !== 'localshops' && currentCat !== 'all');
      const isSortActive = (userHasExplicitSort && currentSortOption !== (currentSearchQuery ? 'relevance' : 'newest'));

      const hasActiveFilters = Boolean(currentSearchQuery || isLocalCatActive || isNormalCatActive || isSortActive);
      if (clearAllBtn) {
        clearAllBtn.style.display = hasActiveFilters ? 'inline-flex' : 'none';
      }
    }

    function syncUrlAndSeo() {
      try {
        const urlObj = new URL(window.location.href);
        
        // 1. Tab parameter
        const tabParam = activeSource === 'localshops' ? 'local' : activeSource;
        if (tabParam && tabParam !== 'moonoh') urlObj.searchParams.set('tab', tabParam);
        else urlObj.searchParams.delete('tab');

        // 2. Query parameter
        if (currentSearchQuery) urlObj.searchParams.set('q', currentSearchQuery);
        else urlObj.searchParams.delete('q');

        // 3. Category parameter
        const currentCat = (activeSource === 'localshops') ? activeLocalCategory : getActiveCategoryKeyword();
        if (currentCat && currentCat.toLowerCase() !== 'all') urlObj.searchParams.set('category', currentCat.toLowerCase().replace(/\\s+/g, '-'));
        else urlObj.searchParams.delete('category');

        // 4. Sort parameter
        const defaultSortForState = currentSearchQuery ? 'relevance' : 'newest';
        if (currentSortOption && currentSortOption !== defaultSortForState && userHasExplicitSort) {
          urlObj.searchParams.set('sort', currentSortOption);
        } else {
          urlObj.searchParams.delete('sort');
        }

        // 5. Area / Location parameter
        if (activeTown) urlObj.searchParams.set('area', activeTown);
        else urlObj.searchParams.delete('area');

        const newUrlStr = urlObj.pathname + (urlObj.search ? urlObj.search : '');
        window.history.replaceState({
          tab: activeSource,
          q: currentSearchQuery,
          category: currentCat,
          sort: currentSortOption,
          area: activeTown
        }, '', newUrlStr);

        // Update robots meta (noindex for search/filter parameters)
        const hasParams = urlObj.searchParams.toString().length > 0;
        let robotsMeta = document.querySelector('meta[name="robots"]');
        if (robotsMeta) {
          robotsMeta.setAttribute('content', hasParams ? 'noindex, follow' : 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1');
        }
      } catch (e) {}
    }

    function clearSearchQueryOnly() {
      const prevQuery = currentSearchQuery;
      currentSearchQuery = '';
      if (!userHasExplicitSort) {
        currentSortOption = 'newest';
      }
      const searchInput = document.getElementById('explore-search-input');
      if (searchInput) searchInput.value = '';
      const searchClearBtn = document.getElementById('explore-search-clear');
      if (searchClearBtn) searchClearBtn.style.display = 'none';

      if (prevQuery && typeof gtag === 'function') {
        gtag('event', 'clear_search', {
          previous_search_term: prevQuery,
          active_tab: activeSource
        });
      }

      applyFilters();
    }

    function clearAllFilters() {
      const prevQuery = currentSearchQuery;
      currentSearchQuery = '';
      userHasExplicitSort = false;
      currentSortOption = 'newest';

      // Reset category pills to 'All'
      if (activeSource === 'localshops') {
        activeLocalCategory = 'All';
        document.querySelectorAll('#local-filter-container .filter-pill').forEach(btn => {
          btn.classList.toggle('active', btn.getAttribute('data-local-cat') === 'All');
        });
      } else {
        document.querySelectorAll('#filter-container .filter-pill').forEach(btn => {
          btn.classList.toggle('active', btn.textContent.trim() === 'All');
        });
      }

      if (prevQuery && typeof gtag === 'function') {
        gtag('event', 'clear_search', {
          previous_search_term: prevQuery,
          active_tab: activeSource
        });
      }

      applyFilters();
    }
'''

# 2. Rewrite applyFilters with Relevance scoring, Newest, Price sorting & Clear integration
new_apply_filters_code = '''    function applyFilters(categorySlug = null) {
      const targetSlug = categorySlug || getActiveCategoryKeyword() || 'all';
      let filtered = [];

      // 1. Scoped Active Tab Pool
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

      // 2. Area / Location filter (Preserved on filter clear)
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

      // 4. Search query filter & relevance calculation
      if (currentSearchQuery) {
        const normQuery = normalizeSearchText(currentSearchQuery);
        const queryTokens = normQuery.split(' ').filter(Boolean);
        if (queryTokens.length > 0) {
          filtered = filtered.filter(item => {
            const target = getItemSearchText(item);
            return queryTokens.every(token => target.includes(token));
          });
          // Attach score for relevance sort
          filtered.forEach(item => {
            item._relevanceScore = calculateRelevanceScore(item, queryTokens, normQuery);
          });
        }
      }

      // 5. Sorting
      const effectiveSort = currentSortOption || (currentSearchQuery ? 'relevance' : 'newest');

      if (effectiveSort === 'relevance' && currentSearchQuery) {
        filtered.sort((a, b) => (b._relevanceScore || 0) - (a._relevanceScore || 0));
      } else if (effectiveSort === 'newest') {
        if (activeSource === 'localshops' && !currentSearchQuery && typeof getBalancedLocalProducts === 'function') {
          filtered = getBalancedLocalProducts(filtered, { context: 'explore-local' });
        } else if ((activeSource === 'marketplaces' || activeSource === 'others') && !currentSearchQuery && typeof getBalancedMarketplaceProducts === 'function') {
          filtered = getBalancedMarketplaceProducts(filtered, { context: 'explore-marketplace' });
        } else {
          filtered.sort((a, b) => {
            const dateA = a.source_published_at ? new Date(a.source_published_at).getTime() : (a.postedAt ? new Date(a.postedAt).getTime() : (typeof a.no === 'number' ? a.no : 0));
            const dateB = b.source_published_at ? new Date(b.source_published_at).getTime() : (b.postedAt ? new Date(b.postedAt).getTime() : (typeof b.no === 'number' ? b.no : 0));
            if (dateA !== dateB) return dateB - dateA;
            return (b.no || 0) - (a.no || 0);
          });
        }
      } else if (effectiveSort === 'price-asc') {
        filtered.sort((a, b) => {
          const priceA = (typeof a.price === 'number' && a.price > 0) ? a.price : ((typeof a.current_price === 'number' && a.current_price > 0) ? a.current_price : null);
          const priceB = (typeof b.price === 'number' && b.price > 0) ? b.price : ((typeof b.current_price === 'number' && b.current_price > 0) ? b.current_price : null);
          if (priceA !== null && priceB !== null) return priceA - priceB;
          if (priceA !== null && priceB === null) return -1;
          if (priceA === null && priceB !== null) return 1;
          return 0;
        });
      } else if (effectiveSort === 'price-desc') {
        filtered.sort((a, b) => {
          const priceA = (typeof a.price === 'number' && a.price > 0) ? a.price : ((typeof a.current_price === 'number' && a.current_price > 0) ? a.current_price : null);
          const priceB = (typeof b.price === 'number' && b.price > 0) ? b.price : ((typeof b.current_price === 'number' && b.current_price > 0) ? b.current_price : null);
          if (priceA !== null && priceB !== null) return priceB - priceA;
          if (priceA !== null && priceB === null) return -1;
          if (priceA === null && priceB !== null) return 1;
          return 0;
        });
      }

      currentFiltered = filtered;
      visibleCount = 40;
      renderGrid(currentFiltered);
      updateLocationCount(filtered.length);
      updateResultsLabel(filtered.length);
      updateSearchUI();
      syncUrlAndSeo();

      // Trigger view_search_results if query active
      if (currentSearchQuery && typeof gtag === 'function') {
        gtag('event', 'view_search_results', {
          search_term: currentSearchQuery,
          active_tab: activeSource,
          result_count: filtered.length
        });
      }
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

# Replace old search state block & applyFilters in explore.html
old_search_pattern = r'\/\/\s*Phase 3C:\s*Explore Search[\s\S]*?function applyFilters\(categorySlug = null\) \{[\s\S]*?updateResultsLabel\(filtered\.length\);\s*updateSearchUI\(\);\s*syncUrlAndSeo\(\);\s*\}'
html = re.sub(old_search_pattern, lambda m: full_search_logic + '\n\n' + new_apply_filters_code, html, count=1)

# 3. Update switchSource to preserve category only if valid in new tab
old_switch_source = r'async function switchSource\(source\) \{[\s\S]*?if \(filterContainer\) \{[\s\S]*?if \(localFilterContainer\) \{[\s\S]*?applyFilters\(getActiveCategoryKeyword\(\)\);\s*\}'
new_switch_source = '''async function switchSource(source) {
      activeSource = source;
      const btnMoonoh = document.getElementById('tab-source-moonoh');
      const btnFoodRescue = document.getElementById('tab-source-foodrescue');
      const btnLocalShops = document.getElementById('tab-source-localshops');
      const btnMarketplaces = document.getElementById('tab-source-marketplaces');

      if (btnMoonoh) btnMoonoh.classList.toggle('active', source === 'moonoh');
      if (btnFoodRescue) btnFoodRescue.classList.toggle('active', source === 'foodrescue');
      if (btnLocalShops) btnLocalShops.classList.toggle('active', source === 'localshops');
      if (btnMarketplaces) btnMarketplaces.classList.toggle('active', source === 'marketplaces' || source === 'others');

      const subtitleLabel = document.getElementById('section-subtitle-label');
      if (subtitleLabel) {
        if (source === 'foodrescue') subtitleLabel.textContent = "Food Rescue";
        else if (source === 'localshops') subtitleLabel.textContent = "Local";
        else if (source === 'marketplaces' || source === 'others') subtitleLabel.textContent = "Other Marketplaces";
        else subtitleLabel.textContent = "Moonoh Marketplace";
      }

      const foodRescueBanner = document.getElementById("food-rescue-banner");
      if (foodRescueBanner) {
        foodRescueBanner.style.display = source === 'foodrescue' ? 'flex' : 'none';
      }

      const filterContainer = document.getElementById("filter-container");
      const localFilterContainer = document.getElementById("local-filter-container");
      if (filterContainer) {
        filterContainer.style.display = (source === 'foodrescue' || source === 'localshops') ? 'none' : 'flex';
      }
      if (localFilterContainer) {
        localFilterContainer.style.display = source === 'localshops' ? 'flex' : 'none';
      }

      // Lazy load data for respective tabs
      if (source === 'localshops') {
        await preloadLocalShopsItems();
      } else if (source === 'foodrescue') {
        await preloadFoodRescueItems();
      } else if (source === 'marketplaces' || source === 'others') {
        await preloadExternalItems();
      }

      // Update Search placeholder for new tab
      updateSearchUI();
      applyFilters();
    }'''

html = re.sub(old_switch_source, lambda m: new_switch_source, html, count=1)

# 4. Wire up Events: 250ms debounce, Escape, Enter, Clear Filters, Sort Change, Popstate
new_event_wiring = '''
    // =========================================================================
    // Search, Clear & Sort Event Listeners
    // =========================================================================
    const searchInputEl = document.getElementById('explore-search-input');
    const searchClearEl = document.getElementById('explore-search-clear');
    const sortSelectEl = document.getElementById('explore-sort-select');
    const clearAllBtnEl = document.getElementById('btn-clear-all-filters');

    if (searchInputEl) {
      searchInputEl.addEventListener('input', (e) => {
        const val = e.target.value;
        if (searchClearEl) searchClearEl.style.display = val ? 'flex' : 'none';

        if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
          currentSearchQuery = val.trim();
          if (!userHasExplicitSort) {
            currentSortOption = currentSearchQuery ? 'relevance' : 'newest';
          }
          if (currentSearchQuery && typeof gtag === 'function') {
            gtag('event', 'search', {
              search_term: currentSearchQuery,
              active_tab: activeSource,
              result_count: currentFiltered.length
            });
          }
          applyFilters();
        }, 250);
      });

      searchInputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          clearSearchQueryOnly();
        } else if (e.key === 'Enter') {
          if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
          currentSearchQuery = searchInputEl.value.trim();
          if (!userHasExplicitSort) {
            currentSortOption = currentSearchQuery ? 'relevance' : 'newest';
          }
          applyFilters();
        }
      });
    }

    if (searchClearEl) {
      searchClearEl.addEventListener('click', clearSearchQueryOnly);
    }

    if (clearAllBtnEl) {
      clearAllBtnEl.addEventListener('click', clearAllFilters);
    }

    if (sortSelectEl) {
      sortSelectEl.addEventListener('change', (e) => {
        userHasExplicitSort = true;
        currentSortOption = e.target.value;
        if (typeof gtag === 'function') {
          gtag('event', 'sort_results', {
            sort_value: currentSortOption,
            active_tab: activeSource,
            result_count: currentFiltered.length
          });
        }
        applyFilters();
      });
    }

    // Handle browser back/forward popstate
    window.addEventListener('popstate', (e) => {
      try {
        const params = new URLSearchParams(window.location.search);
        
        // Restore Tab
        const tabParam = params.get('tab');
        if (tabParam) {
          activeSource = (tabParam === 'local') ? 'localshops' : tabParam;
        } else {
          activeSource = 'moonoh';
        }

        // Restore Search Query
        currentSearchQuery = params.get('q') || '';
        
        // Restore Sort
        if (params.has('sort')) {
          currentSortOption = params.get('sort');
          userHasExplicitSort = true;
        } else {
          currentSortOption = currentSearchQuery ? 'relevance' : 'newest';
          userHasExplicitSort = false;
        }

        // Restore Location
        const areaParam = params.get('area');
        const locSelect = document.getElementById('location-select');
        if (locSelect) {
          locSelect.value = areaParam || '';
          activeTown = areaParam || '';
        }

        switchSource(activeSource);
      } catch (err) {}
    });

    // Parse initial URL parameters on page load
    try {
      const initialParams = new URLSearchParams(window.location.search);
      if (initialParams.has('tab')) {
        const t = initialParams.get('tab');
        activeSource = (t === 'local') ? 'localshops' : t;
      }
      if (initialParams.has('q')) {
        currentSearchQuery = initialParams.get('q') || '';
      }
      if (initialParams.has('sort')) {
        currentSortOption = initialParams.get('sort');
        userHasExplicitSort = true;
      } else {
        currentSortOption = currentSearchQuery ? 'relevance' : 'newest';
        userHasExplicitSort = false;
      }
      if (initialParams.has('area')) {
        activeTown = initialParams.get('area') || '';
        const locSelect = document.getElementById('location-select');
        if (locSelect) locSelect.value = activeTown;
      }
      updateSearchUI();
    } catch (err) {}
'''

# Replace old event listeners with new_event_wiring
old_event_pattern = r'\/\/\s*Phase 3C Event Listeners[\s\S]*?updateSearchUI\(\);\s*\}\s*catch\s*\(err\)\s*\{\}'
html = re.sub(old_event_pattern, lambda m: new_event_wiring, html, count=1)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ Saved explore.html with complete search, sort, clear, URL state & analytics logic")
