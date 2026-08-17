import json
import re

with open('local_shops_data.json', 'r', encoding='utf-8') as f:
    local_db = json.load(f)

hg_products = [p for p in local_db['products'] if p['shop_id'] == 'happier-grocery']

def clean_title_to_slug(title, brand=''):
    t = title.lower()
    # Replace special characters, apostrophes, ampersands
    t = t.replace("'", "").replace('"', '').replace('&', 'and').replace('+', 'plus').replace('%', 'percent')
    t = re.sub(r'[^a-z0-9]+', '-', t)
    t = re.sub(r'-+', '-', t).strip('-')
    return t

used_slugs = set()
audit_results = []

for idx, p in enumerate(hg_products):
    source_id = p['source_product_id']
    official_title = p['title']
    current_slug = p['slug']
    current_url = f"https://moon-oh.com/local-product/happier-grocery/{current_slug}"
    
    expected_slug = clean_title_to_slug(official_title)
    if expected_slug in used_slugs:
        expected_slug = f"{expected_slug}-{source_id.replace('hg-', '')[:6]}"
    used_slugs.add(expected_slug)
    
    expected_url = f"https://moon-oh.com/local-product/happier-grocery/{expected_slug}"
    
    # Check semantic equivalence between current_slug and official_title
    curr_tokens = set(re.findall(r'[a-z0-9]+', current_slug))
    title_tokens = set(re.findall(r'[a-z0-9]+', clean_title_to_slug(official_title)))
    overlap = curr_tokens.intersection(title_tokens)
    
    if current_slug == expected_slug:
        classification = "SAME_PRODUCT_KEEP"
        final_action = "KEEP_CANONICAL_200"
    elif len(overlap) >= 2 and len(overlap) / len(curr_tokens) > 0.5:
        classification = "SAME_PRODUCT_301"
        final_action = "1_HOP_301_TO_NEW_CANONICAL"
    else:
        classification = "SEMANTIC_MISMATCH_404_OR_410"
        final_action = "OLD_URL_CONTROLLED_404_NEW_CANONICAL_200"
        
    audit_results.append({
        "index": idx + 1,
        "source_product_id": source_id,
        "official_title": official_title,
        "brand": p['brand'],
        "price": p['current_price'],
        "current_slug": current_slug,
        "current_canonical_url": current_url,
        "expected_slug": expected_slug,
        "expected_canonical_url": expected_url,
        "classification": classification,
        "final_action": final_action,
        "old_slug": current_slug,
        "new_slug": expected_slug,
        "image_url": p['image_source_url']
    })

print(f"Audited {len(audit_results)} Happier Grocery records:\n")
counts = {}
for r in audit_results:
    c = r['classification']
    counts[c] = counts.get(c, 0) + 1

for k, v in counts.items():
    print(f"  {k}: {v}")

with open('scripts/happier_slug_audit.json', 'w', encoding='utf-8') as f:
    json.dump(audit_results, f, indent=2)
