import sys
import os
import re
import json
import urllib.parse
from datetime import datetime

def inject_sponsored_rel(text):
    # Regex to find <a href="..."> and inject rel="sponsored nofollow"
    # only if the URL is external (i.e. starts with http and doesn't contain cryptocasinomedia.com)
    def replacer(match):
        tag = match.group(0)
        href_match = re.search(r'href=["\'](https?://[^"\']+)["\']', tag)
        if href_match:
            url = href_match.group(1)
            if 'cryptocasinomedia.com' not in url:
                if 'rel=' in tag:
                    tag = re.sub(r'rel=["\'][^"\']*["\']', 'rel="sponsored nofollow"', tag)
                else:
                    tag = tag.replace('<a ', '<a rel="sponsored nofollow" ')
        return tag
    return re.sub(r'<a\s+[^>]*>', replacer, text)

# Setup paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from update_articles import articles_data
except ImportError as e:
    print(f"Error importing articles_data: {e}")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_path = os.path.join(PROJECT_ROOT, "index/index.html.template")
output_base_dir = os.path.join(PROJECT_ROOT, "index")

# Sort articles newest first
articles_sorted = sorted(articles_data, key=lambda x: x['publishedAt'], reverse=True)

try:
    with open(os.path.join(PROJECT_ROOT, "data", "expert_analysis.json"), "r", encoding="utf-8") as f:
        expert_analysis_data = json.load(f)
except Exception:
    expert_analysis_data = {}

# L2 and Navigation configuration
L2_MENUS = {
    '/press-releases/': ['All', 'New Launches', 'Partnerships', 'Bonuses', 'Expansion', 'Technology', 'Compliance'],
    '/regulation/': ['USA', 'Canada', 'Europe', 'Asia', 'Licensing', 'Enforcement'],
    '/payments/': ['Bitcoin', 'Ethereum', 'Stablecoins', 'Fast Withdrawals', 'No KYC'],
    '/sweepstakes/': ['Market Updates', 'Coin Trends', 'Operator Launches', 'Promotions', 'Guides']
}

navItems = [
    { 'label': 'Press Releases', 'path': '/press-releases/' },
    { 'label': 'Crypto Casinos', 'path': '/crypto-casinos/' },
    { 'label': 'Sportsbook', 'path': '/sportsbook/' },
    { 'label': 'Regulation', 'path': '/regulation/' },
    { 'label': 'Payments', 'path': '/payments/' },
    { 'label': 'Sweepstakes', 'path': '/sweepstakes/' },
    { 'label': 'Guides', 'path': '/guides/' },
]

# Global Wikidata Entity mappings for high-value B2B concepts
WIKIDATA_MAPPING = {
    'bitcoin': 'https://www.wikidata.org/wiki/Q11660',
    'ethereum': 'https://www.wikidata.org/wiki/Q20105098',
    'stablecoins': 'https://www.wikidata.org/wiki/Q60752538',
    'cryptocurrency': 'https://www.wikidata.org/wiki/Q13479982',
    'blockchain': 'https://www.wikidata.org/wiki/Q20312506',
    'igaming': 'https://www.wikidata.org/wiki/Q1367983',
    'licensing': 'https://www.wikidata.org/wiki/Q1377161',
    'usa': 'https://www.wikidata.org/wiki/Q30',
    'canada': 'https://www.wikidata.org/wiki/Q16',
    'europe': 'https://www.wikidata.org/wiki/Q46',
    'asia': 'https://www.wikidata.org/wiki/Q48',
    'compliance': 'https://www.wikidata.org/wiki/Q1140324'
}

# Rendering helpers in Python matching the JS template output
def getLogoHTML(dark=False, iconOnly=False):
    fillColor = "#FFFFFF" if dark else "#111111"
    icon = f"""<svg width="28" height="28" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="100" height="100" fill="{fillColor}" />
                        <path d="M40 30H25V70H40V60H35V40H40V30Z" fill="{'#111' if dark else '#FFF'}" />
                        <path d="M60 30H45V70H60V60H55V40H60V30Z" fill="{'#111' if dark else '#FFF'}" />
                        <path d="M85 30H65V70H75V45L80 55L85 45V70H95V30H85Z" fill="{'#111' if dark else '#FFF'}" />
                    </svg>"""
    if iconOnly:
        return icon
    text_color = "text-white" if dark else "text-gray-900"
    return f"""
                <div class="flex items-center gap-2">
                    {icon}
                    <span class="font-semibold tracking-tight text-lg {text_color}">CryptoCasinoMedia</span>
                </div>
            """

def renderHeader(currentPath):
    desktopNav = ""
    mobileNav = ""
    for item in navItems:
        is_active = currentPath.startswith(item['path'])
        active_class = 'text-blue-700 border-b-2 border-blue-700' if is_active else 'text-gray-900'
        desktopNav += f"""
                <a href="{item['path']}"  class="text-[13px] font-medium transition-colors hover:text-blue-700 py-5 {active_class}">
                    {item['label']}
                </a>
            """
        active_class_mobile = 'bg-gray-50 text-blue-700' if is_active else 'text-gray-900 hover:bg-gray-50'
        mobileNav += f"""
                <a href="{item['path']}" onclick="toggleMobileMenu()" class="block px-3 py-2 rounded-md text-base font-medium {active_class_mobile}">
                    {item['label']}
                </a>
            """
    return f"""
                <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex justify-between items-center h-16">
                        <a href="/" class="flex-shrink-0 flex items-center">
                            {getLogoHTML()}
                        </a>
                        <nav class="hidden lg:flex space-x-4 xl:space-x-6">
                            {desktopNav}
                        </nav>
                        <div class="hidden lg:flex items-center relative">
                            <div class="flex items-center border border-gray-200 rounded-sm px-2.5 py-1 bg-gray-50 focus-within:bg-white focus-within:border-gray-400 transition-colors">
                                <i data-lucide="search" class="w-[14px] h-[14px] text-gray-400 mr-2"></i>
                                <input id="search-input" type="text" placeholder="Search news..." oninput="handleSearchInput(event)" class="bg-transparent text-xs outline-none w-40 xl:w-48 text-gray-800 placeholder-gray-400 font-medium">
                            </div>
                            <!-- Live Search Results -->
                            <div id="search-results-overlay" class="absolute top-10 right-0 w-80 bg-white border border-gray-200 rounded-sm shadow-lg hidden z-50 max-h-96 overflow-y-auto"></div>
                        </div>
                        <div class="lg:hidden flex items-center">
                            <button onclick="toggleMobileMenu()" class="text-gray-500 hover:text-gray-900 p-2">
                                <i id="mobile-menu-icon" data-lucide="menu" class="w-6 h-6"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div id="mobile-menu" class="hidden lg:hidden border-t border-gray-200 bg-white">
                    <div class="px-2 pt-2 pb-3 space-y-1">
                        {mobileNav}
                    </div>
                </div>
            """

def renderSubNav(currentPath):
    activeCategory = None
    for path in L2_MENUS.keys():
        if currentPath.startswith(path):
            activeCategory = path
            break
    if not activeCategory:
        return ''

    items = ""
    for item in L2_MENUS[activeCategory]:
        topicSlug = item.lower().replace(' ', '-')
        targetPath = activeCategory if item == 'All' else f"{activeCategory}/topic/{topicSlug}"
        isActive = currentPath == targetPath
        active_class = 'text-blue-700 font-semibold border-b border-blue-700' if isActive else 'text-gray-500 hover:text-gray-900'
        items += f"""
                    <a href="{targetPath}" class="text-xs uppercase tracking-wider whitespace-nowrap py-2 transition-colors {active_class}">
                        {item}
                    </a>
                """

    return f"""
                <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
                    <nav class="flex space-x-6 py-2">
                        {items}
                    </nav>
                </div>
            """

def renderFooter():
    # Force 2026 for consistency with B2B audit ecosystem
    current_year = 2026
    return f"""
                <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                        <div class="col-span-1 md:col-span-2">
                            {getLogoHTML(dark=True)}
                            <p class="text-gray-400 mt-4 text-sm max-w-sm leading-relaxed">
                                CryptoCasinoMedia is an independent editorial organization dedicated to providing professional, verified news, press releases, and analysis covering the intersection of digital assets and iGaming.
                            </p>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold uppercase tracking-wider mb-4 text-gray-300">Sections</h4>
                            <ul class="space-y-2 text-sm text-gray-400">
                                <li><a href="/press-releases" class="hover:text-white transition-colors">Press Releases</a></li>
                                <li><a href="/regulation" class="hover:text-white transition-colors">Regulation & Compliance</a></li>
                                <li><a href="/payments" class="hover:text-white transition-colors">Payments & Tech</a></li>
                                <li><a href="/sweepstakes" class="hover:text-white transition-colors">Sweepstakes</a></li>
                                <li><a href="/industry/crypto" class="hover:text-white transition-colors">Crypto Industry</a></li>
                                <li><a href="/industry/igaming" class="hover:text-white transition-colors">iGaming Industry</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 class="text-sm font-semibold uppercase tracking-wider mb-4 text-gray-300">Corporate</h4>
                            <ul class="space-y-2 text-sm text-gray-400">
                                <li><a href="/about" class="hover:text-white transition-colors">About Us</a></li>
                                <li><a href="/editorial-standards" class="hover:text-white transition-colors">Editorial Standards</a></li>
                                <li><a href="/advertise" class="hover:text-white transition-colors">Advertise</a></li>
                                <li><a href="/submit" class="hover:text-white transition-colors">Submit Release</a></li>
                                <li><a href="/privacy" class="hover:text-white transition-colors">Privacy Policy</a></li>
                                <li><a href="/terms" class="hover:text-white transition-colors">Terms of Service</a></li>
                                <li><a href="/how-crypto-casino-news-works" class="hover:text-white transition-colors">How It Works</a></li>
                                <li><a href="/aeo-best-practices" class="hover:text-white transition-colors">AEO Guide</a></li>
                                <li><a href="/press-release-seo" class="hover:text-white transition-colors">Press Release SEO</a></li>
                            </ul>
                        </div>
                    </div>
                    <div class="border-t border-gray-800 pt-8 text-xs text-gray-500 space-y-4 leading-relaxed">
                        <p><strong>Disclaimer:</strong> CryptoCasinoMedia is a B2B news and editorial publisher. We are not a casino operator. The content published on this site is intended for informational and industry analysis purposes only.</p>
                        <p><strong>Responsible Gambling:</strong> If you or someone you know has a gambling problem, crisis counseling and referral services can be accessed by calling 1-800-GAMBLER.</p>
                        <p><strong>Corporate Info:</strong> CryptoCasinoMedia Group LLC, 1209 North Orange Street, Wilmington, DE 19801, USA. Tel: +1 (302) 200-3498. Email: cryptocasinomedia@gmail.com. For direct support, please use our <a href="/contact" class="text-gray-400 hover:text-white transition-colors underline font-medium">Contact Form</a>.</p>
                        <p>&copy; {current_year} CryptoCasinoMedia. All rights reserved.</p>
                    </div>
                </div>
            """

