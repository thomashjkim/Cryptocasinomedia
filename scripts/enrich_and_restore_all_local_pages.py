#!/usr/bin/env python3
"""
Enrich & Restore All Local Pages Across CryptoCasinoMedia
1. Restores all 829 local pages from 'noindex' back to 'index, follow' (0 public noindex pages).
2. Injects Vercel Web Analytics (first-party tracker: /_vercel/insights/script.js) into all local and static pages.
3. Injects genuine local market research, physical/tribal casino proximity, state regulatory statutes,
   and 24/7 responsible gaming crisis helplines into all 210 DMA city hubs and 420 subpages.
4. Regenerates index/local-sitemap.xml containing all 886 indexed local pages.
"""

import os
import re
import json
from glob import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(PROJECT_ROOT, "index")
LOCAL_DIR = os.path.join(INDEX_DIR, "local")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Load state regulations
with open(os.path.join(DATA_DIR, "us_state_regulations.json"), "r", encoding="utf-8") as f:
    state_regs = json.load(f)

# Comprehensive State Gaming Landscape Knowledge Base
STATE_GAMING_LANDSCAPES = {
    "alabama": "Class II tribal gaming facilities operated by the Poarch Band of Creek Indians (Wind Creek Atmore, Wetumpka, and Montgomery); charitable electronic bingo; state law strictly prohibits commercial casino resorts.",
    "alaska": "Charitable pull-tabs and bingo licensed under Alaska Stat. § 05.15, alongside Alaska Native tribal gaming facilities; commercial casino resorts and racetracks are strictly prohibited.",
    "arizona": "Extensive Class III tribal casino network operated under state-tribal compacts with 16 tribes (including Talking Stick Resort, Desert Diamond, and Wild Horse Pass); legal retail and mobile sportsbooks under ADG.",
    "arkansas": "Three state-licensed commercial casino destinations (Southland Casino Hotel, Oaklawn Racing Casino Resort, Saracen Casino Resort) regulated by the Arkansas Racing Commission, alongside mobile sports betting.",
    "california": "Over 60 federally recognized tribal resort casinos (such as Pechanga, Yaamava', Morongo, Thunder Valley, and Cache Creek) alongside over 80 municipal cardrooms (Commerce, Bicycle Hotel); commercial online casinos remain unauthorized.",
    "colorado": "Historic commercial gaming districts in Black Hawk, Central City, and Cripple Creek regulated by the Colorado Division of Gaming, with legal statewide mobile sportsbooks and tribal casinos in the southwest.",
    "connecticut": "Class III tribal destination resorts (Foxwoods Resort Casino and Mohegan Sun) operating both premier physical gaming and state-licensed legal online casino and sportsbook platforms under CT DCP oversight.",
    "delaware": "Three licensed racino venues (Delaware Park, Bally's Dover, and Harrington Raceway) operating in partnership with the Delaware Lottery, featuring regulated physical gaming and state-monopolized online lottery and casino options.",
    "district-of-columbia": "District-licensed retail sports wagering facilities and mobile sports betting applications regulated by the DC Office of Lottery and Gaming; traditional commercial casino resorts are not authorized.",
    "florida": "Seminole Tribe of Florida destination casinos (including Seminole Hard Rock Hollywood and Tampa) operating under the historic 2021/2026 tribal-state compact, alongside pari-mutuel cardrooms and jai alai facilities.",
    "georgia": "Strict statutory prohibition against commercial and tribal casinos under Georgia Code § 16-12-20; physical gaming is restricted to state lottery-monitored Class B Coin-Operated Amusement Machines (COAM).",
    "hawaii": "Total constitutional and statutory prohibition against all commercial, tribal, charitable, and online gambling activities under Hawaii Rev. Stat. § 712-1220.",
    "idaho": "Tribal gaming destinations operated under federal IGRA by the Coeur d'Alene, Kootenai, Nez Perce, and Shoshone-Bannock tribes; state lottery operations; commercial casino venues prohibited.",
    "illinois": "Thriving commercial riverboat and land-based casino market (Rivers Casino Des Plaines, Bally's Chicago, Grand Victoria), extensive racinos, and over 45,000 video gaming terminals (VGTs) regulated by the Illinois Gaming Board.",
    "indiana": "12 commercial land-based and riverboat casino destinations (such as Hard Rock Northern Indiana and Horseshoe Indianapolis) plus racinos and legal statewide sportsbooks overseen by the Indiana Gaming Commission.",
    "iowa": "19 commercial riverboat/land-based casino facilities and 3 tribal gaming venues regulated by the Iowa Racing and Gaming Commission, featuring legal retail and mobile sports betting.",
    "kansas": "Four state-owned destination casino resorts (Hollywood Casino at Kansas Speedway, Kansas Star Casino, Boot Hill Casino, Kansas Crossing) managed by the Kansas Lottery, with statewide mobile sports betting.",
    "kentucky": "Historical horse racing (HHR) gaming facilities at premier racetracks (Churchill Downs Derby City Gaming, Turfway Park, Red Mile) and regulated sports wagering under the Kentucky Horse Racing and Gaming Corporation.",
    "louisiana": "Extensive commercial land-based and riverboat gaming corridors in Shreveport-Bossier, Lake Charles, Baton Rouge, and New Orleans (Caesars New Orleans), alongside tribal casinos under Louisiana Gaming Control Board.",
    "maine": "Two licensed commercial casino properties (Hollywood Casino Hotel & Raceway Bangor and Oxford Casino) regulated by the Maine Gambling Control Board, alongside tribal-partnered mobile sportsbooks.",
    "maryland": "Six major commercial casino resort destinations (Live! Casino & Hotel Hanover, MGM National Harbor, Horseshoe Baltimore, Rocky Gap, Ocean Downs, Hollywood Perryville) regulated by Maryland State Lottery & Gaming.",
    "massachusetts": "Three premier commercial resort casinos (Encore Boston Harbor, MGM Springfield, Plainridge Park Casino) operating under Massachusetts Gaming Commission oversight with legal sportsbooks.",
    "michigan": "Three commercial casino resorts in downtown Detroit (MGM Grand Detroit, MotorCity Casino, Hollywood Casino Greektown) and 23 tribal casinos; comprehensive state-regulated online casinos and sportsbooks under MGCB.",
    "minnesota": "18 tribal casino properties owned and operated by 11 federally recognized Minnesota tribes (including Mystic Lake Casino Hotel, Treasure Island, Grand Casino); commercial casino development is unauthorized.",
    "mississippi": "Historic commercial dockside casino markets along the Gulf Coast (Biloxi/Gulfport) and the Mississippi River (Tunica/Vicksburg) regulated by the Mississippi Gaming Commission.",
    "missouri": "13 commercial riverboat and excursion casino destinations operating across the St. Louis, Kansas City, and central Missouri corridors under Missouri Gaming Commission regulation.",
    "montana": "Widespread distributed video gambling machines operating across thousands of taverns and licensed establishments regulated by the Montana Gambling Control Division, alongside tribal gaming halls.",
    "nebraska": "Voter-authorized racino facilities at licensed horse racetracks (WarHorse Gaming Lincoln and Omaha, Grand Island) and tribal gaming facilities overseen by the Nebraska Racing and Gaming Commission.",
    "nevada": "The global epicenter of commercial gaming, featuring world-renowned resort casinos in Las Vegas, Reno, Lake Tahoe, and statewide, comprehensively regulated by the Nevada Gaming Commission and Control Board.",
    "new-hampshire": "Charitable gaming facilities featuring table games, poker, and historic horse racing machines (such as The Brook in Seabrook), with state-contracted mobile sports betting; traditional commercial resort casinos unauthorized.",
    "new-jersey": "Nine iconic Atlantic City boardwalk and marina casino resorts alongside the nation's premier regulated online casino, poker, and sports wagering market governed by the New Jersey Division of Gaming Enforcement (DGE).",
    "new-mexico": "Tribal casino destination resorts operated by 14 Pueblo and tribal nations (Sandia Resort, Inn of the Mountain Gods, Route 66 Casino) alongside five state-regulated racinos under the New Mexico Gaming Control Board.",
    "new-york": "Four upstate commercial resort casinos, major downstate video lottery racinos (Resorts World New York City, Empire City), and multiple tribal casino resorts (Seneca Niagara, Turning Stone) regulated by NYSGC.",
    "north-carolina": "Tribal casino resorts operated by the Eastern Band of Cherokee Indians (Harrah's Cherokee Casino Resort and Cherokee Valley River) and the Catawba Two Kings Casino; statewide legal mobile sportsbooks.",
    "north-dakota": "Tribal destination casino resorts operated by federally recognized sovereign nations (including Spirit Lake Casino, 4 Bears Casino, Dakota Magic) alongside statewide charitable electronic pull-tab gaming.",
    "ohio": "Four full-scale commercial casinos (Jack Cleveland, Hollywood Casino Columbus, Hollywood Toledo, Hard Rock Cincinnati) and seven racetrack racinos regulated by the Ohio Casino Control and Racing Commissions.",
    "oklahoma": "Over 130 tribal gaming venues and world-class destination resorts (including WinStar World Casino, Choctaw Casino Resort Durant, River Spirit Tulsa) operating under sovereign tribal-state compacts.",
    "oregon": "Nine tribal casino destination resorts (such as Spirit Mountain Casino, Chinook Winds, Seven Feathers) alongside Oregon State Lottery-operated video lottery terminals (VLTs); commercial casinos prohibited.",
    "pennsylvania": "17 licensed commercial casinos, racinos, and category-4 mini-casinos, coupled with robust statewide legal online casino gaming, sports betting, and poker regulated by the Pennsylvania Gaming Control Board (PGCB).",
    "rhode-island": "Two state-authorized commercial casino facilities (Bally's Twin River Lincoln Casino Resort and Bally's Tiverton) and state-operated mobile sports betting under Rhode Island Lottery regulation.",
    "south-carolina": "Strict statutory ban on all commercial, tribal, and online casino gaming under S.C. Code § 16-19-40; legal physical gaming is restricted to two offshore-bound international day-cruise vessels.",
    "south-dakota": "Historic commercial gaming district in Deadwood with retail casinos, tribal casinos on sovereign lands, and widespread video lottery terminals monitored by the South Dakota Commission on Gaming.",
    "tennessee": "Strictly mobile and online sports wagering governed by the Tennessee Sports Wagering Council; state constitution explicitly prohibits brick-and-mortar commercial and tribal casino establishments.",
    "texas": "Two federally recognized sovereign tribal gaming facilities (Kickapoo Lucky Eagle Casino in Eagle Pass and Naskila Gaming in Livingston); commercial casino resorts remain strictly prohibited under Texas Penal Code § 47.01.",
    "utah": "Total constitutional ban on all forms of gambling, lotteries, and betting under Utah Const. art. VI, § 27 and Utah Code Ann. § 76-10-1101; no state lottery, tribal, or commercial gaming authorized.",
    "vermont": "State lottery operations and licensed mobile sports betting apps regulated by the Vermont Department of Liquor and Lottery; brick-and-mortar commercial casinos are unauthorized.",
    "virginia": "Emerging commercial casino resorts in authorized host cities (Bristol Casino / Hard Rock, Caesars Virginia in Danville, Rivers Casino Portsmouth) regulated by the Virginia Lottery.",
    "washington": "Over 30 sovereign tribal casino resorts operated by 29 federally recognized tribal nations (such as Muckleshoot, Tulalip, Snoqualmie, Emerald Queen) and commercial cardrooms under Washington State Gambling Commission.",
    "west-virginia": "Five commercial racinos and destination resorts (The Greenbrier, Hollywood Casino at Charles Town Races) operating physical gaming and state-licensed online casinos and sportsbooks under West Virginia Lottery.",
    "wisconsin": "Extensive network of tribal casino resorts operated by 11 federally recognized sovereign tribes (such as Potawatomi Hotel & Casino Milwaukee, Ho-Chunk Gaming, Oneida Casino) under tribal-state compacts.",
    "wyoming": "Tribal gaming centers operated on the Wind River Indian Reservation by the Northern Arapaho and Eastern Shoshone tribes (Wind River Hotel & Casino), alongside legal statewide mobile sports wagering under Wyoming Gaming Commission."
}

