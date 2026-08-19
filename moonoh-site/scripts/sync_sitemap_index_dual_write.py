with open('build_all_sitemaps.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
    f.write('\\n'.join(xml_index))'''

replacement = '''with open('sitemap-index.xml', 'w', encoding='utf-8') as f:
    f.write('\\n'.join(xml_index))

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\\n'.join(xml_index))'''

if target in code:
    code = code.replace(target, replacement)
    with open('build_all_sitemaps.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ build_all_sitemaps.py updated to write both sitemap-index.xml and sitemap.xml")
else:
    print("Already updated or target not found")
