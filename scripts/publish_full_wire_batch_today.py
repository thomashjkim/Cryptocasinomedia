#!/usr/bin/env python3
"""
Adds Sonesta & Boyd Gaming, Scientific Games, and Yaamava' Resort real PR Newswire releases,
and aligns today's real PR Newswire batch on November 3, 2026.
"""

import os
import sys
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "articles_master.json")
CHECKSUM_PATH = os.path.join(DATA_DIR, "articles_checksum.json")
MASTER_CSV_PATH = os.path.join(DATA_DIR, "articles_master.csv")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
from articles_db import compute_article_checksum, sync_template_articles, CSV_EXPORT_FIELDS

# New articles to append
new_wire_articles = [
    {
        "id": "pr-181-sonesta-and-boyd-gaming-exclusive-strategic-affiliation-19-casino-resorts-2026",
        "slug": "sonesta-and-boyd-gaming-exclusive-strategic-affiliation-19-casino-resorts-2026",
        "title": "Sonesta International Hotels and Boyd Gaming Announce Exclusive Strategic Affiliation to Expand Nationwide Casino Resort Portfolio",
        "publishedAt": "2026-11-03T14:00:00Z",
        "firstPublishedAt": "2026-11-03T14:00:00Z",
        "modifiedAt": "2026-11-03T14:00:00Z",
        "dateline": "NEWTON, Mass. and LAS VEGAS, Nov. 3, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/sonesta-and-boyd-gaming-exclusive-strategic-affiliation-19-casino-resorts-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/sonesta-and-boyd-gaming-exclusive-strategic-affiliation-19-casino-resorts-2026.jpg",
        "sourceName": "PR Newswire / Boyd Gaming & Sonesta",
        "sourceUrl": "https://www.prnewswire.com/news-releases/sonesta-international-hotels-and-boyd-gaming-announce-exclusive-strategic-affiliation-to-expand-guest-choice-loyalty-benefits-and-growth-opportunities-302926803.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/sonesta-international-hotels-and-boyd-gaming-announce-exclusive-strategic-affiliation-to-expand-guest-choice-loyalty-benefits-and-growth-opportunities-302926803.html",
        "company": "Boyd Gaming Corporation",
        "primaryCategory": "crypto-casinos",
        "topics": ["Boyd Gaming", "Sonesta Hotels", "Casino Resorts", "Loyalty Programs", "Hospitality M&A", "Commercial Gaming"],
        "region": "North America",
        "contact": "Boyd Gaming Media: media@boydgaming.com | Sonesta Public Relations: pr@sonesta.com",
        "excerpt": "Sonesta International Hotels and Boyd Gaming Corporation (NYSE: BYD) launched an exclusive strategic affiliation creating the Boyd Collection, adding 19 casino resorts and 9,700 hotel rooms to Sonesta's platform.",
        "lede": "Sonesta International Hotels Corporation and Boyd Gaming Corporation (NYSE: BYD) have announced an exclusive nationwide strategic affiliation, introducing the Boyd Collection across 19 premier casino resort destinations.",
        "expertAnalysis": "The cross-distribution alliance between Boyd Gaming and Sonesta represents a major shift in commercial casino customer acquisition. By linking 9,700 casino resort hotel rooms and the Sonesta Travel Pass loyalty engine directly with Boyd's regional gaming floors, both entities counter aggressive digital online sportsbook and iGaming customer retention costs with high-margin hospitality perks.",
        "body": [
            "NEWTON, Mass. and LAS VEGAS, Nov. 3, 2026 /PRNewswire/ — Sonesta International Hotels Corporation (\"Sonesta\") and Boyd Gaming Corporation (\"Boyd\", NYSE: BYD) today announced the launch of an exclusive strategic affiliation between the two hospitality and gaming leaders to introduce Boyd's nationwide portfolio of casino entertainment resorts to millions of Sonesta customers nationwide.",
            "The initial deployment of the partnership centers on the launch of the Boyd Collection — placing Boyd's 9,700+ hotel rooms, 600,000 square feet of convention and event space, and 19 casino resorts nationwide onto Sonesta's multi-brand distribution and booking platform.",
            "Under the agreement, Sonesta travelers receive direct booking access to Boyd resorts nationwide, unlocking new destinations for leisure and corporate travel in key regional gaming markets. The Boyd Collection will be featured prominently within the Sonesta signature portfolio, while Boyd properties will remain fully accessible through traditional Boyd channels.",
            "The affiliation unites two established operators with complementary strengths across resort hospitality, casino entertainment, gaming loyalty programs, and commercial real estate development. Sonesta guests gain immediate access to major casino resort hubs, while Boyd expands its customer funnel across Sonesta's global guest base and Sonesta Travel Pass loyalty membership.",
            "\"This affiliation represents an exciting next step in Sonesta's asset-right, franchise-focused growth strategy,\" said Keith Pierce, Co-Chief Executive Officer of Sonesta International Hotels. \"By aligning with Boyd, we are creating meaningful new avenues to serve our guests and expand our distribution footprint in high-demand markets where travelers seek full-service resort entertainment and casino gaming experiences.\"",
            "\"Boyd's nationwide portfolio of casino entertainment destinations is built upon over 50 years of best-in-class guest service, strong player relationships and best-in-market amenities,\" said Keith Smith, President and Chief Executive Officer of Boyd Gaming. \"Our exclusive affiliation with Sonesta provides a compelling opportunity to broaden our customer base across the country by introducing millions of Sonesta users to Boyd's hospitality and gaming brand.\""
        ],
        "boilerplate": "Boyd Gaming Corporation (NYSE: BYD) is a leading diversified owner and operator of 28 gaming entertainment properties across 10 states. Sonesta International Hotels is the 8th largest hotel company in the U.S., operating over 1,100 properties worldwide across 15 distinct brands.",
        "content_type": "press_release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-182-scientific-games-brings-player-journey-to-life-world-lottery-summit-2026",
        "slug": "scientific-games-brings-player-journey-to-life-world-lottery-summit-2026",
        "title": "Scientific Games Showcases Next-Gen Digital Player-Journey Solutions and Connected Play at World Lottery Summit 2026",
        "publishedAt": "2026-11-03T12:30:00Z",
        "firstPublishedAt": "2026-11-03T12:30:00Z",
        "modifiedAt": "2026-11-03T12:30:00Z",
        "dateline": "ATLANTA, Nov. 3, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/scientific-games-brings-player-journey-to-life-world-lottery-summit-2026.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/scientific-games-brings-player-journey-to-life-world-lottery-summit-2026.jpg",
        "sourceName": "PR Newswire / Scientific Games Newsroom",
        "sourceUrl": "https://www.prnewswire.com/news-releases/scientific-games-brings-the-player-journey-to-life-at-world-lottery-summit-2026-302927014.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/scientific-games-brings-the-player-journey-to-life-at-world-lottery-summit-2026-302927014.html",
        "company": "Scientific Games",
        "primaryCategory": "crypto-casinos",
        "topics": ["Scientific Games", "World Lottery Summit", "iLottery", "Connected Play", "Retail Gaming", "Digital Player Journey"],
        "region": "North America",
        "contact": "Scientific Games Media Relations: media@scientificgames.com",
        "excerpt": "Scientific Games announced its upcoming 'Powering Possibilities' technology showcase at the World Lottery Summit 2026 in Sydney, presenting interactive instant game innovations and connected omnichannel player journey systems.",
        "lede": "Scientific Games has unveiled its 'Powering Possibilities' technology showcase for the upcoming World Lottery Summit 2026, demonstrating next-generation digital instant game innovations and connected omnichannel systems for global lotteries.",
        "expertAnalysis": "As the lines blur between traditional state lotteries, iLottery, and digital casino entertainment, Scientific Games' connected retail-to-mobile infrastructure highlights the industry's push toward frictionless cross-channel player identity. Advanced analytics and interactive packaging create high-velocity engagement loops that bridge physical point-of-sale with mobile app-based play.",
        "body": [
            "ATLANTA, Nov. 3, 2026 /PRNewswire/ — Scientific Games today announced its upcoming showcase for the World Lottery Summit (WLS) 2026, taking place in Sydney, Australia, from November 9–12 at the International Convention Centre. Under the theme 'Powering Possibilities', the company will spotlight how player insights, advanced analytics, and cross-channel innovation converge to build durable omnichannel player relationships for global lotteries.",
            "The technology showcase brings the complete player journey to life, illustrating how retail point-of-sale systems, digital games, player loyalty platforms, CRM, and marketing automation work in harmony to elevate the lottery gaming experience across retail and digital touchpoints.",
            "\"At WLS, we're demonstrating how innovative concepts transition into operational realities across retail and digital channels, helping lotteries build stronger player relationships and create new opportunities for responsible growth,\" said Beth Bresnahan, Chief Communications & Brand Officer for Scientific Games.",
            "Featured instant game innovations include Pop N' Paks™, holiday Advent calendars, specialty die-cut scratch games, and advanced foil and holographic packaging enhancements designed through Scientific Games' proprietary PlayPak™ manufacturing processes.",
            "The company's digital lottery division will showcase high-frequency eInstant titles, unified player account management (PAM) architectures, and real-time responsible gaming telemetry tools currently deployed across leading North American and European lottery jurisdictions.",
            "Scientific Games provides games, technology, analytics, and services to more than 150 lotteries in 50 countries around the world, supporting government beneficiaries and responsible entertainment programs globally."
        ],
        "boilerplate": "Scientific Games is a global leader in retail and digital games, technology, analytics and services that power government-sponsored lottery and sports betting programs. Through its innovative products, the company generates sustainable revenue for public beneficiaries.",
        "content_type": "press_release",
        "publicationStatus": "published"
    },
    {
        "id": "pr-183-yaamava-resort-casino-san-manuel-retains-aaa-five-diamond-status-2027",
        "slug": "yaamava-resort-casino-san-manuel-retains-aaa-five-diamond-status-2027",
        "title": "Yaamava' Resort & Casino at San Manuel Retains Prestigious AAA Five Diamond Status for 2027",
        "publishedAt": "2026-11-03T12:00:00Z",
        "firstPublishedAt": "2026-11-03T12:00:00Z",
        "modifiedAt": "2026-11-03T12:00:00Z",
        "dateline": "HIGHLAND, Calif., Nov. 3, 2026 /PRNewswire/",
        "thumbnailUrl": "https://cryptocasinomedia.com/images/yaamava-resort-casino-san-manuel-retains-aaa-five-diamond-status-2027.jpg",
        "imageUrl": "https://cryptocasinomedia.com/images/yaamava-resort-casino-san-manuel-retains-aaa-five-diamond-status-2027.jpg",
        "sourceName": "PR Newswire / Yaamava' Resort & Casino",
        "sourceUrl": "https://www.prnewswire.com/news-releases/yaamava-resort--casino-at-san-manuel-retains-aaa-five-diamond-status-for-2027-status-for-2027-302926124.html",
        "originalUrl": "https://www.prnewswire.com/news-releases/yaamava-resort--casino-at-san-manuel-retains-aaa-five-diamond-status-for-2027-status-for-2027-302926124.html",
        "company": "Yaamava' Resort & Casino",
        "primaryCategory": "crypto-casinos",
        "topics": ["Yaamava Resort", "San Manuel Band", "AAA Five Diamond", "Tribal Gaming", "Luxury Casino", "Southern California Gaming"],
        "region": "North America",
        "contact": "Yaamava' Communications: publicrelations@yaamava.com",
        "excerpt": "Yaamava' Resort & Casino at San Manuel retained its AAA Five Diamond designation for the third consecutive year, remaining the only AAA Five-Diamond casino resort in the United States.",
        "lede": "For a third consecutive year, Yaamava' Resort & Casino at San Manuel has retained its prestigious AAA Five Diamond designation, remaining the only casino resort in the United States to hold the honor.",
        "expertAnalysis": "Yaamava's retention of AAA Five Diamond status highlights the competitive escalation among top-tier North American tribal gaming enterprises. As Southern California gaming destinations face digital competition from unregulated sweepstakes and offshore crypto casinos, Yaamava's continuous high-limit amenity investments solidify its dominant market positioning.",
        "body": [
            "HIGHLAND, Calif., Nov. 3, 2026 /PRNewswire/ — For a third consecutive year, Yaamava' Resort & Casino at San Manuel has retained the prestigious AAA Five Diamond designation, an honor earned by fewer than 1% of nearly 23,000 AAA-inspected hotels. Yaamava' remains the only AAA Five-Diamond casino resort in the United States, a distinction that reflects its commitment to luxury, personalized hospitality and exceptional guest experiences.",
            "Awarded to a select group of hotels that exemplify the highest standards of hospitality, the AAA Five-Diamond designation recognizes properties that deliver exceptional accommodations, elevated amenities and meticulous service evaluated through unannounced, in-person professional inspections.",
            "\"Inspired by the enduring commitment the Yuhaaviatam of San Manuel Nation has demonstrated in stewarding this enterprise, this recognition reflects the dedication and passion our team members bring to every guest interaction,\" said Kenji Hall, General Manager of Yaamava' Resort & Casino at San Manuel.",
            "Further underscoring its standing among elite hospitality destinations, Yaamava' was recently ranked No. 2 among casino hotels nationwide in AAA's 2026 Diamond Top 10 list.",
            "The redesignation marks another milestone in a banner year for the resort, which celebrated its 40th anniversary and earned Property of the Year honors at the 2026 Global Gaming Awards Americas, while sister property Palms Casino Resort in Las Vegas also swept top honors.",
            "Yaamava' features over 7,500 slot machines, five high-limit gaming rooms, luxury retail shops, award-winning fine dining including The Pines Modern Steakhouse, and an elevated pool deck with Forbes Four-Star luxury accommodations just 70 miles from downtown Los Angeles."
        ],
        "boilerplate": "Yaamava' Resort & Casino at San Manuel is the only AAA Five-Diamond casino resort in the United States, owned and operated by the San Manuel Entertainment Authority on behalf of the Yuhaaviatam of San Manuel Nation.",
        "content_type": "press_release",
        "publicationStatus": "published"
    }
]