def formatDateMeta(dateStr):
    try:
        dt = datetime.fromisoformat(dateStr.replace('Z', '+00:00'))
    except Exception:
        try:
            dt = datetime.strptime(dateStr.replace('Z', ''), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            try:
                dt = datetime.strptime(dateStr.split('.')[0].replace('Z', ''), "%Y-%m-%dT%H:%M:%S")
            except Exception:
                return dateStr
    return dt.strftime("%b %d, %Y")

def renderArticleMeta(article):
    cat_display = article['primaryCategory'].replace('-', ' ')
    html = f"""<div class="flex items-center text-[12px] uppercase tracking-wider text-gray-500 mb-2">
                <span class="text-blue-700 font-semibold">{cat_display}</span>
                <span class="mx-2 text-gray-300">|</span>
                <span>{formatDateMeta(article['publishedAt'])}</span>"""
    if article.get('sourceName'):
        html += f"""<span class="mx-2 text-gray-300">•</span>
                         <span class="truncate max-w-[120px]" title="{article['sourceName']}">{article['sourceName']}</span>"""
    html += "</div>"
    return html

def renderStoryRow(article):
    return f"""
                <a href="/press-releases/{article['slug']}" class="group flex flex-col sm:flex-row gap-4 py-5 border-b border-gray-200 hover:bg-gray-50 transition-colors -mx-4 px-4 sm:mx-0 sm:px-0 rounded-sm">
                    <div class="sm:w-1/3 md:w-1/4 flex-shrink-0">
                        <div class="aspect-[3/2] w-full bg-gray-100 overflow-hidden border border-gray-200">
                            <img src="{article['thumbnailUrl']}" alt="{article['title']}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                        </div>
                    </div>
                    <div class="flex-1 flex flex-col justify-center">
                        {renderArticleMeta(article)}
                        <h3 class="text-lg font-semibold text-gray-900 group-hover:text-blue-700 transition-colors leading-snug mb-2">
                            {article['title']}
                        </h3>
                        <p class="text-sm text-gray-600 line-clamp-2">
                            {article['excerpt']}
                        </p>
                    </div>
                </a>
            """

def renderStoryGridCard(article):
    return f"""
                <a href="/press-releases/{article['slug']}" class="group flex flex-col border-b sm:border-b-0 sm:border-r border-gray-200 sm:last:border-r-0 pb-6 sm:pb-0 sm:pr-6 sm:last:pr-0">
                    <div class="aspect-[3/2] w-full bg-gray-100 overflow-hidden mb-4 border border-gray-200">
                        <img src="{article['thumbnailUrl']}" alt="{article['title']}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                    </div>
                    {renderArticleMeta(article)}
                    <h3 class="text-[17px] font-semibold text-gray-900 group-hover:text-blue-700 transition-colors leading-snug mb-2">
                        {article['title']}
                    </h3>
                </a>
            """

def renderHomePage():
    leadStory = articles_sorted[0]
    topStories = articles_sorted[1:7]
    latestSidebar = articles_sorted[7:12]
    gridStories = articles_sorted[12:15]
    guidesStories = articles_sorted[15:18]
    trendingTopics = ['Regulation', 'Sweepstakes', 'Bitcoin', 'USA', 'Esports', 'Compliance']

    topStoriesHtml = "".join([renderStoryRow(a) for a in topStories])
    latestSidebarHtml = "".join([f"""
                                        <div class="border-b border-gray-100 pb-4 last:border-0">
                                            {renderArticleMeta(article)}
                                            <a href="/press-releases/{article['slug']}" class="text-[15px] font-medium text-gray-900 hover:text-blue-700 transition-colors leading-snug">
                                                {article['title']}
                                            </a>
                                        </div>
                                    """ for article in latestSidebar])
    promoted_guides_html = """<a href="/guides/regulation-2026" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">Regulation 2026</a><a href="/guides/sweepstakes-market" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">Sweepstakes</a><a href="/guides/gamblefi-telegram" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">GambleFi</a>"""
    trendingHtml = promoted_guides_html + "".join([f"""
                                        <a href="/press-releases/topic/{topic.lower()}" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">
                                            {topic}
                                        </a>
                                    """ for topic in trendingTopics])
    gridHtml = "".join([renderStoryGridCard(a) for a in gridStories])
    guidesHtml = "".join([renderStoryGridCard(a) for a in guidesStories])

    return f"""
                <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
                    <div class="flex flex-col lg:flex-row gap-8 lg:gap-12">
                        <div class="lg:w-[70%]">
                            <a href="/press-releases/{leadStory['slug']}" class="group block mb-10">
                                <div class="aspect-[21/9] w-full bg-gray-100 overflow-hidden border border-gray-200 mb-4 relative">
                                    <img src="{leadStory['thumbnailUrl']}" alt="{leadStory['title']}" fetchpriority="high" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
                                </div>
                                {renderArticleMeta(leadStory)}
                                <h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 group-hover:text-blue-700 transition-colors leading-tight mb-3">
                                    {leadStory['title']}
                                </h1>
                                <p class="text-base text-gray-600 line-clamp-2 sm:line-clamp-3 leading-relaxed">
                                    {leadStory['lede']}
                                </p>
                            </a>

                            <div class="w-full h-[1px] bg-gray-900 mb-6"></div>
                            <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4">Top Stories</h2>
                            
                            <div class="flex flex-col">
                                {topStoriesHtml}
                            </div>
                            
                            <div class="mt-8">
                               <a href="/press-releases" class="inline-flex items-center text-sm font-semibold text-blue-700 hover:underline">
                                 View all press releases <i data-lucide="arrow-right" class="w-4 h-4 ml-1"></i>
                               </a>
                            </div>
                        </div>

                        <div class="lg:w-[30%]">
                            <div class="sticky top-24">
                                <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4 border-b border-gray-900 pb-2">Latest Updates</h2>
                                <div class="flex flex-col space-y-4 mb-10">
                                    {latestSidebarHtml}
                                </div>

                                <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4 border-b border-gray-900 pb-2">Trending Topics</h2>
                                <div class="flex flex-wrap gap-2">
                                    {trendingHtml}
                                </div>
                                
                                <div class="mt-10 bg-gray-50 border border-gray-200 p-6">
                                    <h3 class="text-sm font-semibold uppercase tracking-wider mb-2">Submit a Press Release</h3>
                                    <p class="text-sm text-gray-600 mb-4">Reach key decision makers, operators, and analysts in the crypto and iGaming sector.</p>
                                    <a href="/submit" class="block w-full text-center bg-gray-900 text-white text-sm font-medium py-2 hover:bg-blue-700 transition-colors">
                                        View Distribution Plans
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="mt-16 pt-12 border-t border-gray-200">
                        <div class="flex justify-between items-baseline mb-6 border-b border-gray-900 pb-2">
                            <h2 class="text-xl font-semibold tracking-tight text-gray-900">Operator Expansion</h2>
                            <a href="/press-releases" class="text-sm font-semibold text-blue-700 hover:underline">See all <i data-lucide="arrow-right" class="w-3.5 h-3.5 inline ml-1"></i></a>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                            {gridHtml}
                        </div>
                    </div>

                    <div class="mt-16 pt-12 border-t border-gray-200">
                        <div class="flex justify-between items-baseline mb-6 border-b border-gray-900 pb-2">
                            <h2 class="text-xl font-semibold tracking-tight text-gray-900">Industry Insights & Guides</h2>
                            <a href="/guides" class="text-sm font-semibold text-blue-700 hover:underline">See all <i data-lucide="arrow-right" class="w-3.5 h-3.5 inline ml-1"></i></a>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                            {guidesHtml}
                        </div>
                    </div>
                </div>
            """

def renderSectionPage(title, description, filterCategory, filterTopic=None):
    filteredArticles = []
    for article in articles_sorted:
        match = True
        if filterCategory and filterCategory != 'press-releases':
            match = article['primaryCategory'] == filterCategory
        if filterTopic:
            match = match and any(t.lower().replace(' ', '-') == filterTopic for t in article['topics'])
        if match:
            filteredArticles.append(article)

    displayTitle = f"{filterTopic.replace('-', ' ')} News & Releases" if filterTopic else title

    mainColumnHtml = ''
    if not filteredArticles:
        mainColumnHtml = '<div class="py-12 text-center text-gray-500">No articles found for this section.</div>'
    else:
        first = filteredArticles[0]
        rows = "".join([renderStoryRow(a) for a in filteredArticles[1:]])
        mainColumnHtml = f"""
                    <a href="/press-releases/{first['slug']}" class="group flex flex-col sm:flex-row gap-6 mb-10">
                        <div class="sm:w-1/2 aspect-[4/3] bg-gray-100 overflow-hidden border border-gray-200">
                            <img src="{first['thumbnailUrl']}" alt="{first['title']}" fetchpriority="high" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                        </div>
                        <div class="sm:w-1/2 flex flex-col justify-center">
                            {renderArticleMeta(first)}
                            <h2 class="text-2xl font-semibold text-gray-900 group-hover:text-blue-700 transition-colors leading-tight mb-3">
                                {first['title']}
                            </h2>
                            <p class="text-base text-gray-600 line-clamp-4 leading-relaxed">
                                {first['excerpt']}
                            </p>
                        </div>
                    </a>
                    <div class="w-full h-[1px] bg-gray-200 mb-6"></div>
                    <div class="flex flex-col">
                        {rows}
                    </div>
                """

    mostReadHtml = "".join([f"""
                <a href="/press-releases/{article['slug']}" class="group flex gap-3 border-b border-gray-100 pb-4 last:border-0">
                    <span class="text-2xl font-bold text-gray-200 group-hover:text-blue-200 transition-colors">{str(idx + 1).zfill(2)}</span>
                    <div>
                        {renderArticleMeta(article)}
                        <h3 class="text-[14px] font-medium text-gray-900 group-hover:text-blue-700 transition-colors leading-snug">
                            {article['title']}
                        </h3>
                    </div>
                </a>
            """ for idx, article in enumerate(articles_sorted[:5])])

    desc_html = f'<p class="text-gray-600 mt-2 text-lg max-w-2xl leading-relaxed">{description}</p>' if description else ''

    topic_name_clean = filterTopic.replace('-', ' ').title() if filterTopic else filterCategory.replace('-', ' ').title()
    
    topic_editorial_overview = f"""
            <div class="mt-6 p-6 bg-blue-50/60 border-l-4 border-blue-600 rounded-r-lg font-sans">
                <h2 class="text-xs uppercase tracking-widest font-semibold text-blue-900 mb-2">Category Overview & B2B Industry Scope</h2>
                <p class="text-sm text-blue-950 leading-relaxed m-0">
                    Welcome to the CryptoCasinoMedia B2B coverage hub for <strong>{topic_name_clean}</strong>. This archive provides real-time operator press releases, regulatory compliance mandates, financial transaction data, and market analysis. All published releases are verified against primary registries and structured with machine-readable schema for search engines and answer engines.
                </p>
            </div>
    """

    return f"""
        <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
            <div class="mb-8 border-b border-gray-200 pb-8">
                <h1 class="text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 capitalize">{displayTitle}</h1>
                {desc_html}
                {topic_editorial_overview}
            </div>

            <div class="flex flex-col lg:flex-row gap-8 lg:gap-12">
                <div class="lg:w-[70%]">
                    {mainColumnHtml}
                </div>

                <div class="lg:w-[30%]">
                    <div class="sticky top-24">
                        <div class="bg-gray-50 border border-gray-200 p-6 mb-8">
                            <h2 class="text-sm font-semibold uppercase tracking-wider mb-2 font-sans">Section Filter</h2>
                            <div class="space-y-2 mt-4 font-sans">
                                <div class="flex justify-between items-center text-sm border-b border-gray-200 pb-2">
                                    <span class="text-gray-600">Region</span>
                                    <span class="font-medium text-gray-900">Global</span>
                                </div>
                                <div class="flex justify-between items-center text-sm border-b border-gray-200 pb-2">
                                    <span class="text-gray-600">Sort By</span>
                                    <span class="font-medium text-gray-900">Newest</span>
                                </div>
                            </div>
                        </div>

                        <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4 border-b border-gray-900 pb-2">Most Read (Industry)</h2>
                        <div class="flex flex-col space-y-4">
                            {mostReadHtml}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """

def renderArticlePage(slug):
    article = next((a for a in articles_sorted if a['slug'] == slug), None)
    if not article:
        return '<div class="py-24 text-center text-gray-500">Article not found.</div>'

    relatedArticles = [a for a in articles_sorted if a['id'] != article['id'] and any(t in article['topics'] for t in a['topics'])][:3]
    
    # Published date parsing
    try:
        dt = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
    except Exception:
        try:
            dt = datetime.strptime(article['publishedAt'].replace('Z', ''), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            dt = datetime.strptime(article['publishedAt'].split('.')[0].replace('Z', ''), "%Y-%m-%dT%H:%M:%S")
        
    formattedDate = dt.strftime("%B %d, %Y")

    expert_text = expert_analysis_data.get(slug)
    if expert_text:
        expert_paragraphs = expert_text.split('\n\n')
        expert_html = f"""
                                <section id="expert-analysis" data-semantic-role="analysis" class="my-8 bg-blue-50 border-l-4 border-blue-600 p-6 rounded-r-lg font-sans">
                                    <h2 class="flex items-center text-blue-900 font-bold mb-3 uppercase tracking-wider text-sm">
                                        <i data-lucide="brain-circuit" class="w-5 h-5 mr-2"></i> CryptoCasinoMedia Expert Analysis
                                    </h2>
                                    <div class="space-y-4">
"""
        for ep in expert_paragraphs:
            if ep.strip():
                expert_html += f'                                        <p class="text-blue-800 text-sm leading-relaxed m-0">{ep.strip()}</p>\n'
        expert_html += """                                    </div>
                                </section>
        """
    else:
        expert_html = ""

    tldr_section = expert_html + f"""
                                <section id="tldr" data-semantic-role="summary" class="my-8 bg-gray-50 border-l-4 border-gray-400 p-6 rounded-sm">
                                    <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-2 font-sans">Key Takeaways (AI Overview)</h2>
                                    <p class="text-sm font-sans text-gray-800 leading-relaxed m-0">
                                        {article['excerpt']}
                                    </p>
                                </section>
                                """
                                
    ADSENSE_IN_ARTICLE = '''
<!-- In-article Ad (fluid) -->
<ins class="adsbygoogle"
     style="display:block; text-align:center"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-1468812481841371"
     data-ad-slot="5804892373"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
'''
    bodyHtml = f'<section id="core-announcement" data-semantic-role="body" data-key-entities="{", ".join(article["topics"])}">'
    for idx, p in enumerate(article['body'][1:]):
        p_formatted = inject_sponsored_rel(p)
        if p.startswith('"') or p.startswith('“') or p.startswith('`'):
            bodyHtml += f'<blockquote id="quote-{idx+1}" data-semantic-role="editorial-quote" class="pl-4 border-l-4 border-blue-600 italic my-6 text-gray-700 font-serif font-medium text-lg leading-relaxed">{p_formatted}</blockquote>'
        else:
            bodyHtml += f'<p id="p-{idx+1}" data-semantic-role="narrative-chunk" class="mt-6 font-serif text-[17px] text-gray-800 leading-relaxed">{p_formatted}</p>'
        # Insert ad after 2nd paragraph (index 1)
        if idx == 1:
            bodyHtml += ADSENSE_IN_ARTICLE
    bodyHtml += '</section>'

    # FAQ structured blocks for AEO
    faqHtml = "".join([f"""
                                <div class="border-b border-gray-100 pb-4 last:border-0">
                                    <h4 class="text-sm font-semibold text-gray-900 mb-1">What is the latest news about {topic}?</h4>
                                    <p class="text-sm text-gray-600">{article['excerpt']}</p>
                                </div>
                            """ for topic in article['topics'][:3]])

    faq_section_html = ""
    if faqHtml:
        faq_section_html = f"""
                                <section id="article-faq" class="my-10 border-t border-gray-200 pt-8 font-sans">
                                    <h3 class="text-lg font-bold text-gray-900 mb-6">Frequently Asked Questions</h3>
                                    <div class="space-y-6">
                                        {faqHtml}
                                    </div>
                                </section>
                                """

    category_name = article['primaryCategory'].replace('-', ' ').title()
    topics_list_str = ", ".join(article['topics'])
    
    industry_analysis_block = f"""
                                <section id="industry-analysis" data-semantic-role="analysis" class="my-10 border-t border-gray-200 pt-8 font-sans">
                                    <h3 class="text-xl font-bold text-gray-900 mb-4">Industry Context & Strategic Analysis</h3>
                                    <p class="text-base text-gray-700 leading-relaxed mb-4">
                                        The development surrounding {article['company']} highlights broader structural shifts within the global interactive gaming ecosystem. As operators and technology providers navigate evolving multi-jurisdictional compliance, integration of decentralized asset rails, and regulatory oversight across key markets ({article['region']}), industry standards continue to mature rapidly.
                                    </p>
                                    <p class="text-base text-gray-700 leading-relaxed mb-4">
                                        Key operational priorities for market participants in the {category_name} sector—specifically regarding {topics_list_str}—revolve around verifying transaction integrity, guaranteeing transparent odds or payouts, and establishing robust anti-money laundering (AML) protocols. Strategic announcements of this nature signal ongoing technical consolidation and institutional maturity across the digital gaming market.
                                    </p>
                                    <div class="bg-gray-50 border border-gray-200 p-4 rounded-sm text-xs text-gray-600">
                                        <strong>Editorial Verification Note:</strong> This press release was verified by the CryptoCasinoMedia B2B Desk. All corporate claims, licensing credentials, and technical assertions are cross-referenced against official regulatory registries and market benchmarks in accordance with Google Publisher Policies.
                                    </div>
                                </section>
                                """


    relatedHtml = "".join([f"""
                <div class="border-b border-gray-100 pb-4 last:border-0">
                    {renderArticleMeta(rel)}
                    <a href="/press-releases/{rel['slug']}" class="text-[14px] font-medium text-gray-900 hover:text-blue-700 transition-colors leading-snug">
                        {rel['title']}
                    </a>
                </div>
            """ for rel in relatedArticles])

    promoted_aside_html = """<a href="/guides/regulation-2026" class="inline-flex items-center px-2 py-1 bg-gray-100 text-[11px] font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm"><i data-lucide="tag" class="w-[10px] h-[10px] mr-1"></i> Regulation 2026</a><a href="/guides/sweepstakes-market" class="inline-flex items-center px-2 py-1 bg-gray-100 text-[11px] font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm"><i data-lucide="tag" class="w-[10px] h-[10px] mr-1"></i> Sweepstakes</a><a href="/guides/gamblefi-telegram" class="inline-flex items-center px-2 py-1 bg-gray-100 text-[11px] font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm"><i data-lucide="tag" class="w-[10px] h-[10px] mr-1"></i> GambleFi</a>"""
    topicsHtml = promoted_aside_html + "".join([f"""
                <a href="/press-releases/topic/{topic.lower().replace(' ', '-')}" class="inline-flex items-center px-2 py-1 bg-gray-100 text-[11px] font-medium text-gray-700 hover:bg-gray-200 transition-colors">
                    <i data-lucide="tag" class="w-[10px] h-[10px] mr-1"></i> {topic}
                </a>
            """ for topic in article['topics']])

    excerpt_block = f'<p class="text-lg text-gray-600 font-serif italic mb-6 leading-relaxed">{article["excerpt"]}</p>' if article.get("excerpt") else ''
    thumbnail_figure = f"""
                            <figure class="mb-8 border border-gray-200 bg-gray-50 p-1">
                                <img src="{article['thumbnailUrl']}" alt="{article['title']}" fetchpriority="high" class="w-full h-auto object-cover max-h-[450px]" />
                                <figcaption class="text-[12px] text-gray-500 mt-2 px-2 pb-1 text-right font-sans">
                                    Image provided by {article['sourceName']}
                                </figcaption>
                            </figure>
                            """ if article.get('thumbnailUrl') else ''

    contact_block = f"""
                                <div class="mt-8 font-sans text-sm">
                                    <strong>Media Contact:</strong><br />
                                    <a href="mailto:{article['contact']}" class="text-blue-700 hover:underline">{article['contact']}</a>
                                </div>
                                """ if article.get('contact') else ''

    promoted_footer_html = """<a href="/guides/regulation-2026" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">Regulation 2026</a><a href="/guides/sweepstakes-market" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">Sweepstakes</a><a href="/guides/gamblefi-telegram" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">GambleFi</a>"""
    topics_footer_html = promoted_footer_html + "".join([f'<a href="/press-releases/topic/{t.lower().replace(" ", "-")}" class="px-3 py-1.5 bg-gray-100 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors rounded-sm">{t}</a>' for t in article['topics']])

    company_name = article['company']
    if any(p in company_name for p in ["Polymarket", "Kalshi", "CFTC"]):
        about_company_text = f"The platforms and protocols referenced ({company_name}) represent leading digital prediction networks and regulated event contract markets, facilitating peer-to-peer wagering and structured hedging on global event outcomes."
    elif any(p in company_name for p in ["Google", "Alphabet"]):
        about_company_text = "Google (Alphabet Inc.) is a global technology leader, specializing in search engine platforms, digital advertising, and cloud computing infrastructure, defining advertising policy and compliance standards globally."
    elif "," in company_name or "&" in company_name or " and " in company_name:
        about_company_text = f"The platforms and operators referenced ({company_name}) represent leading digital asset wagering networks, decentralized sportsbooks, or compliance entities operating within the interactive gaming space."
    else:
        about_company_text = f"{company_name} is a leading operator in the digital asset and interactive gaming space, committed to providing secure, transparent, and innovative entertainment experiences globally. For more information, visit the official corporate portal."

    return f"""
                <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
                    <nav aria-label="Breadcrumb" class="flex text-[11px] uppercase tracking-wider text-gray-500 mb-6 font-sans">
                        <a href="/" class="hover:text-gray-900">Home</a>
                        <span class="mx-2">/</span>
                        <a href="/press-releases" class="hover:text-gray-900">Press Releases</a>
                        <span class="mx-2">/</span>
                        <a href="/{article['primaryCategory']}" class="hover:text-gray-900">{article['primaryCategory'].replace('-', ' ')}</a>
                        <span class="mx-2">/</span>
                        <span class="text-gray-900 font-medium truncate max-w-[200px] sm:max-w-none">{article['title'][:40]}...</span>
                    </nav>

                    <div class="flex flex-col lg:flex-row gap-12">
                        <article class="lg:w-[70%] max-w-[760px]">
                            <div class="mb-6">
                                <span class="inline-block px-2 py-1 bg-gray-900 text-white text-[10px] uppercase tracking-widest font-semibold mb-4 font-sans">
                                    Press Release
                                </span>
                                <h1 id="article-headline" class="text-3xl sm:text-[40px] leading-[1.15] font-semibold tracking-tight text-gray-900 mb-4">
                                    {article['title']}
                                </h1>
                                {excerpt_block}
                                
                                <div class="flex flex-col sm:flex-row sm:items-center justify-between py-4 border-y border-gray-200 gap-4 font-sans">
                                    <div>
                                        <div class="flex items-center gap-2 mb-1">
                                            <span class="text-sm font-semibold text-gray-900" itemprop="author">{article['sourceName']}</span>
                                            <span class="text-gray-300">•</span>
                                            <span class="text-[11px] uppercase tracking-wider text-blue-700 font-semibold">{article['region']}</span>
                                        </div>
                                        <div class="text-[13px] text-gray-500 flex items-center gap-2">
                                            <i data-lucide="calendar" class="w-[14px] h-[14px]"></i>
                                            <time datetime="{article['publishedAt']}">{formattedDate}</time>
                                            <span class="text-gray-300">•</span>
                                            <span>Verified Source</span>
                                        </div>
                                    </div>
                                    <div class="flex gap-2">
                                        <a href="https://twitter.com/intent/tweet?text={urllib.parse.quote(article['title'])}&url=https://cryptocasinomedia.com/press-releases/{slug}" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center text-gray-500 hover:text-blue-700 hover:border-blue-700 transition-colors" aria-label="Share on Twitter">
                                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>
                                        </a>
                                        <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://cryptocasinomedia.com/press-releases/{slug}" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center text-gray-500 hover:text-blue-700 hover:border-blue-700 transition-colors" aria-label="Share on LinkedIn">
                                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                                        </a>
                                    </div>
                                </div>
                            </div>

                            {thumbnail_figure}

                            <div class="prose prose-lg prose-gray max-w-none font-serif text-[17px] leading-relaxed text-gray-800">
                                {tldr_section}
                                <p id="p-0" data-semantic-role="origin-chunk" class="font-serif text-[17px] text-gray-800 leading-relaxed">
                                    <strong>{article['dateline']}</strong> — {inject_sponsored_rel(article['body'][0])}
                                </p>
                                {bodyHtml}
                                
                                {industry_analysis_block}
                                
                                {faq_section_html}
                                
                                <div class="my-10 border-t border-b border-gray-200 py-6 bg-gray-50 px-6 font-sans">
                                    <h2 class="text-lg font-semibold mb-3 text-gray-900">About {article['company']}</h2>
                                    <p class="text-sm text-gray-700 m-0">
                                        {about_company_text}
                                    </p>
                                </div>

                                <div class="my-10 bg-gradient-to-r from-blue-900 to-indigo-900 rounded-lg shadow-lg overflow-hidden flex flex-col md:flex-row items-center justify-between p-8 font-sans text-white">
                                    <div class="mb-6 md:mb-0 md:mr-8 text-center md:text-left flex-1">
                                        <p class="text-2xl font-bold mb-2 text-white">Reach Key iGaming Operators & Analysts</p>
                                        <p class="text-blue-100 text-sm m-0">Distribute your corporate announcements, product launches, and regulatory updates directly to decision-makers across the crypto casino ecosystem.</p>
                                    </div>
                                    <a href="/advertise" class="shrink-0 bg-white text-blue-900 hover:bg-blue-50 font-bold py-3 px-6 rounded-md transition-colors whitespace-nowrap text-sm shadow-md cursor-pointer no-underline block">
                                        Submit Press Release
                                    </a>
                                </div>

                                {contact_block}

                                <section class="mt-8 pt-6 border-t border-gray-200 font-sans">
                                    <h3 class="text-base font-semibold uppercase tracking-wider text-gray-900 mb-3">Related Topics</h3>
                                    <div class="flex flex-wrap gap-2">
                                        {topics_footer_html}
                                    </div>
                                </section>
                            </div>
                        </article>

                        <aside class="lg:w-[30%] font-sans">
                            <div class="sticky top-24">
                                <div class="bg-white border border-gray-200 mb-8 shadow-sm">
                                    <div class="bg-gray-50 border-b border-gray-200 px-5 py-3">
                                        <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900">Release Facts</h2>
                                    </div>
                                    <div class="p-5 space-y-4 text-sm">
                                        <div>
                                            <span class="block text-gray-500 text-[11px] uppercase tracking-wider mb-1">Author</span>
                                            <span class="font-semibold text-gray-900">CryptoCasinoMedia Desk</span>
                                        </div>
                                        <div>
                                            <span class="block text-gray-500 text-[11px] uppercase tracking-wider mb-1">Source</span>
                                            <span class="font-semibold text-gray-900">{article['sourceName']}</span>
                                        </div>
                                        <div>
                                            <span class="block text-gray-500 text-[11px] uppercase tracking-wider mb-1">Region</span>
                                            <div class="flex items-center text-gray-900">
                                                <i data-lucide="map-pin" class="w-[14px] h-[14px] mr-1.5 text-gray-400"></i> {article['region']}
                                            </div>
                                        </div>
                                        <div>
                                            <span class="block text-gray-500 text-[11px] uppercase tracking-wider mb-2">Topics</span>
                                            <div class="flex flex-wrap gap-2">
                                                {topicsHtml}
                                            </div>
                                        </div>

                                    </div>
                                </div>

                                <div>
                                    <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4 border-b border-gray-900 pb-2">Related Releases</h2>
                                    <div class="flex flex-col space-y-4">
                                        {relatedHtml}
                                    </div>
                                </div>

                                <!-- Ad_01 - Sidebar Display Ad -->
                                <div class="mt-8" aria-label="Advertisement">
                                    <ins class="adsbygoogle"
                                         style="display:block"
                                         data-ad-client="ca-pub-1468812481841371"
                                         data-ad-slot="2743614767"
                                         data-ad-format="auto"
                                         data-full-width-responsive="true"></ins>
                                    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
                                </div>

                                <div class="mt-8">
                                    <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4 border-b border-gray-900 pb-2">Knowledge Base</h2>
                                    <div class="flex flex-col space-y-2 text-sm">
                                        <a href="/industry/crypto" class="text-blue-700 hover:underline">Crypto Casino Industry Overview</a>
                                        <a href="/industry/igaming" class="text-blue-700 hover:underline">iGaming Industry Overview</a>
                                        <a href="/how-crypto-casino-news-works" class="text-blue-700 hover:underline">How News Distribution Works</a>
                                        <a href="/aeo-best-practices" class="text-blue-700 hover:underline">AEO Best Practices</a>
                                        <a href="/press-release-seo" class="text-blue-700 hover:underline">Press Release SEO Guide</a>
                                    </div>
                                </div>

                                <div class="mt-8 bg-gray-50 border border-gray-200 p-4">
                                    <h2 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-2">Submit Your Release</h2>
                                    <p class="text-xs text-gray-600 mb-3">Reach AI systems, search engines, and industry professionals.</p>
                                    <a href="/submit" class="block w-full text-center bg-gray-900 text-white text-xs font-semibold py-2 hover:bg-blue-700 transition-colors">Get Started</a>
                                </div>
                            </div>
                        </aside>
                    </div>
                </div>
            """

def renderIndustryPage(industry):
    data = {
        'crypto': {
            'title': 'Crypto Casino Industry',
            'description': 'The crypto casino industry generated $81.4 billion in gross gaming revenue in 2024, growing fivefold since 2022. It represents approximately 15% of all iGaming payments globally.',
            'facts': [
                {'label': 'Global GGR (2024)', 'value': '$81.4 Billion'},
                {'label': 'YoY Bet Growth', 'value': '18.7%'},
                {'label': 'Share of iGaming Payments', 'value': '~15%'},
                {'label': 'Leading Operator', 'value': 'Stake ($4.7B GGR)'},
                {'label': 'Dominant Currency', 'value': 'Bitcoin (66%)'},
                {'label': 'Fastest Growing Payment', 'value': 'Stablecoins (USDT/USDC)'}
            ],
            'concepts': [
                {'name': 'Provably Fair Gaming', 'desc': 'Cryptographic proof that game outcomes are not manipulated by the operator.'},
                {'name': 'Instant Withdrawals', 'desc': 'Blockchain-based settlements enabling sub-10-minute payout processing.'},
                {'name': 'MiCA Regulation', 'desc': 'EU Markets in Crypto-Assets regulation, in force since December 2024, impacting crypto casino payment flows.'},
                {'name': 'Curacao License', 'desc': 'Primary licensing jurisdiction for offshore crypto casino operators.'},
                {'name': 'GambleFi', 'desc': 'Decentralized finance protocols integrated with gambling mechanics, enabling on-chain betting.'}
            ],
            'related': [
                {'label': 'Regulation & Compliance', 'path': '/regulation'},
                {'label': 'Payments & Technology', 'path': '/payments'},
                {'label': 'Sweepstakes', 'path': '/sweepstakes'},
                {'label': 'Press Releases', 'path': '/press-releases'}
            ]
        },
        'igaming': {
            'title': 'iGaming Industry',
            'description': 'The global iGaming industry encompasses online casinos, sportsbooks, poker, and sweepstakes platforms. US market leaders BetMGM, DraftKings, and FanDuel are targeting a $55-$80 billion opportunity by 2030.',
            'facts': [
                {'label': 'US Market Leader', 'value': 'BetMGM (21% share)'},
                {'label': 'BetMGM FY2025 Revenue', 'value': '$2.8 Billion'},
                {'label': '2030 TAM Estimate', 'value': '$55-$80 Billion'},
                {'label': 'Brazil Market Open', 'value': 'January 2025'},
                {'label': 'Key Technology Trend', 'value': 'AI-driven personalization'},
                {'label': 'Leading Sweepstakes TAM', 'value': '$4B+ by Q4 2026'}
            ],
            'concepts': [
                {'name': 'Real Money Gaming (RMG)', 'desc': 'Licensed online gambling where players wager and win real currency.'},
                {'name': 'Sweepstakes Model', 'desc': 'Legal US gaming model using dual-currency (Gold Coins + Sweeps Coins) to operate in states without RMG licenses.'},
                {'name': 'GGR', 'desc': 'Gross Gaming Revenue: total wagers minus winnings paid to players. The primary revenue metric for operators.'},
                {'name': 'KYC / AML', 'desc': 'Know Your Customer and Anti-Money Laundering compliance requirements for all licensed operators.'},
                {'name': 'Responsible Gambling', 'desc': 'Operator obligations to detect and protect problem gamblers, including self-exclusion tools and deposit limits.'}
            ],
            'related': [
                {'label': 'Crypto Casinos', 'path': '/crypto-casinos'},
                {'label': 'Regulation', 'path': '/regulation'},
                {'label': 'Sportsbook', 'path': '/sportsbook'},
                {'label': 'Guides', 'path': '/guides'}
            ]
        }
    }
    d = data[industry] if industry in data else data['crypto']
    factsHtml = "".join([f'<div class="flex justify-between items-center py-2 border-b border-gray-100 text-sm"><span class="text-gray-500">{f["label"]}</span><span class="font-semibold text-gray-900">{f["value"]}</span></div>' for f in d['facts']])
    conceptsHtml = "".join([f'<div class="border border-gray-200 p-4"><h4 class="font-semibold text-gray-900 mb-1">{c["name"]}</h4><p class="text-sm text-gray-600">{c["desc"]}</p></div>' for c in d['concepts']])
    relatedHtml = "".join([f'<a href="{r["path"]}" class="px-4 py-2 bg-gray-100 text-sm font-medium text-gray-700 hover:bg-gray-200 transition-colors">{r["label"]}</a>' for r in d['related']])
    latestCoverageHtml = "".join([f'<a href="/press-releases/{a["slug"]}" class="block border-b border-gray-100 pb-3 hover:text-blue-700"><span class="text-xs text-gray-400 uppercase tracking-wider">{a["primaryCategory"]}</span><h4 class="text-sm font-medium text-gray-900 hover:text-blue-700 mt-0.5">{a["title"]}</h4></a>' for a in articles_sorted[:5]])

    return f"""<div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in"><div class="flex flex-col lg:flex-row gap-12"><div class="lg:w-[65%]"><nav class="flex text-[11px] uppercase tracking-wider text-gray-500 mb-6"><a href="/" class="hover:text-gray-900">Home</a><span class="mx-2">/</span><span>Industry</span><span class="mx-2">/</span><span class="text-gray-900 font-medium">{d['title']}</span></nav><h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-4">{d['title']}</h1><p class="text-lg text-gray-600 leading-relaxed mb-8">{d['description']}</p><section class="mb-10"><h2 class="text-xl font-semibold text-gray-900 mb-4">Key Concepts</h2><div class="grid grid-cols-1 sm:grid-cols-2 gap-3">{conceptsHtml}</div></section><section class="mb-10"><h2 class="text-xl font-semibold text-gray-900 mb-4">Related Sections</h2><div class="flex flex-wrap gap-2">{relatedHtml}</div></section><section><h2 class="text-xl font-semibold text-gray-900 mb-4">Latest Coverage</h2><div class="space-y-4">{latestCoverageHtml}</div></section></div><aside class="lg:w-[35%]"><div class="sticky top-24"><div class="bg-white border border-gray-200 p-6"><h3 class="text-xs uppercase tracking-widest font-semibold text-gray-900 mb-4">Industry Facts</h3><div>{factsHtml}</div></div></div></aside></div></div>"""

def renderKnowledgePage(type):
    pages = {

        'regulation-2026': {
            'title': 'The 2026 Crypto Casino Regulatory Guide',
            'h1': 'The 2026 Crypto Casino Regulatory Guide',
            'sections': [
                {'heading': 'Executive Summary', 'body': 'The regulatory landscape for crypto casinos has matured significantly in 2026. With the full implementation of MiCA in Europe and the restructuring of Curacao\'s licensing framework, operators must navigate a complex web of multijurisdictional compliance to maintain market access and banking relationships.'},
                {'heading': 'Curacao License Restructuring', 'body': 'Historically the primary jurisdiction for crypto casinos, Curacao has replaced its master license system with the National Ordinance for Games of Chance (LOK). In 2026, operators face stricter KYC/AML requirements, mandatory physical presence on the island, and enhanced player protection standards. Existing sub-license holders must fully transition to the new framework by Q3 2026.'},
                {'heading': 'The MiCA Impact in Europe', 'body': 'The Markets in Crypto-Assets (MiCA) regulation has fundamentally altered how crypto casinos operate within the EU. While MiCA does not regulate gambling directly, it strictly regulates the stablecoins (E-Money Tokens) and service providers that casinos rely on. Casinos must ensure their payment gateways and custody solutions are fully MiCA-compliant to serve European players legally.'},
                {'heading': 'Emerging Markets: LatAm & Brazil', 'body': 'Brazil\'s fully regulated iGaming market, which opened in early 2025, has become a primary target for crypto operators. However, the Brazilian framework requires strict local entity establishment and mandates fiat-crypto on-ramps through licensed financial institutions using PIX. Unlicensed offshore crypto casinos face aggressive ISP blocking and payment processor sanctions.'},
                {'heading': 'UKGC & Crypto Integration', 'body': 'The UK Gambling Commission maintains its stringent stance on crypto assets. While direct crypto deposits remain highly restricted, operators are increasingly utilizing licensed third-party processors that instantly convert crypto deposits to fiat. Proving source of funds (SOF) for crypto wealth remains the highest compliance hurdle for UK-licensed operators.'}
            ]
        },
        'sweepstakes-market': {
            'title': 'Sweepstakes Casinos: Market Size & Legal Framework',
            'h1': 'Sweepstakes Casinos: Market Size & Legal Framework 2026',
            'sections': [
                {'heading': 'The Sweepstakes Model Explained', 'body': 'Sweepstakes casinos operate under US sweepstakes laws rather than traditional gambling regulations. They utilize a dual-currency system: "Gold Coins" (GC) which hold no monetary value and are used for free play, and "Sweeps Coins" (SC) which are given away for free as a promotional entry and can be redeemed for real cash prizes. Players cannot purchase Sweeps Coins directly.'},
                {'heading': 'Market Size and Growth', 'body': 'The US sweepstakes casino market has exploded, surpassing $4 billion in estimated revenue in 2026. This exponential growth is driven by the slow rollout of legal real-money online casinos (iGaming) in the US, which remains restricted to only a handful of states. Sweepstakes provide a legal, casino-like experience to players in over 40 states.'},
                {'heading': 'Legal Framework and State Restrictions', 'body': 'While federally legal under sweepstakes provisions, state-level regulations vary wildly. In 2026, states like Michigan, Idaho, and Washington have taken aggressive stances against the sweepstakes model, forcing operators to geoblock residents. The legal distinction hinges on the "No Purchase Necessary" clause and the Alternative Method of Entry (AMOE), typically via mail-in requests.'},
                {'heading': 'Convergence with Crypto', 'body': 'A major trend in 2026 is the integration of cryptocurrency into the sweepstakes model. Operators are increasingly allowing users to purchase Gold Coin packages using Bitcoin or stablecoins, and redeeming Sweeps Coins via crypto payouts. This bypasses traditional banking hurdles that often plague the high-risk sweepstakes sector.'},
                {'heading': 'Future Outlook', 'body': 'As the market matures, regulatory scrutiny will intensify. Major traditional iGaming operators are expected to launch their own sweepstakes brands or acquire existing market leaders to capture the massive US audience currently inaccessible via regulated real-money channels.'}
            ]
        },
        'gamblefi-telegram': {
            'title': 'GambleFi & Telegram Casinos: Web3 Betting',
            'h1': 'GambleFi & Telegram Casinos: The Future of Web3 Betting',
            'sections': [
                {'heading': 'What is GambleFi?', 'body': 'GambleFi sits at the intersection of decentralized finance (DeFi) and iGaming. It encompasses decentralized betting protocols, on-chain casinos, and platforms that utilize smart contracts to execute bets and distribute winnings without a centralized house. This model offers unparalleled transparency, as the house edge and payout mechanics are verifiable on the blockchain.'},
                {'heading': 'The Rise of Telegram Casinos', 'body': 'Telegram casinos have become the fastest-growing acquisition channel in the crypto gambling space in 2026. By integrating directly into the Telegram messaging app via bots and mini-apps, operators eliminate the friction of traditional account creation. Players can deposit, bet, and withdraw seamlessly within the chat interface, often without extensive KYC requirements.'},
                {'heading': 'Tokenomics and Revenue Sharing', 'body': 'A defining feature of GambleFi is revenue sharing. Many decentralized casinos issue native utility tokens. Token holders can stake their assets to act as the "house bankroll," earning a yield generated from the platform\'s profits. This aligns the incentives of players, liquidity providers, and the platform.'},
                {'heading': 'Zero-Knowledge and Privacy', 'body': 'As regulatory pressures mount, GambleFi platforms are adopting Zero-Knowledge (ZK) proofs. This allows players to prove they are of legal age or not located in a restricted jurisdiction without revealing their actual identity or location, balancing compliance with the privacy ethos of Web3.'},
                {'heading': 'Challenges and Risks', 'body': 'The GambleFi sector faces significant risks, including smart contract vulnerabilities, rug pulls, and ambiguous legal status. Because many platforms operate entirely on-chain without traditional licenses, they exist in a regulatory gray area, making them vulnerable to enforcement actions from global financial regulators.'}
            ]
        },
        'how': {
            'title': 'How Crypto Casino News Distribution Works',
            'h1': 'How Crypto Casino News Distribution Works',
            'sections': [
                {'heading': 'What is Crypto Casino News Distribution?', 'body': 'Crypto casino news distribution is the process by which operators, platforms, and industry organizations publish verified announcements to editorial outlets, wire services, and B2B audiences. Unlike consumer press releases, B2B crypto casino distribution targets operators, investors, compliance teams, and technology vendors.'},
                {'heading': 'Why It Matters', 'body': 'For AI systems and search engines, verified news distribution establishes entity authority. When an operator is covered consistently across multiple independent editorial sources, AI models are more likely to cite that entity as authoritative. Consistent distribution creates a public knowledge layer that AI agents can learn from and reference.'},
                {'heading': 'How It Works — Step by Step', 'body': '1. Operator submits a verified press release with company details, contact, and dated announcement. 2. Editorial team reviews for factual accuracy and compliance with responsible gambling guidelines. 3. Content is published with structured schema markup (NewsArticle, Organization). 4. Article is indexed by Google, Bing, and AI crawlers including GPTBot and ClaudeBot. 5. Schema data enables AI systems to extract structured facts: source, date, topic, entity.'},
                {'heading': 'SEO and AEO Impact', 'body': 'Structured press release distribution creates permanent indexed URLs that accumulate domain authority over time. Each article creates internal linking opportunities and builds topical clusters that signal expertise to both search engines and AI answer engines.'},
                {'heading': 'Related Concepts', 'body': 'See also: Press Release SEO, AEO Best Practices, Crypto Casino Industry, iGaming Regulation.'}
            ]
        },
        'aeo': {
            'title': 'AEO Best Practices for Crypto and iGaming',
            'h1': 'Answer Engine Optimization (AEO) for iGaming Publishers',
            'sections': [
                {'heading': 'What is AEO?', 'body': 'Answer Engine Optimization (AEO) is the practice of structuring content so that AI systems — including ChatGPT, Perplexity, Google AI Overviews, and Claude — can accurately extract, cite, and surface your information in response to user queries.'},
                {'heading': 'Why AEO Matters for Crypto Casino Media', 'body': 'As AI-driven search becomes the primary discovery channel for B2B research, operators and publishers who optimize for AI readability gain a structural advantage. AI systems prioritize public, structured, entity-rich content over private dashboards and JavaScript-heavy SPAs.'},
                {'heading': 'Core AEO Principles', 'body': '1. Public Knowledge Surface: All key information must be on publicly accessible, crawlable pages with clean semantic URLs. 2. Entity-Centric Architecture: Build dedicated pages for each core concept — operators, regulations, technologies, markets. 3. Structured HTML: Use semantic tags (h1, h2, article, section, nav, a href) rather than div-heavy layouts. 4. AI-Readable Content Blocks: Short, factual, definitional sections with clear headings. 5. Schema Markup: NewsArticle, Organization, FAQPage, and BreadcrumbList schemas help AI systems parse content structure. 6. Provenance and Attribution: Author identity, timestamps, source citations, and organizational reputation signals all increase AI citation likelihood.'},
                {'heading': 'What to Avoid', 'body': 'Avoid canvas-only UI, JavaScript-generated hidden content, onclick-only navigation, and content that requires authentication to access. AI crawlers cannot execute complex JavaScript or log in to access content.'},
                {'heading': 'Implementation Checklist', 'body': 'Use semantic HTML throughout. Add schema markup to every article. Create entity pages for industries, operators, and concepts. Build internal topic clusters with consistent cross-linking. Ensure all URLs are descriptive and publicly accessible.'}
            ]
        },
        'seo': {
            'title': 'Press Release SEO for Crypto and iGaming Operators',
            'h1': 'Press Release SEO: How to Maximize Organic Visibility',
            'sections': [
                {'heading': 'What is Press Release SEO?', 'body': 'Press release SEO is the practice of structuring press releases to maximize organic search visibility and long-term indexing. Unlike traditional PR which optimizes for immediate news pickup, SEO-focused press releases are written for permanent search discovery.'},
                {'heading': 'Why Press Release SEO Matters', 'body': 'A well-optimized press release creates a permanent indexed asset. Over time, as it accumulates backlinks and internal links, it builds domain authority and topical relevance signals. For AI answer engines, indexed press releases with structured schema markup become citable sources for factual claims about operators and industry events.'},
                {'heading': 'Key SEO Elements for Crypto Press Releases', 'body': '1. Semantic URL: Use descriptive slugs like /press-releases/stake-10-billion-monthly-bets-2026 rather than /pr?id=8821. 2. Headline: Include the primary entity name and year. 3. Dateline: Always include city, country, and date. 4. Structured body: Lead paragraph answers who, what, where, when, why. 5. Schema: NewsArticle markup with datePublished, author, publisher, and keywords. 6. Internal links: Connect to related articles and entity pages. 7. Media contact: Include verified contact information for authoritativeness.'},
                {'heading': 'Common Mistakes to Avoid', 'body': 'Avoid keyword stuffing, duplicate content across wire services, vague headlines without entity names, missing dates, and uncrawlable JavaScript-only pages. Each press release should have a unique permanent URL.'},
                {'heading': 'Measuring Press Release SEO Performance', 'body': 'Track indexed URLs in Google Search Console, monitor organic impressions and clicks per article, check AI citation frequency using tools like Perplexity and ChatGPT queries, and measure referral traffic from backlinks acquired through press release syndication.'}
            ]
        }
    }
    p = pages[type] if type in pages else pages['how']
    sectionsHtml = "".join([f'<section class="mb-8"><h2 class="text-xl font-semibold text-gray-900 mb-3">{s["heading"]}</h2><p class="text-gray-700 leading-relaxed">{s["body"]}</p></section>' for s in p['sections']])
    return f"""<div class="max-w-[900px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in"><nav class="flex text-[11px] uppercase tracking-wider text-gray-500 mb-8"><a href="/" class="hover:text-gray-900">Home</a><span class="mx-2">/</span><a href="/guides" class="hover:text-gray-900">Guides</a><span class="mx-2">/</span><span class="text-gray-900 font-medium">{p['title']}</span></nav><h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-6">{p['h1']}</h1><div class="mt-8">{sectionsHtml}</div><div class="mt-10 pt-8 border-t border-gray-200"><h3 class="text-sm font-semibold uppercase tracking-wider text-gray-900 mb-3">Related Knowledge</h3><div class="flex flex-wrap gap-2"><a href="/how-crypto-casino-news-works" class="px-4 py-2 bg-gray-100 text-sm font-medium text-gray-700 hover:bg-gray-200">How Distribution Works</a><a href="/aeo-best-practices" class="px-4 py-2 bg-gray-100 text-sm font-medium text-gray-700 hover:bg-gray-200">AEO Best Practices</a><a href="/press-release-seo" class="px-4 py-2 bg-gray-100 text-sm font-medium text-gray-700 hover:bg-gray-200">Press Release SEO</a><a href="/industry/crypto" class="px-4 py-2 bg-gray-100 text-sm font-medium text-gray-700 hover:bg-gray-200">Crypto Industry</a><a href="/industry/igaming" class="px-4 py-2 bg-gray-100 text-sm font-medium text-gray-700 hover:bg-gray-200">iGaming Industry</a></div></div></div>"""

def renderContactPage():
    return '<div class="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in"><div class="mb-10 border-b border-gray-200 pb-8"><h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-3">Contact Us</h1><p class="text-lg text-gray-600">Reach our editorial team for inquiries, partnerships, or general questions.</p></div><form name="contact" method="POST" data-netlify="true" class="space-y-6"><input type="hidden" name="form-name" value="contact"><div class="grid grid-cols-1 sm:grid-cols-2 gap-6"><div><label class="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label><input type="text" name="name" required placeholder="John Smith" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Email Address *</label><input type="email" name="email" required placeholder="you@company.com" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Subject *</label><input type="text" name="subject" required placeholder="How can we help?" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Message *</label><textarea name="message" required rows="6" placeholder="Your message..." class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white resize-none"></textarea></div><button type="submit" class="px-8 py-3 bg-gray-900 text-white text-sm font-semibold hover:bg-blue-700 transition-colors">Send Message</button></form><div id="contact-success" class="hidden mt-6 p-4 bg-green-50 border border-green-200 text-green-800 text-sm font-medium">Thank you! Your message has been sent. We will get back to you within 1-2 business days.</div><div class="mt-12 pt-8 border-t border-gray-200"><h3 class="text-lg font-semibold text-gray-900 mb-4">Corporate Office</h3><p class="text-sm text-gray-600 mb-1"><strong>CryptoCasinoMedia Group LLC</strong></p><p class="text-sm text-gray-600 mb-4">1209 North Orange Street, Wilmington, DE 19801, USA</p><p class="text-sm text-gray-600">For direct support, please fill out the contact form above.</p></div></div>'

def renderSubmitPage():
    return '<div class="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in"><div class="mb-10 border-b border-gray-200 pb-8"><h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-3">Submit a Press Release</h1><p class="text-lg text-gray-600">Reach key decision makers, operators, and analysts in the crypto and iGaming sector.</p></div><form name="press-release" method="POST" data-netlify="true" class="space-y-6"><input type="hidden" name="form-name" value="press-release"><div class="grid grid-cols-1 sm:grid-cols-2 gap-6"><div><label class="block text-sm font-semibold text-gray-700 mb-2">Company Name *</label><input type="text" name="company" required placeholder="Your Company" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Contact Name *</label><input type="text" name="contact-name" required placeholder="Jane Doe" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div></div><div class="grid grid-cols-1 sm:grid-cols-2 gap-6"><div><label class="block text-sm font-semibold text-gray-700 mb-2">Email Address *</label><input type="email" name="email" required placeholder="press@yourcompany.com" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Distribution Date</label><input type="date" name="distribution-date" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Press Release Headline *</label><input type="text" name="headline" required placeholder="Your Press Release Title" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Category *</label><select name="category" required class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"><option value="">Select a category...</option><option value="crypto-casinos">Crypto Casinos</option><option value="sportsbook">Sportsbook</option><option value="regulation">Regulation and Compliance</option><option value="payments">Payments and Technology</option><option value="sweepstakes">Sweepstakes</option><option value="guides">Industry Guides</option></select></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Press Release Body *</label><textarea name="body" required rows="10" placeholder="Paste the full text of your press release here..." class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white resize-none"></textarea></div><div><label class="block text-sm font-semibold text-gray-700 mb-2">Image URL (optional)</label><input type="url" name="image-url" placeholder="https://yoursite.com/image.jpg" class="w-full border border-gray-300 px-4 py-2.5 text-sm focus:outline-none focus:border-gray-900 bg-white"></div><div class="bg-gray-50 border border-gray-200 p-4 text-sm text-gray-600">Distribution includes strict editorial review, permanent archiving with verified source attribution, and indexing across our network partner feeds (including Google News, Bing News, IndexNow feeds, and the iGaming Retail Syndicate). Standard turnaround is 1-3 business days.</div><button type="submit" class="px-8 py-3 bg-gray-900 text-white text-sm font-semibold hover:bg-blue-700 transition-colors">Submit Press Release</button></form><div id="pr-success" class="hidden mt-6 p-4 bg-green-50 border border-green-200 text-green-800 text-sm font-medium">Thank you for your submission! Our editorial team will review your press release and follow up within 1-3 business days.</div></div>'

def renderAboutPage():
    return """
                <div class="max-w-[900px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in">
                    <div class="mb-12 border-b border-gray-200 pb-10">
                        <h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-4">About CryptoCasinoMedia</h1>
                        <p class="text-xl text-gray-600 leading-relaxed">CryptoCasinoMedia is an independent B2B editorial news publisher covering the intersection of digital assets, online gaming, regulation, and payments.</p>
                    </div>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">What We Do</h2>
                        <p class="text-gray-700 leading-relaxed mb-4">We publish verified press releases, operator announcements, regulatory updates, and industry analysis for professionals in the crypto and iGaming sector. Our content reaches operators, investors, regulators, and technology partners across North America, Europe, and Asia.</p>
                        <p class="text-gray-700 leading-relaxed">CryptoCasinoMedia is not a casino operator. We do not accept money to publish favorable editorial coverage. All press releases are clearly labeled as such and sourced from verified operators.</p>
                    </section>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-6">What We Cover</h2>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="bg-gray-50 border border-gray-200 p-5">
                                <h3 class="font-semibold text-gray-900 mb-2">Crypto Casinos</h3>
                                <p class="text-sm text-gray-600">Platform launches, bonus structures, technology infrastructure, and operator expansions across global markets.</p>
                            </div>
                            <div class="bg-gray-50 border border-gray-200 p-5">
                                <h3 class="font-semibold text-gray-900 mb-2">Regulation & Compliance</h3>
                                <p class="text-sm text-gray-600">MiCA implementation, US state-level licensing, Curacao reforms, and emerging regulatory frameworks in Brazil and Asia.</p>
                            </div>
                            <div class="bg-gray-50 border border-gray-200 p-5">
                                <h3 class="font-semibold text-gray-900 mb-2">Payments & Technology</h3>
                                <p class="text-sm text-gray-600">Stablecoin adoption, blockchain payment rails, KYC automation, and the shift from Bitcoin to multi-asset settlement.</p>
                            </div>
                            <div class="bg-gray-50 border border-gray-200 p-5">
                                <h3 class="font-semibold text-gray-900 mb-2">Sweepstakes & Social Gaming</h3>
                                <p class="text-sm text-gray-600">US sweepstakes market growth, dual-currency models, regulatory compliance, and operator rankings.</p>
                            </div>
                        </div>
                    </section>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Our Reach</h2>
                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
                            <div class="border border-gray-200 p-4">
                                <div class="text-3xl font-bold text-gray-900">75+</div>
                                <div class="text-sm text-gray-500 mt-1">Articles Published</div>
                            </div>
                            <div class="border border-gray-200 p-4">
                                <div class="text-3xl font-bold text-gray-900">6</div>
                                <div class="text-sm text-gray-500 mt-1">Coverage Sections</div>
                            </div>
                            <div class="border border-gray-200 p-4">
                                <div class="text-3xl font-bold text-gray-900">Global</div>
                                <div class="text-sm text-gray-500 mt-1">Audience Reach</div>
                            </div>
                            <div class="border border-gray-200 p-4">
                                <div class="text-3xl font-bold text-gray-900">2026</div>
                                <div class="text-sm text-gray-500 mt-1">Founded</div>
                            </div>
                        </div>
                    </section>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-6">Editorial Team</h2>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                            <div class="bg-gray-50 border border-gray-200 p-6 rounded-sm">
                                <h3 class="font-bold text-gray-900 text-lg"><a href="/authors/marcus-vance" class="text-gray-900 hover:text-blue-700 transition-colors underline decoration-dotted">Marcus Vance</a></h3>
                                <p class="text-xs text-blue-700 font-semibold mb-2">Lead iGaming Analyst</p>
                                <p class="text-sm text-gray-600 leading-relaxed">Marcus has over a decade of experience analyzing digital asset betting volumes, platform architectures, and offshore operator trends. Formerly a compliance consultant for major European sportsbooks.</p>
                            </div>
                            <div class="bg-gray-50 border border-gray-200 p-6 rounded-sm">
                                <h3 class="font-bold text-gray-900 text-lg"><a href="/authors/sophia-chen" class="text-gray-900 hover:text-blue-700 transition-colors underline decoration-dotted">Sophia Chen</a></h3>
                                <p class="text-xs text-blue-700 font-semibold mb-2">Regulatory & Compliance Editor</p>
                                <p class="text-sm text-gray-600 leading-relaxed">Sophia specializes in global online gaming legal frameworks, focusing on the Curacao GCB reforms, Brazilian iGaming regulation, and compliance standards within the US sweepstakes industry.</p>
                            </div>
                        </div>
                    </section>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Corporate Office</h2>
                        <p class="text-gray-700 mb-2"><strong>CryptoCasinoMedia Group LLC</strong></p>
                        <p class="text-gray-700 mb-4">1209 North Orange Street, Wilmington, DE 19801, USA</p>
                        <p class="text-gray-700">For direct support, you can reach our team via our <a href="/contact" class="text-blue-700 hover:underline font-semibold">Contact Form</a>.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Contact</h2>
                        <p class="text-gray-700 mb-4">For editorial inquiries, press release submissions, or advertising partnerships, use our <a href="/contact" class="text-blue-700 hover:underline">contact form</a> or <a href="/submit" class="text-blue-700 hover:underline">submit a press release</a> directly.</p>
                    </section>
                </div>
            """

def renderEditorialPage():
    return """
                <div class="max-w-[900px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in">
                    <div class="mb-12 border-b border-gray-200 pb-10">
                        <h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-4">Editorial Standards</h1>
                        <p class="text-xl text-gray-600 leading-relaxed">CryptoCasinoMedia maintains strict editorial independence. Our standards define how we source, verify, and publish content.</p>
                    </div>

                    <section class="mb-10">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Independence</h2>
                        <p class="text-gray-700 leading-relaxed">CryptoCasinoMedia does not accept payment for editorial coverage. Advertisers have no influence over news content. Press releases are published as submitted by verified operators and clearly labeled as such — they do not represent the editorial opinions of CryptoCasinoMedia.</p>
                    </section>

                    <section class="mb-10">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Verification</h2>
                        <p class="text-gray-700 leading-relaxed mb-3">We verify the following before publishing any press release:</p>
                        <ul class="space-y-2 text-gray-700">
                            <li class="flex items-start gap-2"><span class="text-blue-700 mt-0.5">&#10003;</span> Source identity and company registration</li>
                            <li class="flex items-start gap-2"><span class="text-blue-700 mt-0.5">&#10003;</span> Factual claims are not demonstrably false</li>
                            <li class="flex items-start gap-2"><span class="text-blue-700 mt-0.5">&#10003;</span> No impersonation of regulators, licensed entities, or public figures</li>
                            <li class="flex items-start gap-2"><span class="text-blue-700 mt-0.5">&#10003;</span> Content complies with responsible gambling guidelines</li>
                        </ul>
                    </section>

                    <section class="mb-10">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Corrections Policy</h2>
                        <p class="text-gray-700 leading-relaxed">If factual errors are identified in published content, we will issue a correction note within 48 hours of verification. Corrections are appended to the original article with a timestamp. We do not silently edit published articles.</p>
                    </section>

                    <section class="mb-10">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Responsible Gambling</h2>
                        <p class="text-gray-700 leading-relaxed">CryptoCasinoMedia does not promote gambling to vulnerable populations. All content is intended for B2B industry professionals. We include responsible gambling resources in our footer and reject content that targets minors or exploits addiction.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">AI Content Policy</h2>
                        <p class="text-gray-700 leading-relaxed">Some editorial summaries and article metadata on this platform are generated with AI assistance and reviewed by human editors before publication. AI-generated content is always fact-checked against primary sources. We do not publish AI-hallucinated facts.</p>
                    </section>
                </div>
            """

def renderAdvertisePage():
    return """
                <div class="max-w-[900px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in">
                    <div class="mb-12 border-b border-gray-200 pb-10">
                        <h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-4">Advertise with CryptoCasinoMedia</h1>
                        <p class="text-xl text-gray-600 leading-relaxed">Reach operators, investors, and technology partners in the crypto and iGaming industry.</p>
                    </div>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-6">Advertising Options</h2>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div class="border border-gray-200 p-6">
                                <h3 class="font-semibold text-gray-900 mb-2">Sponsored Content</h3>
                                <p class="text-sm text-gray-600 mb-3">Branded articles and thought leadership pieces clearly labeled as sponsored. Distributed across all sections.</p>
                                <span class="text-xs uppercase tracking-wider font-semibold text-blue-700">Editorial placement</span>
                            </div>
                            <div class="border border-gray-200 p-6">
                                <h3 class="font-semibold text-gray-900 mb-2">Press Release Distribution</h3>
                                <p class="text-sm text-gray-600 mb-3">Submit verified press releases for homepage and section-level distribution with full SEO indexing.</p>
                                <span class="text-xs uppercase tracking-wider font-semibold text-blue-700">News distribution</span>
                            </div>
                            <div class="border border-gray-200 p-6">
                                <h3 class="font-semibold text-gray-900 mb-2">Industry Reports</h3>
                                <p class="text-sm text-gray-600 mb-3">Co-branded market research and sector analysis reports distributed to our B2B audience.</p>
                                <span class="text-xs uppercase tracking-wider font-semibold text-blue-700">Research partnership</span>
                            </div>
                        </div>
                    </section>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Why CryptoCasinoMedia</h2>
                        <div class="space-y-3 text-gray-700">
                            <div class="flex items-start gap-3"><span class="text-blue-700 font-bold mt-0.5">&#10003;</span><span>Targeted B2B audience: operators, analysts, investors, technology vendors, and compliance teams</span></div>
                            <div class="flex items-start gap-3"><span class="text-blue-700 font-bold mt-0.5">&#10003;</span><span>Verified editorial Desk: every press release and announcement is fact-checked before publication</span></div>
                            <div class="flex items-start gap-3"><span class="text-blue-700 font-bold mt-0.5">&#10003;</span><span>Permanent syndication: published articles remain archived permanently with clear source attribution</span></div>
                            <div class="flex items-start gap-3"><span class="text-blue-700 font-bold mt-0.5">&#10003;</span><span>Global coverage: reach decision-makers across key growth regions in Europe, Latin America, and Asia</span></div>
                            <div class="flex items-start gap-3"><span class="text-blue-700 font-bold mt-0.5">&#10003;</span><span>No competitor ads or intrusive banners, ensuring direct reader attention to your announcement</span></div>
                        </div>
                    </section>

                    <section class="mb-12">
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Our Syndication & Reach Network</h2>
                        <p class="text-gray-700 leading-relaxed mb-6">We provide verified distribution and structured indexing across major financial news indexes and professional opt-in channels, ensuring high-authority visibility:</p>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 text-sm">
                            <div class="border-l-4 border-blue-700 pl-4">
                                <h4 class="font-bold text-gray-900 mb-1">Direct B2B Audience Reach</h4>
                                <p class="text-gray-600 m-0">Our CCM Weekly iGaming Newsletter is delivered directly to over 50,000 double opt-in B2B iGaming professionals, including operators, regulators, compliance officers, and technology investors.</p>
                            </div>
                            <div class="border-l-4 border-blue-700 pl-4">
                                <h4 class="font-bold text-gray-900 mb-1">Search & Feed Indexing</h4>
                                <p class="text-gray-600 m-0">Every release is mapped with JSON-LD structured schema metadata and pushed instantly to the Google News Index, Bing News indexer, and IndexNow syndicate partners (Yandex, Seznam, Naver) for immediate discovery.</p>
                            </div>
                        </div>
                    </section>

                    <section>
                        <h2 class="text-2xl font-semibold text-gray-900 mb-4">Get in Touch</h2>
                        <p class="text-gray-700 mb-4">Contact our partnerships team to discuss advertising and distribution options.</p>
                        <a href="/contact" class="inline-block px-8 py-3 bg-gray-900 text-white text-sm font-semibold hover:bg-blue-700 transition-colors">Contact Us</a>
                    </section>
                </div>
            """

def renderPrivacyPage():
    return """
                <div class="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in prose prose-lg prose-gray">
                    <h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-6 border-b border-gray-200 pb-4">Privacy Policy</h1>
                    <p class="text-xs text-gray-500 mb-8">Effective Date: May 1, 2026</p>
                    
                    <p>CryptoCasinoMedia Group LLC ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website, including any other media form, media channel, mobile website, or mobile application related or connected thereto.</p>
                    
                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">1. Collection of Your Information</h2>
                    <p>We may collect information about you in a variety of ways. The information we may collect on the Site includes:</p>
                    <ul>
                        <li><strong>Personal Data:</strong> Personally identifiable information, such as your name, shipping address, email address, and telephone number, and demographic information, such as your age, gender, hometown, and interests, that you voluntarily give to us when you choose to participate in various activities related to the Site, such as contact forms and press release submissions.</li>
                        <li><strong>Derivative Data:</strong> Information our servers automatically collect when you access the Site, such as your IP address, your browser type, your operating system, your access times, and the pages you have viewed directly before and after accessing the Site.</li>
                    </ul>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">2. Use of Your Information</h2>
                    <p>Having accurate information about you permits us to provide you with a smooth, efficient, and customized experience. Specifically, we may use information collected about you via the Site to:</p>
                    <ul>
                        <li>Deliver targeted editorial newsletters and press release confirmations.</li>
                        <li>Process and review press release submissions.</li>
                        <li>Respond to customer service and partnership inquiries.</li>
                        <li>Analyze usage and trends to improve user experience.</li>
                    </ul>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">3. Disclosure of Your Information</h2>
                    <p>We do not sell, trade, or otherwise transfer to outside parties your personally identifiable information unless we provide users with advance notice. This does not include website hosting partners and other parties who assist us in operating our website, conducting our business, or serving our B2B users, so long as those parties agree to keep this information confidential.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">4. Security of Your Information</h2>
                    <p>We use administrative, technical, and physical security measures to help protect your personal information. While we have taken reasonable steps to secure the personal information you provide to us, please be aware that despite our efforts, no security measures are perfect or impenetrable, and no method of data transmission can be guaranteed against any interception or other type of misuse.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">5. Contact Us</h2>
                    <p>If you have questions or comments about this Privacy Policy, please contact us using our <a href="/contact" class="text-blue-700 hover:underline">Contact Form</a>.</p>
                </div>
            """

def renderTermsPage():
    return """
                <div class="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in prose prose-lg prose-gray">
                    <h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-6 border-b border-gray-200 pb-4">Terms of Service</h1>
                    <p class="text-xs text-gray-500 mb-8">Effective Date: May 1, 2026</p>
                    
                    <p>Welcome to CryptoCasinoMedia.com. These Terms of Service ("Terms") govern your access to and use of the website operated by CryptoCasinoMedia Group LLC ("we," "our," or "us"). By accessing or using the Site, you agree to be bound by these Terms.</p>
                    
                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">1. Agreement to Terms</h2>
                    <p>By using our Site, you agree to these Terms and our Privacy Policy. If you do not agree to these Terms, do not use the Site. We reserve the right to modify these Terms at any time, and your continued use of the Site signifies your acceptance of any updated terms.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">2. Intellectual Property Rights</h2>
                    <p>Unless otherwise indicated, the Site and its entire contents, features, and functionality (including but not limited to all information, software, text, displays, images, video, and audio, and the design, selection, and arrangement thereof) are owned by us, our licensors, or other providers of such material and are protected by United States and international copyright, trademark, patent, trade secret, and other intellectual property or proprietary rights laws.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">3. User Content & Submissions</h2>
                    <p>When you submit a press release, article, or other content ("User Content") through our submission portal, you grant us a worldwide, non-exclusive, royalty-free, perpetual, and transferable license to publish, distribute, translate, and archive your content across our networks and partner syndicates. You warrant that you own or control all rights to the User Content and that it is factual, verified, and compliant with local iGaming regulations.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">4. Disclaimer of Warranties</h2>
                    <p>The Site and all content, materials, and services provided on the Site are provided on an "as is" and "as available" basis, without any warranties of any kind, either express or implied. Neither we nor any person associated with us makes any warranty or representation with respect to the completeness, security, reliability, quality, accuracy, or availability of the Site.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">5. Limitation of Liability</h2>
                    <p>In no event will we, our affiliates, or their licensors, service providers, employees, agents, officers, or directors be liable for damages of any kind, under any legal theory, arising out of or in connection with your use, or inability to use, the Site, any websites linked to it, or any content on the Site.</p>

                    <h2 class="text-xl font-semibold text-gray-900 mt-8 mb-4">6. Contact Us</h2>
                    <p>For questions or formal inquiries regarding these Terms, please submit them via our <a href="/contact" class="text-blue-700 hover:underline">Contact Form</a>.</p>
                </div>
            """

def renderAuthorPage(author):
    author_articles = [a for a in articles_sorted if (
        (author['slug'] == 'marcus-vance' and a['primaryCategory'] in ['sportsbook', 'payments']) or
        (author['slug'] == 'sophia-chen' and a['primaryCategory'] in ['regulation', 'sweepstakes', 'guides'])
    )]
    
    articles_html = "".join([f"""
                <div class="border-b border-gray-200 py-6 last:border-0">
                    <div class="flex items-center gap-2 mb-2 text-xs text-gray-500 font-sans">
                        <span>{a['sourceName']}</span>
                        <span>•</span>
                        <span>{formatDateMeta(a['publishedAt'])}</span>
                    </div>
                    <a href="/press-releases/{a['slug']}" class="text-xl font-semibold text-gray-900 hover:text-blue-700 transition-colors block mb-2 leading-snug">
                        {a['title']}
                    </a>
                    <p class="text-sm text-gray-600 font-sans m-0">{a['excerpt']}</p>
                </div>
            """ for a in author_articles])
            
    return f"""
                <div class="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in font-sans">
                    <div class="flex flex-col sm:flex-row items-center gap-8 border-b border-gray-200 pb-10 mb-10">
                        <img src="{author['avatar']}" alt="{author['name']}" class="w-24 h-24 rounded-full object-cover shadow-md" />
                        <div class="text-center sm:text-left flex-1">
                            <h1 class="text-3xl font-semibold text-gray-900 mb-1">{author['name']}</h1>
                            <p class="text-sm font-semibold uppercase tracking-wider text-blue-700 mb-4">{author['role']}</p>
                            <p class="text-gray-600 leading-relaxed text-[15px] m-0">{author['bio']}</p>
                        </div>
                    </div>
                    
                    <h2 class="text-xl font-semibold text-gray-900 mb-6">Articles & Publications by {author['name']}</h2>
                    <div class="space-y-2">
                        {articles_html}
                    </div>
                </div>
            """

def renderAdminPage():
    return """
        <div class="max-w-[800px] mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center animate-fade-in">
            <h1 class="text-4xl font-semibold tracking-tight text-gray-900 mb-6">⚡ B2B Audit & Amplifier Agent Dashboard</h1>
            <p class="text-lg text-gray-600 mb-8">
                Welcome to the CryptoCasinoMedia index acceleration and syndication audit command center.
            </p>
            <div class="bg-gray-50 border border-gray-200 p-8 rounded-sm text-left max-w-md mx-auto">
                <div class="mb-4">
                    <label class="block text-xs uppercase tracking-wider font-semibold text-gray-600 mb-2">Security Authentication Required</label>
                    <input type="password" id="admin-password-input" placeholder="Enter security passphrase..." class="w-full border border-gray-300 px-4 py-2 text-sm focus:outline-none focus:border-gray-900 bg-white">
                </div>
                <button onclick="handleAdminLogin()" class="w-full py-2 bg-gray-900 text-white hover:bg-blue-700 font-semibold text-sm transition-colors">Authenticate</button>
                <div id="login-error-msg" class="hidden mt-3 text-xs text-red-600 font-medium">Invalid passphrase. Access denied.</div>
            </div>
        </div>
    """

# Text replacement helper using robust string index logic
def replace_tag_content(html_content, tag_start_marker, tag_end_marker, new_inner_content):
    idx = html_content.find(tag_start_marker)
    if idx == -1:
        raise ValueError(f"Marker {tag_start_marker} not found")
    
    tag_open_end = html_content.find('>', idx)
    if tag_open_end == -1:
        raise ValueError(f"Closing '>' of start tag not found for {tag_start_marker}")
        
    end_idx = html_content.find(tag_end_marker, tag_open_end)
    if end_idx == -1:
        raise ValueError(f"End marker {tag_end_marker} not found after {tag_start_marker}")
        
    return html_content[:tag_open_end + 1] + new_inner_content + html_content[end_idx:]

def normalize_links(html):
    def replacer(match):
        full_match = match.group(0)
        url = match.group(1)
        
        # Strip domain if it's absolute
        is_absolute = False
        domain = "https://cryptocasinomedia.com"
        if url.startswith(domain):
            url = url[len(domain):]
            is_absolute = True
            
        # Split anchor
        parts = url.split("#")
        path_part = parts[0]
        anchor = f"#{parts[1]}" if len(parts) > 1 else ""
        
        # Skip if it has a dot (asset file) or is root or empty
        if "." in path_part or path_part == "/" or path_part == "":
            return full_match
            
        if not path_part.endswith("/"):
            path_part = f"{path_part}/"
            
        new_url = f"{domain}{path_part}{anchor}" if is_absolute else f"{path_part}{anchor}"
        return f'href="{new_url}"'
        
    return re.sub(r'href="((?:/|https://cryptocasinomedia\.com)[^"]*)"', replacer, html)

BASE_ORGANIZATION_SCHEMA = {
    "@type": "Organization",
    "@id": "https://cryptocasinomedia.com/#organization",
    "name": "CryptoCasinoMedia",
    "url": "https://cryptocasinomedia.com/",
    "logo": {
        "@type": "ImageObject",
        "@id": "https://cryptocasinomedia.com/#logo",
        "url": "https://cryptocasinomedia.com/favicon.ico",
        "caption": "CryptoCasinoMedia Logo"
    },
    "sameAs": [
        "https://x.com/CryptoCasinoM"
    ]
}

BASE_WEBSITE_SCHEMA = {
    "@type": "WebSite",
    "@id": "https://cryptocasinomedia.com/#website",
    "name": "CryptoCasinoMedia",
    "url": "https://cryptocasinomedia.com/",
    "publisher": {
        "@id": "https://cryptocasinomedia.com/#organization"
    },
    "potentialAction": {
        "@type": "SearchAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://cryptocasinomedia.com/?search={search_term_string}"
        },
        "query-input": "required name=search_term_string"
    }
}

def build_static_page(template_content, path, title, description, body_content, schemas=[], og_image=None):
    if path != "/" and not path.endswith("/"):
        path = f"{path}/"
    content = template_content
    
    # Default OG image fallback
    default_og_image = "https://cryptocasinomedia.com/og-image.jpg"
    image_url = og_image if og_image else default_og_image
    
    # Meta tag replacements (case-insensitive option or exact matches)
    content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content)
    content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', content)
    content = re.sub(r'<link rel="canonical" href=".*?" id="canonical-link">', f'<link rel="canonical" href="https://cryptocasinomedia.com{path}" id="canonical-link">', content)
    
    # Open Graph properties
    og_type = "article" if path.startswith("/press-releases/") and len(path.split("/")) > 2 else "website"
    content = re.sub(r'<meta property="og:type" content=".*?">', f'<meta property="og:type" content="{og_type}">', content)
    content = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">', content)
    content = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{description}">', content)
    content = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="https://cryptocasinomedia.com{path}">', content)
    
    # Inject og:image + Twitter Card tags + additional AEO meta tags
    extra_meta = f"""
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image_url}">
    <meta name="twitter:site" content="@CryptoCasinoM">"""
    
    # Insert extra_meta before the closing </head> tag (before GA tag)
    # Remove any existing og:image tags first to avoid duplicates
    content = re.sub(r'\n\s*<meta property="og:image"[^>]*>', '', content)
    content = re.sub(r'\n\s*<meta name="twitter:[^>]*>', '', content)
    
    # Compile a unified Schema.org graph
    graph_elements = []
    
    # 1. Base entities
    graph_elements.append(BASE_ORGANIZATION_SCHEMA)
    graph_elements.append(BASE_WEBSITE_SCHEMA)
    
    # 2. Base WebPage entity (if not explicitly provided as CollectionPage or WebPage)
    has_webpage_like = False
    for s in schemas:
        if s.get("@type") in ["WebPage", "CollectionPage", "FAQPage", "AboutPage", "ContactPage"]:
            has_webpage_like = True
            break
            
    if not has_webpage_like:
        webpage_schema = {
            "@type": "WebPage",
            "@id": f"https://cryptocasinomedia.com{path}#webpage",
            "url": f"https://cryptocasinomedia.com{path}",
            "name": title,
            "description": description,
            "isPartOf": {
                "@id": "https://cryptocasinomedia.com/#website"
            },
            "publisher": {
                "@id": "https://cryptocasinomedia.com/#organization"
            }
        }
        graph_elements.append(webpage_schema)
        
    # 3. Process custom schemas and add to graph
    for s in schemas:
        schema_copy = s.copy()
        if "@context" in schema_copy:
            del schema_copy["@context"]
            
        # Link Article to the correct webpage
        if schema_copy.get("@type") == "Article":
            if not has_webpage_like:
                schema_copy["mainEntityOfPage"] = f"https://cryptocasinomedia.com{path}#webpage"
            else:
                for temp_s in schemas:
                    if temp_s.get("@type") == "WebPage":
                        schema_copy["mainEntityOfPage"] = temp_s.get("@id")
                        break
                        
        graph_elements.append(schema_copy)
        
    unified_schema = {
        "@context": "https://schema.org",
        "@graph": graph_elements
    }
    
    schema_tags = f'\n    <script type="application/ld+json">{json.dumps(unified_schema, ensure_ascii=False)}</script>'
    
    content = content.replace('<!-- Google tag (gtag.js) -->', f'{extra_meta}\n{schema_tags}\n    <!-- Google tag (gtag.js) -->')
    
    # Header and footer rendering
    rendered_header = renderHeader(path)
    rendered_footer = renderFooter()
    
    # Sub navigation
    rendered_sub_nav = renderSubNav(path)
    if rendered_sub_nav:
        content = content.replace(
            '<div id="context-sub-nav" class="bg-white border-b border-gray-200 overflow-x-auto no-scrollbar hidden"></div>',
            '<div id="context-sub-nav" class="bg-white border-b border-gray-200 overflow-x-auto no-scrollbar"></div>'
        )
        content = replace_tag_content(content, '<div id="context-sub-nav" class="bg-white border-b border-gray-200 overflow-x-auto no-scrollbar"', '</div>', rendered_sub_nav)
    else:
        content = replace_tag_content(content, '<div id="context-sub-nav"', '</div>', '')
        
    content = replace_tag_content(content, '<header id="primary-nav"', '</header>', rendered_header)
    content = replace_tag_content(content, '<main id="main-content"', '</main>', body_content)
    content = replace_tag_content(content, '<footer id="footer"', '</footer>', rendered_footer)
    
    return normalize_links(content)

