with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

handler = '''
export default async (req, context) => {
  const combined = [...realKarrotItems, ...realHeyKoreanItems];
  return new Response(JSON.stringify(combined), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=0, must-revalidate, s-maxage=0"
    }
  });
};
'''

if 'export default async' not in code:
    code = code.strip() + '\n' + handler
    with open('netlify/functions/external-items.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ Appended default export handler to netlify/functions/external-items.mjs")
else:
    print("Export handler already present")
