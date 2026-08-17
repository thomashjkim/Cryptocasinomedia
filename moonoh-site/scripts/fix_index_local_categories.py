with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the pill listener section in index.html
old_pills_logic = '''      document.querySelectorAll('.filter-pill:not(.filter-pill-more)').forEach(btn => {
        btn.addEventListener('click', function() {
          // Toggle active state
          document.querySelectorAll('.filter-pill:not(.filter-pill-more)').forEach(b => b.classList.remove('active'));
          this.classList.add('active');

          const label = this.textContent.trim();
          const keyword = categoryMap[label];

          const currentLoc = locationSelect ? locationSelect.value.toLowerCase() : '';
          filterAndRender(currentLoc, keyword);
        });
      });'''

new_pills_logic = '''      // Main Category Pills (Moonoh & Marketplaces)
      document.querySelectorAll('#filter-container .filter-pill:not(.filter-pill-more)').forEach(btn => {
        btn.addEventListener('click', function() {
          document.querySelectorAll('#filter-container .filter-pill:not(.filter-pill-more)').forEach(b => b.classList.remove('active'));
          this.classList.add('active');

          const label = this.textContent.trim();
          const keyword = categoryMap[label];

          const currentLoc = locationSelect ? locationSelect.value.toLowerCase() : '';
          filterAndRender(currentLoc, keyword);
        });
      });

      // Local Shop Category Pills (Local Tab)
      document.querySelectorAll('#local-filter-container .filter-pill').forEach(btn => {
        btn.addEventListener('click', function() {
          document.querySelectorAll('#local-filter-container .filter-pill').forEach(b => b.classList.remove('active'));
          this.classList.add('active');

          activeLocalCategory = this.getAttribute('data-local-cat') || 'All';
          const currentLoc = locationSelect ? locationSelect.value.toLowerCase() : '';
          filterAndRender(currentLoc, null);
        });
      });'''

html = html.replace(old_pills_logic, new_pills_logic)

# Ensure activeLocalCategory is defined at top of setupFilters
if 'let activeLocalCategory = ' not in html:
    html = html.replace("let activeSource = 'moonoh';", "let activeSource = 'moonoh';\n    let activeLocalCategory = 'All';")

# Reset activeLocalCategory when switching source in switchSource
if 'activeLocalCategory = \'All\';' not in html:
    html = html.replace(
        "if (localFilterContainer) {\n          localFilterContainer.style.display = (source === 'localshops') ? 'flex' : 'none';\n        }",
        "if (localFilterContainer) {\n          localFilterContainer.style.display = (source === 'localshops') ? 'flex' : 'none';\n          if (source === 'localshops') {\n            activeLocalCategory = 'All';\n            document.querySelectorAll('#local-filter-container .filter-pill').forEach(b => b.classList.toggle('active', b.getAttribute('data-local-cat') === 'All'));\n          }\n        }"
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Saved index.html with clean Local category filtering logic!")
