import glob
import re
import os

html_files = glob.glob("*.html")

# 1. Update Navigation across all files
for f in html_files:
    try:
        with open(f, "r") as file:
            content = file.read()
            
        nav_target = """<nav role="navigation" class="navbar-menu w-nav-menu">
          <a href="/about" class="navbar-link w-nav-link">About</a>"""
          
        new_nav = """<nav role="navigation" class="navbar-menu w-nav-menu">
          <a href="/explore" class="navbar-link w-nav-link">Explore</a>
          <a href="/about" class="navbar-link w-nav-link">About</a>"""
          
        if nav_target in content:
            content = content.replace(nav_target, new_nav)
            with open(f, "w") as file:
                file.write(content)
            print(f"Updated nav in {f}")
    except Exception as e:
        print(f"Error in {f}: {e}")

# 2. Update index.html CSS, HTML, and JS for Karrot UI
try:
    with open("index.html", "r") as file:
        content = file.read()
    
    # 2a. Update CSS
    old_css = """
    .item-card {
      background: #FFFFFF;
      border: 1px solid #EBEBEB;
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      display: flex;
      flex-direction: column;
    }
    .item-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(0,0,0,0.08);
    }
    .item-card-image {
      width: 100%;
      aspect-ratio: 1 / 1;
      background-color: #F3F4F6;
      object-fit: cover;
    }
    .item-card-content {
      padding: 12px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }
    .item-card-price {
      font-weight: 800;
      font-size: 16px;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .item-card-title {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }"""
    
    new_css = """
    .item-card {
      background: transparent;
      border: none;
      cursor: pointer;
      transition: transform 0.2s ease;
      display: flex;
      flex-direction: column;
    }
    .item-card:hover {
      transform: translateY(-4px);
    }
    .item-card-image {
      width: 100%;
      aspect-ratio: 1 / 1;
      background-color: #F3F4F6;
      object-fit: cover;
      border-radius: 12px;
    }
    .item-card-content {
      padding: 12px 4px 0 4px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }
    .item-card-price {
      font-weight: 800;
      font-size: 18px;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .item-card-title {
      font-size: 15px;
      color: var(--text-main);
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      margin-bottom: 4px;
    }
    .item-card-location {
      font-size: 13px;
      color: #717171;
    }
    
    /* Filter Pills */
    .filter-container {
      display: flex;
      overflow-x: auto;
      gap: 12px;
      padding-bottom: 12px;
      margin-bottom: 24px;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .filter-container::-webkit-scrollbar {
      display: none;
    }
    .filter-pill {
      white-space: nowrap;
      padding: 10px 18px;
      border-radius: 12px;
      font-size: 14px;
      font-weight: 600;
      color: #111;
      background-color: #F3F4F6;
      border: none;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    .filter-pill.active {
      background-color: #222;
      color: #FFF;
    }
    .filter-pill:hover:not(.active) {
      background-color: #E5E7EB;
    }"""
    
    if old_css in content:
        content = content.replace(old_css, new_css)
        print("Updated CSS in index.html")
    else:
        print("old_css not found in index.html")

    # 2b. Update HTML (Add Filters)
    old_html = """      <h2 class="item-feed-title">Recently Listed in Your Neighborhood</h2>
      <div class="item-grid" id="moonoh-item-grid">"""
      
    new_html = """      <h2 class="item-feed-title" style="margin-bottom: 16px;">Buy and sell used items in your neighborhood</h2>
      <div class="filter-container">
        <button class="filter-pill active">All</button>
        <button class="filter-pill">Furniture</button>
        <button class="filter-pill">Electronics & Appliances</button>
        <button class="filter-pill">Women's Fashion</button>
        <button class="filter-pill">Men's Fashion</button>
        <button class="filter-pill">Vehicles & Parts</button>
        <button class="filter-pill">Rentals</button>
        <button class="filter-pill">Home & Garden</button>
        <button class="filter-pill">More ></button>
      </div>
      <div class="item-grid" id="moonoh-item-grid">"""
      
    if old_html in content:
        content = content.replace(old_html, new_html)
        print("Updated HTML Filters in index.html")
    else:
        print("old_html not found in index.html")

    # 2c. Update JS (Mock Data Generator - Add Location and change order: Price -> Title -> Location)
    old_js = """        items.push({
          id: i,
          title: mockTitles[Math.floor(Math.random() * mockTitles.length)],
          price: "$" + Math.floor(Math.random() * 300 + 10),
          image: mockImages[Math.floor(Math.random() * mockImages.length)]
        });"""
        
    new_js = """        const locations = ["3mi · Manhattan", "5mi · Flushing", "2mi · Astoria", "8mi · Jersey City", "1mi · Brooklyn Heights", "12mi · Hoboken", "4mi · Williamsburg"];
        items.push({
          id: i,
          title: mockTitles[Math.floor(Math.random() * mockTitles.length)],
          price: "$" + Math.floor(Math.random() * 300 + 10),
          image: mockImages[Math.floor(Math.random() * mockImages.length)],
          location: locations[Math.floor(Math.random() * locations.length)]
        });"""
        
    old_render = """              <div class="item-card-price">${item.price}</div>
              <div class="item-card-title">${item.title}</div>
            </div>"""
            
    new_render = """              <div class="item-card-price">${item.price}</div>
              <div class="item-card-title">${item.title}</div>
              <div class="item-card-location">${item.location}</div>
            </div>"""
            
    if old_js in content:
        content = content.replace(old_js, new_js)
        print("Updated JS Mock Data in index.html")
    else:
        print("old_js not found in index.html")
    
    if old_render in content:
        content = content.replace(old_render, new_render)
        print("Updated JS Render in index.html")
    else:
        print("old_render not found in index.html")
        
    with open("index.html", "w") as file:
        file.write(content)