# Load the master dynamic index.html as our base template
with open(template_path, "r", encoding="utf-8") as f:
    template_content = f.read()

ENTITY_MAPPINGS = {
    "Stake.com": "https://en.wikipedia.org/wiki/Stake.com",
    "Stake": "https://en.wikipedia.org/wiki/Stake.com",
    "Polymarket": "https://en.wikipedia.org/wiki/Polymarket",
    "Kalshi": "https://en.wikipedia.org/wiki/Kalshi",
    "Tether": "https://en.wikipedia.org/wiki/Tether_(cryptocurrency)",
    "USDT": "https://en.wikipedia.org/wiki/Tether_(cryptocurrency)",
    "USD Coin": "https://en.wikipedia.org/wiki/USD_Coin",
    "USDC": "https://en.wikipedia.org/wiki/USD_Coin",
    "Bitcoin": "https://en.wikipedia.org/wiki/Bitcoin",
    "BTC": "https://en.wikipedia.org/wiki/Bitcoin",
    "Ethereum": "https://en.wikipedia.org/wiki/Ethereum",
    "ETH": "https://en.wikipedia.org/wiki/Ethereum",
    "Curacao Gaming Control Board": "https://www.wikidata.org/wiki/Q114881518",
    "Curacao": "https://en.wikipedia.org/wiki/Cura%C3%A7ao",
    "FIFA World Cup": "https://en.wikipedia.org/wiki/FIFA_World_Cup",
    "Telegram": "https://en.wikipedia.org/wiki/Telegram_(software)",
    "GambleFi": "https://www.wikidata.org/wiki/Q122971271",
    "Roobet": "https://en.wikipedia.org/wiki/Roobet",
    "DraftKings": "https://en.wikipedia.org/wiki/DraftKings",
    "BetMGM": "https://en.wikipedia.org/wiki/BetMGM",
    "LBLOCK": "https://www.wikidata.org/wiki/Q110823377"
}

