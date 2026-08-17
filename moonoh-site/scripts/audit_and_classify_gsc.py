import csv
import json
import re
import os
from urllib.parse import urlparse, parse_qs
from collections import Counter

def run_audit():
    # 1. Load databases
    with open('data.json', 'r', encoding='utf-8') as f:
        moonoh_raw = json.load(f)
    moonoh_items = moonoh_raw if isinstance(moonoh_raw, list) else moonoh_raw.get('data', [])

    with open('netlify/functions/food-rescue-items.mjs', 'r', encoding='utf-8') as f:
        code = f.read()
    m_food = re.search(r'export const realFoodRescueItems = (\[.*?\]);', code, re.DOTALL)
    food_items = json.loads(m_food.group(1)) if m_food else []

    with open('netlify/functions/external-items.mjs', 'r', encoding='utf-8') as f:
        code = f.read()
    m_karrot = re.search(r'export const realKarrotItems = (\[.*?\]);', code, re.DOTALL)
    m_hey = re.search(r'export const realHeyKoreanItems = (\[.*?\]);', code, re.DOTALL)
    karrot_items = json.loads(m_karrot.group(1)) if m_karrot else []
    heykorean_items = json.loads(m_hey.group(1)) if m_hey else []

    with open('local_shops_data.json', 'r', encoding='utf-8') as f:
        local_shops_data = json.load(f)
    local_products = local_shops_data.get('products', [])

    def clean_slug(s):
        if not s: return ''
        s = s.lower().strip()
        s = re.sub(r'[^a-z0-9\s-]', '', s)
        s = re.sub(r'\s+', '-', s)
        return re.sub(r'-+', '-', s).strip('-')

    def get_neighborhood_slug(loc_str):
        if not loc_str: return 'nyc-ny'
        l = loc_str.lower()
        if 'upper west side' in l or 'uws' in l: return 'upper-west-side'
        if 'upper east side' in l or 'ues' in l: return 'upper-east-side'
        if 'midtown' in l: return 'midtown'
        if 'east village' in l: return 'east-village'
        if 'west village' in l: return 'west-village'
        if 'soho' in l: return 'soho'
        if 'tribeca' in l: return 'tribeca'
        if 'chelsea' in l: return 'chelsea'
        if 'greenpoint' in l: return 'greenpoint'
        if 'williamsburg' in l: return 'williamsburg'
        if 'dumbo' in l: return 'dumbo'
        if 'bushwick' in l: return 'bushwick'
        if 'flushing' in l: return 'flushing'
        if 'bayside' in l: return 'bayside'
        if 'astoria' in l: return 'astoria'
        if 'lic' in l or 'long island city' in l: return 'long-island-city'
        if 'fort lee' in l: return 'fort-lee'
        if 'jersey city' in l: return 'jersey-city'
        if 'hoboken' in l: return 'hoboken'
        if 'manhattan' in l: return 'manhattan'
        if 'brooklyn' in l: return 'brooklyn'
        if 'queens' in l: return 'queens'
        if 'bronx' in l: return 'bronx'
        if 'staten island' in l: return 'staten-island'
        if 'bergen' in l: return 'bergen-county'
        if 'hudson' in l: return 'hudson-county'
        return clean_slug(loc_str) or 'nyc-ny'

    # Build active canonical URL lookups
    active_canonical_urls = set()
    item_id_to_canonical = {}

    for it in moonoh_items:
        no = str(it.get('no', it.get('id', '')))
        ts = clean_slug(it.get('title', 'item'))
        loc = get_neighborhood_slug(it.get('rawTown', it.get('location', '')))
        c_url = f'https://moon-oh.com/item/{ts}-{loc}-{no}'
        active_canonical_urls.add(c_url)
        item_id_to_canonical[('moonoh', no)] = c_url

    for it in heykorean_items:
        raw_id = str(it.get('id', ''))
        clean_id = raw_id.replace('heykorean-', '')
        ts = clean_slug(it.get('title', 'item'))
        loc = get_neighborhood_slug(it.get('location', ''))
        c_url = f'https://moon-oh.com/item/{ts}-{loc}-ext-{raw_id}'
        active_canonical_urls.add(c_url)
        item_id_to_canonical[('heykorean', raw_id)] = c_url
        item_id_to_canonical[('heykorean', clean_id)] = c_url

    for it in karrot_items:
        raw_id = str(it.get('id', ''))
        clean_id = raw_id.replace('karrot-', '')
        ts = clean_slug(it.get('title', 'item'))
        loc = get_neighborhood_slug(it.get('location', ''))
        c_url = f'https://moon-oh.com/item/{ts}-{loc}-ext-{raw_id}'
        active_canonical_urls.add(c_url)
        item_id_to_canonical[('karrot', raw_id)] = c_url
        item_id_to_canonical[('karrot', clean_id)] = c_url

    for it in food_items:
        iid = str(it.get('id', ''))
        ts = clean_slug(it.get('title', 'item'))
        loc = get_neighborhood_slug(it.get('location', ''))
        c_url = f'https://moon-oh.com/item/{ts}-{loc}-ext-{iid}'
        active_canonical_urls.add(c_url)
        item_id_to_canonical[('kimc', iid)] = c_url

    local_prod_slugs = set()
    for p in local_products:
        c_url = f"https://moon-oh.com/local-product/{p.get('shop_slug')}/{p.get('slug')}"
        active_canonical_urls.add(c_url)
        local_prod_slugs.add(f"{p.get('shop_slug')}/{p.get('slug')}")

    # Read GSC CSV
    csv_path = '/Users/thomaskim/Downloads/Merged_URL_Issues_Final_v2.csv'
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    classification_results = []
    action_counter = Counter()

    for row in rows:
        issue, url, last_crawled, val_status = row[0], row[1], row[2], row[3]
        parsed = urlparse(url)
        path = parsed.path
        query = parsed.query
        
        action = None
        reason = ''
        detected_canonical = ''
        resolved_url = url
        sitemap_status = 'In Sitemap' if url in active_canonical_urls else 'Excluded'
        
        # 1. 5xx errors
        if issue == 'Server error (5xx)':
            if path.startswith('/image-proxy/'):
                action = 'FIX_5XX'
                reason = 'Temporary image proxy 502/504 error on deleted assets; systemic fix returns controlled 404 and excludes from sitemap.'
                resolved_url = url
            elif path.startswith('/item/'):
                m_hk = re.search(r'-ext-(?:heykorean-)?(\d+)$', path)
                m_kt = re.search(r'-ext-(?:karrot-)?([a-z0-9]+)$', path)
                m_mo = re.search(r'-(\d+)$', path)
                target = None
                if m_hk and ('heykorean', m_hk.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('heykorean', m_hk.group(1))]
                elif m_kt and ('karrot', m_kt.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('karrot', m_kt.group(1))]
                elif m_mo and ('moonoh', m_mo.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('moonoh', m_mo.group(1))]
                
                if target:
                    if target == url:
                        action = 'RESTORE_200'
                        reason = 'Valid active item page previously throwing 500; restored to stable 200.'
                    else:
                        action = '301_TO_KNOWN_CANONICAL'
                        reason = 'Item exists under updated canonical slug; 301 redirects to canonical target.'
                    resolved_url = target
                    detected_canonical = target
                else:
                    action = '404_410_OK_REMOVE_REFERENCES'
                    reason = 'Item deleted/non-existent; returns controlled 404 instead of 500.'
            else:
                action = 'FIX_5XX'
                reason = 'Server error on route; resolved with stable response or controlled 404.'

        # 2. Redirects
        elif issue == 'Page with redirect':
            if url in ['http://www.moon-oh.com/', 'http://moon-oh.com/', 'https://www.moon-oh.com/']:
                action = 'EXPECTED'
                reason = 'Standard 301 domain canonicalization to https://moon-oh.com/.'
                resolved_url = 'https://moon-oh.com/'
                detected_canonical = 'https://moon-oh.com/'
            elif path.endswith('/') and path not in ['/', '']:
                clean_p = path.rstrip('/')
                action = 'KEEP_301_REMOVE_REFERENCES'
                reason = 'Trailing slash normalization redirect; remove trailing-slash references from sitemap.'
                resolved_url = f'https://moon-oh.com{clean_p}'
                detected_canonical = f'https://moon-oh.com{clean_p}'
            elif path.startswith('/item/'):
                m_hk = re.search(r'-ext-(?:heykorean-)?(\d+)$', path)
                m_kt = re.search(r'-ext-(?:karrot-)?([a-z0-9]+)$', path)
                m_kc = re.search(r'-ext-(?:kimc-)?(\d+)$', path)
                m_mo = re.search(r'-(\d+)$', path)
                target = None
                if m_hk and ('heykorean', m_hk.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('heykorean', m_hk.group(1))]
                elif m_kt and ('karrot', m_kt.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('karrot', m_kt.group(1))]
                elif m_kc and ('kimc', m_kc.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('kimc', m_kc.group(1))]
                elif m_mo and ('moonoh', m_mo.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('moonoh', m_mo.group(1))]
                
                if target:
                    action = 'KEEP_301_REMOVE_REFERENCES'
                    reason = 'Legitimate 1-hop 301 alias redirect to current canonical item URL.'
                    resolved_url = target
                    detected_canonical = target
                else:
                    action = '404_410_OK_REMOVE_REFERENCES'
                    reason = 'Redirect source item no longer exists in database; returns controlled 404.'
            else:
                action = 'KEEP_301_REMOVE_REFERENCES'
                reason = 'Legitimate redirect.'

        # 3. Not found (404)
        elif issue == 'Not found (404)':
            if path.startswith('/local-product/'):
                action = '404_410_OK_REMOVE_REFERENCES'
                reason = 'Legacy unverified local shop product replaced during 90-item curation; 404 is valid, remove from sitemap.'
            elif path.startswith('/press-releases/'):
                action = '404_410_OK_REMOVE_REFERENCES'
                reason = 'Legacy demo press release URL permanently removed; 404 is correct.'
            elif path.startswith('/item/'):
                m_mo = re.search(r'-(\d+)$', path)
                m_hk = re.search(r'-ext-(?:heykorean-)?(\d+)$', path)
                target = None
                if m_mo and ('moonoh', m_mo.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('moonoh', m_mo.group(1))]
                elif m_hk and ('heykorean', m_hk.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('heykorean', m_hk.group(1))]
                if target:
                    action = '301_TO_KNOWN_CANONICAL'
                    reason = 'Item exists under canonical slug; 301 redirect mapped.'
                    resolved_url = target
                else:
                    action = '404_410_OK_REMOVE_REFERENCES'
                    reason = 'Permanently removed sublet or deleted C2C listing; 404 is correct, exclude from sitemap.'
            else:
                action = '404_410_OK_REMOVE_REFERENCES'
                reason = 'Permanently deleted route; 404 is correct.'

        # 4. Soft 404
        elif issue == 'Soft 404':
            action = 'INDEXABLE_CONTENT_IMPROVEMENT'
            reason = 'Explore category landing page (/explore/manhattan/food-groceries); now provides rich SSR listings, H1, unique summary, and ItemList schema.'
            resolved_url = url
            detected_canonical = url

        # 5. Duplicate, Google chose different canonical
        elif issue == 'Duplicate, Google chose different canonical than user':
            if path == '/privacy':
                action = 'FIX_CANONICAL'
                reason = 'Ensure strict self-canonical https://moon-oh.com/privacy.'
                resolved_url = url
                detected_canonical = url
            elif path.startswith('/item/'):
                m_mo = re.search(r'-(\d+)$', path)
                m_hk = re.search(r'-ext-(?:heykorean-)?(\d+)$', path)
                m_kt = re.search(r'-ext-(?:karrot-)?([a-z0-9]+)$', path)
                target = None
                if m_mo and ('moonoh', m_mo.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('moonoh', m_mo.group(1))]
                elif m_hk and ('heykorean', m_hk.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('heykorean', m_hk.group(1))]
                elif m_kt and ('karrot', m_kt.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('karrot', m_kt.group(1))]
                
                if target and target == url:
                    action = 'FIX_CANONICAL'
                    reason = 'Align internal links, OG URL, Product schema URL to this canonical URL.'
                    resolved_url = url
                    detected_canonical = url
                elif target:
                    action = '301_TO_KNOWN_CANONICAL'
                    reason = 'Old address-based slug 301 redirects to updated neighborhood canonical URL.'
                    resolved_url = target
                    detected_canonical = target
                else:
                    action = '404_410_OK_REMOVE_REFERENCES'
                    reason = 'Deleted item slug; returns controlled 404.'
            else:
                action = 'FIX_CANONICAL'
                reason = 'Align canonical signals.'

        # 6. Alternate page with proper canonical tag
        elif issue == 'Alternate page with proper canonical tag':
            action = 'EXPECTED'
            reason = 'Intentional query/filter variant or trailing slash correctly self-canonicalizing to clean landing page.'
            resolved_url = url
            detected_canonical = 'https://moon-oh.com' + (path.rstrip('/') or '/')

        # 7. Excluded by noindex tag
        elif issue.startswith('Excluded by'):
            if '${article.slug}' in url or '${' in url:
                action = '404_410_OK_REMOVE_REFERENCES'
                reason = 'Unresolved template literal placeholder; removed from templates and returns 404.'
            else:
                action = 'NOINDEX_REMOVE_FROM_SITEMAP'
                reason = 'Intentionally or legacy noindexed page; ensure excluded from all XML sitemaps.'

        # 8. Crawled - currently not indexed
        elif issue.startswith('Crawled'):
            if path.startswith('/image-proxy/'):
                action = 'EXPECTED'
                reason = 'Non-HTML image asset crawled by Googlebot; excluded from XML sitemaps.'
            elif path.startswith('/api/') or path.startswith('/.netlify/') or path.endswith('.json'):
                action = 'EXPECTED'
                reason = 'Technical API / backend JSON endpoint; not an indexable HTML page.'
            elif path.startswith('/item/'):
                m_mo = re.search(r'-(\d+)$', path)
                m_hk = re.search(r'-ext-(?:heykorean-)?(\d+)$', path)
                m_kt = re.search(r'-ext-(?:karrot-)?([a-z0-9]+)$', path)
                m_kc = re.search(r'-ext-(?:kimc-)?(\d+)$', path)
                target = None
                if m_mo and ('moonoh', m_mo.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('moonoh', m_mo.group(1))]
                elif m_hk and ('heykorean', m_hk.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('heykorean', m_hk.group(1))]
                elif m_kt and ('karrot', m_kt.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('karrot', m_kt.group(1))]
                elif m_kc and ('kimc', m_kc.group(1)) in item_id_to_canonical:
                    target = item_id_to_canonical[('kimc', m_kc.group(1))]
                
                if target and target == url:
                    action = 'INDEXABLE_CONTENT_IMPROVEMENT'
                    reason = 'Active index-worthy item; equipped with rich SSR HTML, H1, unique title, and Product schema.'
                elif target:
                    action = '301_TO_KNOWN_CANONICAL'
                    reason = 'Old slug crawled previously; 301 redirects to active canonical item URL.'
                    resolved_url = target
                else:
                    action = '404_410_OK_REMOVE_REFERENCES'
                    reason = 'Expired/deleted listing; returns controlled 404.'
            elif path.startswith('/local-product/'):
                lp_slug = path.replace('/local-product/', '')
                if lp_slug in local_prod_slugs:
                    action = 'INDEXABLE_CONTENT_IMPROVEMENT'
                    reason = 'Curated active local product page; equipped with SSR HTML and Product schema.'
                else:
                    action = '404_410_OK_REMOVE_REFERENCES'
                    reason = 'Unverified legacy product slug; returns 404.'
            elif path.startswith('/explore'):
                action = 'INDEXABLE_CONTENT_IMPROVEMENT'
                reason = 'Explore hub / category landing page; enriched with H1, intro text, and ItemList schema.'
            else:
                action = 'INDEXABLE_CONTENT_IMPROVEMENT'
                reason = 'Index-worthy page.'

        if not action:
            action = 'MANUAL_REVIEW'
            reason = 'Unclassified URL'

        action_counter[action] += 1
        classification_results.append({
            'url': url,
            'issue': issue,
            'action': action,
            'reason': reason,
            'resolved_url': resolved_url,
            'detected_canonical': detected_canonical,
            'sitemap_status': sitemap_status,
            'last_crawled': last_crawled
        })

    print(f'Total Classified: {len(classification_results)} / 1695\n')
    print('Action Breakdown:')
    for act, cnt in sorted(action_counter.items(), key=lambda x: -x[1]):
        print(f'  {act}: {cnt}')

    # Save audit report CSV
    out_csv = 'gsc_audit_report.csv'
    with open(out_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'issue', 'action', 'reason', 'resolved_url', 'detected_canonical', 'sitemap_status', 'last_crawled'])
        writer.writeheader()
        writer.writerows(classification_results)
    print(f'\n✅ Saved detailed audit report to {out_csv}')

if __name__ == '__main__':
    run_audit()
