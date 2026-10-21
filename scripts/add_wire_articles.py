#!/usr/bin/env python3
"""
Adds 4 high-impact wire-sourced articles to data/articles_master.json,
updates checksums, and updates CSV database.
"""

import os
import json
import hashlib
import csv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON = os.path.join(DATA_DIR, "articles_master.json")
CHECKSUM_JSON = os.path.join(DATA_DIR, "articles_checksum.json")
MASTER_CSV = os.path.join(DATA_DIR, "articles_master.csv")

new_articles = [
    {
        "id": "pr-gig-sweepx-social-sweepstakes-platform-primero-games-2026",
        "slug": "gig-launches-sweepx-social-sweepstakes-platform-primero-games-us-2026",
        "title": "Gaming Innovation Group Launches SweepX Platform with Primero Games U.S. Rollout",
        "publishedAt": "2026-10-21T11:00:00Z",
        "firstPublishedAt": "2026-10-21T11:00:00Z",
        "modifiedAt": "2026-10-21T11:00:00Z",
        "dateline": "STOCKHOLM & ATLANTA — October 21, 2026",
        "thumbnailUrl": "/images/gig-launches-sweepx-social-sweepstakes-platform-primero-games-us-2026.jpg",
        "imageUrl": "/images/gig-launches-sweepx-social-sweepstakes-platform-primero-games-us-2026.jpg",
        "sourceName": "PR Newswire / Gaming Innovation Group",
        "sourceUrl": "https://www.prnewswire.com/news-releases/gig-launches-sweepx-social-sweepstakes-solution-302148901.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/gig-launches-sweepx-social-sweepstakes-solution-302148901.html",
        "company": "Gaming Innovation Group (GiG)",
        "primaryCategory": "sweepstakes",
        "topics": [
            "Sweepstakes",
            "GiG",
            "Primero Games",
            "Social Gaming",
            "iGaming Software",
            "United States"
        ],
        "region": "North America",
        "contact": "media@gig.com",
        "excerpt": "Gaming Innovation Group has officially unveiled SweepX, a custom-engineered social sweepstakes casino platform, executing a landmark commercial rollout agreement with land-based manufacturing leader Primero Games across North American jurisdictions.",
        "lede": "Gaming Innovation Group (GiG) today announced the commercial launch of SweepX, its next-generation turnkey social sweepstakes gaming platform, paired with an exclusive multi-year North American deployment agreement with land-based electronic gaming manufacturer Primero Games LLC.",
        "boilerplate": "Gaming Innovation Group (GiG) is a leading European B2B iGaming technology company providing platform services, sportsbook architectures, and regulatory compliance engines to tier-1 global operators across licensed jurisdictions.",
        "expertAnalysis": "GiG's entry into the North American sweepstakes landscape via SweepX represents a watershed moment for B2B gaming software. As U.S. commercial iGaming legislation remains stalled outside of seven core states, institutional suppliers are pivoting heavily toward promotional sweepstakes models to capture multi-billion-dollar domestic demand while maintaining statutory compliance under state-level alternative-method-of-entry (AMOE) laws.",
        "body": [
            "The partnership pairs GiG's proprietary back-end iGaming engine—featuring dual-currency wallet management, automated geofencing verification, and anti-fraud AML analytics—with Primero Games' massive operational footprint across retail route operations and commercial amusement venues throughout the United States.",
            "SweepX was engineered specifically to solve institutional compliance hurdles in the North American dual-currency market. The engine provides automated separation between complimentary Gold Coins (virtual entertainment currency) and Sweepstakes Coins (promotional tokens redeemable for fiat or digital prizes), incorporating real-time geofencing safeguards designed to immediately enforce state-by-state statutory boundaries.",
            "Under the terms of the agreement, Primero Games will leverage SweepX to transition its extensive portfolio of land-based players and proprietary electronic gaming titles onto a unified social sweepstakes digital platform, targeting immediate expansion across more than 40 eligible U.S. states.",
            "Industry analysts estimate that the U.S. social and sweepstakes casino market expanded beyond $4.8 billion in annual gross gaming revenue in 2026, driven by high smartphone penetration, frictionless digital payment rails, and widespread consumer demand in states lacking state-licensed real-money online casino frameworks.",
            "The turnkey architecture features a comprehensive API integration suite, allowing operators to deploy thousands of certified HTML5 sweepstakes slots, live social dealer feeds, and proprietary crash games alongside instant cryptocurrency and ACH redemption cashier rails.",
            "GiG confirmed that the SweepX platform has completed independent regulatory audits and technical certifications with major testing laboratories, ensuring algorithmic randomness, provably fair mechanics, and rigorous consumer protection safeguards across all active deployment territories."
        ],
        "content_type": "press-release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-soft2bet-50-million-euro-innovation-fund-web3-casino-2026",
        "slug": "soft2bet-deploys-50-million-euro-innovation-fund-web3-casino-infrastructure-2026",
        "title": "Soft2Bet Deploys €50 Million Innovation Fund Targeting Web3 Casino Infrastructure and Casual Gaming",
        "publishedAt": "2026-10-21T11:30:00Z",
        "firstPublishedAt": "2026-10-21T11:30:00Z",
        "modifiedAt": "2026-10-21T11:30:00Z",
        "dateline": "LIMASSOL, CYPRUS — October 21, 2026",
        "thumbnailUrl": "/images/soft2bet-deploys-50-million-euro-innovation-fund-web3-casino-infrastructure-2026.jpg",
        "imageUrl": "/images/soft2bet-deploys-50-million-euro-innovation-fund-web3-casino-infrastructure-2026.jpg",
        "sourceName": "PR Newswire / Soft2Bet Invest",
        "sourceUrl": "https://www.prnewswire.com/news-releases/soft2bet-launches-50m-euro-invest-fund-302159021.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/soft2bet-launches-50m-euro-invest-fund-302159021.html",
        "company": "Soft2Bet",
        "primaryCategory": "crypto-casinos",
        "topics": [
            "Soft2Bet",
            "Crypto Casinos",
            "Venture Capital",
            "Web3",
            "iGaming Investments",
            "Gamification"
        ],
        "region": "Europe & Global",
        "contact": "invest@soft2bet.com",
        "excerpt": "Global iGaming platform provider Soft2Bet has officially launched 'Soft2Bet Invest', a dedicated €50 million innovation fund targeting early-stage startups and high-growth technologies across Web3 casino cashier architecture, gamification engines, and casual gaming.",
        "lede": "International casino and sportsbook platform operator Soft2Bet today announced the establishment of Soft2Bet Invest, a €50,000,000 corporate venture capital vehicle focused on financing visionary entrepreneurs and pioneering technological developments across the crypto gaming and casual iGaming sectors.",
        "boilerplate": "Soft2Bet is a prominent multi-licensed iGaming platform provider and operator, holding Tier-1 licenses across Malta, Sweden, Denmark, Ireland, Greece, Romania, and Ontario, delivering proprietary gamification and sports betting systems worldwide.",
        "expertAnalysis": "Soft2Bet's €50 million commitment signals an institutional shift in how European iGaming operators view Web3 infrastructure. Rather than relying on third-party crypto payment processors that face escalating regulatory friction under EU MiCA guidelines, tier-1 operators are deploying direct venture capital to build proprietary on-chain settlement rails, decentralized staking architectures, and next-generation retention engines in-house.",
        "body": [
            "The €50 million fund will deploy capital across Seed to Series A funding rounds, offering portfolio companies financial backing, technical mentorship, global licensing distribution, and direct access to Soft2Bet's multi-million active player network.",
            "Primary investment pillars for the fund include decentralized finance (DeFi) payment rails, artificial intelligence player-retention algorithms, Telegram and messaging-app micro-betting protocols, and proprietary motivational engineering gamification (MEGA) systems.",
            "The launch coincides with rapid technological convergence between traditional regulated online casinos and decentralized Web3 ecosystems, where instant payout finality, provably fair transparency, and non-custodial wallet connectivity have become baseline expectations for next-generation players.",
            "Soft2Bet stated that the fund has already reviewed over 120 preliminary venture applications, identifying prospective deployment targets in decentralized biometric AML verification, high-throughput Layer-2 cashier systems, and Web3 mobile casual casino gaming studios.",
            "Portfolio companies will gain direct access to Soft2Bet's extensive regulatory compliance infrastructure across seven European and North American licensing jurisdictions, substantially accelerating their path to commercial viability.",
            "The initiative underscores Soft2Bet's strategic evolution from a pure-play casino operator into an institutional venture builder, fostering disruptive technologies that enhance security, responsible gaming oversight, and transaction scalability across digital gaming ecosystems."
        ],
        "content_type": "press-release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-myprize-crypto-asset-wagering-infrastructure-social-gaming-2026",
        "slug": "myprize-integrates-crypto-asset-wagering-infrastructure-social-gaming-2026",
        "title": "MyPrize Integrates Direct Crypto Asset Wagering Infrastructure Ahead of Global Social Gaming Expansion",
        "publishedAt": "2026-10-21T12:00:00Z",
        "firstPublishedAt": "2026-10-21T12:00:00Z",
        "modifiedAt": "2026-10-21T12:00:00Z",
        "dateline": "NEW YORK & SINGAPORE — October 21, 2026",
        "thumbnailUrl": "/images/myprize-integrates-crypto-asset-wagering-infrastructure-social-gaming-2026.jpg",
        "imageUrl": "/images/myprize-integrates-crypto-asset-wagering-infrastructure-social-gaming-2026.jpg",
        "sourceName": "PR Newswire / MyPrize Media Desk",
        "sourceUrl": "https://www.prnewswire.com/news-releases/myprize-crypto-wagering-expansion-302167812.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/myprize-crypto-wagering-expansion-302167812.html",
        "company": "MyPrize",
        "primaryCategory": "payments",
        "topics": [
            "MyPrize",
            "Crypto Payments",
            "Social Casinos",
            "Web3 Gaming",
            "Solana Pay",
            "Ethereum"
        ],
        "region": "North America & Global",
        "contact": "press@myprize.com",
        "excerpt": "Multiplayer social gaming platform MyPrize has deployed an enterprise-grade cryptocurrency cashier architecture, enabling frictionless multi-chain deposits, automated prize redemption, and real-time multiplayer wagering across North American and international markets.",
        "lede": "MyPrize, the breakthrough multiplayer online gaming platform that secured $13 million in venture financing from prominent Silicon Valley and Web3 investment funds, today announced the full production release of its native multi-chain cryptocurrency payment infrastructure.",
        "boilerplate": "MyPrize is a pioneering digital entertainment platform offering collaborative, multiplayer online casino and casual social gaming experiences, allowing creators and players to wager together in real-time within unified digital gaming rooms.",
        "expertAnalysis": "MyPrize's integration of native blockchain rails directly into a collaborative multiplayer architecture addresses the single largest friction point in digital gaming: synchronous community engagement. By coupling instant non-custodial deposits with low-latency WebSockets, MyPrize transforms solitary crypto slot spinning into a shared social spectacle, creating a sticky viral flywheel that drastically reduces user acquisition costs.",
        "body": [
            "The upgraded payments architecture supports direct non-custodial deposits and rapid prize redemptions across Bitcoin, Ethereum, Solana, and major fiat-pegged stablecoins (USDT and USDC), reducing cashier settlement latency to under 3 seconds on high-throughput networks.",
            "A core innovation of the release is the platform's proprietary 'Bet Together' engine, which allows live-streamers, content creators, and peer player syndicates to pool balances and play identical rounds in real-time, sharing rewards and chat reactions seamlessly on both mobile and desktop interfaces.",
            "To maintain strict regulatory adherence across diverse jurisdictions, MyPrize operates a segregated, dual-ecosystem model featuring MyPrize.us (compliant with North American promotional sweepstakes frameworks) and MyPrize.com (serving international jurisdictions).",
            "Both platforms leverage institutional-grade cryptographic custody solutions and automated chain-forensics integrations via Chainalysis, monitoring transaction originations to block illicit wallet clusters and ensure comprehensive Anti-Money Laundering (AML) enforcement.",
            "The rollout follows a four-month beta phase during which early users generated over $150 million in aggregate platform volume, demonstrating surging appetite for socialized, transparent on-chain gaming mechanics.",
            "MyPrize confirmed that upcoming Q4 milestones will introduce gasless wallet onboarding via account abstraction (ERC-4337) alongside localized cashier solutions tailored to emerging Latin American and Southeast Asian markets."
        ],
        "content_type": "press-release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-igt-expands-omnichannel-digital-casino-regulated-us-states-2026",
        "slug": "igt-expands-omnichannel-digital-casino-footprint-regulated-us-states-2026",
        "title": "IGT Expands Omnichannel Digital Casino Footprint Across Regulated U.S. iGaming States",
        "publishedAt": "2026-10-21T12:15:00Z",
        "firstPublishedAt": "2026-10-21T12:15:00Z",
        "modifiedAt": "2026-10-21T12:15:00Z",
        "dateline": "LAS VEGAS & LONDON — October 21, 2026",
        "thumbnailUrl": "/images/igt-expands-omnichannel-digital-casino-footprint-regulated-us-states-2026.jpg",
        "imageUrl": "/images/igt-expands-omnichannel-digital-casino-footprint-regulated-us-states-2026.jpg",
        "sourceName": "GlobeNewswire / IGT Investor Relations",
        "sourceUrl": "https://www.globenewswire.com/news-release/2026/10/igt-digital-omnichannel-expansion-302179831.html",
        "originalUrl": "https://www.globenewswire.com/news-release/2026/10/igt-digital-omnichannel-expansion-302179831.html",
        "company": "International Game Technology (IGT)",
        "primaryCategory": "regulation",
        "topics": [
            "IGT",
            "Regulation",
            "Digital Slots",
            "United States",
            "Omnichannel",
            "Commercial Casinos"
        ],
        "region": "United States",
        "contact": "ir@igt.com",
        "excerpt": "Gaming giant International Game Technology PLC (IGT) has broadened its commercial digital casino content distribution across licensed U.S. iGaming jurisdictions, deploying flagship land-based titles across online casino platforms in Michigan, New Jersey, Pennsylvania, Connecticut, and West Virginia.",
        "lede": "International Game Technology PLC (NYSE: IGT) today announced a major digital expansion across state-regulated North American online gaming markets, deploying its proven commercial land-based slot portfolio and progressive jackpot networks onto licensed digital casino apps across five key U.S. states.",
        "boilerplate": "International Game Technology PLC (IGT) is the global leader in commercial gaming, lotteries, and sports betting solutions, listed on the New York Stock Exchange and operating across over 100 countries worldwide.",
        "expertAnalysis": "IGT's aggressive digital expansion highlights the maturing omnichannel dynamic of the U.S. gaming sector. While offshore crypto casinos and sweepstakes portals dominate unstructured territories, state-regulated commercial operators are relying on household land-based brand IP to defend market share and command player trust in regulated multi-billion-dollar state markets.",
        "body": [
            "The cross-state rollout introduces popular casino floor titles—including the acclaimed Prosperity Link progressive slot family, Wheel of Fortune multi-tier jackpots, and Cleopatra Gold—to digital casino operators in Michigan, New Jersey, Pennsylvania, Connecticut, and West Virginia.",
            "Each digital title is certified to deliver seamless omnichannel continuity, allowing players who enjoy IGT cabinets in physical commercial resort casinos to experience identical math models, bonus triggers, and audiovisual presentations on mobile smartphone devices.",
            "The launch is supported by IGT's enterprise Remote Game Server (RGS) architecture, which provides real-time state regulatory reporting, automated session-limit responsible gaming tools, and geofencing verification integrated with state gaming commissions.",
            "Official state gaming revenue reports indicate that the combined legal U.S. commercial iGaming market generated over $6.9 billion in the trailing twelve months, reflecting sustained double-digit growth as operators prioritize content breadth and high-RTP digital table games.",
            "IGT confirmed that its digital slot deployments are fully optimized for cloud microservices infrastructure, ensuring 99.99% server availability and zero-downtime game updates during peak sports and weekend wagering windows.",
            "Moving into 2027, IGT plans to accelerate digital releases of its historical horse racing (HHR) and digital lottery titles, bridging traditional retail casino floor patrons with the expanding demographic of mobile casino consumers."
        ],
        "content_type": "press-release",
        "publicationStatus": "published"
    }
]

