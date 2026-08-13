import json

with open('real_external_items.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

hk_items = data['heykorean']
kr_items = data['karrot']

# Format JS array content
js_content = f"""// netlify/functions/external-items.mjs
// Serves REAL live scraped external listings from Karrot and HeyKorean with translated English titles and real seller photo URLs.

export const realKarrotItems = {json.dumps(kr_items, ensure_ascii=False, indent=2)};
export const realHeyKoreanItems = {json.dumps(hk_items, ensure_ascii=False, indent=2)};

let cachedCombined = null;

export default async (req, context) => {{
  if (!cachedCombined) {{
    const combined = [];
    const maxLen = Math.max(realKarrotItems.length, realHeyKoreanItems.length);
    for (let i = 0; i < maxLen; i++) {{
      if (i < realKarrotItems.length) combined.push(realKarrotItems[i]);
      if (i < realHeyKoreanItems.length) combined.push(realHeyKoreanItems[i]);
    }}
    cachedCombined = combined;
  }}

  return new Response(JSON.stringify(cachedCombined), {{
    status: 200,
    headers: {{
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=300, s-maxage=600"
    }}
  }});
}};
"""

with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated external-items.mjs with REAL scraped items and photos!")
