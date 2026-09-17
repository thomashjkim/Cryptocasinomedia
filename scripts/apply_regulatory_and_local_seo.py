import os
import re
import json
from glob import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(PROJECT_ROOT, "index")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# 1. Load state regulations
with open(os.path.join(DATA_DIR, "us_state_regulations.json"), "r", encoding="utf-8") as f:
    state_regs = json.load(f)

state_slug_to_name = {slug: data["state_name"] for slug, data in state_regs.items()}

# 2. Build authoritative DMA -> State mapping
dma_to_state = {}
for p in glob(os.path.join(INDEX_DIR, "local/*/*/index.html")):
    parts = p.split(os.sep)
    state = parts[-3]
    dma = parts[-2]
    if not dma.startswith(("crypto-", "how-", "top-")):
        dma_to_state[dma] = state

print(f"Built authoritative mapping for {len(dma_to_state)} DMAs.")

# Helper: format DMA and State names
def format_names(state_slug, dma_slug=None):
    state_name = state_slug_to_name.get(state_slug, state_slug.replace("-", " ").title())
    if dma_slug:
        dma_name = dma_slug.replace("-", " ").title()
        # Clean up acronyms if needed
        dma_name = re.sub(r'\bLa\b', 'LA', dma_name)
        dma_name = re.sub(r'\bNy\b', 'NY', dma_name)
        dma_name = re.sub(r'\bDc\b', 'DC', dma_name)
        dma_name = re.sub(r'\bTn\b', 'TN', dma_name)
        dma_name = re.sub(r'\bVa\b', 'VA', dma_name)
        dma_name = re.sub(r'\bSc\b', 'SC', dma_name)
        dma_name = re.sub(r'\bGa\b', 'GA', dma_name)
        dma_name = re.sub(r'\bOh\b', 'OH', dma_name)
        dma_name = re.sub(r'\bMs\b', 'MS', dma_name)
        return state_name, dma_name
    return state_name, None

# 12-week date ranges
WEEK_RANGES = [
    ("W1", "May 31 – Jun 6, 2026"),
    ("W2", "Jun 7 – Jun 13, 2026"),
    ("W3", "Jun 14 – Jun 20, 2026"),
    ("W4", "Jun 21 – Jun 27, 2026"),
    ("W5", "Jun 28 – Jul 4, 2026"),
    ("W6", "Jul 5 – Jul 11, 2026"),
    ("W7", "Jul 12 – Jul 18, 2026"),
    ("W8", "Jul 19 – Jun 25, 2026"),
    ("W9", "Jul 26 – Aug 1, 2026"),
    ("W10", "Aug 2 – Aug 8, 2026"),
    ("W11", "Aug 9 – Aug 15, 2026"),
    ("W12", "Aug 16 – Aug 22, 2026"),
]

# 3. Fix broken cross-state links in all HTML files
print("--- Scanning and fixing cross-state DMA links across index/ ---")
fixed_links_count = 0
all_html_files = []
for root, dirs, files in os.walk(INDEX_DIR):
    for f in files:
        if f.endswith(".html"):
            all_html_files.append(os.path.join(root, f))

def fix_file_links(file_path):
    global fixed_links_count
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    def reg_replace(match):
        nonlocal modified
        global fixed_links_count
        prefix = match.group(1) # '/regulation/us/' or '/local/'
        st = match.group(2)
        dm = match.group(3)
        if dm in dma_to_state and dma_to_state[dm] != st:
            correct_st = dma_to_state[dm]
            modified = True
            fixed_links_count += 1
            return f"{prefix}{correct_st}/{dm}/"
        return match.group(0)

    content_new = re.sub(r'(href=["\'](?:/regulation/us/|/local/))([a-z-]+)/([a-z-]+)/', reg_replace, content)
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content_new)

for fp in all_html_files:
    fix_file_links(fp)

print(f"Fixed {fixed_links_count} broken cross-state DMA links across {len(all_html_files)} pages.")

# 4. Enhance 522 pages with 12-Week Trend SVG
print("--- Enhancing 12-Week Trend SVG pages with Accessible Table, Summary, and Dataset Schema ---")
svg_enhanced_count = 0

