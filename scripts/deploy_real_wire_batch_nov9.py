#!/usr/bin/env python3
"""
Publishes Nov 9 authentic PR Newswire releases with 100% authentic wire photos.
Preserves PR-1 through PR-201 historical immutability.
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
        "filename": "pnc-bank-incoming-usdc-stablecoin-payments-corporate-banking-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1882224/PNC-Logo_original.jpg?p=publish",
        "max_width": 1200
    },
    {
        "filename": "bitmine-immersion-technologies-eth-treasury-holdings-14-billion-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2030224/image1.jpg?p=publish",
        "max_width": 1200
    },
    {
        "filename": "casino-teamsters-win-strike-at-encore-boston-harbor-historic-union-contract-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS685095/Teamsters-Logo-v1.jpg?p=publish",
        "max_width": 1200
    },
    {
        "filename": "scientific-games-powering-possibilities-world-lottery-summit-sydney-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2025761/Scientific-Games-is-Powering-Possibilities-at-WLS.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "acr-poker-moneymaker-mystery-pko-the-quattro-tournament-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2026597/ACR-Poker-Event.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "hyperscale-data-reports-50-million-bitcoin-cash-holdings-q4-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1845972/Hyperscale-Data-Registered-Mark-Logo.jpg?p=publish",
        "max_width": 1600
    }
]

print("--- Downloading authentic PR Newswire media assets for Nov 9 ---")
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

real_wire_articles_nov9 = [
    {
        "id": "pr-202-pnc-bank-launches-incoming-usdc-stablecoin-payments-powered-by-coinbase-2026",
        "slug": "pnc-bank-launches-incoming-usdc-stablecoin-payments-powered-by-coinbase-2026",
        "title": "PNC Bank Launches Pilot for Incoming USDC Stablecoin Payments Powered by Coinbase for Institutional Banking Clients",
        "publishedAt": "2026-11-09T14:00:00Z",
        "firstPublishedAt": "2026-11-09T14:00:00Z",
        "modifiedAt": "2026-11-09T14:00:00Z",
        "dateline": "PITTSBURGH, Nov. 9, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/pnc-bank-incoming-usdc-stablecoin-payments-corporate-banking-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/pnc-bank-incoming-usdc-stablecoin-payments-corporate-banking-2026.jpg",
        "sourceName": "PR Newswire / PNC Financial Services Group",
        "sourceUrl": "https://www.prnewswire.com/news-releases/pnc-bank-launches-incoming-stablecoin-payments-for-corporate-and-institutional-banking-clients-302932728.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/pnc-bank-launches-incoming-stablecoin-payments-for-corporate-and-institutional-banking-clients-302932728.html",
        "company": "PNC Bank",
        "primaryCategory": "payments",
        "topics": ["PNC Bank", "USDC", "Coinbase", "Stablecoins", "Institutional Banking", "Crypto Payments", "Treasury Management"],
        "region": "North America",
        "contact": "PNC Media Relations: media.relations@pnc.com",
        "excerpt": "PNC Bank announced a pilot program enabling incoming USDC payments on the Ethereum blockchain powered by Coinbase, automatically converting stablecoins 1-to-1 into USD deposits for corporate and institutional banking clients.",
        "lede": "PNC Bank, one of the largest diversified financial services institutions in the United States, today announced a pilot program enabling incoming USDC payments for its Corporate & Institutional Banking (C&IB) clients, powered by Coinbase payment infrastructure.",
        "expertAnalysis": "PNC's integration of Coinbase payment infrastructure to accept USDC directly into commercial treasury accounts represents a landmark watershed for regulated digital finance. By handling instant on-chain conversion into USD, PNC eliminates crypto balance sheet volatility for commercial enterprises while enabling instant, 24/7 cross-border settlement for international merchants, digital entertainment platforms, and global cashiers.",
        "body": [
            "PITTSBURGH, Nov. 9, 2026 /PRNewswire/ — PNC Bank today announced an expansion of its strategic collaboration with Coinbase to make incoming USDC payments available for its Corporate & Institutional Banking (C&IB) clients.",
            "Through this new capability, corporate clients can receive payments in USDC—a leading U.S. dollar-backed stablecoin issued by Circle—on the Ethereum blockchain. Payments received are automatically converted on a 1-to-1 basis into U.S. dollars and deposited directly into the client's designated PNC commercial bank account.",
            "The backend payment execution is powered by Coinbase Payment products and integrated developer APIs, connecting seamlessly with PNC's enterprise treasury management systems.",
            "\"Our clients increasingly conduct business in real-time global environments where speed, predictability, and efficiency are paramount,\" said Emma Loftus, Head of PNC Treasury Management. \"Enabling incoming stablecoin settlement provides our clients with cutting-edge digital liquidity while keeping funds anchored within their trusted banking infrastructure.\"",
            "The initial deployment is available on a pilot basis to eligible institutional clients, allowing commercial treasurers to accelerate international cash cycles, reduce friction in digital settlements, and explore next-generation payments without holding digital asset inventory."
        ]
    },
    {
        "id": "pr-203-bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-balance-sheet-2026",
        "slug": "bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-balance-sheet-2026",
        "title": "Bitmine Immersion Technologies Announces ETH Holdings Reach 6.07 Million Tokens with $14.3 Billion Balance Sheet",
        "publishedAt": "2026-11-09T13:30:00Z",
        "firstPublishedAt": "2026-11-09T13:30:00Z",
        "modifiedAt": "2026-11-09T13:30:00Z",
        "dateline": "LAS VEGAS, Nov. 9, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/bitmine-immersion-technologies-eth-treasury-holdings-14-billion-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/bitmine-immersion-technologies-eth-treasury-holdings-14-billion-2026.jpg",
        "sourceName": "PR Newswire / Bitmine Immersion Technologies",
        "sourceUrl": "https://www.prnewswire.com/news-releases/bitmine-immersion-technologies-bmnr-announces-eth-holdings-reach-6-07-million-tokens-and-total-crypto-and-total-cash--marketable-securities-holdings-of-14-3-billion-302932890.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/bitmine-immersion-technologies-bmnr-announces-eth-holdings-reach-6-07-million-tokens-and-total-crypto-and-total-cash--marketable-securities-holdings-of-14-3-billion-302932890.html",
        "company": "Bitmine Immersion Technologies, Inc.",
        "primaryCategory": "crypto-casinos",
        "topics": ["Bitmine", "Ethereum", "Crypto Treasury", "ETH Staking", "Institutional Crypto", "Digital Assets", "Wall Street Staking"],
        "region": "Global",
        "contact": "Bitmine Investor Relations: ir@bitmine.tech",
        "excerpt": "Bitmine Immersion Technologies announced its corporate treasury has accumulated 6,070,092 Ethereum tokens—representing nearly 5% of global supply—powering a $14.3 billion institutional balance sheet with over $300M in annualized staking rewards.",
        "lede": "Bitmine Immersion Technologies, Inc. (NYSE: BMNR), a pioneer in institutional digital asset infrastructure and high-efficiency compute, today reported its corporate Ethereum holdings have reached 6,070,092 tokens, valuing its aggregate cryptocurrency, cash, and marketable securities portfolio at $14.3 billion.",
        "expertAnalysis": "Bitmine's strategic accumulation of 4.97% of the entire circulating Ethereum supply positions the firm as the dominant corporate validator globally. With over 5.22 million ETH deployed across institutional staking pools yielding upwards of $350 million in annual protocol rewards, Bitmine demonstrates how treasury yield management is migrating directly into base-layer decentralized infrastructure.",
        "body": [
            "LAS VEGAS, Nov. 9, 2026 /PRNewswire/ — Bitmine Immersion Technologies, Inc. (NYSE: BMNR) today released its weekly asset portfolio update, disclosing that its total corporate Ethereum (ETH) treasury holdings have expanded to 6,070,092 tokens.",
            "This accumulation brings Bitmine to 4.97% of Ethereum's total circulating supply of 122.2 million tokens, placing the company approximately 99% of the way toward its strategic \"Alchemy of 5%\" accumulation mandate.",
            "As of November 8, 2026, Bitmine's aggregate cryptocurrency holdings, cash, marketable securities, and strategic investments totaled approximately $14.3 billion. The portfolio includes 216 Bitcoin (BTC), $475 million in cash reserves, a $180 million strategic equity stake in Beast Industries, and $75 million in Eightco Holdings (NASDAQ: ORBS).",
            "Significantly, Bitmine disclosed that 5,227,037 ETH—valued at approximately $11.7 billion—are currently staked in secure institutional validator nodes, generating an estimated $309 million to $359 million in annualized staking rewards based on prevailing Ethereum network yield rates.",
            "\"Ethereum co-founder Vitalik Buterin recently reinforced that Ethereum functions fundamentally as a global monetary store of value and foundational economic settlement layer,\" said Tom Lee, Chairman of Bitmine. \"Our corporate treasury positioning enables public market investors to participate directly in the fundamental tokenization and decentralized compute supercycle.\""
        ]
    },
    {
        "id": "pr-204-casino-teamsters-win-strike-at-encore-boston-harbor-ratify-historic-union-contract-2026",
        "slug": "casino-teamsters-win-strike-at-encore-boston-harbor-ratify-historic-union-contract-2026",
        "title": "Over 1,300 Casino Workers at Encore Boston Harbor Overwhelmingly Ratify Historic 5.5-Year Union Contract Ending 62-Day Strike",
        "publishedAt": "2026-11-09T13:00:00Z",
        "firstPublishedAt": "2026-11-09T13:00:00Z",
        "modifiedAt": "2026-11-09T13:00:00Z",
        "dateline": "EVERETT, Mass., Nov. 9, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/casino-teamsters-win-strike-at-encore-boston-harbor-historic-union-contract-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/casino-teamsters-win-strike-at-encore-boston-harbor-historic-union-contract-2026.jpg",
        "sourceName": "PR Newswire / Teamsters Local 25 & UNITE HERE Local 26",
        "sourceUrl": "https://www.prnewswire.com/news-releases/casino-teamsters-win-strike-at-encore-boston-harbor-302932291.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/casino-teamsters-win-strike-at-encore-boston-harbor-302932291.html",
        "company": "Encore Boston Harbor / Teamsters Local 25",
        "primaryCategory": "press-releases",
        "topics": ["Encore Boston Harbor", "Casino Labor", "Teamsters", "UNITE HERE", "Massachusetts Gaming", "Resort Operations", "Casino Strike"],
        "region": "North America",
        "contact": "Teamsters Media Relations: media@teamster.org",
        "excerpt": "More than 1,300 workers at Encore Boston Harbor ratified a milestone 5.5-year collective bargaining agreement following a 62-day strike, securing historic wage increases, enhanced benefits, and modernized working conditions across casino floor departments.",
        "lede": "After an eight-and-a-half-week strike spanning 62 days on the picket line, more than 1,300 frontline casino and resort workers at Encore Boston Harbor, represented by Teamsters Local 25 and UNITE HERE Local 26, overwhelmingly ratified a landmark five-and-a-half-year collective bargaining agreement.",
        "expertAnalysis": "The successful contract resolution at Encore Boston Harbor concludes one of the longest major gaming work stoppages in recent Massachusetts history. With commercial casino revenues facing heightened operational cost pressures, the agreement establishes a competitive wage floor and modernized scheduling protections across critical non-gaming and gaming floor operations, setting a labor precedent for luxury destination resorts nationwide.",
        "body": [
            "EVERETT, Mass., Nov. 9, 2026 /PRNewswire/ — Following 62 days of picket line action, more than 1,300 union workers at Wynn Resorts' flagship East Coast property, Encore Boston Harbor, have voted overwhelmingly to ratify a new five-and-a-half-year collective bargaining agreement.",
            "The newly ratified contract delivers substantial wage increases, improved healthcare and pension protections, enhanced workload controls, and enhanced safety standards across both gaming floor and back-of-house operations.",
            "The bargaining coalition represents workers across vital resort departments, including cage cashiers, slot floor attendants, warehouse technicians, valet drivers, culinary staff, housekeepers, and guest services personnel.",
            "\"This victory demonstrates what happens when working men and women stand shoulder-to-shoulder with unyielding solidarity,\" said Thomas G. Mari, President of Teamsters Local 25. \"Encore Boston Harbor operates as a premier Forbes Five-Star resort because of the dedicated staff who make it run 24 hours a day. This agreement guarantees our members the respect, fair compensation, and security they have rightfully earned.\"",
            "Following the ratification vote, union members began phased returns to their positions, restoring full staffing levels across Encore Boston Harbor's 210,000-square-foot casino floor, dining venues, and luxury hotel accommodations."
        ]
    },
    {
        "id": "pr-205-scientific-games-showcases-powering-possibilities-omnichannel-ecosystem-world-lottery-summit-2026",
        "slug": "scientific-games-showcases-powering-possibilities-omnichannel-ecosystem-world-lottery-summit-2026",
        "title": "Scientific Games Showcases \"Powering Possibilities\" Omnichannel Ecosystem at World Lottery Summit 2026 in Sydney",
        "publishedAt": "2026-11-09T12:00:00Z",
        "firstPublishedAt": "2026-11-09T12:00:00Z",
        "modifiedAt": "2026-11-09T12:00:00Z",
        "dateline": "SYDNEY, Nov. 9, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/scientific-games-powering-possibilities-world-lottery-summit-sydney-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/scientific-games-powering-possibilities-world-lottery-summit-sydney-2026.jpg",
        "sourceName": "PR Newswire / Scientific Games Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/scientific-games-brings-the-player-journey-to-life-at-world-lottery-summit-2026-302927014.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/scientific-games-brings-the-player-journey-to-life-at-world-lottery-summit-2026-302927014.html",
        "company": "Scientific Games",
        "primaryCategory": "press-releases",
        "topics": ["Scientific Games", "World Lottery Summit", "Digital Lottery", "iLottery", "Omnichannel Gaming", "Retail Terminals", "Responsible Gaming"],
        "region": "Global",
        "contact": "Scientific Games Media: media@scientificgames.com",
        "excerpt": "Scientific Games unveiled its unified 'Powering Possibilities' omnichannel showcase at the World Lottery Summit 2026 in Sydney, demonstrating breakthrough instant game technology, digital CRM solutions, and retail cashier integrations.",
        "lede": "Scientific Games today unveiled its comprehensive \"Powering Possibilities\" showcase at the prestigious World Lottery Summit (WLS) 2026 in Sydney, Australia, highlighting the industry's most advanced digital and retail lottery technology ecosystem.",
        "expertAnalysis": "Scientific Games' demonstration at WLS 2026 highlights the ongoing technical convergence between regulated lotteries and digital casino entertainment. By unifying retail POS terminals, digital loyalty CRM, and cloud-native iLottery engines under a single player journey, lottery operators worldwide can capture modern digital demographics while driving sustainable returns for public beneficiaries.",
        "body": [
            "SYDNEY, Nov. 9, 2026 /PRNewswire/ — At the biennial World Lottery Summit 2026 held at the International Convention Centre in Sydney, Scientific Games officially launched its global showcase designed to bring every touchpoint of the modern lottery player journey to life.",
            "The company's \"Powering Possibilities\" pavilion highlights innovations across five core dimensions: premier game design, connected retail environments, advanced digital solutions, bespoke licensed brand properties, and player health protections.",
            "Attendees experienced live demonstrations of next-generation physical-digital crossover formats, including proprietary Pop N' Paks™ packaging, multi-jurisdiction progressive jackpot systems, and frictionless self-service ticketing kiosks powered by real-time analytics engines.",
            "The showcase also features high-profile licensed entertainment franchises spanning MONOPOLY™, UNO™, and Frida Kahlo, alongside Scientific Games' enhanced \"Healthy Play\" responsible gaming framework integrated across digital cashier workflows.",
            "\"Our team is honored to present our vision for the future of global lottery entertainment in Sydney,\" said Dan Flynn, newly appointed Chief Executive Officer of Scientific Games. \"By connecting world-class game content with seamless omnichannel retail and mobile architectures, we empower government-sponsored lotteries to maximize funding for critical community causes.\""
        ]
    },
    {
        "id": "pr-206-acr-poker-adds-1m-moneymaker-mystery-pko-event-the-quattro-tournament-schedule-2026",
        "slug": "acr-poker-adds-1m-moneymaker-mystery-pko-event-the-quattro-tournament-schedule-2026",
        "title": "ACR Poker Expands Mystery PKO Schedule with Moneymaker $1M GTD and The Quattro Following ScreenShield Rollout",
        "publishedAt": "2026-11-09T11:30:00Z",
        "firstPublishedAt": "2026-11-09T11:30:00Z",
        "modifiedAt": "2026-11-09T11:30:00Z",
        "dateline": "SAN JOSE, Costa Rica, Nov. 9, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/acr-poker-moneymaker-mystery-pko-the-quattro-tournament-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/acr-poker-moneymaker-mystery-pko-the-quattro-tournament-2026.jpg",
        "sourceName": "PR Newswire / ACR Poker Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/acr-poker-adds-1m-moneymaker-event-and-the-quattro-to-mystery-pko-schedule-302928387.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/acr-poker-adds-1m-moneymaker-event-and-the-quattro-to-mystery-pko-schedule-302928387.html",
        "company": "ACR Poker",
        "primaryCategory": "crypto-casinos",
        "topics": ["ACR Poker", "Mystery PKO", "Chris Moneymaker", "Online Poker", "The Quattro", "Crypto Poker", "ScreenShield"],
        "region": "Global",
        "contact": "ACR Poker Media: press@acrpoker.eu",
        "excerpt": "ACR Poker has bolstered its tournament roster with the Moneymaker $1M GTD Mystery PKO and 'The Quattro' weekly series, backed by a network-wide security upgrade that enables ScreenShield table protection by default.",
        "lede": "ACR Poker, the flagship room on the Winning Poker Network (WPN), today announced a massive expansion of its multi-flight tournament calendar with the launch of the Moneymaker $1M GTD Mystery PKO and 'The Quattro' tournament series.",
        "expertAnalysis": "ACR Poker's rapid tournament expansion reflects surging player liquidity in crypto-accessible poker networks. By coupling high-stakes multi-flight mystery bounty formats with mandatory client-side ScreenShield integrity protocols, the operator directly addresses player demand for verifiable fair play and massive guaranteed prize pools across multi-crypto banking rails.",
        "body": [
            "SAN JOSE, Costa Rica, Nov. 9, 2026 /PRNewswire/ — ACR Poker today confirmed major enhancements to its weekly tournament lineup, introducing the Moneymaker $1 Million Guaranteed Mystery Progressive Knockout (PKO) alongside \"The Quattro\" multi-flight schedule.",
            "The Moneymaker $1M GTD event features an accessible $109 buy-in with Day 1 flights running multiple times daily, culminating in a Day 2 finale featuring a headline $100,000 top mystery bounty.",
            "In addition, ACR Poker introduced \"The Quattro,\" a recurring Sunday tournament series offering four concurrent guaranteed flight tiers designed to accommodate micro, mid, and high-roller bankrolls.",
            "The expanded tournament slate is supported by ACR Poker's latest client software release, which activates \"ScreenShield\" security technology across all network tables by default to protect game integrity and prevent unauthorized third-party overlays.",
            "\"We are continuously refining our tournament ecosystem to ensure players of all stakes have access to premier bounty action with industry-leading table security,\" said ACR Pro Chris Moneymaker. \"The Moneymaker Mystery PKO gives every grinder the shot at pulling a life-changing six-figure bounty on Day 2.\""
        ]
    },
    {
        "id": "pr-207-hyperscale-data-reports-50-million-bitcoin-cash-holdings-q4-2026",
        "slug": "hyperscale-data-reports-50-million-bitcoin-cash-holdings-q4-2026",
        "title": "Hyperscale Data Reports $50.6 Million in Liquid Assets with 211 Bitcoin and Cash Holdings Heading into AI Expansion",
        "publishedAt": "2026-11-09T10:30:00Z",
        "firstPublishedAt": "2026-11-09T10:30:00Z",
        "modifiedAt": "2026-11-09T10:30:00Z",
        "dateline": "LAS VEGAS, Nov. 9, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/hyperscale-data-reports-50-million-bitcoin-cash-holdings-q4-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/hyperscale-data-reports-50-million-bitcoin-cash-holdings-q4-2026.jpg",
        "sourceName": "PR Newswire / Hyperscale Data",
        "sourceUrl": "https://www.prnewswire.com/news-releases/hyperscale-data-held-approximately-50-6-million-of-bitcoin-cash-and-restricted-cash-as-of-november-1--2026--302927361.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/hyperscale-data-held-approximately-50-6-million-of-bitcoin-cash-and-restricted-cash-as-of-november-1--2026--302927361.html",
        "company": "Hyperscale Data, Inc.",
        "primaryCategory": "payments",
        "topics": ["Hyperscale Data", "Bitcoin Treasury", "Corporate Treasury", "Digital Assets", "AI Data Centers", "Institutional Bitcoin"],
        "region": "North America",
        "contact": "Hyperscale Data Investor Relations: ir@hyperscaledata.com",
        "excerpt": "Hyperscale Data reported holding approximately $50.6 million in liquid assets, including 211.46 Bitcoin and $34.1 million in cash reserves, backing its aggressive data center transformation and high-performance compute infrastructure.",
        "lede": "Hyperscale Data, Inc. (NYSE American: GPUS), a diversified infrastructure provider specializing in AI compute facilities and digital assets, today reported holding approximately $50.6 million in Bitcoin, cash, and restricted cash as of November 1, 2026.",
        "expertAnalysis": "Hyperscale Data's balance sheet management reflects the maturing intersection of high-density AI computing and sovereign digital asset reserves. By maintaining substantial unencumbered Bitcoin alongside liquid treasury cash, public tech operators enhance capital flexibility to fund mission-critical power and cooling infrastructure while preserving long-term digital asset appreciation.",
        "body": [
            "LAS VEGAS, Nov. 9, 2026 /PRNewswire/ — Hyperscale Data, Inc. (NYSE American: GPUS) today published an operational and balance sheet update detailing its liquid treasury asset position.",
            "As of November 1, 2026, Hyperscale Data held approximately 211.4639 Bitcoin valued at approximately $16.5 million based on prevailing market pricing, combined with $34.1 million in cash and restricted cash, bringing total liquid treasury holdings to approximately $50.6 million.",
            "The company's treasury strategy is designed to preserve balance sheet strength while deploying capital into high-margin enterprise data center conversions, including its flagship facility in Michigan scheduled for phase-one commissioning in December 2026.",
            "\"Our balance sheet position provides a solid financial runway as we advance our high-performance AI data center capabilities,\" said Milton \"Todd\" Ault III, Executive Chairman of Hyperscale Data. \"Holding pure Bitcoin reserves in conjunction with strong cash balances ensures we can execute strategic infrastructure expansions without relying on dilutive market financing.\"",
            "Hyperscale Data continues to evaluate institutional crypto staking, high-efficiency GPU hosting, and sovereign compute operations as core pillars of its long-term enterprise growth roadmap."
        ]
    }
]

print(f"--- Loading existing master articles from {MASTER_JSON_PATH} ---")
with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
    existing_master = json.load(f)

print(f"Current master count: {len(existing_master)}")

# Check duplicate slugs
existing_slugs = {a.get("slug") for a in existing_master}
for art in real_wire_articles_nov9:
    if art["slug"] in existing_slugs:
        raise ValueError(f"Duplicate slug detected: {art['slug']}")

# Prepend new articles (newest first)
updated_master = real_wire_articles_nov9 + existing_master
print(f"New master count: {len(updated_master)}")

# Write updated master JSON
with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(updated_master, f, indent=2, ensure_ascii=False)
print("Updated articles_master.json successfully.")

# Update checksums
with open(CHECKSUM_PATH, "r", encoding="utf-8") as f:
    checksums = json.load(f)

for art in real_wire_articles_nov9:
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

print("=== DEPLOYMENT OF NOV 9 REAL WIRE BATCH COMPLETED 100% SUCCESSFULLY ===")
