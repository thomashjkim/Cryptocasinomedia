with open('netlify/functions/explore.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

new_cats = '''  'food-groceries': { slug: 'food-groceries', name: 'Food & Groceries', kw: 'food', keywords: ['food', 'groceries', 'snack', 'sauce', 'oil', 'rice', 'tea', 'noodle', 'kimchi', 'pantry', 'drink', 'beverage', 'korean food', 'cookie', 'juice', 'chip'] },
  'coffee-pantry': { slug: 'coffee-pantry', name: 'Coffee & Pantry', kw: 'coffee', keywords: ['coffee', 'pantry', 'tea', 'beans', 'roast', 'olive oil', 'syrup', 'snack'] },
  'vintage-fashion': { slug: 'vintage-fashion', name: 'Vintage & Fashion', kw: 'vintage', keywords: ['vintage', 'fashion', 'clothing', 'jacket', 'denim', 'dress', 'belt', 'leather'] },
  'home-objects': { slug: 'home-objects', name: 'Home & Objects', kw: 'home', keywords: ['home', 'objects', 'glass', 'dish', 'ceramic', 'candle', 'linen', 'plate', 'towel'] },
  'gifts-culture': { slug: 'gifts-culture', name: 'Gifts & Culture', kw: 'gifts', keywords: ['gifts', 'culture', 'book', 'stationery', 'print', 'card', 'poster'] },'''

code = code.replace(
    "'food-groceries': { slug: 'food-groceries', name: 'Food & Groceries', kw: 'food', keywords: ['food', 'groceries', 'snack', 'sauce', 'oil', 'rice', 'tea', 'noodle', 'kimchi', 'pantry', 'drink', 'beverage', 'korean food', 'cookie', 'juice', 'chip'] },",
    new_cats
)

with open('netlify/functions/explore.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Added local shop categories to explore.mjs CATEGORIES map")