for file_path in all_html_files:
    if "index/local" not in file_path:
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "12-Week Search Attention Trend" not in content:
        continue

    # Avoid double-injecting
    if 'aria-label="12-week search trend data"' in content:
        continue

    m_us = re.search(r'<polyline[^>]*stroke=["\']#cbd5e1["\'][^>]*points=["\']([^"\']+)["\']', content)
    m_mkt = re.search(r'<polyline[^>]*stroke=["\']#1d4ed8["\'][^>]*points=["\']([^"\']+)["\']', content)

    if not (m_us and m_mkt):
        continue

    try:
        pts_us = [float(p.split(',')[1]) for p in m_us.group(1).split()]
        pts_mkt = [float(p.split(',')[1]) for p in m_mkt.group(1).split()]
        if len(pts_us) != 12 or len(pts_mkt) != 12:
            continue
        scores_us = [max(0, min(100, int(round((160.0 - y) / 1.4)))) for y in pts_us]
        scores_mkt = [max(0, min(100, int(round((160.0 - y) / 1.4)))) for y in pts_mkt]
    except Exception as e:
        print(f"Error parsing points in {file_path}: {e}")
        continue

    # Determine market name
    rel_path = os.path.relpath(file_path, INDEX_DIR)
    parts = rel_path.split(os.sep)
    state_slug = parts[1]
    dma_slug = parts[2] if len(parts) >= 4 and not parts[2].startswith(("crypto-", "how-", "top-")) else None
    state_name, dma_name = format_names(state_slug, dma_slug)
    market_display = f"{dma_name}, {state_name}" if dma_name else state_name

    # Build semantic HTML table rows
    table_rows = []
    for i in range(12):
        w_lbl, d_range = WEEK_RANGES[i]
        m_sc = scores_mkt[i]
        u_sc = scores_us[i]
        diff = m_sc - u_sc
        diff_str = f"+{diff}" if diff > 0 else f"{diff}"
        diff_color = "text-emerald-700 font-medium" if diff > 0 else ("text-rose-700 font-medium" if diff < 0 else "text-gray-500")
        table_rows.append(f"""                        <tr class="hover:bg-gray-50/80 transition-colors">
                            <td class="py-1 px-2 font-mono font-medium text-gray-900">{w_lbl}</td>
                            <td class="py-1 px-2 text-gray-600">{d_range}</td>
                            <td class="py-1 px-2 text-right font-bold text-blue-700">{m_sc}</td>
                            <td class="py-1 px-2 text-right text-gray-600">{u_sc}</td>
                            <td class="py-1 px-2 text-right {diff_color}">{diff_str}</td>
                        </tr>""")

    tbody_html = "\n".join(table_rows)

    # Narrative trend summary
    min_sc = min(scores_mkt)
    max_sc = max(scores_mkt)
    avg_sc = round(sum(scores_mkt) / len(scores_mkt), 1)
    w1_sc = scores_mkt[0]
    w12_sc = scores_mkt[-1]
    trend_dir = "increased" if w12_sc > w1_sc else ("decreased" if w12_sc < w1_sc else "held steady")

    summary_text = (
        f"Over the 12-week observation cycle (May 31 to August 22, 2026), search attention for crypto casino terms in "
        f"<strong>{market_display}</strong> {trend_dir} from {w1_sc}/100 in W1 to {w12_sc}/100 in W12, averaging {avg_sc}/100 "
        f"(12-week high: {max_sc}, low: {min_sc}) against the national baseline (which moved from {scores_us[0]} to {scores_us[-1]})."
    )

    table_section = f"""
        <section aria-label="12-week search trend data" class="mt-4 pt-4 border-t border-gray-100 font-sans">
            <h4 class="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">12-Week Search Index Breakdown</h4>
            <div class="overflow-x-auto">
                <table class="w-full text-xs text-left text-gray-700">
                    <thead class="bg-gray-50 text-gray-600 uppercase text-[10px]">
                        <tr>
                            <th class="py-1.5 px-2">Week</th>
                            <th class="py-1.5 px-2">Observation Window</th>
                            <th class="py-1.5 px-2 text-right">Market Score</th>
                            <th class="py-1.5 px-2 text-right">U.S. Benchmark</th>
                            <th class="py-1.5 px-2 text-right">Spread</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
{tbody_html}
                    </tbody>
                </table>
            </div>
            <p class="text-xs text-gray-600 mt-2.5 leading-relaxed">
                {summary_text}
            </p>
            <div class="text-[11px] text-gray-400 mt-1.5">
                Data period: May 31 – August 22, 2026 | Last verified: August 2026 | Source: Google Trends Public Dataset (BigQuery) via CryptoCasinoMedia Research
            </div>
        </section>"""

    # Inject table section right after the SVG container
    svg_container_pattern = r'(<div class="w-full overflow-x-auto">\s*<svg.*?</svg>\s*</div>)'
    m_cont = re.search(svg_container_pattern, content, re.DOTALL)
    if not m_cont:
        continue

    content = content[:m_cont.end()] + table_section + content[m_cont.end():]

    # Inject Schema.org Dataset into <head>
    dataset_schema = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": f"12-Week Search Attention Index: {market_display}",
        "description": f"Weekly normalized search attention index (May 31 - August 22, 2026) for crypto gambling and casino queries in {market_display}, benchmarked against U.S. national averages.",
        "creator": {
            "@type": "Organization",
            "name": "CryptoCasinoMedia Research",
            "url": "https://cryptocasinomedia.com"
        },
        "temporalCoverage": "2026-05-31/2026-08-22",
        "spatialCoverage": market_display,
        "variableMeasured": [
            {
                "@type": "PropertyValue",
                "name": "Market Score",
                "description": f"Normalized search attention index for {market_display} (0-100)"
            },
            {
                "@type": "PropertyValue",
                "name": "U.S. Benchmark",
                "description": "National baseline search attention index (0-100)"
            }
        ]
    }
    schema_script = f"""
    <script type="application/ld+json">
    {json.dumps(dataset_schema, indent=2)}
    </script>"""

    # Insert schema before </head>
    content = content.replace("</head>", f"{schema_script}\n</head>", 1)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    svg_enhanced_count += 1