pages_generated = 0

# List of pages to compile:
# 1. 34 Articles
for article in articles_sorted:
    slug = article['slug']
    path = f"/press-releases/{slug}/"
    title = f"{article['title']} — CryptoCasinoMedia"
    description = article['excerpt']
    
    # Generate image crops (16:9, 4:3, 1:1) from Unsplash URL
    image_base = article.get('thumbnailUrl') or "https://cryptocasinomedia.com/og-image.jpg"
    image_16_9 = image_base
    image_4_3 = image_base.replace('w=800', 'w=800&ar=4:3&fit=crop') if 'unsplash.com' in image_base else image_base
    image_1_1 = image_base.replace('w=800', 'w=800&ar=1:1&fit=crop') if 'unsplash.com' in image_base else image_base

    # Resolve entity about mappings for AEO Knowledge Graph
    mentions = []
    company_name = article.get('company')
    if company_name:
        for part in [p.strip() for p in company_name.split('&')]:
            if part in ENTITY_MAPPINGS:
                mentions.append({
                    "@type": "Thing",
                    "name": part,
                    "sameAs": ENTITY_MAPPINGS[part]
                })
            elif part.endswith(".com") and part[:-4] in ENTITY_MAPPINGS:
                mentions.append({
                    "@type": "Thing",
                    "name": part,
                    "sameAs": ENTITY_MAPPINGS[part[:-4]]
                })
    for topic in article.get('topics', []):
        if topic in ENTITY_MAPPINGS:
            if not any(m['name'] == topic for m in mentions):
                mentions.append({
                    "@type": "Thing",
                    "name": topic,
                    "sameAs": ENTITY_MAPPINGS[topic]
                })

    # Generate static Article + FAQPage + BreadcrumbList schemas
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": f"https://cryptocasinomedia.com/press-releases/{slug}/#article",
        "isPartOf": {
            "@id": "https://cryptocasinomedia.com/#website"
        },
        "headline": article['title'],
        "description": article['excerpt'],
        "datePublished": article['publishedAt'],
        "dateModified": article['publishedAt'],
        "inLanguage": "en-US",
        "mainEntityOfPage": f"https://cryptocasinomedia.com/press-releases/{slug}/",
        "author": {
            "@type": "Organization",
            "name": article['sourceName'],
            "url": article.get('originalUrl') or "https://cryptocasinomedia.com/"
        },
        "publisher": {
            "@id": "https://cryptocasinomedia.com/#organization"
        },
        "image": [image_16_9, image_4_3, image_1_1],
        "articleSection": "Press Releases",
        "keywords": ", ".join(article['topics']),
        "articleBody": " ".join(article['body']),
        "dateline": article['dateline'],
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": ["#article-headline", "#p-0"]
        }
    }
    if mentions:
        article_schema["about"] = mentions
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": f"What is the latest news about {topic}?",
            "acceptedAnswer": {"@type": "Answer", "text": article['excerpt']}
        } for topic in article['topics'][:3]]
    }
    
    cat_slug = article['primaryCategory']
    cat_name = cat_slug.replace('-', ' ').title()
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cryptocasinomedia.com/"},
            {"@type": "ListItem", "position": 2, "name": "Press Releases", "item": "https://cryptocasinomedia.com/press-releases/"},
            {"@type": "ListItem", "position": 3, "name": cat_name, "item": f"https://cryptocasinomedia.com/{cat_slug}/"},
            {"@type": "ListItem", "position": 4, "name": article['title'], "item": f"https://cryptocasinomedia.com/press-releases/{slug}/"}
        ]
    }
    
    body = renderArticlePage(slug)
    # Pass article thumbnail as og:image for rich social sharing previews
    article_og_image = article.get('thumbnailUrl')
    html = build_static_page(template_content, path, title, description, body, [article_schema, faq_schema, breadcrumb_schema], og_image=article_og_image)
    
    # Write to index/press-releases/[slug]/index.html
    out_dir = os.path.join(output_base_dir, "press-releases", slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    pages_generated += 1

# 2. L2 category hubs
categories = [
    ("/press-releases/", "Press Releases", "The latest official statements and corporate announcements from verified operators in the crypto and iGaming sector.", "press-releases"),
    ("/crypto-casinos/", "Crypto Casinos", "Latest updates, compliance standards, and game launches in the crypto casino sector.", "crypto-casinos"),
    ("/sportsbook/", "Sportsbook", "Crypto sports betting, partnership deals, and major global sportsbook news.", "sportsbook"),
    ("/regulation/", "Regulation & Compliance", "Regulatory compliance, licensing standards, and legal updates in key jurisdictions.", "regulation"),
    ("/payments/", "Payments & Technology", "Payment processing infrastructure, blockchain integrations, and stablecoin trends.", "payments"),
    ("/sweepstakes/", "Sweepstakes", "US sweepstakes casino market analysis, operator updates, and coin trends.", "sweepstakes"),
    ("/guides/", "Industry Guides", "B2B tutorials, knowledge-base guides, and professional advice for iGaming publishers.", "guides")
]

for path, title, description, filter_cat in categories:
    body = renderSectionPage(title, description, filter_cat)
    
    # Get articles for this category
    cat_articles = [a for a in articles_sorted if a['primaryCategory'] == filter_cat] if filter_cat else articles_sorted
    
    item_list = {
        "@type": "ItemList",
        "itemListElement": []
    }
    for i, a in enumerate(cat_articles):
        item_list["itemListElement"].append({
            "@type": "ListItem",
            "position": i + 1,
            "item": {
                "@type": "Article",
                "headline": a['title'],
                "url": f"https://cryptocasinomedia.com/press-releases/{a['slug']}/"
            }
        })

    collection_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"https://cryptocasinomedia.com{path}#collection",
        "name": f"{title} — CryptoCasinoMedia",
        "url": f"https://cryptocasinomedia.com{path}",
        "description": description,
        "isPartOf": {
            "@id": "https://cryptocasinomedia.com/#website"
        },
        "about": {
            "@id": "https://cryptocasinomedia.com/#organization"
        },
        "mainEntity": item_list
    }
    
    category_breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cryptocasinomedia.com/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": f"https://cryptocasinomedia.com{path}"}
        ]
    }
    
    # Generate list schema
    list_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{title} — CryptoCasinoMedia",
        "description": description,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "url": f"https://cryptocasinomedia.com/press-releases/{a['slug']}/"
            } for i, a in enumerate([x for x in articles_sorted if filter_cat == 'press-releases' or x['primaryCategory'] == filter_cat][:10])
        ]
    }
    
    html = build_static_page(template_content, path, f"{title} — CryptoCasinoMedia", description, body, [collection_schema, category_breadcrumb_schema, list_schema])
    
    # Write to index/[category]/index.html
    # Remove leading slash for folder creation
    folder_name = path.strip("/")
    out_dir = os.path.join(output_base_dir, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    pages_generated += 1

# 3. Topic pages
for category, topics in L2_MENUS.items():
    for topic in topics:
        if topic == 'All':
            continue
        topic_slug = topic.lower().replace(' ', '-')
        path = f"{category}topic/{topic_slug}/"
        title = f"{topic} News & Press Releases — CryptoCasinoMedia"
        description = f"Comprehensive B2B coverage, press releases, and compliance updates regarding {topic} in the online gaming ecosystem."
        
        body = renderSectionPage(f"{topic} News & Releases", description, category.strip("/"), topic_slug)
        
        filtered_topic_articles = [a for a in articles_sorted if any(t.lower().replace(' ', '-') == topic_slug for t in a['topics'])]
        
        topic_collection_schema = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": f"https://cryptocasinomedia.com{path}#webpage",
            "url": f"https://cryptocasinomedia.com{path}",
            "name": title,
            "description": description,
            "isPartOf": {"@id": "https://cryptocasinomedia.com/#website"},
            "publisher": {"@id": "https://cryptocasinomedia.com/#organization"}
        }
        
        topic_list_schema = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": title,
            "description": description,
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "url": f"https://cryptocasinomedia.com/press-releases/{a['slug']}/"
                } for i, a in enumerate(filtered_topic_articles[:10])
            ]
        }
        
        html = build_static_page(template_content, path, title, description, body, [topic_collection_schema, topic_list_schema])
        
        out_dir = os.path.join(output_base_dir, category.strip("/"), "topic", topic_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        pages_generated += 1

# 4. Industry hubs
industries = [
    ('crypto', 'Crypto Casino Industry Overview', 'The crypto casino industry generated $81.4B in GGR in 2024. Comprehensive industry data, key operators, regulation, and technology trends.'),
    ('igaming', 'iGaming Industry Overview', 'Global iGaming industry overview: BetMGM, DraftKings, regulation, payments, and market data for 2026.')
]

for key, title, description in industries:
    path = f"/industry/{key}/"
    body = renderIndustryPage(key)
    
    industry_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{title} — CryptoCasinoMedia",
        "description": description,
        "url": f"https://cryptocasinomedia.com{path}",
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cryptocasinomedia.com/"},
            {"@type": "ListItem", "position": 2, "name": "Industry", "item": "https://cryptocasinomedia.com/industry/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"https://cryptocasinomedia.com{path}"}
        ]},
        "publisher": {"@type": "Organization", "name": "CryptoCasinoMedia", "url": "https://cryptocasinomedia.com/"}
    }
    
    html = build_static_page(template_content, path, f"{title} — CryptoCasinoMedia", description, body, [industry_schema])
    
    out_dir = os.path.join(output_base_dir, "industry", key)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    pages_generated += 1

