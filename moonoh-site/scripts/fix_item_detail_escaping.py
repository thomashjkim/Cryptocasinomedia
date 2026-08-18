with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix escaping in line 25461
code = code.replace(
    'style="background:${btnBgColor}; color:${btnTextColor || \\\'#FFFFFF\\\'};"',
    'style="background:${btnBgColor}; color:${btnTextColor || "#FFFFFF"};"'
)
code = code.replace(
    'if(typeof gtag===\\\'function\\\')gtag(\\\'event\\\',\\\'click_external_source\\\',{item_id:\\\'${productNo}\\\',item_name:${JSON.stringify(title)},source:\\\'${externalSource}\\\',store_name:\\\'${sourceDisplayName}\\\',destination_url:\\\'${externalUrl}\\\'});',
    "if(typeof gtag==='function')gtag('event','click_external_source',{item_id:'${productNo}',item_name:${JSON.stringify(title)},source:'${externalSource}',store_name:'${sourceDisplayName}',destination_url:'${externalUrl}'});"
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Fixed quote escaping in item-detail.mjs")
