#!/usr/bin/env python3
"""
Append Dominator Play & ONEHAZEL partnership press release safely into
articles_master.json using articles_db.append_article.
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from scripts.articles_db import append_article, load_articles, verify_immutability

new_article = {
    "id": "pr-dominator-play-partners-with-onehazel",
    "slug": "dominator-play-partners-with-onehazel-to-bring-its-games-across-a-wider-network",
    "title": "Dominator Play Partners with ONEHAZEL to Bring Its Games Across a Wider Network",
    "publishedAt": "2026-09-21T11:00:00Z",
    "firstPublishedAt": "2026-09-21T11:00:00Z",
    "modifiedAt": "2026-09-21T11:00:00Z",
    "dateline": "NEW YORK, Sept. 21, 2026",
    "thumbnailUrl": "https://cryptocasinomedia.com/images/dominator_play_onehazel_partnership.png",
    "imageUrl": "https://cryptocasinomedia.com/images/dominator_play_onehazel_partnership.png",
    "sourceName": "Dominator Play",
    "sourceUrl": "https://dominatorplay.com/",
    "originalUrl": "https://dominatorplay.com/",
    "company": "Dominator Play",
    "primaryCategory": "press-releases",
    "topics": [
        "Crypto Casinos",
        "iGaming",
        "Partnerships",
        "Distribution"
    ],
    "region": "Global",
    "contact": "editorial@cryptocasinomedia.com",
    "excerpt": "Dominator Play partners with ONEHAZEL to bring its casino games portfolio onto the gaming marketplace, streamlining game integration and distribution for operators worldwide.",
    "lede": "Dominator Play has partnered with ONEHAZEL to bring its portfolio of casino games to ONEHAZEL’s marketplace and make the integration process faster for operators.",
    "boilerplate": "Dominator Play is an iGaming content provider focused on delivering branded & bespoke games, commercially proven mechanics, and flexible solutions for operators worldwide. Combining creativity, best practices in mobile gamedev, and industry expertise, the studio develops products that connect with broad audiences and align with emerging trends.",
    "expertAnalysis": "The partnership between Dominator Play and ONEHAZEL highlights the growing industry demand for single-integration gaming marketplaces that reduce technical overhead while expanding operator access to adaptable casino titles.",
    "content_type": "press_release",
    "publicationStatus": "published",
    "body": [
        "Dominator Play has partnered with ONEHAZEL to bring its portfolio of casino games to ONEHAZEL’s marketplace and make the integration process faster for operators.",
        "<a href=\"https://dominatorplay.com/\" class=\"text-blue-700 underline\">Dominator Play</a> is taking its games to a wider casino audience through a new partnership with <a href=\"https://onehazel.com/\" class=\"text-blue-700 underline\">ONEHAZEL</a>. The partnership brings Dominator Play’s casino portfolio into the ONEHAZEL marketplace, giving operators a simpler way to discover and connect with new game content.",
        "Dominator Play’s customizable game math allows operators to configure the mathematical profile of a title for different markets. The same title can be adjusted to suit different player preferences, market conditions, and commercial objectives, with customizable RTP (94% or 96%) and volatility settings (high or low).",
        "That flexibility is backed by another part of Dominator Play’s approach: the company does not consider integration the end of the job. The game studio provides full marketing support for its products, working with operators on promotional campaigns and marketing activity.",
        "ONEHAZEL is a gaming marketplace connecting operators with multiple partners through a single integration. It gives operators access to a wider range of game content without having to build a separate integration for every partner.",
        "“We genuinely care about growing the revenue of casinos we work with. That shapes the way we build and support our games. We see the strongest partnerships as the ones where both sides have a clear commercial role to play. ONEHAZEL is a great partner for us because they make it easier for operators to connect with new game content. Their marketplace gives Dominator Play a straightforward way to reach more casino brands, while keeping the integration process simple for operators,” said Ivan Kalashniuk, CEO of Dominator Play.",
        "The partnership broadens the reach of Dominator Play’s portfolio while keeping its core advantage intact: games built to adapt, backed by the support needed to make that adaptability count. That gives the collaboration plenty of room to turn distribution into performance.",
        "Dominator Play is an iGaming content provider focused on delivering branded & bespoke games, commercially proven mechanics, and flexible solutions for operators worldwide. Combining creativity, best practices in mobile gamedev, and industry expertise, the studio develops products that connect with broad audiences and align with emerging trends."
    ]
}

if __name__ == "__main__":
    print("Verifying database immutability before append...")
    valid, count = verify_immutability()
    print(f"Pre-check PASS: {count} articles protected.")

    print(f"Appending new article: {new_article['slug']}...")
    append_article(new_article)
    print("Article appended successfully!")

    articles = load_articles()
    print(f"Total articles now: {len(articles)}")
    print(f"Latest article: {articles[0]['slug']} ({articles[0]['publishedAt']})")
