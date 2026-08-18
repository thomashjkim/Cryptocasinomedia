with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

target = '    // Determine exact source context and breadcrumb links\n    if (localProductMatch) {'
replacement = '''    // Determine exact source context and breadcrumb links
    let currentSourceKey = 'moonoh';
    let fallbackExploreUrl = '/explore?source=moonoh';
    let breadcrumbHtml = '';
    if (localProductMatch) {'''

code = code.replace(target, replacement)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Declared currentSourceKey, fallbackExploreUrl, and breadcrumbHtml")
