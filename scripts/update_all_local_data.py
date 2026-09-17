#!/usr/bin/env python3
"""
Update all state and city legal guides, tax guides, hub cards, and local index
to today's date (September 17, 2026) across the entire local directory.
"""
import os
import re

INDEX_DIR = "/Users/thomaskim/Cryptocasinomedia/index"
LOCAL_DIR = os.path.join(INDEX_DIR, "local")

NEW_DATE_DISPLAY = "September 17, 2026"
NEW_DATE_SHORT = "SEP 17, 2026"
NEW_DATE_ISO = "2026-09-17T15:00:00Z"

def update_legal_guides():
    guide_count = 0
    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if f == "index.html" and "crypto-gambling-and-advertising-legal-regulatory-guide-" in root:
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                modified = False
                
                # 1. Update <time> tag
                if '<time datetime="2026-08-20T09:00:00Z">August 20, 2026</time>' in content:
                    content = content.replace(
                        '<time datetime="2026-08-20T09:00:00Z">August 20, 2026</time>',
                        f'<time datetime="2026-09-17T09:00:00Z">{NEW_DATE_DISPLAY}</time>'
                    )
                    modified = True
                
                # 2. Update dateModified in Schema
                if '"dateModified": "2026-08-20T09:00:00Z"' in content:
                    content = content.replace(
                        '"dateModified": "2026-08-20T09:00:00Z"',
                        '"dateModified": "2026-09-17T09:00:00Z"'
                    )
                    modified = True
                
                if modified:
                    with open(p, "w", encoding="utf-8") as fp:
                        fp.write(content)
                    guide_count += 1
                    
    print(f"[1] Updated {guide_count} state & city Legal & Regulatory Guides.")

def update_tax_guides():
    tax_count = 0
    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if f == "index.html" and "crypto-casino-taxes-" in root:
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                modified = False
                
                # 1. Update UPDATED header
                if 'UPDATED: August 29, 2026' in content:
                    content = content.replace('UPDATED: August 29, 2026', f'UPDATED: {NEW_DATE_DISPLAY}')
                    modified = True
                
                # 2. Update dateModified in Schema
                if '"dateModified": "2026-08-29T14:15:00Z"' in content:
                    content = content.replace(
                        '"dateModified": "2026-08-29T14:15:00Z"',
                        f'"dateModified": "{NEW_DATE_ISO}"'
                    )
                    modified = True
                
                if modified:
                    with open(p, "w", encoding="utf-8") as fp:
                        fp.write(content)
                    tax_count += 1
                    
    print(f"[2] Updated {tax_count} state Tax Guides.")

def update_hub_legal_and_tax_cards():
    hub_legal_count = 0
    hub_tax_count = 0
    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if f == "index.html" and not any(sub in root for sub in ["top-10-", "how-crypto-", "crypto-"]):
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                modified = False
                
                # Legal & Regulatory card
                # Pattern: <span>Aug 20, 2026</span>
                if "LEGAL & REGULATORY" in content or "LEGAL &amp; REGULATORY" in content:
                    if "<span>Aug 20, 2026</span>" in content:
                        content = content.replace("<span>Aug 20, 2026</span>", f"<span>{NEW_DATE_SHORT}</span>")
                        modified = True
                        hub_legal_count += 1
                
                # Tax & Revenue card
                # Pattern: <span>Aug 29, 2026</span>
                if "TAX & REVENUE GUIDE" in content or "TAX &amp; REVENUE GUIDE" in content:
                    if "<span>Aug 29, 2026</span>" in content:
                        content = content.replace("<span>Aug 29, 2026</span>", f"<span>{NEW_DATE_SHORT}</span>")
                        modified = True
                        hub_tax_count += 1

                if modified:
                    with open(p, "w", encoding="utf-8") as fp:
                        fp.write(content)

    print(f"[3] Updated {hub_legal_count} Hub Legal cards and {hub_tax_count} Hub Tax cards.")

def update_root_local_index():
    p = os.path.join(LOCAL_DIR, "index.html")
    if not os.path.exists(p):
        return
    with open(p, "r", encoding="utf-8") as fp:
        content = fp.read()

    # Tax Series featured card
    content = content.replace("<span>AUG 29, 2026</span>", f"<span>{NEW_DATE_SHORT}</span>")
    
    # Regional stories list cards
    content = content.replace("<span>Aug 16, 2026</span>", f"<span>{NEW_DATE_SHORT}</span>")
    content = content.replace("<span>Aug 20, 2026</span>", f"<span>{NEW_DATE_SHORT}</span>")

    with open(p, "w", encoding="utf-8") as fp:
        fp.write(content)
    print("[4] Updated root local index (index/local/index.html).")

def sync_local_sitemap():
    sitemap_path = os.path.join(INDEX_DIR, "local-sitemap.xml")
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as fp:
            content = fp.read()
        
        # Replace any remaining older lastmod dates with 2026-09-17
        content = re.sub(r'<lastmod>2026-08-\d{2}</lastmod>', '<lastmod>2026-09-17</lastmod>', content)
        content = re.sub(r'<lastmod>2026-09-15</lastmod>', '<lastmod>2026-09-17</lastmod>', content)
        
        with open(sitemap_path, "w", encoding="utf-8") as fp:
            fp.write(content)
        print("[5] Synchronized all local-sitemap.xml entries to 2026-09-17.")

if __name__ == "__main__":
    print("=== Updating All State & City Legal, Tax, and Local Index Data ===")
    update_legal_guides()
    update_tax_guides()
    update_hub_legal_and_tax_cards()
    update_root_local_index()
    sync_local_sitemap()
    print("=== Complete! ===")
