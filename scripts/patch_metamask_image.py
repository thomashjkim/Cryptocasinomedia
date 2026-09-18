import json, hashlib, csv, os, re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "index/index.html.template")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "index/images")
BASE_URL = "https://cryptocasinomedia.com/images/"

# Metamask was assigned ccm_040 which conflicts with scam-alert.
# Fix: give metamask ccm_059 (freed slot+blockchain - fits DeFi/payments)
# scam-alert keeps ccm_040 (AI risk analysis dashboard + casino chips)
PATCH = {
    "metamask-casino-staking-programs-defi-yield-2026": "ccm_059.jpg",
}

def compute_checksum(a):
    s = f"{a.get('id')}|{a.get('slug')}|{a.get('title')}|{a.get('publishedAt')}|{a.get('dateline')}|{a.get('thumbnailUrl')}|{a.get('company')}|{a.get('sourceUrl')}"
    return hashlib.sha256(s.encode()).hexdigest()

CSV_FIELDS = ['id','slug','title','publishedAt','firstPublishedAt','modifiedAt','dateline','thumbnailUrl','sourceName','sourceUrl','company','primaryCategory','region','contact','excerpt','boilerplate']

with open(MASTER_JSON_PATH) as f:
    articles = json.load(f)

for a in articles:
    slug = a.get("slug")
    if slug in PATCH:
        new_img = PATCH[slug]
        img_path = os.path.join(IMAGES_DIR, new_img)
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Missing: {img_path}")
        old = a.get("thumbnailUrl","").split("/")[-1]
        a["thumbnailUrl"] = BASE_URL + new_img
        a["imageUrl"] = BASE_URL + new_img
        print(f"PATCH: {slug}")
        print(f"  WAS: {old}")
        print(f"  NOW: {new_img}")

with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

checksums = {a["slug"]: compute_checksum(a) for a in articles}
with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
    json.dump(checksums, f, indent=2)

with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline='') as f:
    w = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction='ignore')
    w.writeheader()
    for item in articles:
        w.writerow(item)

with open(TEMPLATE_PATH) as f:
    tpl = f.read()
start_marker = "const ARTICLES = ["
end_marker = "];\n\n        // ============================================================================\n        // 2. COMPONENT RENDERERS"
sp = tpl.find(start_marker)
ep = tpl.find(end_marker, sp)
if sp == -1 or ep == -1:
    m = re.search(r'const ARTICLES = \[.*?\];', tpl, re.DOTALL)
    sp, ep = m.start(), m.end()-2
new_tpl = tpl[:sp] + "const ARTICLES = " + json.dumps(articles, indent=8, ensure_ascii=False) + ";" + tpl[ep+2:]
with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
    f.write(new_tpl)

print()
print("Verifying no duplicates...")
img_counts = {}
for a in articles:
    img = a.get("thumbnailUrl","").split("/")[-1]
    img_counts[img] = img_counts.get(img, []) + [a["slug"]]
dups = {img: slugs for img, slugs in img_counts.items() if len(slugs) > 1}
if dups:
    print(f"STILL DUPLICATES: {dups}")
else:
    print("PASS: Zero duplicates across all 107 articles.")
print("Done.")
