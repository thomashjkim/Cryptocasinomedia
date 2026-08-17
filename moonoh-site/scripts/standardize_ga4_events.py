import re

# 1. Update netlify/functions/item-detail.mjs
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace click_external_source with full clean parameters (item_id, item_name, source, store_name, destination_url)
code = re.sub(
    r"onclick=\"if\(typeof gtag==='function'\)gtag\('event','click_external_source',\{source:'\${externalSource}',item_url:'\${externalUrl}'\}\);\"",
    r"""onclick="if(typeof gtag==='function')gtag('event','click_external_source',{item_id:'${productNo}',item_name:'${title.replace(/'/g, \"\\\\'\")}',source:'${externalSource}',store_name:'${sourceDisplayName}',destination_url:'${externalUrl}'});" """,
    code
)

# Replace click_buy_chat with contact_seller (Key Event)
code = re.sub(
    r"onclick=\"if\(typeof gtag==='function'\)gtag\('event','click_buy_chat',\{item_id:'\${productNo}'\}\);\"",
    r"""onclick="if(typeof gtag==='function')gtag('event','contact_seller',{item_id:'${productNo}',item_name:'${title.replace(/'/g, \"\\\\'\")}',location:'${townName}',category:'${categoryName}'});" """,
    code
)

# Replace click_app_store and click_google_play with open_in_app (Key Event)
code = re.sub(
    r"onclick=\"if\(typeof gtag==='function'\)gtag\('event','click_app_store',\{platform:'ios'\}\);\"",
    r"""onclick="if(typeof gtag==='function')gtag('event','open_in_app',{source:'ios',destination_url:'https://apps.apple.com/us/app/moonoh/id6477390079'});" """,
    code
)
code = re.sub(
    r"onclick=\"if\(typeof gtag==='function'\)gtag\('event','click_google_play',\{platform:'android'\}\);\"",
    r"""onclick="if(typeof gtag==='function')gtag('event','open_in_app',{source:'android',destination_url:'https://play.google.com/store/apps/details?id=com.moonoh'});" """,
    code
)

# Claim store modal click
code = re.sub(
    r"onclick=\"openClaimModal\(\)\"",
    r"""onclick="if(typeof gtag==='function')gtag('event','claim_business_click',{store_name:'${sourceDisplayName}',destination_url:'/contact?claim=true'});openClaimModal();" """,
    code
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ Standardized GA4 events in item-detail.mjs")

# 2. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

# Update Navbar Download app button to fire open_in_app
exp_html = re.sub(
    r'<a href="https:\/\/apps\.apple\.com\/us\/app\/moonoh\/id6477390079" target="_blank" class="navbar-button w-nav-link">',
    r'<a href="https://apps.apple.com/us/app/moonoh/id6477390079" target="_blank" class="navbar-button w-nav-link" onclick="if(typeof gtag===\'function\')gtag(\'event\',\'open_in_app\',{source:\'navbar_cta\',destination_url:\'https://apps.apple.com/us/app/moonoh/id6477390079\'});">',
    exp_html
)

# Update Card Click in renderGrid to fire select_search_result if search is active
card_click_replacement = '''
        const clickAttr = `href="${extSlug}" onclick="if(currentSearchQuery && typeof gtag==='function')gtag('event','select_search_result',{item_id:'${item.no || item.id || ''}',item_name:'${itemTitle.replace(/'/g, "\\\\'")}',search_term:currentSearchQuery,tab_name:activeSource,category:'${item.category || item.categoryName || ''}',source:'${item.source || 'moonoh'}'});"`;
'''

exp_html = re.sub(r'const clickAttr = `href="\${extSlug}"`;', card_click_replacement, exp_html, count=1)

# Ensure event parameters match user specification
exp_html = exp_html.replace("active_tab: activeSource", "tab_name: activeSource")
exp_html = exp_html.replace("sort_value: currentSortOption", "sort_method: currentSortOption")
exp_html = exp_html.replace("previous_search_term: prevQuery", "search_term: prevQuery")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp_html)
print("✅ Standardized GA4 events in explore.html")

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

# Update Navbar Download app button to fire open_in_app
idx_html = re.sub(
    r'<a href="https:\/\/apps\.apple\.com\/us\/app\/moonoh\/id6477390079" target="_blank" class="navbar-button w-nav-link">',
    r'<a href="https://apps.apple.com/us/app/moonoh/id6477390079" target="_blank" class="navbar-button w-nav-link" onclick="if(typeof gtag===\'function\')gtag(\'event\',\'open_in_app\',{source:\'navbar_cta\',destination_url:\'https://apps.apple.com/us/app/moonoh/id6477390079\'});">',
    idx_html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_html)
print("✅ Standardized GA4 events in index.html")
