import os
import re

def update_file(filepath, limit):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace the JS logic
    # We will find the script block and replace the generateMockItems and renderItems functions.
    
    # Let's find the start of function generateMockItems
    start_idx = content.find("function generateMockItems(count)")
    if start_idx == -1:
        print(f"Skipping {filepath}, generateMockItems not found")
        return
        
    # Find the end of renderItems
    # It ends before "    // Modal Logic" or "function openModal"
    end_idx = content.find("// Modal Logic", start_idx)
    if end_idx == -1:
        end_idx = content.find("function openModal", start_idx)
        
    if end_idx == -1:
        print(f"Could not find end index in {filepath}")
        return
        
    new_js = f"""
    async function renderItems() {{
      const grid = document.getElementById("moonoh-item-grid");
      if (!grid) return;
      
      try {{
        const response = await fetch('data.json');
        let items = await response.json();
        
        // Filter out items without images
        items = items.filter(item => !item.image.includes("ico_profile_empty.png"));
        
        // Limit to {limit} items
        items = items.slice(0, {limit});
        
        let html = "";
        items.forEach(item => {{
          const safeTitle = item.title.replace(/'/g, "\\\\'");
          const priceStr = item.price > 0 ? "$" + item.price.toLocaleString() : "Free";
          html += `
          <div class="item-card" onclick="openModal('${{safeTitle}}')">
            <img src="${{item.image}}" alt="${{item.title}}" class="item-card-image" loading="lazy" onerror="this.src='images/common/ico_profile_empty.png'">
            <div class="item-card-content">
              <div class="item-card-price">${{priceStr}}</div>
              <div class="item-card-title">${{item.title}}</div>
              <div class="item-card-location">${{item.location}}</div>
            </div>
          </div>
          `;
        }});
        grid.innerHTML = html;
      }} catch (e) {{
        console.error("Error loading items:", e);
      }}
    }}

    """
    
    new_content = content[:start_idx] + new_js + content[end_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

update_file("index.html", 50)
update_file("explore.html", 200)

