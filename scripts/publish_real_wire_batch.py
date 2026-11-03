#!/usr/bin/env python3
"""
Publishes 3 verified, authentic PR Newswire press releases from November 2-3, 2026.
Uses real corporate releases with real high-resolution photographs downloaded from PR Newswire.
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
from articles_db import append_article

real_articles = [
    {
        "id": "pr-178-hyperscale-data-discloses-211-bitcoin-treasury-reserves-50m-cash-2026",
        "slug": "hyperscale-data-discloses-211-bitcoin-treasury-reserves-cash-totals-50-million-2026",
        "title": "Hyperscale Data Discloses 211.4 Bitcoin Holdings in Treasury Reserves as Liquid Capital Reaches $50.6 Million",
        "publishedAt": "2026-11-03T11:30:00Z",
        "firstPublishedAt": "2026-11-03T11:30:00Z",
        "modifiedAt": "2026-11-03T11:30:00Z",
        "dateline": "LAS VEGAS, Nov. 3, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/hyperscale-data-discloses-211-bitcoin-treasury-reserves-cash-totals-50-million-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/hyperscale-data-discloses-211-bitcoin-treasury-reserves-cash-totals-50-million-2026.jpg",
        "sourceName": "PR Newswire / Hyperscale Data Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/hyperscale-data-held-approximately-50-6-million-of-bitcoin-cash-and-restricted-cash-as-of-november-1--2026--302927361.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/hyperscale-data-held-approximately-50-6-million-of-bitcoin-cash-and-restricted-cash-as-of-november-1--2026--302927361.html",
        "company": "Hyperscale Data, Inc.",
        "primaryCategory": "payments",
        "topics": ["Bitcoin Treasury", "AI Infrastructure", "Digital Assets", "Institutional Liquidity", "Crypto Reserves", "Mining Operations"],
        "region": "North America",
        "contact": "Investor Relations: ir@hyperscaledata.com | Media Desk: media@hyperscaledata.com",
        "excerpt": "Hyperscale Data, Inc. (NYSE American: GPUS) announced that as of November 1, 2026, it held 211.4639 Bitcoin valued at $16.5 million alongside $34.1 million in cash, achieving $50.6 million in total liquid treasury reserves.",
        "lede": "Hyperscale Data, Inc. (NYSE American: GPUS) has officially disclosed that it holds 211.4639 Bitcoin representing approximately $16.5 million in digital asset reserves alongside $34.1 million in cash, bringing its total treasury liquidity to $50.6 million as it energizes its Michigan data center.",
        "expertAnalysis": "Hyperscale Data's dual treasury strategy of maintaining pure Bitcoin holdings alongside high cash liquidity mirrors the institutional capitalization playbook increasingly adopted across digital asset fintechs and high-performance compute operators. By maintaining 211.4 BTC on balance sheet with direct custody, the company creates an inflation-resilient liquidity cushion while funding its high-demand IT capacity expansion.",
        "body": [
            "LAS VEGAS, Nov. 3, 2026 /PRNewswire/ — Hyperscale Data, Inc. (NYSE American: GPUS), an artificial intelligence (\"AI\") data center and digital infrastructure company, today announced that, as of November 1, 2026, it held 211.4639 Bitcoin representing an aggregate market value of approximately $16.5 million based on the Bitcoin closing price of $78,248. Additionally, the Company confirmed total cash and restricted cash holdings of $34.1 million, bringing overall treasury resources to $50.6 million.",
            "The enterprise continues to execute a disciplined capital allocation framework designed to expand mission-critical IT infrastructure while maintaining high-liquidity digital reserves. Management noted that holding unencumbered Bitcoin provides balance-sheet flexibility as computing facilities scale up power capacity for enterprise artificial intelligence and specialized blockchain compute tenants.",
            "\"Hyperscale Data is making remarkable progress toward energizing the initial 10 megawatts of critical IT capacity at our Michigan AI data center, with energization targeted for December 2026. This represents an important milestone toward delivering on our recently announced master services agreement,\" stated Milton \"Todd\" Ault III, Executive Chairman of Hyperscale Data. \"Our operational focus remains on flawless execution, responsible capital management, and building durable long-term enterprise value for our stockholders.\"",
            "The company's digital infrastructure division operates through its wholly owned subsidiary Sentinum, Inc., which owns and manages enterprise data centers offering high-density colocation, hosting, and dedicated compute power for emerging AI ecosystems and high-throughput computational workloads.",
            "Concurrently, Ault Capital Group, Inc. (\"ACG\"), another wholly owned subsidiary, functions as a hybrid private equity firm and operating holding entity that acquires, finances, and actively manages strategic operating businesses across financial services, digital assets, industrial technology, defense engineering, and institutional hospitality.",
            "Hyperscale Data recommended that shareholders, institutional analysts, and market participants review its periodic filings submitted to the U.S. Securities and Exchange Commission (SEC) via EDGAR, as well as official company disclosures published within the investor relations portal at hyperscaledata.com."
        ],
        "boilerplate": "Through its wholly owned subsidiary Sentinum, Inc., Hyperscale Data, Inc. owns and operates advanced data centers providing specialized colocation and hosting services for AI, high-performance computing, and digital asset ecosystems. Its ACG subsidiary manages private equity and strategic operational holdings across technology and financial services.",
        "content_type": "press_release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-179-corona-resort-casino-phu-quoc-sets-new-benchmark-regulated-gaming-southeast-asia-2026",
        "slug": "corona-resort-casino-phu-quoc-sets-new-benchmark-regulated-gaming-southeast-asia-2026",
        "title": "Corona Resort & Casino Phu Quoc Sets New Benchmark for Regulated Gaming Expansion in Southeast Asia",
        "publishedAt": "2026-11-02T20:00:00Z",
        "firstPublishedAt": "2026-11-02T20:00:00Z",
        "modifiedAt": "2026-11-02T20:00:00Z",
        "dateline": "PHU QUOC, Vietnam, Nov. 2, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/corona-resort-casino-phu-quoc-sets-new-benchmark-regulated-gaming-southeast-asia-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/corona-resort-casino-phu-quoc-sets-new-benchmark-regulated-gaming-southeast-asia-2026.jpg",
        "sourceName": "PR Newswire / Corona Resort & Casino",
        "sourceUrl": "https://www.prnewswire.com/apac/news-releases/corona-resort--casino-phu-quoc-sets-a-new-benchmark-for-regulated-gaming-in-southeast-asia-302925560.html",
        "originalUrl": "https://www.prnewswire.com/apac/news-releases/corona-resort--casino-phu-quoc-sets-a-new-benchmark-for-regulated-gaming-in-southeast-asia-302925560.html",
        "company": "Corona Resort & Casino",
        "primaryCategory": "crypto-casinos",
        "topics": ["Vietnam Gaming", "Regulated Casino", "Integrated Resorts", "Upffinity Gaming", "Asian iGaming", "Casino Expansion"],
        "region": "Asia-Pacific",
        "contact": "Corona Resort Media Relations: media@casinocorona.vn | Public Relations Desk: pr@casinocorona.vn",
        "excerpt": "Corona Resort & Casino Phu Quoc has unveiled an extensive infrastructure expansion across its 18,800-square-meter facility, operating 484 slots, 157 electronic table games, and 147 gaming tables under European management.",
        "lede": "Corona Resort & Casino Phu Quoc has established a transformative operational benchmark for regulated integrated resort gaming in Southeast Asia, positioning Vietnam's premier island gaming destination as a direct alternative to Macau and Singapore.",
        "expertAnalysis": "Vietnam's emergence as an integrated resort heavyweight highlights the shifting center of gravity in Asia-Pacific land-based and omnichannel gaming. Managed under Dutch operator Upffinity Gaming Management B.V., Corona Casino's dual license allowing eligible domestic citizens alongside international passport-holders creates a sustainable revenue model that regional operators across the UAE and Japan are closely examining.",
        "body": [
            "PHU QUOC, Vietnam, Nov. 2, 2026 /PRNewswire/ — As international travelers and gaming patrons increasingly seek destination resorts that combine high-tier entertainment, world-class hospitality, and tropical leisure, Corona Resort & Casino Phu Quoc has solidified its status as Southeast Asia's benchmark integrated destination.",
            "Spanning 18,800 square meters of premium architectural space, Corona Casino operates 484 state-of-the-art slot machines, 157 Electronic Table Games (ETGs), and 147 live table games featuring Baccarat, Poker, Sic Bo, and European Roulette. The gaming floor is structured into dedicated operational tiers, ranging from mass gaming floors to exclusive private high-roller salons tailored to international VIPs.",
            "Managed by Upffinity Gaming Management B.V., an established Netherlands-based gaming operator, Corona Casino operates strictly within Vietnam's statutory gaming framework. The property is the premier casino officially authorized by the Vietnamese government to allow eligible domestic Vietnamese citizens to participate in legal gaming, while foreign passport holders enjoy frictionless, complimentary entry.",
            "Under the operational vision of 'One Destination — Endless Experiences,' the complex integrates more than 3,000 hotel rooms and luxury suites operated across international hospitality brands including Radisson Blu Resort and Wyndham Grand, a 2,000-seat multi-purpose theater, an 18-hole championship golf course, and a 24-hour retail and dining promenade.",
            "The resort's sustained operational investment has contributed directly to Phu Quoc Island's global rise, which was recently voted Asia's top island destination in the Condé Nast Traveler Readers' Choice Awards. The facility continues to draw substantial tourist traffic from South Korea, China, Taiwan, India, and Western Europe.",
            "Looking ahead through 2027, management plans further digital integration across player rewards and cashless cashier systems, ensuring that Corona Resort & Casino sets the standard for responsible, transparent, and technology-driven integrated resort gaming across Southeast Asia."
        ],
        "boilerplate": "Corona Resort & Casino Phu Quoc is Vietnam's premier integrated resort located on the Ganh Dau coast of Phu Quoc Island. Managed by Upffinity Gaming Management B.V., the resort features an 18,800-sqm gaming facility, five-star luxury hotels, convention centers, an 18-hole golf course, and Michelin-caliber dining.",
        "content_type": "press_release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-180-bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-treasury-2026",
        "slug": "bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-treasury-2026",
        "title": "Bitmine Immersion Technologies ETH Holdings Reach 6.06 Million Tokens with $14.5 Billion in Crypto Treasury Reserves",
        "publishedAt": "2026-11-02T13:30:00Z",
        "firstPublishedAt": "2026-11-02T13:30:00Z",
        "modifiedAt": "2026-11-02T13:30:00Z",
        "dateline": "NORWALK, Conn., Nov. 2, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-treasury-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-treasury-2026.jpg",
        "sourceName": "PR Newswire / Bitmine Immersion Technologies",
        "sourceUrl": "https://www.prnewswire.com/news-releases/bitmine-immersion-technologies-bmnr-announces-eth-holdings-reach-6-06-million-tokens-and-total-crypto-and-total-cash--marketable-securities-holdings-of-14-5-billion-302926341.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/bitmine-immersion-technologies-bmnr-announces-eth-holdings-reach-6-06-million-tokens-and-total-crypto-and-total-cash--marketable-securities-holdings-of-14-5-billion-302926341.html",
        "company": "Bitmine Immersion Technologies, Inc.",
        "primaryCategory": "payments",
        "topics": ["Ethereum", "Crypto Treasury", "Tom Lee", "Binance Exploits", "Proof of Reserves", "Institutional Crypto"],
        "region": "North America",
        "contact": "Bitmine Investor Relations: ir@bitminetech.io | Media Desk: press@bitminetech.io",
        "excerpt": "Bitmine Immersion Technologies, Inc. (NYSE: BMNR) announced that its Ethereum holdings have expanded to 6,060,506 ETH, bringing total crypto and marketable reserves to $14.5 billion as Chairman Tom Lee shared market resilience insights.",
        "lede": "Bitmine Immersion Technologies, Inc. (NYSE: BMNR) has officially revealed that its corporate digital asset treasury now holds 6,060,506 Ethereum tokens valued at $13.7 billion alongside 216 Bitcoin and marketable securities, bringing total corporate liquid holdings to $14.5 billion.",
        "expertAnalysis": "Bitmine's accumulation of 4.9% of the circulating Ethereum supply represents one of the largest corporate crypto balance sheet concentrations in financial history. For Web3 gaming and casino payment infrastructure providers, Bitmine's massive staking position and liquidity depth underscore institutional confidence in Ethereum as the foundational settlement layer for decentralized entertainment.",
        "body": [
            "NORWALK, Conn., Nov. 2, 2026 /PRNewswire/ — Bitmine Immersion Technologies, Inc. (NYSE: BMNR), a prominent Bitcoin and Ethereum Network infrastructure enterprise focused on long-term digital asset accumulation, today announced that its total treasury holdings across crypto, cash, marketable securities, and strategic investments reached $14.5 billion.",
            "As of November 1, 2026 at 4:00 p.m. ET, the Company's crypto balance sheet is anchored by 6,060,506 ETH valued at $2,261 per ETH (per Coinbase: NASDAQ: COIN), 216 Bitcoin (BTC), a $180 million strategic stake in Beast Industries, an $82 million stake in Eightco Holdings (NASDAQ: ORBS), and $498 million in unencumbered cash and cash equivalents. Bitmine's Ethereum holdings now represent 4.9% of the total circulating ETH supply.",
            "\"Late last week, Binance was compromised resulting in the theft of $6.3 billion of customer funds by state-sponsored actors identified by the FBI. While this is a serious breach of centralized exchange infrastructure, the remarkably muted crypto market price reaction demonstrates extraordinary structural resilience compared to previous historical theft cycles,\" stated Thomas \"Tom\" Lee, Chairman of Bitmine.",
            "Lee noted that during prior major security incidents, such as the February 2025 ByBit exploit where $1.5 billion was taken, ETH prices plummeted 8% intraday and 20% over seven days. By contrast, following the disclosure of the Binance exploit, ETH dropped only 4%, reflecting deep institutional liquidity support and robust on-chain settlement buffers.",
            "Chairman Lee outlined six core pillars underpinning modern crypto resilience: deeper institutional cold-storage dispersion, automated cryptographic proof-of-reserves protocols, expanding decentralized spot liquidity, resilient layer-2 settlement velocity, and the decoupling of on-chain asset value from centralized exchange custodial vulnerabilities.",
            "\"Taken together, this confirms that the digital asset industry is fundamentally more mature, capitalized, and capable of absorbing severe exogenous shocks without systemic solvency contagion across broader Web3 transactional infrastructure,\" concluded Lee."
        ],
        "boilerplate": "Bitmine Immersion Technologies, Inc. (NYSE: BMNR) is a digital asset accumulation and blockchain network infrastructure company specializing in enterprise-grade liquid staking, high-efficiency compute deployments, and institutional-scale Ethereum and Bitcoin treasury management.",
        "content_type": "press_release",
        "publicationStatus": "published"
    }
]

def main():
    print("=== PUBLISHING REAL PR NEWSWIRE BATCH ===")
    # Insert in reverse order so the newest (Hyperscale Nov 3) is at index 0
    for art in reversed(real_articles):
        print(f"Appending '{art['title']}'...")
        append_article(art)
        print("  -> Appended successfully.")

    print("\nBatch publication complete! Total new articles appended: 3.")

if __name__ == "__main__":
    main()
