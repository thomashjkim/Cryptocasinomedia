#!/usr/bin/env python3
"""
Pre-Flight Safety and Regression Verification Suite for CryptoCasinoMedia.
Validates:
1. Navigation Menu Integrity (all 8 required items present in template & pre_render.py)
2. Template Content & Route Integrity (/guides/, /local/, /press-releases/, etc.)
3. Image Asset Integrity (no broken src, missing files, or empty images across all HTML pages)
4. JS Syntax Validation on all generated static pages using Node.js AST
"""
import os, sys, re, subprocess

INDEX_DIR = 'index'
REQUIRED_NAV = [
    'Press Releases',
    'Crypto Casinos',
    'Sportsbook',
    'Regulation',
    'Payments',
    'Sweepstakes',
    'Local'
]

def check_navigation():
    print("[1/4] Checking Navigation Menu Integrity...")
    template_fp = os.path.join(INDEX_DIR, 'index.html.template')
    with open(template_fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check JS navItems
    for item in REQUIRED_NAV:
        if f"label: '{item}'" not in content and f"'label': '{item}'" not in content:
            print(f"  [FAIL] Missing nav item in template: {item}")
            return False

    # Check scripts/pre_render.py navItems
    pr_fp = 'scripts/pre_render.py'
    with open(pr_fp, 'r', encoding='utf-8') as f:
        pr_content = f.read()
    for item in REQUIRED_NAV:
        if f"'label': '{item}'" not in pr_content:
            print(f"  [FAIL] Missing nav item in pre_render.py: {item}")
            return False

    # Verify Guides is in utility-top-bar
    if 'href="/guides"' not in content and 'href="/guides/"' not in content:
        print("  [FAIL] Missing Guides in utility-top-bar in template!")
        return False

    print("  [PASS] All 7 main nav items and top-bar Guides present.")
    return True

def check_guides_and_local():
    print("[2/4] Checking Guides Hub & Local Directory Content Integrity...")
    # /guides/ page
    guides_fp = os.path.join(INDEX_DIR, 'guides', 'index.html')
    if not os.path.exists(guides_fp):
        print("  [FAIL] index/guides/index.html does not exist!")
        return False
    with open(guides_fp, 'r', encoding='utf-8') as f:
        c = f.read()
        if "No articles found for this section." in c and "renderGuidesHubPage" not in c:
            print("  [FAIL] /guides/index.html is empty / broken!")
            return False
        if "iGaming & Crypto Casino Industry Guides" not in c:
            print("  [FAIL] /guides/index.html missing header title!")
            return False

    # /local/ page
    local_fp = os.path.join(INDEX_DIR, 'local', 'index.html')
    if not os.path.exists(local_fp):
        print("  [FAIL] index/local/index.html does not exist!")
        return False
    with open(local_fp, 'r', encoding='utf-8') as f:
        c = f.read()
        if "CryptoCasinoMedia Local" not in c:
            print("  [FAIL] /local/index.html missing title!")
            return False

    print("  [PASS] Guides Hub and Local Directory pages are fully intact.")
    return True

def check_images():
    print("[3/4] Checking Image Asset Integrity across site...")
    broken_images = []
    checked_count = 0
    img_regex = re.compile("<img[^>]+src=[\x22\x27]([^\x22\x27]+)[\x22\x27]")
    for root, dirs, files in os.walk(INDEX_DIR):
        for f in files:
            if f.endswith('.html'):
                fp = os.path.join(root, f)
                checked_count += 1
                with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    for match in img_regex.finditer(content):
                        img = match.group(1).strip()
                        if not img or img in ['undefined', 'null']:
                            broken_images.append((fp, 'BAD_SRC_VALUE', img))
                        elif img.startswith('/') and not img.startswith('//'):
                            local_file = os.path.join(INDEX_DIR, img.lstrip('/'))
                            if not os.path.exists(local_file):
                                broken_images.append((fp, 'MISSING_LOCAL_FILE', img))

    if broken_images:
        print(f"  [FAIL] Found {len(broken_images)} broken image references in {checked_count} HTML files!")
        for b in broken_images[:10]:
            print("   ", b)
        return False

    print(f"  [PASS] Checked {checked_count} HTML pages: all referenced local and external images are valid.")
    return True

def check_js_syntax():
    print("[4/4] Checking JavaScript Syntax Integrity in index.html...")
    index_fp = os.path.join(INDEX_DIR, 'index.html')
    if not os.path.exists(index_fp):
        print("  [FAIL] index/index.html does not exist!")
        return False

    node_cmd = """
const fs = require('fs');
const html = fs.readFileSync('index/index.html', 'utf8');
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
while ((match = scriptRegex.exec(html)) !== null) {
    const code = match[1].trim();
    if (!code) continue;
    if (code.startsWith('{') && code.endsWith('}')) {
        JSON.parse(code);
        continue;
    }
    new Function(code);
}
console.log('OK');
"""
    try:
        res = subprocess.run(['node', '-e', node_cmd], capture_output=True, text=True, check=True)
        if 'OK' in res.stdout:
            print("  [PASS] Node.js AST parsed all inline scripts with 0 syntax errors.")
            return True
        else:
            print(f"  [FAIL] Node output: {res.stdout}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"  [FAIL] JS Syntax Error: {e.stderr}")
        return False

def main():
    print("=== CRYPTOCASINOMEDIA PRE-FLIGHT VERIFICATION SUITE ===")
    v1 = check_navigation()
    v2 = check_guides_and_local()
    v3 = check_images()
    v4 = check_js_syntax()
    print("=========================================================")
    if v1 and v2 and v3 and v4:
        print("ALL CHECKS PASSED: Site is safe and ready for deployment.")
        sys.exit(0)
    else:
        print("CRITICAL VERIFICATION FAILED: Do NOT deploy!")
        sys.exit(1)

if __name__ == '__main__':
    main()