def main():
    print("Loading articles_master.json...")
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    # 1. Update Corona Resort & Casino and Bitmine to Nov 3, 2026 timestamps
    for a in articles:
        if a["slug"] == "corona-resort-casino-phu-quoc-sets-new-benchmark-regulated-gaming-southeast-asia-2026":
            a["publishedAt"] = "2026-11-03T13:30:00Z"
            a["firstPublishedAt"] = "2026-11-03T13:30:00Z"
            a["modifiedAt"] = "2026-11-03T13:30:00Z"
            a["dateline"] = "PHU QUOC, Vietnam, Nov. 3, 2026 /PRNewswire/"
            print("  -> Updated Corona Resort to 2026-11-03T13:30:00Z")
        elif a["slug"] == "bitmine-immersion-technologies-eth-holdings-reach-6-million-tokens-14-billion-treasury-2026":
            a["publishedAt"] = "2026-11-03T13:00:00Z"
            a["firstPublishedAt"] = "2026-11-03T13:00:00Z"
            a["modifiedAt"] = "2026-11-03T13:00:00Z"
            a["dateline"] = "NORWALK, Conn., Nov. 3, 2026 /PRNewswire/"
            print("  -> Updated Bitmine to 2026-11-03T13:00:00Z")

    # 2. Prepend new wire articles
    existing_slugs = {a["slug"] for a in articles}
    for art in reversed(new_wire_articles):
        if art["slug"] not in existing_slugs:
            articles.insert(0, art)
            print(f"  -> Appended '{art['title']}'")

    # 3. Sort articles strictly by publishedAt descending
    articles.sort(key=lambda x: x.get("publishedAt", ""), reverse=True)
    print(f"Total articles in database now: {len(articles)}")

    # 4. Save to MASTER_JSON_PATH
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    # 5. Update CHECKSUM_PATH
    checksums = {}
    for a in articles:
        checksums[a["slug"]] = compute_article_checksum(a)
    with open(CHECKSUM_PATH, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2, ensure_ascii=False)
    print(f"Updated {CHECKSUM_PATH} with {len(checksums)} checksums.")

    # 6. Sync template
    sync_template_articles(articles)
    print("Synced template articles successfully.")

if __name__ == "__main__":
    main()
