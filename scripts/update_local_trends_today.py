#!/usr/bin/env python3
"""
Update Crypto Casino Market & Search Trends and Top 10 by Search Interest
across all state and DMA local pages to today's date (September 17, 2026).
"""
import os
import re

INDEX_DIR = "/Users/thomaskim/Cryptocasinomedia/index"
LOCAL_DIR = os.path.join(INDEX_DIR, "local")

NEW_DATE_DISPLAY = "September 17, 2026"
NEW_DATE_SHORT = "SEP 17, 2026"
NEW_DATE_ISO = "2026-09-17T15:00:00Z"
NEW_RANKING_PERIOD = "Sep 7 – Sep 13, 2026"
NEW_WEEKLY_PERIOD = "September 13, 2026"

WEEK_RANGES = [
    ("W1", "Jun 21 – Jun 27, 2026"),
    ("W2", "Jun 28 – Jul 4, 2026"),
    ("W3", "Jul 5 – Jul 11, 2026"),
    ("W4", "Jul 12 – Jul 18, 2026"),
    ("W5", "Jul 19 – Jul 25, 2026"),
    ("W6", "Jul 26 – Aug 1, 2026"),
    ("W7", "Aug 2 – Aug 8, 2026"),
    ("W8", "Aug 9 – Aug 15, 2026"),
    ("W9", "Aug 16 – Aug 22, 2026"),
    ("W10", "Aug 23 – Aug 29, 2026"),
    ("W11", "Aug 30 – Sep 5, 2026"),
    ("W12", "Sep 6 – Sep 12, 2026"),
]

week_dict = dict(WEEK_RANGES)

def update_top_10_pages():
    count = 0
    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if f == "index.html" and "top-10-crypto-casinos-" in root:
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                # 1. Update date in byline
                content = re.sub(
                    r'<span>Updated August 23, 2026</span>',
                    f'<span>Updated {NEW_DATE_DISPLAY}</span>',
                    content
                )
                
                # 2. Update ranking period in chart header
                content = re.sub(
                    r'Period: Aug 10 – Aug 16, 2026',
                    f'Period: {NEW_RANKING_PERIOD}',
                    content
                )
                
                # 3. Update dateModified in Schema
                content = re.sub(
                    r'"dateModified":\s*"2026-08-23T15:00:00Z"',
                    f'"dateModified": "{NEW_DATE_ISO}"',
                    content
                )
                
                with open(p, "w", encoding="utf-8") as fp:
                    fp.write(content)
                count += 1
    print(f"[1] Updated {count} Top 10 State Ranking pages.")

def update_hub_ranking_cards():
    count = 0
    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if f == "index.html" and "top-10-crypto-casinos-" not in root and "how-crypto-gaming-search-trends-" not in root and "crypto-" not in root:
                p = os.path.join(root, f)
                with open(p, "r", encoding="utf-8") as fp:
                    content = fp.read()
                
                if "RANKING INDEX" in content and "AUG 23, 2026" in content:
                    content = content.replace("AUG 23, 2026", NEW_DATE_SHORT)
                    with open(p, "w", encoding="utf-8") as fp:
                        fp.write(content)
                    count += 1
    print(f"[2] Updated {count} Hub Top 10 Ranking cards.")

def update_12_week_trend_tables():
    count = 0
    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fp:
                content = fp.read()
            
            if "12-Week Search Index Breakdown" not in content:
                continue

            # Update table rows
            def replace_week_row(match):
                prefix = match.group(1)
                w_num = match.group(2)
                suffix = match.group(3)
                w_key = f"W{w_num}"
                if w_key in week_dict:
                    return f"{prefix}{week_dict[w_key]}{suffix}"
                return match.group(0)

            pattern = r'(<td class="py-1 px-2 font-mono font-medium text-gray-900">W(\d+)</td>\s*<td class="py-1 px-2 text-gray-600">)[^<]+(</td>)'
            content = re.sub(pattern, replace_week_row, content)

            # Update narrative summary
            content = content.replace(
                "Over the 12-week observation cycle (May 31 to August 22, 2026)",
                "Over the 12-week observation cycle (June 21 to September 12, 2026)"
            )

            # Update table footer verification stamp
            content = content.replace(
                "Data period: May 31 – August 22, 2026 | Last verified: August 2026",
                f"Data period: June 21 – September 12, 2026 | Last verified: {NEW_DATE_DISPLAY}"
            )

            # Update Schema Dataset description and temporalCoverage
            content = content.replace(
                "Weekly normalized search attention index (May 31 - August 22, 2026)",
                "Weekly normalized search attention index (June 21 - September 12, 2026)"
            )
            content = content.replace(
                '"temporalCoverage": "2026-05-31/2026-08-22"',
                '"temporalCoverage": "2026-06-21/2026-09-12"'
            )

            with open(p, "w", encoding="utf-8") as fp:
                fp.write(content)
            count += 1
    print(f"[3] Updated 12-week trend tables and Dataset schemas across {count} pages.")