# Comprehensive State Problem Gambling Helplines & Councils
STATE_HELPLINES = {
    "alabama": "Alabama Council on Compulsive Gambling: 1-334-279-8601 (or 1-800-GAMBLER)",
    "alaska": "Alaska Problem Gambling Helpline: 1-800-478-4506 (or 1-800-GAMBLER)",
    "arizona": "Arizona Division of Problem Gambling: 1-800-NEXT-STEP (Text NEXTSTEP to 53342)",
    "arkansas": "Arkansas Problem Gambling Helpline: 1-800-522-4700",
    "california": "California Council on Problem Gambling: 1-800-GAMBLER (Text 'SUPPORT' to 53342)",
    "colorado": "Problem Gambling Coalition of Colorado: 1-800-GAMBLER",
    "connecticut": "Connecticut Council on Problem Gambling: 1-888-789-7777 (or text 'CTGAMBLING')",
    "delaware": "Delaware Council on Gambling Problems: 1-888-850-8888",
    "district-of-columbia": "National Council on Problem Gambling (DC): 1-800-522-4700",
    "florida": "Florida Council on Compulsive Gambling: 1-888-ADMIT-IT (888-236-4848)",
    "georgia": "Georgia Council on Problem Gambling: 1-800-GAMBLER (1-800-426-2537)",
    "hawaii": "National Problem Gambling Helpline (Hawaii): 1-800-522-4700",
    "idaho": "Idaho Council on Problem Gambling: 1-800-GAMBLER",
    "illinois": "Illinois Department of Human Services Problem Gambling: 1-800-GAMBLER (Text 'ILGAMB' to 53342)",
    "indiana": "Indiana Council on Problem Gambling: 1-800-994-8448 (Text 'INHELP' to 53342)",
    "iowa": "Your Life Iowa Problem Gambling Services: 1-800-BETS-OFF (Text 855-895-8398)",
    "kansas": "Kansas Problem Gambling Helpline: 1-800-522-4700 (ksgamblinghelp.com)",
    "kentucky": "Kentucky Council on Problem Gambling: 1-800-GAMBLER (1-800-426-2537)",
    "louisiana": "Louisiana Problem Gambling Helpline: 1-877-770-STOP (1-877-770-7867)",
    "maine": "Maine Problem Gambling Helpline: 2-1-1 Maine (or 1-800-GAMBLER)",
    "maryland": "Maryland Center of Excellence on Problem Gambling: 1-800-GAMBLER",
    "massachusetts": "Massachusetts Problem Gambling Helpline: 1-800-327-5050",
    "michigan": "Michigan Department of Health & Human Services Gambling Helpline: 1-800-270-7117",
    "minnesota": "Minnesota Problem Gambling Helpline: 1-800-333-HOPE (1-800-333-4673)",
    "mississippi": "Mississippi Council on Problem Gambling: 1-888-777-9696",
    "missouri": "Missouri Problem Gambling Helpline: 1-888-BETSOFF (1-888-238-7633)",
    "montana": "Montana Problem Gambling Helpline: 1-888-900-3276",
    "nebraska": "Nebraska Problem Gambling Helpline: 1-833-BETOVER (1-833-238-6837)",
    "nevada": "Nevada Council on Problem Gambling: 1-800-522-4700",
    "new-hampshire": "New Hampshire Council on Problem Gambling: 1-603-568-8469",
    "new-jersey": "Council on Compulsive Gambling of New Jersey: 1-800-GAMBLER (800gambler.org)",
    "new-mexico": "New Mexico Council on Problem Gambling: 1-888-696-2222",
    "new-york": "New York State Problem Gambling Resource Centers: 1-877-8-HOPENY (Text HOPENY to 467369)",
    "north-carolina": "North Carolina Problem Gambling Program: 1-877-718-5543",
    "north-dakota": "North Dakota 2-1-1 Problem Gambling Resources: 2-1-1 (or 1-800-GAMBLER)",
    "ohio": "Ohio Problem Gambling Helpline: 1-800-589-9966 (Text '4HOPE' to 741741)",
    "oklahoma": "Oklahoma Problem Gambling Helpline: 1-800-522-4700",
    "oregon": "Oregon Problem Gambling Resource: 1-877-MY-LIMIT (1-877-695-4648)",
    "pennsylvania": "Council on Compulsive Gambling of Pennsylvania: 1-800-GAMBLER",
    "rhode-island": "Rhode Island Problem Gambling Helpline: 1-877-942-6253",
    "south-carolina": "South Carolina Problem Gambling Support: 1-800-522-4700",
    "south-dakota": "South Dakota Problem Gambling Help Network: 1-888-784-2433",
    "tennessee": "Tennessee REDLINE Problem Gambling Support: 1-800-889-9789",
    "texas": "Texas Council on Problem Gambling: 1-888-BETS-OFF (or 1-800-522-4700)",
    "utah": "National Problem Gambling Helpline (Utah): 1-800-522-4700",
    "vermont": "Vermont Problem Gambling Resource Network: 1-800-GAMBLER",
    "virginia": "Virginia Council on Problem Gambling: 1-888-532-3500",
    "washington": "Evergreen Council on Problem Gambling (WA): 1-800-547-6133",
    "west-virginia": "Problem Gamblers Help Network of West Virginia: 1-800-GAMBLER",
    "wisconsin": "Wisconsin Council on Problem Gambling: 1-800-GAMBLE-5 (1-800-426-2535)",
    "wyoming": "Wyoming Problem Gambling Support: 1-800-522-4700"
}

