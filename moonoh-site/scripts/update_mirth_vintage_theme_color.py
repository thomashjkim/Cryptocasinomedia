import re
import json

# 1. Update local_shops_data.json
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if "shops" in data and "mirth-vintage" in data["shops"]:
    data["shops"]["mirth-vintage"]["theme_color"] = "#000000"
    data["shops"]["mirth-vintage"]["badge_theme"] = {
        "bg": "#F3F4F6",
        "color": "#000000",
        "border": "#000000"
    }
    print("✅ Updated mirth-vintage theme_color to #000000 in local_shops_data.json")

# Also check if any items have theme_color
if "items" in data:
    for item in data["items"]:
        if item.get("shop_id") == "mirth-vintage" or item.get("source") == "mirth-vintage":
            item["theme_color"] = "#000000"

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 2. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    explore_html = f.read()

explore_html = re.sub(
    r'\.badge-mirth\s*\{[\s\S]*?\}',
    '''.badge-mirth {
      background-color: #F3F4F6;
      color: #000000;
      border: 1px solid #000000;
    }''',
    explore_html
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(explore_html)
print("✅ Updated .badge-mirth in explore.html")

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

index_html = re.sub(
    r'\.badge-mirth\s*\{[\s\S]*?\}',
    '''.badge-mirth {
      background-color: #F3F4F6;
      color: #000000;
      border: 1px solid #000000;
    }''',
    index_html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated .badge-mirth in index.html")

# 4. Update import_local_shops.py if present
try:
    with open('import_local_shops.py', 'r', encoding='utf-8') as f:
        import_py = f.read()
    import_py = import_py.replace('"theme_color": "#B8860B"', '"theme_color": "#000000"')
    with open('import_local_shops.py', 'w', encoding='utf-8') as f:
        f.write(import_py)
    print("✅ Updated import_local_shops.py")
except Exception as e:
    pass
