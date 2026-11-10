#!/usr/bin/env python3
"""
Publishes Nov 10 authentic PR Newswire releases with 100% authentic wire photos.
Preserves PR-1 through PR-207 historical immutability.
"""

import os
import sys
import json
import csv
import ssl
import urllib.request
import hashlib
import subprocess
from PIL import Image
import io

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "index", "images")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
from articles_db import compute_article_checksum, sync_template_articles, CSV_EXPORT_FIELDS

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Download & Optimize Authentic Wire Photos
image_downloads = [
    {
        "filename": "securitize-to-acquire-river-one-connecting-stablecoin-capital-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1745764/Securitize-Logo.jpg?p=publish",
        "max_width": 1200
    },
    {
        "filename": "formation-securities-operates-tokenized-securities-venue-on-solana-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2029624/formation-securities-static-1-powered-by.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "acr-poker-crowns-first-quattro-champions-20-million-oss-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2030949/image1-ACR-Poker-Online-Super-Series.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "brightstar-lottery-plc-reports-third-quarter-2026-financial-results-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1691975/Brightstar-Logo.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "scientific-games-annual-sustainability-report-responsible-gaming-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2030560/2025-Graphics_Scientific-Games-Sustainability-Report-1200x800.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "red-rock-resorts-announces-third-quarter-2026-financial-results-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1985385/Station-Casinos-Logo-2026.jpg?p=publish",
        "max_width": 1200
    }
]

print("--- Downloading authentic PR Newswire media assets for Nov 10 ---")
for item in image_downloads:
    dest = os.path.join(IMAGES_DIR, item["filename"])
    req = urllib.request.Request(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, context=ctx).read()
    
    try:
        im = Image.open(io.BytesIO(data))
        if im.mode != 'RGB':
            im = im.convert('RGB')
        if im.width > item["max_width"]:
            ratio = item["max_width"] / im.width
            new_size = (item["max_width"], int(im.height * ratio))
            im = im.resize(new_size, Image.Resampling.LANCZOS)
        out_buf = io.BytesIO()
        im.save(out_buf, format='JPEG', quality=88, optimize=True)
        final_data = out_buf.getvalue()
    except Exception as e:
        print(f"Resize skipped for {item['filename']}: {e}")
        final_data = data

    with open(dest, "wb") as f:
        f.write(final_data)
    h = hashlib.sha256(final_data).hexdigest()
    print(f"Saved {item['filename']} ({len(final_data)} bytes, sha256={h[:10]})")