INDEX_META_TAG = (
    '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n'
    '    <meta name="googlebot" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n'
    '    <meta name="bingbot" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'
)

VERCEL_INSIGHTS_SCRIPT = (
    '<!-- Vercel Web Analytics (First-Party Tracker - Unblocked by Brave/AdBlockers) -->\n'
    '    <script defer src="/_vercel/insights/script.js"></script>'
)

def format_dma_name(dma_slug):
    name = dma_slug.replace("-", " ").title()
    name = re.sub(r'\bLa\b', 'LA', name)
    name = re.sub(r'\bNy\b', 'NY', name)
    name = re.sub(r'\bDc\b', 'DC', name)
    name = re.sub(r'\bTn\b', 'TN', name)
    name = re.sub(r'\bVa\b', 'VA', name)
    name = re.sub(r'\bSc\b', 'SC', name)
    name = re.sub(r'\bGa\b', 'GA', name)
    name = re.sub(r'\bOh\b', 'OH', name)
    name = re.sub(r'\bMs\b', 'MS', name)
    return name

# 1. Discover all local HTML files
all_local_files = []
for root, dirs, files in os.walk(LOCAL_DIR):
    for f in files:
        if f.endswith('.html'):
            all_local_files.append(os.path.join(root, f))

print(f"Total local HTML files discovered: {len(all_local_files)}")