# 5. Knowledge base guides
guides = [
    ('regulation-2026', 'guides/regulation-2026', 'The 2026 Crypto Casino Regulatory Guide', 'A comprehensive B2B guide covering Curacao LOK, EU MiCA impact, and emerging LatAm regulatory frameworks.'),
    ('sweepstakes-market', 'guides/sweepstakes-market', 'Sweepstakes Casinos: Market Size & Legal Framework 2026', 'Understanding the $4B US sweepstakes model, Gold Coins/Sweeps Coins mechanics, and state-by-state legality.'),
    ('gamblefi-telegram', 'guides/gamblefi-telegram', 'GambleFi & Telegram Casinos: Web3 Betting', 'The rise of no-KYC Telegram bots, decentralized on-chain casinos, and revenue-sharing tokenomics.'),    ('how', 'how-crypto-casino-news-works', 'How Crypto Casino News Distribution Works', 'How crypto casino press releases reach AI systems, search engines, and industry professionals through structured news distribution.'),
    ('aeo', 'aeo-best-practices', 'AEO Best Practices for iGaming Publishers', 'Answer Engine Optimization guide for crypto casino and iGaming publishers. Structure content for ChatGPT, Perplexity, and Google AI.'),
    ('seo', 'press-release-seo', 'Press Release SEO for Crypto Operators', 'How to structure press releases for maximum SEO and AI visibility. Semantic URLs, schema markup, and content strategy.')
]

