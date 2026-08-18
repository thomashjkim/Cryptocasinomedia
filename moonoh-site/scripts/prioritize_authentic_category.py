with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''function inferCategoryFromText(title = '', description = '', rawCategory = '') {
  const text = (title + ' ' + (description || '')).toLowerCase();
  const raw = (rawCategory || '').toLowerCase().trim();'''

replacement = '''function inferCategoryFromText(title = '', description = '', rawCategory = '') {
  const text = (title + ' ' + (description || '')).toLowerCase();
  const raw = (rawCategory || '').toLowerCase().trim();

  // If rawCategory is explicitly provided and not generic, prioritize it
  if (raw && !['used items', 'other', 'general', ''].includes(raw)) {
    const standardCategories = [
      'Electronics & appliances', 'Furniture', "Women's & Men's Fashion", 'Shoes', 'Baby & kids',
      'Sports & leisure', 'Luggages & bags', 'Food & Groceries', 'Pet supplies', 'Health & beauty',
      'Antiques & collections', 'Arts, books, music, movies & tickets', 'Jewelry & watches',
      'Coffee & Pantry', 'Vintage & Fashion', 'Home & Objects', 'Gifts & Culture', 'Free'
    ];
    const match = standardCategories.find(c => c.toLowerCase() === raw || raw.includes(c.toLowerCase()) || c.toLowerCase().includes(raw));
    if (match) return match;
    return rawCategory;
  }'''

code = code.replace(target, replacement)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Updated inferCategoryFromText to prioritize authentic categoryName")