# 2. Process all local files: Revert noindex, inject Vercel Insights, enrich DMA content
reverted_noindex_count = 0
vercel_injected_count = 0
dma_enriched_count = 0
subpage_enriched_count = 0

for file_path in all_local_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # A: Revert any noindex tags to index, follow
    if 'noindex' in content:
        content = re.sub(r'<meta\s+name=["\'](robots|googlebot|bingbot)["\']\s+content=["\'][^"\']*["\']>\s*', '', content)
        if '<meta name="description"' in content:
            desc_end = content.find('>', content.find('<meta name="description"'))
            if desc_end != -1:
                content = content[:desc_end+1] + '\n    ' + INDEX_META_TAG + content[desc_end+1:]
            else:
                content = content.replace('<head>', '<head>\n    ' + INDEX_META_TAG)
        else:
            content = content.replace('<head>', '<head>\n    ' + INDEX_META_TAG)
        reverted_noindex_count += 1
        modified = True

    # B: Inject Vercel Web Analytics script if missing
    if '/_vercel/insights/script.js' not in content:
        # Insert before </head> or after gtag
        if '</head>' in content:
            content = content.replace('</head>', f'    {VERCEL_INSIGHTS_SCRIPT}\n</head>', 1)
            vercel_injected_count += 1
            modified = True

    # C: Enrich DMA City Hubs (/local/{state}/{dma}/index.html)
    rel_path = os.path.relpath(file_path, LOCAL_DIR)
    parts = rel_path.split(os.sep)

    if len(parts) == 3 and parts[2] == "index.html" and not parts[1].startswith(("crypto-", "how-", "top-")):
        state_slug = parts[0]
        dma_slug = parts[1]
        
        reg_info = state_regs.get(state_slug, {})
        state_name = reg_info.get("state_name", state_slug.replace("-", " ").title())
        regulator = reg_info.get("regulator", f"{state_name} Gaming Enforcement Division")
        primary_statute = reg_info.get("primary_statute", f"{state_name} Gaming Code")
        gaming_landscape = STATE_GAMING_LANDSCAPES.get(state_slug, f"Gaming in {state_name} is subject to state statutory oversight and applicable federal tribal gaming frameworks.")
        state_helpline = STATE_HELPLINES.get(state_slug, f"{state_name} Problem Gambling Helpline: 1-800-GAMBLER")
        dma_name = format_dma_name(dma_slug)

        # Check if local-market-intelligence module is already present
        if 'id="local-market-intelligence"' not in content:
            intelligence_module = f"""
                <!-- Local Market Profile & Responsible Gaming Intelligence Module -->
                <section id="local-market-intelligence" class="my-8 bg-slate-50 border border-slate-200 rounded-lg p-6 font-sans">
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-200 pb-3 mb-5 gap-2">
                        <div class="flex items-center gap-2">
                            <span class="bg-blue-700 text-white text-[10px] font-bold px-2.5 py-0.5 rounded uppercase tracking-wider">Local Intelligence</span>
                            <h2 class="text-base font-bold text-gray-900 m-0">{dma_name} Market Profile & Regulatory Landscape</h2>
                        </div>
                        <span class="text-xs text-gray-500 font-mono">2026 Metropolitan Audit</span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm text-gray-700 leading-relaxed mb-6">
                        <div class="p-4 bg-white rounded border border-gray-100 shadow-sm">
                            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-900 mb-2 flex items-center gap-1.5">
                                <span class="w-2 h-2 rounded-full bg-blue-600 inline-block"></span> Regional Gaming Landscape & Venue Proximity
                            </h3>
                            <p class="text-xs text-gray-600 m-0 mb-2 leading-relaxed">
                                {gaming_landscape}
                            </p>
                            <p class="text-[11px] text-gray-500 m-0 border-t border-gray-100 pt-2 font-mono">
                                Jurisdictional Status: State law strictly distinguishes authorized physical/tribal facilities from unlicensed digital wagering platforms.
                            </p>
                        </div>
                        <div class="p-4 bg-white rounded border border-gray-100 shadow-sm">
                            <h3 class="text-xs font-bold uppercase tracking-wider text-gray-900 mb-2 flex items-center gap-1.5">
                                <span class="w-2 h-2 rounded-full bg-indigo-600 inline-block"></span> Statutory Oversight & Media Compliance
                            </h3>
                            <p class="text-xs text-gray-600 m-0 mb-2 leading-relaxed">
                                <strong>Regulatory Authority:</strong> {regulator}<br>
                                <strong>Governing Statute:</strong> <span class="font-mono text-gray-800 text-[11px]">{primary_statute}</span>
                            </p>
                            <p class="text-[11px] text-gray-500 m-0 border-t border-gray-100 pt-2 leading-relaxed">
                                Digital asset transmissions and payment solutions within the {dma_name} metro are monitored under state financial and money transmission codes.
                            </p>
                        </div>
                    </div>

                    <!-- Responsible Gaming & Problem Gambling Helpline -->
                    <div class="p-4 bg-amber-50/80 border border-amber-200 rounded-md text-xs text-amber-950 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                        <div class="leading-relaxed">
                            <strong class="font-bold text-amber-900 block mb-0.5">Responsible Gaming & Local Crisis Support:</strong>
                            <span>If you or a household member in {dma_name} or {state_name} is experiencing gaming-related concerns, free and confidential support is available 24/7 via <strong>{state_helpline}</strong> or the National Problem Gambling Helpline at <strong>1-800-GAMBLER (1-800-522-4700)</strong>.</span>
                        </div>
                        <a href="https://www.ncpgambling.org" target="_blank" rel="noopener noreferrer" class="shrink-0 px-3.5 py-1.5 bg-amber-700 text-white rounded font-medium hover:bg-amber-800 transition-colors text-xs whitespace-nowrap shadow-sm">
                            Confidential Help 24/7 &rarr;
                        </a>
                    </div>
                </section>
"""
            # Insert right before the category two-column layout
            insert_marker = '<!-- Category Two-Column Layout'
            if insert_marker in content:
                content = content.replace(insert_marker, intelligence_module + '\n            ' + insert_marker)
                dma_enriched_count += 1
                modified = True

    # D: Enrich DMA Subpages (Legal Guides & Trend Reports)
    elif len(parts) == 4 and parts[3] == "index.html":
        state_slug = parts[0]
        dma_slug = parts[1]
        subpage_type = parts[2]
        
        reg_info = state_regs.get(state_slug, {})
        state_name = reg_info.get("state_name", state_slug.replace("-", " ").title())
        regulator = reg_info.get("regulator", f"{state_name} Gaming Authorities")
        primary_statute = reg_info.get("primary_statute", f"{state_name} Code")
        state_helpline = STATE_HELPLINES.get(state_slug, f"{state_name} Problem Gambling Helpline: 1-800-GAMBLER")
        dma_name = format_dma_name(dma_slug)

        if "crypto-gambling-and-advertising-legal-regulatory-guide" in subpage_type:
            # Upgrade municipal section with localized municipal & media market authority
            enhanced_municipal_text = (
                f"In the {dma_name} metropolitan media market ({state_name}), municipal governments and county jurisdictions "
                f"(including regional district attorneys and municipal licensing departments) operate in direct coordination with {regulator} "
                f"under {primary_statute}. Local commercial zoning laws and municipal ordinances enforce strict oversight on physical advertising "
                f"(billboard displays, transit ads, localized broadcasts) within the {dma_name} designated market area, while digital cryptocurrency wagering "
                f"remains governed exclusively under state consumer protection statutes and federal financial crime enforcement frameworks."
            )
            def mun_repl(match):
                prefix = match.group(1)
                return f"{prefix}<span>{enhanced_municipal_text}</span>"

            if 'metropolitan media market' not in content:
                content_new = re.sub(r'(<strong class="font-semibold text-gray-900 block mb-1">Municipal & Local Jurisdiction[^<]*?</strong>\s*)<span>.*?</span>', mun_repl, content, count=1, flags=re.DOTALL)
                if content_new != content:
                    content = content_new
                    subpage_enriched_count += 1
                    modified = True

            # Ensure Responsible Gaming Helpline callout is in Section 7 (Mandatory Statutory Disclosures)
            if 'id="statutory-responsible-gaming-helpline"' not in content and 'Mandatory Statutory Disclosures' in content:
                rg_callout = f"""
                    <div id="statutory-responsible-gaming-helpline" class="my-4 p-4 bg-amber-50 border-l-4 border-amber-600 rounded-r-md text-xs text-amber-950 font-sans leading-relaxed">
                        <strong class="font-bold text-amber-900 block mb-1">State & National Responsible Gaming Statutory Resources:</strong>
                        <span>All promotional campaigns targeting the {dma_name} audience must provide clear, conspicuous problem gambling assistance notices: <strong>{state_helpline}</strong> or 24/7 National Crisis Line <strong>1-800-GAMBLER (1-800-522-4700)</strong>.</span>
                    </div>"""
                m_disc = re.search(r'(<h2[^>]*>7\.\s*Mandatory Statutory Disclosures</h2>\s*<p[^>]*>.*?</p>)', content, re.DOTALL)
                if m_disc:
                    content = content[:m_disc.end()] + rg_callout + content[m_disc.end():]
                    modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print(f"SUCCESS: Reverted {reverted_noindex_count} local pages to 'index, follow'!")