print(f"Enhanced {svg_enhanced_count} pages with accessible trend tables and Schema.org Dataset.")

# 5. Differentiate search intent: Title, Description, H1
print("--- Differentiating Search Intent on Local Hubs (State and DMA) ---")
intent_count = 0

# A: 210 DMA Local Market Hubs
for dma, state in dma_to_state.items():
    file_path = os.path.join(INDEX_DIR, "local", state, dma, "index.html")
    if not os.path.exists(file_path):
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    state_name, dma_name = format_names(state, dma)

    # 1. Update <title>
    old_title_pat = r'<title>([^<]+?)\s*(?:Local)?\s*—\s*CryptoCasinoMedia</title>'
    new_title = f"<title>{dma_name} Crypto Casino Search Trends & Market Data (2026) — CryptoCasinoMedia</title>"
    content = re.sub(old_title_pat, new_title, content, count=1)

    # 2. Update meta description
    old_desc_pat = r'<meta name="description" content="[^"]*">'
    new_desc = f'<meta name="description" content="2026 crypto casino search trends, market demand index, and regulatory compliance intelligence for {dma_name}, {state_name}.">'
    content = re.sub(old_desc_pat, new_desc, content, count=1)

    # 3. Update H1
    old_h1_pat = r'<h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 capitalize[^"]*">[^<]+</h1>'
    new_h1 = f'<h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 capitalize mb-3">{dma_name} Crypto Casino Market & Search Trends (2026)</h1>'
    content = re.sub(old_h1_pat, new_h1, content, count=1)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    intent_count += 1

# B: 51 State Local Hubs
for state_slug, state_name in state_slug_to_name.items():
    file_path = os.path.join(INDEX_DIR, "local", state_slug, "index.html")
    if not os.path.exists(file_path):
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update <title>
    old_title_pat = r'<title>([^<]+?)\s*(?:Local)?\s*—\s*CryptoCasinoMedia</title>'
    new_title = f"<title>{state_name} Crypto Casino Search Trends & Regional Market Hub (2026) — CryptoCasinoMedia</title>"
    content = re.sub(old_title_pat, new_title, content, count=1)

    # 2. Update meta description
    old_desc_pat = r'<meta name="description" content="[^"]*">'
    new_desc = f'<meta name="description" content="2026 crypto casino search attention trends, regional media market data, and regulatory baseline for {state_name}.">'
    content = re.sub(old_desc_pat, new_desc, content, count=1)

    # 3. Update H1
    old_h1_pat = r'<h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 capitalize[^"]*">[^<]+</h1>'
    new_h1 = f'<h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 capitalize mb-3">{state_name} Crypto Casino Market & Search Trends (2026)</h1>'
    content = re.sub(old_h1_pat, new_h1, content, count=1)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    intent_count += 1

print(f"Updated search intent metadata on {intent_count} local market hubs.")
print("=== SEO & Regulatory Optimization Batch Completed Successfully ===")