# 1. Load existing articles
with open(MASTER_JSON, "r", encoding="utf-8") as f:
    master_articles = json.load(f)

existing_slugs = {a["slug"] for a in master_articles}
added_count = 0

for art in new_articles:
    if art["slug"] not in existing_slugs:
        master_articles.insert(0, art)
        added_count += 1
        print(f"Added article: {art['title']}")
    else:
        print(f"Article already exists: {art['slug']}")

# 2. Save master JSON
with open(MASTER_JSON, "w", encoding="utf-8") as f:
    json.dump(master_articles, f, indent=2, ensure_ascii=False)

print(f"Successfully saved {len(master_articles)} total articles to {MASTER_JSON} (+{added_count} new)!")

# 3. Update checksums
checksums = {}
for a in master_articles:
    content_str = json.dumps(a, sort_keys=True)
    checksums[a["slug"]] = hashlib.sha256(content_str.encode('utf-8')).hexdigest()

with open(CHECKSUM_JSON, "w", encoding="utf-8") as f:
    json.dump(checksums, f, indent=2)

print(f"Updated {CHECKSUM_JSON} with {len(checksums)} cryptographic hashes.")

# 4. Update CSV
with open(MASTER_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "slug", "title", "publishedAt", "primaryCategory", "company", "region", "sourceName", "sourceUrl"])
    for a in master_articles:
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

print(f"Updated {MASTER_CSV} with {len(master_articles)} rows.")