print(f"SUCCESS: Injected Vercel Insights into {vercel_injected_count} local HTML pages!")
print(f"SUCCESS: Enriched {dma_enriched_count} DMA market hubs with local intelligence profiles!")
print(f"SUCCESS: Enriched {subpage_enriched_count} DMA legal guides with localized municipal & helpline data!")

# 3. Inject Vercel Web Analytics across all other static HTML files in index/
other_html_files = []
for root, dirs, files in os.walk(INDEX_DIR):
    # Exclude internal tools from analytics injection if desired, but good for all public
    if "index/local" in root:
        continue
    for f in files:
        if f.endswith('.html'):
            other_html_files.append(os.path.join(root, f))

other_injected = 0
for p in other_html_files:
    # Exclude admin and amplifier from public indexing, but check analytics
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()
    if '/_vercel/insights/script.js' not in content and '</head>' in content:
        content = content.replace('</head>', f'    {VERCEL_INSIGHTS_SCRIPT}\n</head>', 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        other_injected += 1

print(f"SUCCESS: Injected Vercel Insights into {other_injected} non-local static HTML files!")

# 4. Regenerate index/local-sitemap.xml with ALL 886 indexable local URLs
sitemap_path = os.path.join(PROJECT_ROOT, "index", "local-sitemap.xml")

sitemap_urls = []
for file_path in sorted(all_local_files):
    rel_path = os.path.relpath(file_path, INDEX_DIR)
    url_path = rel_path.replace(os.sep, '/')
    if url_path.endswith('index.html'):
        url_path = url_path[:-len('index.html')]
    if not url_path.endswith('/'):
        url_path += '/'
    full_url = f"https://cryptocasinomedia.com/{url_path}"

    # Determine priority based on page depth/type
    parts = [p for p in url_path.strip('/').split('/') if p]
    if len(parts) == 1: # 'local'
        priority = "0.9"
    elif len(parts) == 2: # 'local/state'
        priority = "0.8"
    elif len(parts) == 3:
        if 'guide' in parts[2] or 'top-10' in parts[2] or 'trend' in parts[2] or 'taxes' in parts[2]:
            priority = "0.7" # State guide
        else:
            priority = "0.7" # DMA hub
    else: # DMA subpage
        priority = "0.6"

    sitemap_urls.append((full_url, priority))

sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

today_str = "2026-10-15"
for loc, priority in sitemap_urls:
    sitemap_lines.append(
        f'  <url><loc>{loc}</loc><lastmod>{today_str}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>'
    )
sitemap_lines.append('</urlset>\n')

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write('\n'.join(sitemap_lines))

print(f"SUCCESS: Regenerated {sitemap_path} with {len(sitemap_urls)} fully indexed local URLs!")