for key, slug, title, description in guides:
    path = f"/{slug}/"
    body = renderKnowledgePage(key)
    
    guide_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": f"https://cryptocasinomedia.com{path}",
        "datePublished": "2026-05-01",
        "author": {"@type": "Organization", "name": "CryptoCasinoMedia"},
        "publisher": {"@type": "Organization", "name": "CryptoCasinoMedia", "url": "https://cryptocasinomedia.com/"},
        "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cryptocasinomedia.com/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": "https://cryptocasinomedia.com/guides/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"https://cryptocasinomedia.com{path}"}
        ]}
    }
    
    html = build_static_page(template_content, path, f"{title} — CryptoCasinoMedia", description, body, [guide_schema])
    
    out_dir = os.path.join(output_base_dir, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    pages_generated += 1

# 6. Corporate & Utility Pages
utility_pages = [
    ('/about/', 'About CryptoCasinoMedia — B2B iGaming News Publisher', 'CryptoCasinoMedia is an independent B2B editorial publisher covering crypto casinos, iGaming regulation, payments, and sweepstakes.', renderAboutPage(), [
        {
            "@type": "AboutPage",
            "@id": "https://cryptocasinomedia.com/about/#webpage",
            "url": "https://cryptocasinomedia.com/about/",
            "name": "About CryptoCasinoMedia",
            "description": "CryptoCasinoMedia is an independent B2B editorial publisher covering crypto casinos, iGaming regulation, payments, and sweepstakes.",
            "isPartOf": {
                "@id": "https://cryptocasinomedia.com/#website"
            },
            "about": {
                "@id": "https://cryptocasinomedia.com/#organization"
            }
        }
    ]),
    ('/editorial-standards/', 'Editorial Standards — CryptoCasinoMedia', 'CryptoCasinoMedia maintains strict editorial independence. Our standards define how we source, verify, and publish content.', renderEditorialPage(), [
        {
            "@type": "WebPage",
            "@id": "https://cryptocasinomedia.com/editorial-standards/#webpage",
            "url": "https://cryptocasinomedia.com/editorial-standards/",
            "name": "Editorial Standards — CryptoCasinoMedia",
            "description": "CryptoCasinoMedia maintains strict editorial independence. Our standards define how we source, verify, and publish content.",
            "isPartOf": {
                "@id": "https://cryptocasinomedia.com/#website"
            },
            "about": {
                "@id": "https://cryptocasinomedia.com/#organization"
            }
        }
    ]),
    ('/advertise/', 'Advertise with CryptoCasinoMedia — B2B iGaming News', 'Reach operators, investors, and technology partners in the crypto and iGaming industry.', renderAdvertisePage(), [
        {
            "@type": "Product",
            "@id": "https://cryptocasinomedia.com/advertise/#product",
            "name": "B2B iGaming Sponsorship and Banner Advertising",
            "description": "Targeted B2B advertising campaigns reaching crypto casino decision makers, analysts, and operators.",
            "brand": {
                "@id": "https://cryptocasinomedia.com/#organization"
            },
            "offers": {
                "@type": "Offer",
                "name": "Sponsored Newsletter & Banner Campaign",
                "priceCurrency": "USD",
                "price": "999"
            }
        }
    ]),
    ('/submit/', 'Submit a Press Release — CryptoCasinoMedia', 'Reach key decision makers, operators, and analysts in the crypto and iGaming sector.', renderSubmitPage(), [
        {
            "@type": "Product",
            "@id": "https://cryptocasinomedia.com/submit/#product",
            "name": "Crypto & iGaming Press Release Distribution",
            "description": "Professional B2B press release distribution service reaching operators, investors, and regulators in the crypto casino space.",
            "brand": {
                "@id": "https://cryptocasinomedia.com/#organization"
            },
            "offers": {
                "@type": "AggregateOffer",
                "priceCurrency": "USD",
                "lowPrice": "0",
                "highPrice": "499",
                "offerCount": "3",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": "Basic Distribution",
                        "price": "0",
                        "priceCurrency": "USD",
                        "category": "Press Release Distribution"
                    },
                    {
                        "@type": "Offer",
                        "name": "Premium Distribution",
                        "price": "199",
                        "priceCurrency": "USD",
                        "category": "Press Release Distribution"
                    },
                    {
                        "@type": "Offer",
                        "name": "Enterprise Distribution",
                        "price": "499",
                        "priceCurrency": "USD",
                        "category": "Press Release Distribution"
                    }
                ]
            }
        }
    ]),
    ('/contact/', 'Contact Us — CryptoCasinoMedia', 'Reach our editorial team for inquiries, partnerships, or general questions.', renderContactPage(), [
        {
            "@type": "ContactPage",
            "@id": "https://cryptocasinomedia.com/contact/#webpage",
            "url": "https://cryptocasinomedia.com/contact/",
            "name": "Contact CryptoCasinoMedia",
            "description": "Get in touch with the editorial team at CryptoCasinoMedia.",
            "isPartOf": {
                "@id": "https://cryptocasinomedia.com/#website"
            },
            "about": {
                "@id": "https://cryptocasinomedia.com/#organization"
            }
        }
    ]),
    ('/privacy/', 'Privacy Policy — CryptoCasinoMedia', 'Learn how CryptoCasinoMedia collects, uses, and protects your personal and B2B contact data.', renderPrivacyPage(), [
        {
            "@type": "WebPage",
            "@id": "https://cryptocasinomedia.com/privacy/#webpage",
            "url": "https://cryptocasinomedia.com/privacy/",
            "name": "Privacy Policy — CryptoCasinoMedia",
            "description": "Learn how CryptoCasinoMedia collects, uses, and protects your personal and B2B contact data.",
            "isPartOf": {
                "@id": "https://cryptocasinomedia.com/#website"
            }
        }
    ]),
    ('/terms/', 'Terms of Service — CryptoCasinoMedia', 'Read the terms and conditions governing the use of the CryptoCasinoMedia news and submission portal.', renderTermsPage(), [
        {
            "@type": "WebPage",
            "@id": "https://cryptocasinomedia.com/terms/#webpage",
            "url": "https://cryptocasinomedia.com/terms/",
            "name": "Terms of Service — CryptoCasinoMedia",
            "description": "Read the terms and conditions governing the use of the CryptoCasinoMedia news and submission portal.",
            "isPartOf": {
                "@id": "https://cryptocasinomedia.com/#website"
            }
        }
    ]),
    ('/admin/', '⚡ Amplifier Agent Command Center — CryptoCasinoMedia', 'Automated search engine indexing acceleration, Answer Engine Optimization (AEO), and distribution network health auditing.', renderAdminPage(), []),
    ('/amplifier/', '⚡ Amplifier Agent Command Center — CryptoCasinoMedia', 'Automated search engine indexing acceleration, Answer Engine Optimization (AEO), and distribution network health auditing.', renderAdminPage(), [])
]

