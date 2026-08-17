import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

food_rescue_func = '''
    async function preloadFoodRescueItems() {
      if (foodRescueItemsList.length > 0) return;
      try {
        let res = await fetch('/api/food-rescue');
        if (!res.ok) res = await fetch('/.netlify/functions/food-rescue-items');
        const data = await res.json();
        foodRescueItemsList = (Array.isArray(data) ? data : []).map(r => ({
          no: r.id,
          id: r.id,
          title: r.title,
          price: r.price,
          image: r.image,
          photo: r.image,
          location: r.location || '1mi · Brooklyn, NY',
          rawTown: r.rawTown || 'Brooklyn, NY',
          townName: 'Brooklyn, NY',
          category: r.categoryName || 'Food & Groceries',
          categoryName: r.categoryName || 'Food & Groceries',
          source: 'kimc',
          badgeName: "Kim'C Market",
          url: `/item/${r.handle || 'item'}-brooklyn-ny-ext-${r.id}`
        }));
        if (activeSource === 'foodrescue') applyFilters();
      } catch (e) {
        console.error("Error loading food rescue items:", e);
      }
    }
'''

if 'function preloadFoodRescueItems' not in html:
    html = html.replace('async function preloadExternalItems() {', food_rescue_func + '\n    async function preloadExternalItems() {')

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Added preloadFoodRescueItems to explore.html")
