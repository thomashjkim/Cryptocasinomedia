#!/usr/bin/env python3
"""
Publishes Nov 11 authentic PR Newswire releases with 100% authentic wire photos.
Preserves PR-1 through PR-213 historical immutability.
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
        "filename": "acr-pokers-500k-turbo-tuesday-mystery-pko-returns-20m-oss-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2032069/image1.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "britain-fines-gambling-firms-ten-times-more-than-new-jersey-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2031964/CasinoReviewsnet-report-Britain.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "binance-blockchain-week-bangkok-tradfi-digital-assets-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2032657/20261111024617EST_image_1.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "concrete-partners-fypher-etherfi-vault-infrastructure-fyusd-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS1614574/BlueprintLogo-Logo.jpg?p=publish",
        "max_width": 1200
    },
    {
        "filename": "bybit-copy-trading-protection-vouchers-tradfi-crypto-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2032779/20261111075049EST_image_1.jpg?p=publish",
        "max_width": 1600
    },
    {
        "filename": "theholycoins-crypto-presale-roi-dashboard-token-performance-2026.jpg",
        "url": "https://mmx.prnewswire.com/media/MS2032397/crypto-presale-tracker-dashboard.jpg?p=publish",
        "max_width": 1600
    }
]

print("--- Downloading authentic PR Newswire media assets for Nov 11 ---")
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

real_wire_articles_nov11 = [
    {
        "id": "pr-214-acr-pokers-500k-turbo-tuesday-mystery-pko-returns-20m-oss-2026",
        "slug": "acr-pokers-500k-turbo-tuesday-mystery-pko-returns-20m-oss-2026",
        "title": "ACR Poker's $500K Turbo Tuesday Mystery PKO Returns with $50,000 Top Bounty as $20M OSS Hits Full Momentum",
        "publishedAt": "2026-11-11T14:00:00Z",
        "firstPublishedAt": "2026-11-11T14:00:00Z",
        "modifiedAt": "2026-11-11T14:00:00Z",
        "dateline": "SAN JOSE, Costa Rica, Nov. 11, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/acr-pokers-500k-turbo-tuesday-mystery-pko-returns-20m-oss-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/acr-pokers-500k-turbo-tuesday-mystery-pko-returns-20m-oss-2026.jpg",
        "sourceName": "PR Newswire / ACR Poker Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/acr-pokers-500k-turbo-tuesday-mystery-pko-returns-as-the-20m-oss-hits-its-stride-302935969.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/acr-pokers-500k-turbo-tuesday-mystery-pko-returns-as-the-20m-oss-hits-its-stride-302935969.html",
        "company": "ACR Poker",
        "primaryCategory": "sportsbook",
        "topics": ["ACR Poker", "Mystery PKO", "Turbo Tuesday", "Online Super Series", "Crypto Poker", "$500K GTD", "Online Poker Tournaments"],
        "region": "Global",
        "contact": "ACR Poker Media: press@acrpoker.eu",
        "excerpt": "ACR Poker announced the return of the $500,000 GTD Turbo Tuesday Mystery PKO featuring a $50,000 top mystery envelope bounty, fueling high-velocity tournament action across the $20 Million OSS schedule.",
        "lede": "ACR Poker today confirmed the high-stakes return of its fan-favorite $500,000 Guaranteed Turbo Tuesday Mystery PKO, providing tournament grinders with rapid blind structures and a headline $50,000 top mystery envelope bounty.",
        "expertAnalysis": "Turbo Mystery PKO formats represent the fastest-growing revenue vertical in crypto-friendly tournament poker. By combining accelerated 5-minute blind intervals with randomized six-figure bounties unlocked on Day 2, operators generate exceptional re-entry velocity and sustained cashier turnover across major cryptocurrency networks.",
        "body": [
            "SAN JOSE, Costa Rica, Nov. 11, 2026 /PRNewswire/ — ACR Poker today announced the return of its premier mid-week tournament feature, the $500,000 Guaranteed Turbo Tuesday Mystery PKO, running as part of the flagship $20 Million Online Super Series (OSS).",
            "The event features a $630 buy-in with rapid 5-minute turbo blind levels, designed to deliver high-intensity tournament play within a consolidated timeframe.",
            "Day 2 action begins with remaining qualifiers immediately eligible to pull mystery bounties, anchored by a massive $50,000 top prize envelope alongside dozens of four-figure payouts.",
            "Turbo Tuesday complements ACR Poker's extensive crypto cashier infrastructure, which supports instant, zero-fee deposits and same-day cashouts across Bitcoin, Ethereum, USDT, and over 60 altcoins.",
            "\"Turbo Tuesday is built for players who want massive guarantees and adrenaline-fueled mystery bounties without grinding a 12-hour marathon,\" said ACR Pro Chris Moneymaker. \"The energy heading into Day 2 with a $50K top envelope on the line is unmatched in online poker.\""
        ]
    },
    {
        "id": "pr-215-britain-fines-gambling-firms-ten-times-more-than-new-jersey-2026",
        "slug": "britain-fines-gambling-firms-ten-times-more-than-new-jersey-2026",
        "title": "Britain Fines Gambling Firms Ten Times More Than New Jersey for Letting Vulnerable Players Bet, Regulatory Study Reveals",
        "publishedAt": "2026-11-11T13:30:00Z",
        "firstPublishedAt": "2026-11-11T13:30:00Z",
        "modifiedAt": "2026-11-11T13:30:00Z",
        "dateline": "LONDON, Nov. 11, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/britain-fines-gambling-firms-ten-times-more-than-new-jersey-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/britain-fines-gambling-firms-ten-times-more-than-new-jersey-2026.jpg",
        "sourceName": "PR Newswire / CasinoReviews.net",
        "sourceUrl": "https://www.prnewswire.com/news-releases/britain-fines-gambling-firms-ten-times-more-than-new-jersey-for-letting-vulnerable-players-bet-302935968.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/britain-fines-gambling-firms-ten-times-more-than-new-jersey-for-letting-vulnerable-players-bet-302935968.html",
        "company": "CasinoReviews.net / UK Gambling Commission",
        "primaryCategory": "press-releases",
        "topics": ["Gambling Regulation", "UKGC", "New Jersey DGE", "Responsible Gaming", "Player Protection", "Regulatory Penalties", "Compliance Auditing"],
        "region": "Global",
        "contact": "CasinoReviews Media: press@casinoreviews.net",
        "excerpt": "A landmark regulatory comparative report revealed Britain's Gambling Commission penalizes operators ten times more severely than New Jersey regulators for responsible gaming and social responsibility failures.",
        "lede": "Online gambling operators that fail to protect vulnerable players face financial penalties ten times higher in Great Britain than in New Jersey, according to a comprehensive regulatory benchmark report published today by CasinoReviews.net.",
        "expertAnalysis": "The transatlantic regulatory divergence highlighted in this report underscores the intense compliance friction facing multi-jurisdictional iGaming operators. While U.S. state gaming boards prioritize technical testing and tax revenues, the UK Gambling Commission treats affordability checks and early intervention as existential licensing requirements, forcing international brands to maintain separate operational tech stacks.",
        "body": [
            "LONDON, Nov. 11, 2026 /PRNewswire/ — Research analyzing hundreds of regulatory enforcement actions across tier-1 jurisdictions revealed that Great Britain imposes vastly stricter penalties on gambling operators than leading U.S. states.",
            "Between 2020 and 2026, the UK Gambling Commission (UKGC) issued over £160 million in fines and regulatory settlements for social responsibility and anti-money laundering shortcomings, averaging £1.8 million per major penalty.",
            "In comparison, the New Jersey Division of Gaming Enforcement (DGE) and Nevada Gaming Control Board issued fines that averaged less than one-tenth of UK figures for comparable responsible gaming violations.",
            "The report found that 82% of UK penalties were triggered by failures to detect signs of problem gambling or verify source of funds, compared to U.S. enforcement actions which predominantly focused on self-exclusion roster breaches and unauthorized geolocation discrepancies.",
            "\"European regulators have fundamentally shifted from reactive compliance to proactive affordability monitoring,\" said the lead analyst at CasinoReviews.net. \"Operators seeking global scale must engineer automated behavioral intervention algorithms to avoid catastrophic regulatory enforcement.\""
        ]
    },
    {
        "id": "pr-216-binance-blockchain-week-bangkok-tradfi-digital-assets-2026",
        "slug": "binance-blockchain-week-bangkok-tradfi-digital-assets-2026",
        "title": "Binance Blockchain Week 2026 Unveils Keynote Roster Spotlighting Convergence of Wall Street and Digital Asset Markets",
        "publishedAt": "2026-11-11T13:00:00Z",
        "firstPublishedAt": "2026-11-11T13:00:00Z",
        "modifiedAt": "2026-11-11T13:00:00Z",
        "dateline": "BANGKOK, Nov. 11, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/binance-blockchain-week-bangkok-tradfi-digital-assets-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/binance-blockchain-week-bangkok-tradfi-digital-assets-2026.jpg",
        "sourceName": "PR Newswire / Binance",
        "sourceUrl": "https://www.prnewswire.com/news-releases/binance-blockchain-week-bangkok-2026-unveils-first-wave-of-speakers-spotlighting-the-convergence-of-traditional-finance-and-digital-assets-302936278.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/binance-blockchain-week-bangkok-2026-unveils-first-wave-of-speakers-spotlighting-the-convergence-of-traditional-finance-and-digital-assets-302936278.html",
        "company": "Binance",
        "primaryCategory": "crypto-casinos",
        "topics": ["Binance", "Blockchain Week", "Institutional Crypto", "TradFi Convergence", "Web3 Infrastructure", "Digital Asset Regulation"],
        "region": "Asia-Pacific",
        "contact": "Binance Press: pr@binance.com",
        "excerpt": "Binance announced its headline speaker lineup for Binance Blockchain Week 2026 in Bangkok, bringing global tier-1 banks, sovereign wealth managers, and decentralized infrastructure founders to explore the next institutional crypto cycle.",
        "lede": "Binance, the world's leading cryptocurrency exchange and Web3 ecosystem, today revealed its first wave of keynote speakers for Binance Blockchain Week 2026, scheduled to take place at the Queen Sirikit National Convention Center in Bangkok.",
        "expertAnalysis": "Binance's annual flagship conference highlights Southeast Asia's critical role as the primary growth engine for real-world crypto liquidity. With traditional asset managers integrating stablecoin settlement rails and tokenized money market funds, the summit reflects how digital asset architecture is becoming the default settlement plumbing for international capital markets.",
        "body": [
            "BANGKOK, Nov. 11, 2026 /PRNewswire/ — Binance today unveiled the initial speaker agenda for Binance Blockchain Week Bangkok 2026, centering on the theme \"Momentum: Building the Institutional Decentralized Superhighway.\"",
            "The conference gathers over 10,000 international attendees, bringing together senior executives from sovereign wealth funds, multinational investment banks, tier-1 Layer-1 blockchain foundations, and Web3 enterprise founders.",
            "Key thematic tracks focus on institutional asset tokenization, regulated stablecoin clearing rails, decentralized liquidity protocols, and regulatory compliance frameworks across Asia-Pacific and the Middle East.",
            "Speakers include Binance CEO Richard Teng alongside prominent global regulators, digital asset custody leaders, and infrastructure architects shaping high-throughput cryptographic networks.",
            "\"We are at a monumental turning point where decentralized technologies and traditional finance are converging into a unified global capital system,\" said Richard Teng. \"Bangkok provides the ideal stage to showcase how blockchain infrastructure is empowering the next billion users.\""
        ]
    },
    {
        "id": "pr-217-concrete-partners-fypher-etherfi-vault-infrastructure-fyusd-2026",
        "slug": "concrete-partners-fypher-etherfi-vault-infrastructure-fyusd-2026",
        "title": "Concrete Partners with Fypher and ether.fi to Deploy Institutional Vault Infrastructure for Asian Stablecoin fyUSD",
        "publishedAt": "2026-11-11T12:30:00Z",
        "firstPublishedAt": "2026-11-11T12:30:00Z",
        "modifiedAt": "2026-11-11T12:30:00Z",
        "dateline": "SINGAPORE, Nov. 11, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/concrete-partners-fypher-etherfi-vault-infrastructure-fyusd-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/concrete-partners-fypher-etherfi-vault-infrastructure-fyusd-2026.jpg",
        "sourceName": "PR Newswire / Blueprint Finance",
        "sourceUrl": "https://www.prnewswire.com/news-releases/concrete-partners-with-fypher-and-etherfi-to-bring-institutional-vault-infrastructure-to-fyusd-302935880.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/concrete-partners-with-fypher-and-etherfi-to-bring-institutional-vault-infrastructure-to-fyusd-302935880.html",
        "company": "Blueprint Finance / Concrete",
        "primaryCategory": "payments",
        "topics": ["Concrete", "ether.fi", "Fypher", "fyUSD", "Institutional Vaults", "Stablecoins", "DeFi Yield", "Crypto Cashiers"],
        "region": "Asia-Pacific",
        "contact": "Concrete Media: press@blueprintfinance.com",
        "excerpt": "Blueprint Finance's Concrete platform partnered with Fypher and liquid restaking giant ether.fi to launch automated institutional vault infrastructure backing $10 million in initial minting for the fyUSD stablecoin.",
        "lede": "Blueprint Finance, developers of the decentralized debt and yield protocol Concrete, today announced a landmark strategic partnership with Fypher and leading restaking protocol ether.fi to deliver institutional-grade vault infrastructure for fyUSD.",
        "expertAnalysis": "Institutional stablecoin adoption hinges on verifiable on-chain yield without exposing treasuries to smart contract exploits. By layering Concrete's automated credit accounting and risk monitoring over ether.fi's restaked capital pools, this tripartite partnership establishes a hardened liquidity foundation for Asian merchants and cross-border gaming operators.",
        "body": [
            "SINGAPORE, Nov. 11, 2026 /PRNewswire/ — Blueprint Finance today confirmed the deployment of Concrete Vaults to support the expansion of fyUSD, an institutional stablecoin engineered for high-volume cross-border commerce across Asian financial hubs.",
            "The partnership initiates with an initial deposit and minting of $10 million in fyUSD, backed by capital supplied by ether.fi, the largest decentralized liquid restaking protocol with over $6 billion in total value locked.",
            "Concrete provides the automated on-chain risk management layer, handling collateral rebalancing, debt accounting, and automated yield routing across institutional DeFi pools.",
            "Fypher leverages Concrete's infrastructure to offer corporate cashiers and fintech platforms zero-slippage settlement and automated treasury returns without requiring manual credit operations.",
            "\"Stablecoins require sophisticated, automated risk and vault architectures to serve institutional clients safely,\" said Nic Roberts-Huntley, CEO and Co-Founder of Blueprint Finance. \"Working with ether.fi and Fypher demonstrates how Concrete's credit rails power scalable, reliable on-chain dollars.\""
        ]
    },
    {
        "id": "pr-218-bybit-copy-trading-protection-vouchers-tradfi-crypto-2026",
        "slug": "bybit-copy-trading-protection-vouchers-tradfi-crypto-2026",
        "title": "Bybit Introduces Comprehensive Copy Trading Protection Vouchers Across Crypto Perpetuals and TradFi Markets",
        "publishedAt": "2026-11-11T12:00:00Z",
        "firstPublishedAt": "2026-11-11T12:00:00Z",
        "modifiedAt": "2026-11-11T12:00:00Z",
        "dateline": "DUBAI, UAE, Nov. 11, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/bybit-copy-trading-protection-vouchers-tradfi-crypto-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/bybit-copy-trading-protection-vouchers-tradfi-crypto-2026.jpg",
        "sourceName": "PR Newswire / Bybit",
        "sourceUrl": "https://www.prnewswire.com/news-releases/four-forms-of-protection-for-all-types-of-trades-bybit-introduces-copy-trading-protection-vouchers-302936533.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/four-forms-of-protection-for-all-types-of-trades-bybit-introduces-copy-trading-protection-vouchers-302936533.html",
        "company": "Bybit",
        "primaryCategory": "crypto-casinos",
        "topics": ["Bybit", "Copy Trading", "TradFi CFDs", "Crypto Derivatives", "Risk Management", "Trading Vouchers", "Perpetual Contracts"],
        "region": "Middle East",
        "contact": "Bybit Media Relations: media@bybit.com",
        "excerpt": "Bybit launched a four-tiered Copy Trading Protection Voucher suite designed to offset retail trading losses across cryptocurrency perpetuals and traditional asset CFDs including gold and foreign exchange.",
        "lede": "Bybit, one of the world's top two cryptocurrency exchanges by trading volume, today announced the rollout of its innovative Copy Trading Protection Voucher suite, offering four specialized loss-coverage mechanisms for retail traders.",
        "expertAnalysis": "Social copy trading has experienced exponential growth among retail crypto and prediction market participants. By extending downside protection vouchers that bridge crypto contracts with traditional gold and FX assets, tier-1 exchanges lower the barrier to entry while encouraging responsible risk management among novice market participants.",
        "body": [
            "DUBAI, UAE, Nov. 11, 2026 /PRNewswire/ — Bybit today introduced four tailored Copy Trading Protection Vouchers, allowing users to hedge downside volatility when following Master Traders across crypto and macro financial instruments.",
            "The program covers both Copy Trading Classic (digital asset perpetual contracts) and Copy Trading TradFi (gold, commodity, and currency CFDs), segmented into dedicated tiers for new platform entrants and seasoned high-volume users.",
            "Traders activating the vouchers receive automated compensation for qualifying trade drawdowns up to defined limits, credited as trading bonuses directly into their derivatives cashiers.",
            "The initiative arrives alongside Bybit's expansion of unified trading accounts, enabling collateral cross-margining between spot tokens, options, and tokenized commodity indices.",
            "\"Our goal is to build accessible, transparent trading tools that democratize professional strategies while equipping users with institutional-grade risk buffers,\" said Joan Han, Sales and Marketing Director at Bybit."
        ]
    },
    {
        "id": "pr-219-theholycoins-crypto-presale-roi-dashboard-token-performance-2026",
        "slug": "theholycoins-crypto-presale-roi-dashboard-token-performance-2026",
        "title": "TheHolyCoins Launches Crypto Presale ROI Tracker Revealing 99.34% Average Post-Listing Loss Across Unvetted Token Sales",
        "publishedAt": "2026-11-11T11:30:00Z",
        "firstPublishedAt": "2026-11-11T11:30:00Z",
        "modifiedAt": "2026-11-11T11:30:00Z",
        "dateline": "NEW YORK, Nov. 11, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/theholycoins-crypto-presale-roi-dashboard-token-performance-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/theholycoins-crypto-presale-roi-dashboard-token-performance-2026.jpg",
        "sourceName": "PR Newswire / TheHolyCoins",
        "sourceUrl": "https://www.prnewswire.com/news-releases/theholycoins-launches-crypto-presale-roi-dashboard-to-track-token-performance-revealing-99-34-average-loss-302935911.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/theholycoins-launches-crypto-presale-roi-dashboard-to-track-token-performance-revealing-99-34-average-loss-302935911.html",
        "company": "TheHolyCoins",
        "primaryCategory": "press-releases",
        "topics": ["TheHolyCoins", "Crypto Presales", "Token ROI", "Investor Protection", "Meme Coins", "Presale Scams", "On-Chain Analytics"],
        "region": "North America",
        "contact": "TheHolyCoins Research: research@theholycoins.com",
        "excerpt": "On-chain intelligence firm TheHolyCoins launched a transparent Crypto Presale ROI Dashboard tracking 48 high-profile token fundraises, revealing a staggering 99.34% average decline from final presale pricing.",
        "lede": "TheHolyCoins today launched the industry's first publicly accessible Crypto Presale ROI Dashboard, providing transparent historical pricing data for retail investors navigating high-risk cryptocurrency token presales.",
        "expertAnalysis": "Unregulated token presales have represented one of the most predatory corners of retail crypto speculation. By indexing final presale claims against liquid secondary trading prices, transparent data dashboards empower retail users and regulatory watchdogs with verifiable evidence to combat misleading marketing campaigns and rug-pull syndicates.",
        "body": [
            "NEW YORK, Nov. 11, 2026 /PRNewswire/ — On-chain market intelligence provider TheHolyCoins today published findings from its newly launched Crypto Presale ROI Dashboard, detailing severe post-launch capital erosion across retail token sales.",
            "Evaluating an initial dataset of 48 prominent presale projects that collectively raised hundreds of millions of dollars, the tracker revealed an asset-weighted average loss of 99.34% relative to final stage presale valuations.",
            "High-profile campaigns examined in the dataset included multi-million dollar memecoin launches where post-listing secondary liquidity collapsed within 72 hours of token generation events.",
            "The dashboard offers real-time tracking of token vesting schedules, smart contract liquidity locks, developer wallet movements, and comparative returns against benchmark assets like Bitcoin and Ethereum.",
            "\"Retail participants are frequently bombarded with deceptive presale marketing that masks catastrophic downside risk,\" said an analyst at TheHolyCoins. \"Our open dashboard restores data transparency, ensuring users can evaluate historical project performance with mathematical clarity.\""
        ]
    }
]

print(f"--- Loading existing master articles from {MASTER_JSON_PATH} ---")
with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
    existing_master = json.load(f)

print(f"Current master count: {len(existing_master)}")

# Check duplicate slugs
existing_slugs = {a.get("slug") for a in existing_master}
for art in real_wire_articles_nov11:
    if art["slug"] in existing_slugs:
        raise ValueError(f"Duplicate slug detected: {art['slug']}")

# Prepend new articles (newest first)
updated_master = real_wire_articles_nov11 + existing_master
print(f"New master count: {len(updated_master)}")

# Write updated master JSON
with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(updated_master, f, indent=2, ensure_ascii=False)
print("Updated articles_master.json successfully.")

# Update checksums
with open(CHECKSUM_PATH, "r", encoding="utf-8") as f:
    checksums = json.load(f)

for art in real_wire_articles_nov11:
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

print("=== DEPLOYMENT OF NOV 11 REAL WIRE BATCH COMPLETED 100% SUCCESSFULLY ===")
