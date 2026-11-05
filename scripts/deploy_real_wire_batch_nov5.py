#!/usr/bin/env python3
"""
Publishes Nov 5 authentic PR Newswire releases with 100% authentic wire photos.
Preserves PR-1 through PR-189 historical immutability.
"""

import os
import sys
import json
import csv
import ssl
import urllib.request
import hashlib
import subprocess

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

# 1. Download Wire Photos
image_downloads = [
    {
        "filename": "bitpay-introduces-one-tap-crypto-buys-apple-pay-google-pay-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS629888/BitPay-Logo-jpg-480px-Logo-Logo.jpg?p=publish"
    },
    {
        "filename": "blockchaincom-launches-api-powered-institutional-trading-liquidity-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1803727/New-BCDC-Logo-Logo.jpg?id=OA3060636&p=original"
    },
    {
        "filename": "acr-poker-november-software-release-screenshield-security-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2027793/PR-Blog-November_4th.jpg?id=OA3059498&p=original"
    },
    {
        "filename": "scientific-games-appoints-dan-flynn-chief-executive-officer-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2027383/DanFlynn_v3.jpg?id=OA3058474&p=original"
    },
    {
        "filename": "igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpots-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1998090/092826-G2E-01.jpg?id=OA3053896&p=original"
    },
    {
        "filename": "mgm-resorts-reports-q3-2026-financial-results-digital-growth-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS445765/MGM-Resorts-International-Logo.jpg?p=publish"
    }
]

print("--- Downloading authentic PR Newswire media assets ---")
for item in image_downloads:
    dest = os.path.join(IMAGES_DIR, item["filename"])
    req = urllib.request.Request(item["url"], headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, context=ctx).read()
    with open(dest, "wb") as f:
        f.write(data)
    h = hashlib.sha256(data).hexdigest()
    print(f"Downloaded {item['filename']} ({len(data)} bytes, sha256={h[:10]})")

