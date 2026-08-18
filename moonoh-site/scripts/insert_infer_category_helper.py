with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

helper = '''function inferCategoryFromText(title = '', description = '', rawCategory = '') {
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
  }

  // 1. Electronics & Appliances
  if (/\b(macbook|imac|laptop|computer|monitor|iphone|galaxy|ipad|nintendo|ps5|ps4|playstation|xbox|gaming|console|tv|television|camera|printer|scanner|radiator|heater|aircon|air.?conditioner|air.?fryer|microwave|vacuum|refrigerator|fridge|coffee.?maker|coffee.?machine|nespresso|keurig|blender|cooker|calculator|keyboard|ram|router|headphone|airpods|speaker|bluetooth|vr|tablet|kindle|drone|hair.?dryer|hair.?iron|crimper|straightener|curler|curling|wired|electric|led|charger|battery|cable|amplifier|projector)\b|노트북|컴퓨터|모니터|아이폰|아이패드|에어컨|선풍기|히터|히타|청소기|스피커|전자레인지|냉장고|변압기|디바이스|와인셀러/i.test(text)) {
    return 'Electronics & appliances';
  }

  // 2. Pet Supplies
  if (/\b(pet|dog|cat|puppy|kitten|aquarium|leash|collar|crate|kennel|litter|kibble|ecofetch|chuckit)\b|강아지|고양이|반려/i.test(text)) {
    return 'Pet supplies';
  }

  // 3. Health & Beauty
  if (/\b(beauty|cosmetic|cosmetics|perfume|cologne|cream|lotion|soap|facial|brush|makeup|serum|skincare|sunscreen|foundation|lipstick|mascara|eyeshadow|toner|shampoo|conditioner|thermometer|blood.?pressure|massage|eye.?drops|eyedrops|rohto|mentholatum|lycee)\b|화장품|향수|비누|메이크업|브러쉬|스킨케어|안약/i.test(text)) {
    return 'Health & beauty';
  }

  // 4. Sports & Leisure
  if (/\b(ski|snowboard|bmx|bike|bicycle|golf|putter|vokey|driver|treadmill|exercise|dumbbell|sled|inversion.?table|racket|tent|camping|yoga|weights|gym|fishing|surfboard|skateboard|scooter|paddle)\b|자전거|골프|스키|운동|거꾸리|썰매|헬스|라이딩복|런닝머신/i.test(text)) {
    return 'Sports & leisure';
  }

  // 5. Furniture
  if (/\b(chair|chairs|table|tables|desk|desks|bed|beds|daybed|sofa|sofas|couch|dresser|mattress|shelf|shelves|cabinet|stool|stools|nightstand|nighttable|bench|ottoman|bookcase|wardrobe|armchair|recliner|loveseat|futon|hutch|credenza|sectional|media.?console|entertainment.?center|tv.?stand)\b|테이블|의자|소파|침대|책상|서랍|가구|식탁|선반|수납장/i.test(text)) {
    return 'Furniture';
  }

  // 6. Baby & Kids
  if (/\b(baby|kid|kids|toddler|stroller|crib|diaper|toy|toys|lego|gundam|sylvanian|calico.?critters|bassinet|highchair|playpen|car.?seat|infant|newborn|doll|action.?figure|children)\b|유아|아동|유모차|장난감|레고|베시넷/i.test(text)) {
    return 'Baby & kids';
  }

  // 7. Shoes
  if (/\b(shoe|shoes|sneaker|sneakers|boot|boots|sandal|sandals|hunter|nike|adidas|jordan|heel|heels|loafer|pump|pumps|mule|slipper|espadrille|converse|vans|chuck.?taylor|new.?balance|air.?force|yeezy)\b|신발|운동화|구두|부츠|슬리퍼/i.test(text)) {
    return 'Shoes';
  }

  // 8. Luggages & Bags
  if (/\b(bag|bags|backpack|backpacks|luggage|suitcase|tote|purse|handbag|crossbody|duffle|clutch|briefcase|wallet|cardholder|pouch)\b|가방|백팩|캐리어|토트백|핸드백|지갑/i.test(text)) {
    return 'Luggages & bags';
  }

  // 9. Women's Fashion
  if (/\b(dress|skirt|blouse|coat|jacket|bra|lingerie|heels|earring|necklace|bracelet|jewelry|leggings|cardigan|sweater|hoodie|scarf|maternity)\b|원피스|스커트|블라우스|코트|자켓|가디건|스웨터|여성/i.test(text)) {
    return "Women's & Men's Fashion";
  }

  // 10. Men's Fashion
  if (/\b(suit|blazer|tie|tuxedo|cufflinks|mens|men.?wear)\b|정장|수트|넥타이|남성/i.test(text)) {
    return "Women's & Men's Fashion";
  }

  // 11. Food & Groceries
  if (/\b(food|snack|ramen|noodle|rice|tea|coffee|kimchi|sauce|oil|spices|candy|cookie|drink|juice|beverage|korean.?food|gourmet|pantry|groceries|grocery)\b|식품|라면|과자|김치|쌀|간식|음료/i.test(text)) {
    return 'Food & Groceries';
  }

  // 12. Arts, Books & Music
  if (/\b(book|books|novel|textbook|comic|manga|album|vinyl|cd|dvd|instrument|guitar|piano|violin|ukulele|flute|drum|art|painting|drawing|canvas|poster|ticket|tickets)\b|책|도서|만화|음반|기타|피아노|바이올린|악기|그림|티켓/i.test(text)) {
    return 'Arts, books, music, movies & tickets';
  }

  // 13. Antiques & Collections
  if (/\b(antique|vintage|collectible|collection|figurine|statue|memorabilia|coin|stamp|rare)\b|골동품|빈티지|수집품|피규어/i.test(text)) {
    return 'Antiques & collections';
  }

  // 14. Jewelry & Watches
  if (/\b(ring|necklace|bracelet|earring|jewelry|watch|rolex|omega|cartier|gold|silver|diamond)\b|반지|목걸이|귀걸이|시계|보석/i.test(text)) {
    return 'Jewelry & watches';
  }

  return 'Other';
}
'''

if 'function inferCategoryFromText' not in code:
    code = code.replace('export default async (req, context) => {', helper + '\n\nexport default async (req, context) => {')
    with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ Inserted inferCategoryFromText helper in item-detail.mjs")
else:
    print("Already present")