def update_weekly_trend_reports_and_hub_cards():
    report_count = 0
    hub_card_count = 0
    hub_callout_count = 0

    for root, dirs, files in os.walk(LOCAL_DIR):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8") as fp:
                content = fp.read()
            
            modified = False

            # A. In 261 Weekly Trend Reports
            if "how-crypto-gaming-search-trends-changed-" in p:
                # Time tag
                if '<time datetime="2026-08-20T09:00:00Z">August 16, 2026</time>' in content:
                    content = content.replace(
                        '<time datetime="2026-08-20T09:00:00Z">August 16, 2026</time>',
                        f'<time datetime="2026-09-17T09:00:00Z">{NEW_DATE_DISPLAY}</time>'
                    )
                    modified = True
                
                # dateModified schema
                if '"dateModified": "2026-08-20T09:00:00Z"' in content:
                    content = content.replace(
                        '"dateModified": "2026-08-20T09:00:00Z"',
                        '"dateModified": "2026-09-17T09:00:00Z"'
                    )
                    modified = True

                # Body narrative
                if 'period ending August 16, 2026 was' in content:
                    content = content.replace(
                        'period ending August 16, 2026 was',
                        f'period ending {NEW_WEEKLY_PERIOD} was'
                    )
                    modified = True

                if modified:
                    report_count += 1

            # B. In 261 Hubs (State and DMA)
            # 1. Overview Callout Box
            if 'During the weekly period ending August 16, 2026' in content:
                content = content.replace(
                    'During the weekly period ending August 16, 2026',
                    f'During the weekly period ending {NEW_WEEKLY_PERIOD}'
                )
                modified = True
                hub_callout_count += 1

            # 2. Data Report Card Tag
            if 'DATA REPORT</span>' in content and '<span>Aug 16, 2026</span>' in content:
                content = content.replace(
                    '<span>Aug 16, 2026</span>',
                    f'<span>{NEW_DATE_SHORT}</span>'
                )
                modified = True
                hub_card_count += 1

            if modified:
                with open(p, "w", encoding="utf-8") as fp:
                    fp.write(content)

    print(f"[4] Updated {report_count} weekly trend reports, {hub_callout_count} hub callouts, and {hub_card_count} hub data cards.")

def update_sitemaps():
    sitemap_path = os.path.join(INDEX_DIR, "local-sitemap.xml")
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as fp:
            s_content = fp.read()
        s_content = s_content.replace("<lastmod>2026-09-15</lastmod>", "<lastmod>2026-09-17</lastmod>")
        with open(sitemap_path, "w", encoding="utf-8") as fp:
            fp.write(s_content)
        print("[5] Updated index/local-sitemap.xml lastmod to 2026-09-17.")

    root_sitemap = os.path.join(INDEX_DIR, "sitemap.xml")
    if os.path.exists(root_sitemap):
        with open(root_sitemap, "r", encoding="utf-8") as fp:
            r_content = fp.read()
        r_content = re.sub(
            r'(<sitemap><loc>https://cryptocasinomedia\.com/local-sitemap\.xml</loc><lastmod>)[^<]+(</lastmod></sitemap>)',
            r'\g<1>2026-09-17\g<2>',
            r_content
        )
        with open(root_sitemap, "w", encoding="utf-8") as fp:
            fp.write(r_content)
        print("[6] Updated index/sitemap.xml local-sitemap lastmod to 2026-09-17.")

if __name__ == "__main__":
    print("=== Starting Batch Date Update across Local Directory ===")
    update_top_10_pages()
    update_hub_ranking_cards()
    update_12_week_trend_tables()
    update_weekly_trend_reports_and_hub_cards()
    update_sitemaps()
    print("=== Date Update Completed Successfully ===")