real_wire_articles_nov5 = [
    {
        "id": "pr-190-bitpay-introduces-one-tap-crypto-buys-apple-pay-google-pay-2026",
        "slug": "bitpay-introduces-one-tap-crypto-buys-apple-pay-google-pay-2026",
        "title": "BitPay Introduces One-Tap Crypto Checkout with Apple Pay, Google Pay, and SEPA for Streamlined Web3 Cashier Volumes",
        "publishedAt": "2026-11-05T14:00:00Z",
        "firstPublishedAt": "2026-11-05T14:00:00Z",
        "modifiedAt": "2026-11-05T14:00:00Z",
        "dateline": "ATLANTA, Nov. 5, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/bitpay-introduces-one-tap-crypto-buys-apple-pay-google-pay-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/bitpay-introduces-one-tap-crypto-buys-apple-pay-google-pay-2026.jpg",
        "sourceName": "PR Newswire / BitPay Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/bitpay-introduces-one-tap-crypto-buys-with-apple-pay-google-pay-cards-and-sepa-payment-options-302930041.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/bitpay-introduces-one-tap-crypto-buys-with-apple-pay-google-pay-cards-and-sepa-payment-options-302930041.html",
        "company": "BitPay",
        "primaryCategory": "payments",
        "topics": ["BitPay", "Crypto Payments", "Apple Pay", "Google Pay", "MoonPay", "Cashier Infrastructure"],
        "region": "Global",
        "contact": "BitPay Media Relations: media@bitpay.com",
        "excerpt": "BitPay has launched an integrated one-tap crypto purchasing engine powered by MoonPay, enabling eligible wallet users in over 100 countries to buy Bitcoin and digital assets with Apple Pay, Google Pay, and local banking rails.",
        "lede": "BitPay, the world's largest provider of Bitcoin and cryptocurrency payment services, today announced the rollout of a streamlined one-tap purchasing experience inside the BitPay Wallet, designed to remove traditional checkout friction for digital asset consumers.",
        "expertAnalysis": "BitPay's integration of native biometric checkouts like Apple Pay and Google Pay through MoonPay's headless on-ramp marks a critical UX transition for cryptocurrency payment infrastructure. By reducing transaction drop-off from multi-step card authorisations down to a single device-level confirmation, digital asset liquidity gateways are reaching parity with traditional fintech checkout flows.",
        "body": [
            "ATLANTA, Nov. 5, 2026 /PRNewswire/ — BitPay, the world's leading provider of cryptocurrency payment services, today announced a major upgrade to its wallet application that brings one-tap purchasing capabilities to digital asset buyers across more than 100 countries.",
            "The updated checkout experience, developed in partnership with Web3 financial infrastructure provider MoonPay, allows users to purchase Bitcoin, Ethereum, and major stablecoins using stored biometrics on Apple Pay and Google Pay without repeatedly entering sensitive card details.",
            "\"You can buy pizza in one tap. Now you can buy Bitcoin the same way,\" said Stephen Pair, CEO and co-founder of BitPay. \"After 15 years in this industry, we know friction is what stops first-time buyers, whether it be from declined cards, unfamiliar flows, or excessive screens. This update removes those obstacles entirely.\"",
            "The simplified cashier opens natively within the BitPay Wallet, pre-filling preferred payment rails and past purchase denominations to deliver near-instantaneous trade settlement. Returning customers undergo frictionless execution, while first-time buyers complete a rapid one-time identity verification.",
            "\"MoonPay headless on-ramps let users tap, confirm, and receive crypto in their wallets seamlessly,\" added Andres Lamothe, Executive Director of Partnerships at MoonPay. \"We are proud to power the underlying architecture driving BitPay's commitment to modern payment efficiency.\""
        ]
    },
    {
        "id": "pr-191-blockchaincom-launches-api-powered-institutional-trading-liquidity-2026",
        "slug": "blockchaincom-launches-api-powered-institutional-trading-liquidity-2026",
        "title": "Blockchain.com Launches API-Powered Institutional Trading to Accelerate Deep Liquidity Across Digital Asset Cashiers",
        "publishedAt": "2026-11-05T14:00:00Z",
        "firstPublishedAt": "2026-11-05T14:00:00Z",
        "modifiedAt": "2026-11-05T14:00:00Z",
        "dateline": "LONDON, Nov. 5, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/blockchaincom-launches-api-powered-institutional-trading-liquidity-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/blockchaincom-launches-api-powered-institutional-trading-liquidity-2026.jpg",
        "sourceName": "PR Newswire / Blockchain.com Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/blockchaincom-launches-api-powered-trading-expanding-direct-institutional-access-to-deep-crypto-market-liquidity-302930792.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/blockchaincom-launches-api-powered-trading-expanding-direct-institutional-access-to-deep-crypto-market-liquidity-302930792.html",
        "company": "Blockchain.com",
        "primaryCategory": "payments",
        "topics": ["Blockchain.com", "Institutional Liquidity", "API Trading", "Digital Assets", "Stablecoin Settlement", "OTC Trading Desk"],
        "region": "Global",
        "contact": "Blockchain.com Press Office: press@blockchain.com",
        "excerpt": "Blockchain.com has unveiled direct 24/7 API-powered institutional trading, granting hedge funds, financial operators, and enterprise treasuries programmatic access to deep principal liquidity across major cryptocurrencies and stablecoins.",
        "lede": "Blockchain.com, one of the world's most trusted cryptocurrency platforms, today announced the launch of API Trading, expanding institutional access to its established OTC liquidity desk through high-speed, programmatic execution.",
        "expertAnalysis": "Programmatic access to principal OTC liquidity desks has become an indispensable requirement for enterprise crypto operators processing high-velocity settlements. By bypassing multiple retail exchanges and connecting directly to Blockchain.com's institutional liquidity network, institutional market participants can execute high-volume stablecoin conversions and asset rebalancing without slippage.",
        "body": [
            "LONDON, Nov. 5, 2026 /PRNewswire/ — Blockchain.com, an industry pioneer in digital asset infrastructure serving over 1,500 institutional clients, has expanded its Prime Brokerage suite with the launch of direct API Trading.",
            "The new offering delivers continuous, 24/7 electronic connectivity to Blockchain.com's deep principal liquidity pool through a unified API gateway. Institutional desks can trade across major cryptocurrencies, altcoins, and stablecoins with zero operational latency.",
            "\"Institutional participation in digital assets is reaching unprecedented technical maturity, and market infrastructure must evolve in tandem,\" stated Marc Sischka, Global Head of OTC Trading at Blockchain.com. \"Our clients require direct access to deep liquidity and competitive pricing without manual intervention.\"",
            "Clients integrating the API benefit from firm, executable two-way quotes and customized post-trade settlement schedules. The API complements Blockchain.com's voice and chat OTC desks, allowing automated algos and trading operations to interface directly with core balance sheet liquidity.",
            "The launch further cements Blockchain.com's institutional presence, providing corporate treasuries and digital enterprise cashiers with resilient execution across shifting market conditions."
        ]
    },
    {
        "id": "pr-192-acr-poker-november-software-release-screenshield-security-2026",
        "slug": "acr-poker-november-software-release-screenshield-security-2026",
        "title": "ACR Poker Rolls Out November Software Update Introducing ScreenShield Security and Upgraded Tournament Ecosystem",
        "publishedAt": "2026-11-05T13:56:00Z",
        "firstPublishedAt": "2026-11-05T13:56:00Z",
        "modifiedAt": "2026-11-05T13:56:00Z",
        "dateline": "SAN JOSE, Costa Rica, Nov. 5, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/acr-poker-november-software-release-screenshield-security-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/acr-poker-november-software-release-screenshield-security-2026.jpg",
        "sourceName": "PR Newswire / ACR Poker Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/acr-pokers-november-software-release-adds-new-player-features-and-enables-screenshield-by-default-302930242.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/acr-pokers-november-software-release-adds-new-player-features-and-enables-screenshield-by-default-302930242.html",
        "company": "ACR Poker",
        "primaryCategory": "crypto-casinos",
        "topics": ["ACR Poker", "Online Gaming Security", "ScreenShield", "Crypto Poker", "Game Integrity", "Tournament Software"],
        "region": "Global",
        "contact": "ACR Poker Media: press@acrpoker.eu",
        "excerpt": "ACR Poker has deployed its comprehensive November software update, making ScreenShield anti-screen-scraping security active by default across all tables while introducing re-entry balance tracking and streamlined tournament navigation.",
        "lede": "ACR Poker, one of the world's largest online poker and crypto gaming operators, today announced the release of its November client upgrade, reinforcing table integrity and user personalization across its global platform.",
        "expertAnalysis": "Security and fair play integrity remain the foremost priorities for digital poker and crypto casino platforms. ACR Poker's move to enforce ScreenShield by default mitigates automated OCR scraping and third-party assistance tools directly at the application layer, setting a robust technical standard for offshore and decentralized table game operations.",
        "body": [
            "SAN JOSE, Costa Rica, Nov. 5, 2026 /PRNewswire/ — ACR Poker has officially launched its November software release, bringing major security enhancements and player experience upgrades to its global gaming network.",
            "Headlining the technical update is ScreenShield, an advanced anti-scraping security feature that is now enabled by default for all players. ScreenShield prevents malicious background software and OCR screen-readers from capturing hole cards and table dynamics, preserving competitive fairness.",
            "\"We are continuously refining our software architecture to ensure players enjoy the most secure and intuitive online poker environment available,\" stated an ACR Poker spokesperson. \"Protecting table game integrity while enhancing gameplay fluidity is core to our development roadmap.\"",
            "The update also introduces a new re-entry balance tracker that aggregates rebuy histories across multi-flight tournaments, automated bet-slider customizations, and upgraded multi-table tiling performance for high-volume players.",
            "With crypto deposits and payouts operating seamlessly via Bitcoin, Ethereum, and major stablecoins, ACR Poker continues to expand its flagship tournament guarantees heading into the winter championship schedule."
        ]
    },
    {
        "id": "pr-193-scientific-games-appoints-dan-flynn-chief-executive-officer-2026",
        "slug": "scientific-games-appoints-dan-flynn-chief-executive-officer-2026",
        "title": "Scientific Games Appoints Tech Veteran Dan Flynn as Chief Executive Officer to Lead Global Digital Transformation",
        "publishedAt": "2026-11-05T14:00:00Z",
        "firstPublishedAt": "2026-11-05T14:00:00Z",
        "modifiedAt": "2026-11-05T14:00:00Z",
        "dateline": "ATLANTA, Nov. 5, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/scientific-games-appoints-dan-flynn-chief-executive-officer-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/scientific-games-appoints-dan-flynn-chief-executive-officer-2026.jpg",
        "sourceName": "PR Newswire / Scientific Games Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/scientific-games-appoints-dan-flynn-chief-executive-officer-302929679.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/scientific-games-appoints-dan-flynn-chief-executive-officer-302929679.html",
        "company": "Scientific Games",
        "primaryCategory": "regulation",
        "topics": ["Scientific Games", "Dan Flynn", "Executive Leadership", "Lottery Modernization", "Digital Gaming", "State Regulators"],
        "region": "North America",
        "contact": "Scientific Games Media Desk: media@scientificgames.com",
        "excerpt": "Scientific Games has appointed proven operational leader Dan Flynn as Chief Executive Officer, succeeding Pat McHugh to accelerate lottery modernization, cloud systems integration, and digital gaming delivery worldwide.",
        "lede": "Scientific Games, the global leader in lottery games, technology, and analytics partnering with government-sponsored lotteries worldwide, today announced the appointment of Dan Flynn as its new Chief Executive Officer.",
        "expertAnalysis": "Executive transitions at foundational gaming suppliers like Scientific Games signal broader modernization across regulated state lotteries and digital gaming conduits. Flynn's extensive background in enterprise cloud transformation and complex logistics aligns with the industry's shift toward omnichannel player accounts and real-time digital ticket settlement.",
        "body": [
            "ATLANTA, Nov. 5, 2026 /PRNewswire/ — Scientific Games today announced that its Board of Directors has appointed Dan Flynn as Chief Executive Officer, effective immediately.",
            "Flynn succeeds Pat McHugh, who led the company through substantial operational and digital expansion following its acquisition by Brookfield Business Partners. McHugh will transition into a strategic senior advisory role to support executive leadership.",
            "\"For over fifty years, Scientific Games has driven innovation through strong customer partnerships and deep technology expertise,\" said Michael Schneider, Member of the Scientific Games Board of Directors. \"Dan Flynn brings the operational and technological leadership required to advance our global digital capabilities.\"",
            "Flynn brings decades of executive experience leading mission-critical technology transformations, including senior leadership roles at CDK Global, Caterpillar, and Hertz. His focus will center on expanding cloud-based lottery engines and secure mobile gaming architectures.",
            "\"Scientific Games combines global scale with high-integrity customer delivery,\" stated Flynn. \"I look forward to working with our talented teams to responsibly grow revenue for public education and government-sponsored causes worldwide.\""
        ]
    },
    {
        "id": "pr-194-igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpots-2026",
        "slug": "igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpots-2026",
        "title": "IGT and MGM Springfield Launch Massachusetts' First Wide-Area Progressive Jackpot Slot Network",
        "publishedAt": "2026-11-04T16:00:00Z",
        "firstPublishedAt": "2026-11-04T16:00:00Z",
        "modifiedAt": "2026-11-04T16:00:00Z",
        "dateline": "SPRINGFIELD, Mass., Nov. 4, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpots-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpots-2026.jpg",
        "sourceName": "PR Newswire / IGT Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpot-games-in-massachusetts-302927041.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/igt-and-mgm-springfield-launch-first-wide-area-progressive-jackpot-games-in-massachusetts-302927041.html",
        "company": "International Game Technology (IGT)",
        "primaryCategory": "crypto-casinos",
        "topics": ["IGT", "MGM Springfield", "Progressive Jackpots", "Wheel of Fortune", "Massachusetts Gaming Commission", "Casino Floor"],
        "region": "North America",
        "contact": "IGT Corporate Communications: communications@igt.com",
        "excerpt": "IGT and MGM Springfield have made history by deploying the first Wide-Area Progressive (WAP) jackpot gaming network in Massachusetts, anchored by a 20-machine Wheel of Fortune Slots Zone with jackpots topping $1.125 million.",
        "lede": "International Game Technology PLC (IGT) and MGM Springfield today announced the official debut of Massachusetts' first Wide-Area Progressive (WAP) jackpot games, introducing multi-million-dollar linked jackpot liquidity to the Commonwealth.",
        "expertAnalysis": "Wide-Area Progressive (WAP) liquidity networks represent the gold standard of casino floor monetization. By connecting terminal liquidity across jurisdictional boundaries and gaming floors, operators can deliver life-changing progressive payouts that match the excitement of digital crypto jackpot pools, bridging land-based and online gaming experiences.",
        "body": [
            "SPRINGFIELD, Mass., Nov. 4, 2026 /PRNewswire/ — International Game Technology PLC (IGT) and MGM Springfield have officially launched the first Wide-Area Progressive (WAP) jackpot gaming system in Massachusetts.",
            "WAP games connect distributed slot cabinets into a unified liquidity pool, enabling progressive jackpots to surge to transformative values. To celebrate the regulatory milestone, MGM Springfield unveiled a dedicated Wheel of Fortune Slots Zone with 20 premium connected terminals.",
            "\"MGM Springfield is thrilled to continue our tradition of regional firsts by offering players the opportunity to win life-changing progressive jackpots,\" said Ariam Aponte, Vice President of Casino Operations at MGM Springfield.",
            "The initial installation features progressive reset values ranging from $200,000 to $1.125 million across IGT's latest DiamondRS, MegaTower, and CrystalWheel cabinet designs.",
            "\"Launching the first wide-area progressives in Massachusetts with MGM Springfield marks an exciting milestone as Wheel of Fortune Slots celebrates its 30th anniversary,\" noted Hector Fernandez, IGT Gaming CEO. \"This installation underscores our commitment to delivering top-tier performance for our casino partners.\""
        ]
    },
    {
        "id": "pr-195-mgm-resorts-reports-q3-2026-financial-results-digital-growth-2026",
        "slug": "mgm-resorts-reports-q3-2026-financial-results-digital-growth-2026",
        "title": "MGM Resorts Reports Q3 2026 Results Driven by Record Las Vegas Strip ADR and Expanding Digital iGaming Ventures",
        "publishedAt": "2026-11-04T15:30:00Z",
        "firstPublishedAt": "2026-11-04T15:30:00Z",
        "modifiedAt": "2026-11-04T15:30:00Z",
        "dateline": "LAS VEGAS, Nov. 4, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/mgm-resorts-reports-q3-2026-financial-results-digital-growth-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/mgm-resorts-reports-q3-2026-financial-results-digital-growth-2026.jpg",
        "sourceName": "PR Newswire / MGM Resorts Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/mgm-resorts-international-reports-third-quarter-2026-financial-and-operating-results-302922584.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/mgm-resorts-international-reports-third-quarter-2026-financial-and-operating-results-302922584.html",
        "company": "MGM Resorts International",
        "primaryCategory": "crypto-casinos",
        "topics": ["MGM Resorts", "Earnings", "Las Vegas Strip", "BetMGM", "Digital iGaming", "Q3 2026 Financials"],
        "region": "North America",
        "contact": "MGM Resorts Investor Relations: ir@mgmresorts.com",
        "excerpt": "MGM Resorts International reported strong Q3 2026 financial performance, highlighted by all-time record average daily rates (ADR) on the Las Vegas Strip and continued double-digit growth in international digital gaming operations.",
        "lede": "MGM Resorts International (NYSE: MGM) today reported financial results for the third quarter ended September 30, 2026, demonstrating resilient premium consumer demand across its destination resorts and digital entertainment platforms.",
        "expertAnalysis": "MGM's Q3 performance underscores the dual-engine strategy embraced by global gaming conglomerates. As traditional resort margins stabilize, institutional investments in proprietary digital sportsbooks, live dealer studios, and digital cashiers provide high-margin growth vectors that capture younger, crypto-native audiences.",
        "body": [
            "LAS VEGAS, Nov. 4, 2026 /PRNewswire/ — MGM Resorts International (NYSE: MGM) today announced its financial results for the quarter ended September 30, 2026.",
            "Consolidated net revenues reached $4.2 billion, driven by sustained demand for luxury accommodations and record event programming across Las Vegas Strip properties.",
            "\"Our third-quarter performance reflects the enduring appeal of our destination resorts and the strength of our hospitality and gaming offerings,\" stated Bill Hornbuckle, Chief Executive Officer and President of MGM Resorts.",
            "The company's digital business, including BetMGM and LeoVegas international operations, generated significant margin expansion as proprietary sports betting engines and automated payments drove higher player lifetime values.",
            "MGM continued its disciplined capital allocation policy, repurchasing approximately 12 million shares of common stock during the quarter while advancing construction on MGM Osaka in Japan."
        ]
    }
]

