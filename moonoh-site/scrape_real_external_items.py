import urllib.request
import json
import re
import html
import os

def clean_and_translate_title(title):
    t = title.strip()
    # Remove seller phone numbers or promo prefix
    t = re.sub(r'^[^\w]*[\w\s\$]+｜', '', t).strip()
    t = re.sub(r'\d{3}[-\s]?\d{3,4}[-\s]?\d{4}', '', t).strip()
    
    translations = [
        (r'팝니다', 'for Sale'),
        (r'삽니다', 'Wanted'),
        (r'원형 부탄가스 테이블', 'Round Butane Gas Table'),
        (r'압력밥솥', 'Pressure Rice Cooker'),
        (r'밥솥', 'Rice Cooker'),
        (r'은수저 세트', 'Silver Spoon & Chopstick Set'),
        (r'구름버스 그림책 35권', 'Cloud Bus Children Picture Books (35 Books)'),
        (r'그림책', 'Picture Books'),
        (r'서랍장', 'Dresser'),
        (r'원목 소파 테이블', 'Solid Wood Sofa Table'),
        (r'식탁 세트', 'Dining Table Set'),
        (r'의자 포함', 'with Chairs'),
        (r'세탁기 건조기 세트', 'Washer & Dryer Set'),
        (r'세탁기', 'Washer'),
        (r'건조기', 'Dryer'),
        (r'아기 침대', 'Baby Crib'),
        (r'원목 매트리스 포함', 'with Wooden Mattress'),
        (r'단기 서블렛 1개월', '1-Month Short Term Sublet'),
        (r'정품', 'Authentic'),
        (r'클래식 플랩백 스몰', 'Classic Flap Small Bag'),
        (r'골프클럽 풀세트 캐디백 포함', 'Golf Club Full Set with Caddy Bag'),
        (r'인치 4K UHD 스마트 TV', 'inch 4K UHD Smart TV'),
        (r'네오노에 모노그램', 'NéoNoé Monogram Bag'),
        (r'에어컨', 'Air Conditioner'),
        (r'공기청정기', 'Air Purifier'),
        (r'가습기', 'Humidifier'),
        (r'유모차', 'Stroller'),
        (r'청소기', 'Vacuum Cleaner'),
        (r'화장대', 'Vanity Table'),
        (r'책상', 'Desk'),
        (r'의자', 'Chair'),
        (r'침대', 'Bed'),
        (r'가방', 'Bag'),
        (r'지갑', 'Wallet'),
        (r'신발', 'Shoes'),
        (r'옷', 'Clothing')
    ]

    for kor, eng in translations:
        t = re.sub(kor, eng, t)
        
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def fetch_real_heykorean():
    url = 'https://market.heykorean.com/api/market/list'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    items = []
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_items = data.get('list', [])
            for r in raw_items:
                raw_title = r.get('title', '').strip()
                
                # Exclude commercial ads, car auctions, HVAC, post office, store ads
                if r.get('store_type') == 'B' or '우체국' in raw_title or '경매' in raw_title or 'HVAC' in raw_title or '상점 바로가기' in raw_title or 'CAR SALES' in raw_title or 'FORD' in raw_title or 'KIA' in raw_title or '에어컨' in raw_title or '설치' in raw_title or '구매대행' in raw_title:
                    continue
                
                # Parse main image
                main_img = r.get('main_image') or ''
                img_url = ''
                if main_img:
                    try:
                        img_obj = json.loads(main_img)
                        img_url = img_obj.get('large') or img_obj.get('medium') or img_obj.get('origin') or ''
                    except:
                        img_url = main_img
                
                if not img_url:
                    continue
                
                # Translate title to English
                eng_title = clean_and_translate_title(raw_title)
                price = float(r.get('price', 0))
                area = r.get('area_name_en') or r.get('area_name') or 'New York, NY'
                cat = r.get('category_title_en') or r.get('category_title') or 'Used Items'
                
                items.append({
                    'id': f'heykorean-{r.get("id")}',
                    'title': eng_title,
                    'price': price,
                    'location': f'1mi · {area}',
                    'rawTown': area,
                    'category': cat,
                    'image': img_url,
                    'source': 'heykorean',
                    'sourceName': 'HeyKorean',
                    'url': f'https://market.heykorean.com/market/view/{r.get("id")}'
                })
    except Exception as e:
        print('HeyKorean fetch error:', e)
    return items

def fetch_real_karrot():
    url = 'https://us.karrotmarket.com/buy-sell/'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'})
    items = []
    try:
        with urllib.request.urlopen(req) as resp:
            raw_html = resp.read().decode('utf-8', errors='ignore')
            articles = re.findall(r'<a[^>]*href=\"(/buy-sell/[^\"]+)\"[^>]*>(.*?)</a>', raw_html, re.DOTALL)
            seen_ids = set()
            for href, content in articles:
                img_m = re.search(r'src=\"(https?://img[^\"]+)\"', content)
                title_m = re.search(r'alt=\"([^\"]+)\"', content) or re.search(r'class=\"[^\"]*title[^\"]*\">([^<]+)<', content)
                price_m = re.search(r'\$([0-9,]+)', content)
                
                if img_m and title_m:
                    img_url = html.unescape(img_m.group(1)).replace('&amp;', '&')
                    title = html.unescape(title_m.group(1)).strip()
                    price = float(price_m.group(1).replace(',', '')) if price_m else 0
                    
                    art_id = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                    if art_id in seen_ids:
                        continue
                    seen_ids.add(art_id)
                    
                    items.append({
                        'id': f'karrot-{art_id}',
                        'title': title,
                        'price': price,
                        'location': '1mi · Queens',
                        'rawTown': 'Queens, NY',
                        'category': 'Used Items',
                        'image': img_url,
                        'source': 'karrot',
                        'sourceName': 'Karrot',
                        'url': f'https://us.karrotmarket.com{href}'
                    })
    except Exception as e:
        print('Karrot fetch error:', e)
    return items

if __name__ == '__main__':
    hk = fetch_real_heykorean()
    kr = fetch_real_karrot()
    print(f'Fetched {len(hk)} real HeyKorean items & {len(kr)} real Karrot items.')
    
    with open('real_external_items.json', 'w', encoding='utf-8') as f:
        json.dump({'heykorean': hk, 'karrot': kr}, f, ensure_ascii=False, indent=2)