for path, title, description, body_content, custom_schemas in utility_pages:
    html = build_static_page(template_content, path, title, description, body_content, custom_schemas)
    
    folder_name = path.strip("/")
    out_dir = os.path.join(output_base_dir, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    pages_generated += 1

# 6.5 Render Author Profile Pages
authors_list = [
    {
        "slug": "marcus-vance",
        "name": "Marcus Vance",
        "role": "Lead iGaming Analyst",
        "bio": "Marcus Vance is a leading B2B iGaming analyst with over 8 years of experience covering sportsbooks, crypto casinos, and digital asset integration. Previously, he served as a market research analyst and has been cited in major interactive gaming publications globally. At CryptoCasinoMedia, he focuses on transaction analytics, platform liquidity, and predictive market volumes.",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=300",
        "email": "cryptocasinomedia@gmail.com"
    },
    {
        "slug": "sophia-chen",
        "name": "Sophia Chen",
        "role": "Regulatory Editor",
        "bio": "Sophia Chen is a regulatory editor specializing in international gambling compliance, sweepstakes laws, and digital asset frameworks. Formerly a compliance advisor for European gaming operators, she leads CryptoCasinoMedia's regulatory desk, auditing licensing transitions, AML policies, and the impact of the EU AI Act.",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=300",
        "email": "cryptocasinomedia@gmail.com"
    }
]

for author in authors_list:
    author_body = renderAuthorPage(author)
    author_title = f"{author['name']} Profile & Articles — CryptoCasinoMedia"
    author_desc = f"Read articles and iGaming industry analysis written by {author['name']} at CryptoCasinoMedia."
    
    author_schema = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "@id": f"https://cryptocasinomedia.com/authors/{author['slug']}/#webpage",
        "url": f"https://cryptocasinomedia.com/authors/{author['slug']}/",
        "name": author_title,
        "description": author_desc,
        "mainEntity": {
            "@type": "Person",
            "name": author['name'],
            "jobTitle": author['role'],
            "description": author['bio'],
            "image": author['avatar']
        }
    }
    
    html = build_static_page(template_content, f"/authors/{author['slug']}/", author_title, author_desc, author_body, [author_schema])
    
    out_dir = os.path.join(output_base_dir, "authors", author['slug'])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    pages_generated += 1