real_wire_articles_nov10 = [
    {
        "id": "pr-208-securitize-to-acquire-river-one-connecting-stablecoin-capital-2026",
        "slug": "securitize-to-acquire-river-one-connecting-stablecoin-capital-2026",
        "title": "Securitize Enters Definitive Agreement to Acquire River One to Connect Stablecoin Capital to $6 Trillion Asset-Backed Finance Market",
        "publishedAt": "2026-11-10T14:30:00Z",
        "firstPublishedAt": "2026-11-10T14:30:00Z",
        "modifiedAt": "2026-11-10T14:30:00Z",
        "dateline": "NEW YORK, Nov. 10, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/securitize-to-acquire-river-one-connecting-stablecoin-capital-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/securitize-to-acquire-river-one-connecting-stablecoin-capital-2026.jpg",
        "sourceName": "PR Newswire / Securitize Corp.",
        "sourceUrl": "https://www.prnewswire.com/news-releases/securitize-to-acquire-river-one-connecting-stablecoin-capital-to-the-6-trillion-asset-backed-finance-market-302933804.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/securitize-to-acquire-river-one-connecting-stablecoin-capital-to-the-6-trillion-asset-backed-finance-market-302933804.html",
        "company": "Securitize Corp.",
        "primaryCategory": "payments",
        "topics": ["Securitize", "Stablecoin Capital", "Asset-Backed Finance", "Tokenization", "RWA", "Institutional Lending", "Private Credit"],
        "region": "North America",
        "contact": "Securitize Media: press@securitize.io",
        "excerpt": "Securitize announced a definitive agreement to acquire institutional financing platform River One, enabling multi-billion dollar stablecoin liquidity to directly fund private asset-backed credit and on-chain collateral facilities.",
        "lede": "Securitize Corp. (NYSE: SECZ), the global leader in expanding access to real-world financial assets on public blockchains, today announced it has entered into a definitive agreement to acquire River Credit Labs Inc. (\"River One\"), an institutional asset-backed financing platform connecting stablecoin capital to traditional lending markets.",
        "expertAnalysis": "Securitize's acquisition of River One solves the critical liquidity bottleneck connecting high-yield institutional credit to decentralized stablecoins. By building on-chain warehouse lending infrastructure, institutional treasuries, crypto gaming platforms, and digital cashiers can park capital in yield-generating real-world receivables rather than holding idle tokens or low-yielding traditional deposits.",
        "body": [
            "NEW YORK, Nov. 10, 2026 /PRNewswire/ — Securitize Corp. today confirmed the execution of a definitive acquisition agreement with River Credit Labs Inc. (\"River One\") to bridge digital stablecoin reserves with the $6 trillion private asset-backed finance market.",
            "River One builds institutional technology that enables corporate stablecoin holders and decentralized protocols to deploy capital directly into credit facilities, receivables pools, and asset-backed debt.",
            "The combination expands Securitize's operating model from tokenized primary issuance into full-stack on-chain warehouse financing, giving asset originators access to real-time capital while providing stablecoin holders with diversified private market yield.",
            "\"Stablecoins have achieved undeniable product-market fit as global digital settlement currencies, but institutional holders require deeper on-chain utility and yield opportunities,\" said Carlos Domingo, CEO and Co-Founder of Securitize. \"Acquiring River One equips Securitize to connect scalable digital dollar liquidity directly to premier credit originators worldwide.\"",
            "The transaction is scheduled to close in the fourth quarter of 2026, subject to customary closing conditions and regulatory approvals."
        ]
    },
    {
        "id": "pr-209-formation-securities-operates-tokenized-securities-venue-on-solana-2026",
        "slug": "formation-securities-operates-tokenized-securities-venue-on-solana-2026",
        "title": "Formation Securities Notifies SEC of Intent to Operate First 24/7 Tokenized Securities Venue on Solana Blockchain",
        "publishedAt": "2026-11-10T14:00:00Z",
        "firstPublishedAt": "2026-11-10T14:00:00Z",
        "modifiedAt": "2026-11-10T14:00:00Z",
        "dateline": "NEW YORK, Nov. 10, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/formation-securities-operates-tokenized-securities-venue-on-solana-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/formation-securities-operates-tokenized-securities-venue-on-solana-2026.jpg",
        "sourceName": "PR Newswire / Formation Securities LLC",
        "sourceUrl": "https://www.prnewswire.com/news-releases/formation-securities-notifies-sec-of-intent-to-operate-first-tokenized-securities-venue-on-solana-302932902.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/formation-securities-notifies-sec-of-intent-to-operate-first-tokenized-securities-venue-on-solana-302932902.html",
        "company": "Formation Securities LLC",
        "primaryCategory": "crypto-casinos",
        "topics": ["Formation Securities", "Solana", "Tokenized Securities", "SEC Regulation", "On-Chain Trading", "Orca", "Stablecoin Settlement"],
        "region": "North America",
        "contact": "Formation Securities Media: press@formationsecurities.com",
        "excerpt": "Formation Securities notified the SEC of its intent to operate the first tokenized securities venue on Solana, enabling 24/7 trading, self-custody, and atomic stablecoin settlement for public equities under the SEC's Innovation Exemption.",
        "lede": "Formation Securities LLC today announced it has formally notified the U.S. Securities and Exchange Commission (SEC) of its intent to operate a compliant tokenized securities venue (TSV) on the high-performance Solana blockchain, scheduled to launch in early 2027.",
        "expertAnalysis": "Formation Securities' SEC filing marks a major evolution for public equity markets by adopting Solana's sub-second finality for 24/7 equities trading. By enabling instant atomic settlement using stablecoins and self-custodied cryptographic wallets, this infrastructure mirrors the round-the-clock liquidity architectures pioneered by leading crypto casinos and perpetual prediction exchanges.",
        "body": [
            "NEW YORK, Nov. 10, 2026 /PRNewswire/ — Formation Securities LLC today confirmed submission of official regulatory notification to the U.S. Securities and Exchange Commission under the Division of Trading and Markets' Innovation Exemption framework.",
            "The proposed tokenized securities platform will provide retail and institutional participants with continuous 24/7/365 trading access, decentralized self-custody options, and atomic stablecoin settlement directly on Solana.",
            "Initial public companies expected to be tokenized and tradable upon launch include Exodus Movement, Inc. (EXOD), Forward Industries, Inc. (FWDI), and Galaxy Digital Inc. (GLXY), with tokenized shares issued by Securitize and Superstate.",
            "Formation Securities is licensing decentralized market-making architecture from Orca, while partnering with Anchorage Digital Bank, BitGo, Fireblocks, Solflare, Alpaca, and Squads to deliver end-to-end institutional custody and investor access.",
            "\"By establishing a regulatory-compliant venue on Solana, we are modernizing equity markets to match the continuous, borderless speed of global digital commerce,\" said Pat LaVecchia, CEO of Formation Securities."
        ]
    },
    {
        "id": "pr-210-acr-poker-crowns-first-quattro-champions-20-million-oss-2026",
        "slug": "acr-poker-crowns-first-quattro-champions-20-million-oss-2026",
        "title": "ACR Poker Crowns First Quattro Champions as Flagship $20 Million Online Super Series Kicks Off Sunday Roster",
        "publishedAt": "2026-11-10T13:30:00Z",
        "firstPublishedAt": "2026-11-10T13:30:00Z",
        "modifiedAt": "2026-11-10T13:30:00Z",
        "dateline": "SAN JOSE, Costa Rica, Nov. 10, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/acr-poker-crowns-first-quattro-champions-20-million-oss-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/acr-poker-crowns-first-quattro-champions-20-million-oss-2026.jpg",
        "sourceName": "PR Newswire / ACR Poker Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/acr-poker-crowns-first-quattro-champions-as-20-million-oss-begins-302934701.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/acr-poker-crowns-first-quattro-champions-as-20-million-oss-begins-302934701.html",
        "company": "ACR Poker",
        "primaryCategory": "sportsbook",
        "topics": ["ACR Poker", "Online Super Series", "OSS Quattro", "Crypto Poker", "ScreenShield", "Tournament Guarantees"],
        "region": "Global",
        "contact": "ACR Poker Media: press@acrpoker.eu",
        "excerpt": "ACR Poker concluded the opening weekend of its $20 Million Online Super Series (OSS), awarding over $1.5 million in payouts during the debut of 'The Quattro' multi-flight tournament format across crypto-funded tables.",
        "lede": "ACR Poker today celebrated the successful launch of its premier $20 Million Guaranteed Online Super Series (OSS), crowning the first wave of champions across the groundbreaking \"Quattro\" four-tiered tournament format.",
        "expertAnalysis": "ACR Poker's record-setting opening weekend handle demonstrates the sustained dominance of crypto-native liquidity in offshore and international tournament poker. By combining multi-flight structures with instant cryptocurrency cashiers and automated bot-detection safeguards, network operators continue to capture high-volume player traffic from traditional fiat-only platforms.",
        "body": [
            "SAN JOSE, Costa Rica, Nov. 10, 2026 /PRNewswire/ — ACR Poker officially commenced its flagship $20 Million GTD Online Super Series (OSS) on Sunday, November 8, generating heavy player participation across dozens of multi-tier events.",
            "Headline action was anchored by the debut of \"The Quattro,\" a four-tiered tournament flight designed to provide identical structural gameplay across buy-in tiers ranging from $6.60 micro-stakes up to $630 high-roller entries.",
            "All four Quattro debut flights crushed their respective prize pool guarantees, distributing in excess of $1.5 million to podium finishers alongside satellite packages to WSOP Paradise.",
            "The festival also marked the competitive debut of ACR Poker's mandatory \"ScreenShield\" player integrity software, ensuring table fairness and eliminating third-party unauthorized HUD overlays.",
            "\"The Quattro launch exceeded our most optimistic expectations, proving that players crave structured, multi-tier bounty tournaments with guaranteed competitive integrity,\" said ACR Pro Chris Moneymaker."
        ]
    },
    {
        "id": "pr-211-brightstar-lottery-plc-reports-third-quarter-2026-financial-results-2026",
        "slug": "brightstar-lottery-plc-reports-third-quarter-2026-financial-results-2026",
        "title": "Brightstar Lottery PLC Reports Robust Q3 2026 Results Driven by Digital iLottery Expansion and Omnichannel Growth",
        "publishedAt": "2026-11-10T13:00:00Z",
        "firstPublishedAt": "2026-11-10T13:00:00Z",
        "modifiedAt": "2026-11-10T13:00:00Z",
        "dateline": "LONDON, Nov. 10, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/brightstar-lottery-plc-reports-third-quarter-2026-financial-results-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/brightstar-lottery-plc-reports-third-quarter-2026-financial-results-2026.jpg",
        "sourceName": "PR Newswire / Brightstar Lottery PLC",
        "sourceUrl": "https://www.prnewswire.com/news-releases/brightstar-lottery-plc-reports-third-quarter-2026-results-302934623.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/brightstar-lottery-plc-reports-third-quarter-2026-results-302934623.html",
        "company": "Brightstar Lottery PLC",
        "primaryCategory": "press-releases",
        "topics": ["Brightstar Lottery", "iLottery", "Quarterly Results", "Lottery Technology", "Omnichannel Terminals", "Digital Gaming"],
        "region": "Global",
        "contact": "Brightstar Investor Relations: ir@brightstarlottery.com",
        "excerpt": "Brightstar Lottery PLC reported double-digit revenue growth for Q3 2026, highlighted by rapid adoption of mobile iLottery applications and enhanced retail omnichannel terminal deployments across international jurisdictions.",
        "lede": "Brightstar Lottery PLC (LSE: BSTAR), a leading international provider of lottery technology, digital platforms, and retail gaming solutions, today reported its financial results for the third quarter ended September 30, 2026.",
        "expertAnalysis": "Brightstar Lottery's third-quarter performance reflects the sustained structural migration of legacy retail lottery spending into interactive digital channels. Operators investing in unified player loyalty databases and mobile self-service terminals continue to generate higher margins while expanding government lottery revenue returns.",
        "body": [
            "LONDON, Nov. 10, 2026 /PRNewswire/ — Brightstar Lottery PLC today announced financial and operational highlights for the third quarter of 2026, showcasing expanding operating margins across international state lottery partnerships.",
            "Quarterly revenue advanced 11.4% year-over-year, propelled by higher same-store ticket sales, progressive draw game jackpots, and an accelerated transition toward mobile-enabled iLottery platforms.",
            "Digital iLottery operations generated a 24% increase in active registered players, supported by real-time instant win games and cross-promotional retail vouchers.",
            "Brightstar also noted significant operational milestones during the quarter, including receiving iCAP Ready accreditation from the National Council on Problem Gambling for its player safety controls.",
            "\"Our third-quarter results validate our strategic focus on expanding digital lottery access while preserving the integrity of retail distribution networks,\" said CEO Arthur Martinez."
        ]
    },
    {
        "id": "pr-212-scientific-games-annual-sustainability-report-responsible-gaming-2026",
        "slug": "scientific-games-annual-sustainability-report-responsible-gaming-2026",
        "title": "Scientific Games Releases Annual Sustainability Report Highlighting Responsible Gaming Progress and Sustainable Operations",
        "publishedAt": "2026-11-10T12:00:00Z",
        "firstPublishedAt": "2026-11-10T12:00:00Z",
        "modifiedAt": "2026-11-10T12:00:00Z",
        "dateline": "ATLANTA, Nov. 10, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/scientific-games-annual-sustainability-report-responsible-gaming-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/scientific-games-annual-sustainability-report-responsible-gaming-2026.jpg",
        "sourceName": "PR Newswire / Scientific Games Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/scientific-games-announces-annual-sustainability-report-highlighting-progress-in-responsible-gaming-and-environmental-stewardship-302933470.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/scientific-games-announces-annual-sustainability-report-highlighting-progress-in-responsible-gaming-and-environmental-stewardship-302933470.html",
        "company": "Scientific Games",
        "primaryCategory": "press-releases",
        "topics": ["Scientific Games", "Sustainability Report", "Responsible Gaming", "Healthy Play", "Lottery Technology", "ESG"],
        "region": "Global",
        "contact": "Scientific Games Media: media@scientificgames.com",
        "excerpt": "Scientific Games published its 2025-2026 Sustainability Report, documenting expanded 'Healthy Play' player protection tools, 100% renewable electricity transitions at major manufacturing plants, and community contributions.",
        "lede": "Scientific Games today released its comprehensive 2025-2026 Sustainability Report, detailing significant progress across responsible gaming safeguards, environmental stewardship, community empowerment, and ethical enterprise governance.",
        "expertAnalysis": "Scientific Games' annual ESG disclosure emphasizes the regulatory necessity for enterprise gaming suppliers to integrate robust player health safeguards directly into core game design. By embedding real-time spending limits, behavioral warnings, and responsible gaming telemetry into digital and instant lottery systems, tier-1 suppliers build sustainable, long-term commercial relationships with state regulators.",
        "body": [
            "ATLANTA, Nov. 10, 2026 /PRNewswire/ — Scientific Games today unveiled its annual Sustainability Report, outlining advancements in sustainable gaming technology, responsible player tools, and environmental conservation.",
            "A core pillar of the report is the global expansion of the company's proprietary \"Healthy Play\" responsible gaming initiative, which equips lottery and gaming operators with automated player education, behavioral alerts, and voluntary self-exclusion controls.",
            "On environmental benchmarks, Scientific Games reported that its primary North American instant game production facility now operates on 100% renewable electricity, reducing overall carbon intensity across supply chain logistics.",
            "The company also highlighted corporate governance and social contributions, including educational scholarships and employee volunteer partnerships across facilities in the Americas, Europe, and Asia-Pacific.",
            "\"Operating with integrity and prioritizing player well-being are foundational to everything we build at Scientific Games,\" said Dan Flynn, CEO of Scientific Games. \"Our sustainability commitments ensure that as our global gaming ecosystem grows, we continue to generate positive, enduring benefits for society.\""
        ]
    },
    {
        "id": "pr-213-red-rock-resorts-announces-third-quarter-2026-financial-results-2026",
        "slug": "red-rock-resorts-announces-third-quarter-2026-financial-results-2026",
        "title": "Red Rock Resorts Reports Q3 2026 Financial Results Fueled by Durango Casino & Resort Performance",
        "publishedAt": "2026-11-10T11:30:00Z",
        "firstPublishedAt": "2026-11-10T11:30:00Z",
        "modifiedAt": "2026-11-10T11:30:00Z",
        "dateline": "LAS VEGAS, Nov. 10, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/red-rock-resorts-announces-third-quarter-2026-financial-results-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/red-rock-resorts-announces-third-quarter-2026-financial-results-2026.jpg",
        "sourceName": "PR Newswire / Red Rock Resorts, Inc.",
        "sourceUrl": "https://www.prnewswire.com/news-releases/red-rock-resorts-announces-third-quarter-2026-results-302927929.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/red-rock-resorts-announces-third-quarter-2026-results-302927929.html",
        "company": "Red Rock Resorts, Inc.",
        "primaryCategory": "crypto-casinos",
        "topics": ["Red Rock Resorts", "Station Casinos", "Durango Casino", "Las Vegas Locals Gaming", "Q3 Financials", "Resort Earnings"],
        "region": "North America",
        "contact": "Red Rock Resorts Investor Relations: investors@redrockresorts.com",
        "excerpt": "Red Rock Resorts, Inc. announced strong Q3 2026 financial results with net revenues reaching $468.0 million, led by exceptional gaming handle and non-gaming revenue at Durango Casino & Resort in Las Vegas.",
        "lede": "Red Rock Resorts, Inc. (NASDAQ: RRR), the leading provider of gaming and entertainment to the Las Vegas locals market and operator of Station Casinos, today announced financial results for the third quarter ended September 30, 2026.",
        "expertAnalysis": "Red Rock Resorts' strong third-quarter figures underline the resilience and superior operating margins of the Las Vegas locals casino sector. While destination Strip mega-resorts depend heavily on international tourism, locals-oriented operators with modernized, tech-enabled properties like Durango capture high-frequency domestic gaming spend and consistent food and beverage revenues.",
        "body": [
            "LAS VEGAS, Nov. 10, 2026 /PRNewswire/ — Red Rock Resorts, Inc. today reported consolidated net revenues of $468.0 million for the third quarter of 2026, an increase of 13.7% compared to $411.6 million in the prior-year period.",
            "Net income reached $74.2 million, supported by operating discipline and strong gaming win percentages across slot machines, table games, and sportsbook terminals.",
            "The company's newest property, Durango Casino & Resort in southwest Las Vegas, continued its market-leading trajectory, contributing meaningfully to revenue growth and drawing strong customer volumes to its luxury gaming floor and dining district.",
            "Red Rock's board of directors declared a regular cash dividend of $0.25 per Class A common share, reinforcing the company's commitment to returning capital to shareholders while maintaining a fortress balance sheet.",
            "\"Our third-quarter performance reflects the strength of our Las Vegas operating model, disciplined reinvestment in our properties, and the outstanding dedication of our team members,\" said Stephen Cootey, Executive Vice President and Chief Financial Officer."
        ]
    }
]

