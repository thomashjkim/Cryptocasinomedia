import re
import json

# 1. Update local_shops_data.json
with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if "shops" in data and "salter-house" in data["shops"]:
    data["shops"]["salter-house"]["theme_color"] = "#007a51"
    print("✅ Updated salter-house theme_color to #007a51 in local_shops_data.json")

# Also check if any items have theme_color
if "items" in data:
    for item in data["items"]:
        if item.get("shop_id") == "salter-house" or item.get("source") == "salter-house":
            item["theme_color"] = "#007a51"

with open('local_shops_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 2. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    explore_html = f.read()

explore_html = re.sub(
    r'\.badge-salter\s*\{[\s\S]*?\}',
    '''.badge-salter {
      background-color: #E6F5F0;
      color: #007a51;
      border: 1px solid #99D6C4;
    }''',
    explore_html
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(explore_html)
print("✅ Updated .badge-salter in explore.html")

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

index_html = re.sub(
    r'\.badge-salter\s*\{[\s\S]*?\}',
    '''.badge-salter {
      background-color: #E6F5F0;
      color: #007a51;
      border: 1px solid #99D6C4;
    }''',
    index_html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("✅ Updated .badge-salter in index.html")

# 4. Update import_local_shops.py if present
try:
    with open('import_local_shops.py', 'r', encoding='utf-8') as f:
        import_py = f.read()
    import_py = import_py.replace('"theme_color": "#05452E"', '"theme_color": "#007a51"')
    import_py = import_py.replace('"theme_color": "#4A6B53"', '"theme_color": "#007a51"')
    with open('import_local_shops.py', 'w', encoding='utf-8') as f:
        f.write(import_py)
    print("✅ Updated import_local_shops.py")
except Exception as e:
    pass