# 7. Overwrite index/index.html to pre-render the homepage statically
home_title = "CryptoCasinoMedia — B2B iGaming & Crypto Casino News"
home_description = "The trusted B2B source for crypto casino news, press releases, regulation updates, and iGaming industry analysis."
home_org_schema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://cryptocasinomedia.com/#organization",
    "name": "CryptoCasinoMedia",
    "url": "https://cryptocasinomedia.com",
    "logo": {
        "@type": "ImageObject",
        "url": "https://cryptocasinomedia.com/favicon.ico"
    },
    "sameAs": [
        "https://x.com/CryptoCasinoM"
    ]
}

home_website_schema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://cryptocasinomedia.com/#website",
    "name": "CryptoCasinoMedia",
    "url": "https://cryptocasinomedia.com",
    "publisher": {
        "@id": "https://cryptocasinomedia.com/#organization"
    },
    "potentialAction": {
        "@type": "SearchAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": "https://cryptocasinomedia.com/?search={search_term_string}"
        },
        "query-input": "required name=search_term_string"
    }
}

home_body = renderHomePage()
home_html = build_static_page(template_content, "/", home_title, home_description, home_body, [home_org_schema, home_website_schema])

with open(os.path.join(output_base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(home_html)
pages_generated += 1

print(f"SUCCESS: Pre-rendering complete! Generated {pages_generated} optimized static HTML pages under {output_base_dir}!")
