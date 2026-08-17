import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix switchSource duplicate closing braces / try-catch
old_switch_source = '''      // Update Search placeholder for new tab
      updateSearchUI();
      applyFilters();
    } catch (e) {}
    }'''

new_switch_source = '''      // Update Search placeholder for new tab
      updateSearchUI();
      applyFilters();
    }'''

if old_switch_source in html:
    html = html.replace(old_switch_source, new_switch_source)
    print("✅ Fixed switchSource duplicate closing braces")

# Fix More Categories button logic in initAll
more_btn_fix_old = '''      const btnMore = document.getElementById("btn-more-categories");
      const btnMoreText = document.getElementById("btn-more-text");
      const filterContainer = document.getElementById("filter-container");
      if (btnMore && filterContainer) {
        btnMore.addEventListener("click", function() {
          const isExpanded = filterContainer.classList.toggle("is-expanded");
          if (btnMoreText) btnMoreText.textContent = isExpanded ? "Less" : "More Categories";
        });
      }'''

more_btn_fix_new = '''      const btnMore = document.getElementById("filter-pill-more");
      const btnMoreText = document.getElementById("filter-pill-more-text");
      const filterContainer = document.getElementById("filter-container");
      if (btnMore && filterContainer) {
        btnMore.addEventListener("click", function(e) {
          e.preventDefault();
          const isExpanded = filterContainer.classList.toggle("is-expanded");
          btnMore.setAttribute("aria-expanded", isExpanded ? "true" : "false");
          if (btnMoreText) btnMoreText.textContent = isExpanded ? "Less" : "More";
          const icon = btnMore.querySelector(".filter-more-icon");
          if (icon) {
            icon.style.transform = isExpanded ? "rotate(180deg)" : "rotate(0deg)";
          }
        });
      }'''

if more_btn_fix_old in html:
    html = html.replace(more_btn_fix_old, more_btn_fix_new)
    print("✅ Fixed More Categories button listener")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Applied all interactivity fixes to explore.html")
