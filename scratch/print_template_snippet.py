file_path = "/Users/thomaskim/Cryptocasinomedia/index/index.html.template"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find('if (company.includes("Polymarket")')
if idx != -1:
    print(repr(content[idx:idx+1000]))
else:
    print("Substring not found!")
