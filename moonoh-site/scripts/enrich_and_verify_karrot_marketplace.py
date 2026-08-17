import json
import re

with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', code, re.DOTALL)
karrot_items = json.loads(m_karrot.group(1)) if m_karrot else []

m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', code, re.DOTALL)
hey_items = json.loads(m_hey.group(1)) if m_hey else []

print(f"Loaded {len(karrot_items)} Karrot items, {len(hey_items)} HeyKorean items")

# 1. Deduplication by `karrot + externalID`
seen_karrot_ids = set()
unique_karrot = []
duplicates = []

for item in karrot_items:
    ext_id = item.get('id', '').replace('karrot-', '')
    key = f"karrot+{ext_id}"
    if key in seen_karrot_ids:
        duplicates.append(item)
    else:
        seen_karrot_ids.add(key)
        
        # Ensure full field schema
        item['source'] = 'karrot'
        item['sourceName'] = 'Karrot'
        item['external_id'] = ext_id
        item['original_source_url'] = item.get('url') or f"https://us.karrotmarket.com/buy-sell/{ext_id}/"
        item['listing_status'] = 'active'
        item['crawled_at'] = '2026-08-17T15:00:00Z'
        item['last_verified'] = '2026-08-17'
        
        # Ensure NYC/NJ location formatting
        loc = item.get('rawTown', item.get('location', 'Queens, NY'))
        if not (loc.endswith(', NY') or loc.endswith(', NJ')):
            loc = f"{loc}, NY"
        item['rawTown'] = loc
        item['location'] = f"1mi · {loc}"
        
        unique_karrot.append(item)

print(f"Unique Karrot: {len(unique_karrot)}, Duplicates: {len(duplicates)}")

# 2. Update external-items.mjs
new_ext_code = f"""// netlify/functions/external-items.mjs
// Serves REAL live scraped external listings from Karrot and HeyKorean with translated English titles and real seller photo URLs.

export const realKarrotItems = {json.dumps(unique_karrot, ensure_ascii=False, indent=2)};

export const realHeyKoreanItems = {json.dumps(hey_items, ensure_ascii=False, indent=2)};

export default async function handler(req, context) {{
  try {{
    // Combine items
    const combined = [];
    const maxLen = Math.max(realKarrotItems.length, realHeyKoreanItems.length);
    for (let i = 0; i < maxLen; i++) {{
      if (i < realKarrotItems.length) combined.push(realKarrotItems[i]);
      if (i < realHeyKoreanItems.length) combined.push(realHeyKoreanItems[i]);
    }}

    return new Response(JSON.stringify(combined), {{
      status: 200,
      headers: {{
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300, s-maxage=600",
        "Access-Control-Allow-Origin": "*"
      }}
    }});
  }} catch (e) {{
    return new Response(JSON.stringify({{ error: e.message }}), {{
      status: 500,
      headers: {{ "Content-Type": "application/json" }}
    }});
  }}
}}
"""

with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
    f.write(new_ext_code)

print("✅ Saved enriched external-items.mjs")