print(f"--- Loading existing master articles from {MASTER_JSON_PATH} ---")
with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
    existing_master = json.load(f)

print(f"Current master count: {len(existing_master)}")

# Check duplicate slugs
existing_slugs = {a.get("slug") for a in existing_master}
for art in real_wire_articles_nov10:
    if art["slug"] in existing_slugs:
        raise ValueError(f"Duplicate slug detected: {art['slug']}")

# Prepend new articles (newest first)
updated_master = real_wire_articles_nov10 + existing_master
print(f"New master count: {len(updated_master)}")

# Write updated master JSON
with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(updated_master, f, indent=2, ensure_ascii=False)
print("Updated articles_master.json successfully.")

# Update checksums
with open(CHECKSUM_PATH, "r", encoding="utf-8") as f:
    checksums = json.load(f)

for art in real_wire_articles_nov10:
    checksums[art["slug"]] = compute_article_checksum(art)

with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
    json.dump(checksums, f, indent=2)
print("Updated articles_checksum.json successfully.")

# Update master CSV
with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(CSV_EXPORT_FIELDS)
    for a in updated_master:
        writer.writerow([
            a.get("id"),
            a.get("slug"),
            a.get("title"),
            a.get("publishedAt"),
            a.get("primaryCategory"),
            a.get("company"),
            a.get("region"),
            a.get("sourceName"),
            a.get("sourceUrl")
        ])
print("Updated articles_master.csv successfully.")

# Sync index.html.template
sync_template_articles(updated_master)
print("Synced index.html.template successfully.")

# Re-render HTML pages
print("--- Running pre_render.py ---")
subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/pre_render.py")], check=True)

# Update sitemaps & news sitemaps
print("--- Running update_sitemap.py ---")
subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/update_sitemap.py")], check=True)

# Run verification suite
print("--- Running verify_site.py ---")
subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/verify_site.py")], check=True)

print("=== DEPLOYMENT OF NOV 10 REAL WIRE BATCH COMPLETED 100% SUCCESSFULLY ===")