except Exception as e:
    print(f"Error editing index.html: {e}")

# 3. Create explore.html from index.html
try:
    with open("index.html", "r") as file:
        explore_content = file.read()
        
    # Remove Hero Section
    hero_pattern = re.compile(r"<div class=\"hero-heading-left\">.*?</div>\n    </div>", re.DOTALL)
    explore_content = re.sub(hero_pattern, "", explore_content)
    
    # Remove Summary Box
    tldr_pattern = re.compile(r"<!-- Summary Block.*?</div>", re.DOTALL)
    explore_content = re.sub(tldr_pattern, "", explore_content)
    
    # Remove How Moonoh Works
    team_pattern = re.compile(r"<!-- How moonoh works.*?</div>\n    </div>", re.DOTALL)
    explore_content = re.sub(team_pattern, "", explore_content)
    
    # Remove Comparison Section
    comp_pattern = re.compile(r"<!-- Comparison Table.*?</section>", re.DOTALL)
    explore_content = re.sub(comp_pattern, "", explore_content)
    
    # Remove FAQ Section
    faq_pattern = re.compile(r"<!-- FAQ Section.*?</section>", re.DOTALL)
    explore_content = re.sub(faq_pattern, "", explore_content)
    
    # Change Title to Explore
    explore_content = explore_content.replace("<title>moonoh – NYC & NJ Neighborhood Marketplace App | Buy & Sell Locally</title>", "<title>Explore Items | moonoh</title>")
    
    # Increase item count to 200
    explore_content = explore_content.replace("generateMockItems(50)", "generateMockItems(200)")
    
    # Fix the spacing/margin for the item feed on explore page since it doesn't have hero above it
    explore_content = explore_content.replace("margin: 64px auto !important;", "margin: 96px auto 64px auto !important;")
    
    with open("explore.html", "w") as file:
        file.write(explore_content)
    print("Created explore.html")

except Exception as e:
    print(f"Error creating explore.html: {e}")