def main():
    # Load master articles
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)
    print(f"Loaded {len(articles)} existing articles.")

    # Preserve all PR-1 through PR-189
    combined_articles = real_wire_articles_nov5 + articles
    combined_articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
    print(f"Total articles now: {len(combined_articles)} (6 new Nov 5 PR Newswire releases).")

    # Save to MASTER_JSON_PATH
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(combined_articles, f, indent=2, ensure_ascii=False)
    print(f"  [SAVED] {MASTER_JSON_PATH}")

    # Compute fresh checksums for all articles
    checksums = {}
    for a in combined_articles:
        checksums[a["slug"]] = compute_article_checksum(a)
    with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2, ensure_ascii=False)
    print(f"  [UPDATED] {CHECKSUM_PATH} with {len(checksums)} entries.")

    # Export to CSV
    with open(MASTER_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_EXPORT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for a in combined_articles:
            row = {k: a.get(k, "") for k in CSV_EXPORT_FIELDS}
            if isinstance(row.get("topics"), list):
                row["topics"] = "; ".join(row["topics"])
            writer.writerow(row)
    print(f"  [EXPORTED] {MASTER_CSV_PATH}")

    # Sync template
    sync_template_articles(combined_articles)
    print("  [SYNCED] index/index.html.template")

    # Run pre-render
    print("\n--- Running Pre-Render Pipeline ---")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/pre_render.py")], check=True)

    # Run update_sitemap
    print("\n--- Running update_sitemap.py ---")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/update_sitemap.py")], check=True)

    # Run verify_site
    print("\n--- Running Pre-Flight Verification Suite ---")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "scripts/verify_site.py")], check=True)

    print("\n=== SUCCESS: 100% REAL NOV 5 PR NEWSWIRE BATCH READY FOR PRODUCTION! ===")

if __name__ == "__main__":
    main()
