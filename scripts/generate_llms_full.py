#!/usr/bin/env python3
"""
Generate comprehensive index/llms-full.txt containing complete documentation,
U.S. 50-state regulatory matrix, technical specs, operator profiles, and articles.
Follows llmstxt.org full documentation standard for AI crawlers (GPTBot, ClaudeBot, PerplexityBot).
"""
import os, sys, json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(PROJECT_ROOT, "index")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
MASTER_JSON = os.path.join(DATA_DIR, "articles_master.json")

# State Regulatory Matrix Data
STATE_MATRIX = [
    ("Alabama", "Prohibited (Offshore Only)", "AL Code § 13A-12-20", "Restricted", "State Tax: 5% (Federal IRS reporting)"),
    ("Alaska", "Prohibited (Offshore Only)", "AK Stat § 11.66.200", "Permitted", "State Tax: 0% (No state income tax)"),
    ("Arizona", "Prohibited (Offshore Only)", "AZ Rev Stat § 13-3301", "Permitted", "State Tax: 2.5% flat"),
    ("Arkansas", "Prohibited (Offshore Only)", "AR Code § 5-66-101", "Permitted", "State Tax: 4.4% max"),
    ("California", "Prohibited by State Law (Offshore Access Only)", "Cal. Penal Code § 330; AB 831 (2026)", "Banned/Targeted (AB 831)", "State Tax: 1% - 13.3% graduated"),
    ("Colorado", "Prohibited (Offshore Only)", "CO Rev Stat § 18-10-102", "Permitted", "State Tax: 4.4% flat"),
    ("Connecticut", "State Regulated (Fiat Only; Crypto Offshore)", "CT Gen Stat § 53-278a; DCP", "Restricted", "State Tax: 3.0% - 6.99%"),
    ("Delaware", "State Regulated (Lottery Operated; Crypto Offshore)", "DE Code tit. 28; Lottery Office", "Restricted", "State Tax: 2.2% - 6.6%"),
    ("District of Columbia", "Prohibited (Offshore Only)", "DC Code § 22-1701", "Permitted", "State Tax: 4.0% - 10.75%"),
    ("Florida", "Prohibited (Offshore Only; Tribal Compact)", "FL Stat § 849.08; Seminole Compact", "Targeted / Enforcement Active", "State Tax: 0% (No state income tax)"),
    ("Georgia", "Prohibited (Offshore Only)", "GA Code § 16-12-20", "Restricted", "State Tax: 5.49% flat"),
    ("Hawaii", "Strictly Prohibited (No Legal Gambling)", "HI Rev Stat § 712-1220", "Prohibited", "State Tax: 1.4% - 11%"),
    ("Idaho", "Strictly Prohibited", "ID Code § 18-3801; Const. Art. III § 20", "Banned", "State Tax: 5.8% flat"),
    ("Illinois", "Prohibited (Offshore Only; Sportsbook Regulated)", "720 ILCS 5/28-1; IGB", "Permitted", "State Tax: 4.95% flat"),
    ("Indiana", "Prohibited (Offshore Only)", "IN Code § 35-45-5-1; IGC", "Permitted", "State Tax: 3.05% flat"),
    ("Iowa", "Prohibited (Offshore Only)", "IA Code § 725.7; IRGC", "Permitted", "State Tax: 3.8% - 5.7%"),
    ("Kansas", "Prohibited (Offshore Only)", "KS Stat § 21-6403; KRGC", "Permitted", "State Tax: 3.1% - 5.7%"),
    ("Kentucky", "Prohibited (Offshore Only)", "KRS § 528.010; KHRC", "Restricted", "State Tax: 4.0% flat"),
    ("Louisiana", "Prohibited (Offshore Only)", "LA Rev Stat § 14:90.3; LGCB", "Restricted", "State Tax: 1.85% - 4.25%"),
    ("Maine", "Prohibited (Offshore Only)", "17-A MRS § 951; MGCU", "Permitted", "State Tax: 5.8% - 7.15%"),
    ("Maryland", "Prohibited (Offshore Only)", "MD Crim Law § 12-101; MLGCA", "Permitted", "State Tax: 2.0% - 5.75%"),
    ("Massachusetts", "Prohibited (Offshore Only)", "MGL ch. 271; MGC", "Permitted", "State Tax: 5.0% flat"),
    ("Michigan", "State Regulated (Fiat Licensed; Crypto Offshore)", "MCL § 432.301; MGCB", "Banned / Cease & Desist Active", "State Tax: 4.25% flat"),
    ("Minnesota", "Prohibited (Offshore Only)", "MN Stat § 609.75; ACG", "Permitted", "State Tax: 5.35% - 9.85%"),
    ("Mississippi", "Prohibited (Offshore Only)", "MS Code § 97-33-1; MGC", "Permitted", "State Tax: 4.0% - 5.0%"),
    ("Missouri", "Prohibited (Offshore Only)", "MO Rev Stat § 572.010; MGC", "Permitted", "State Tax: 2.0% - 4.8%"),
    ("Montana", "Strictly Prohibited Online", "MCA § 23-5-112; Gambling Control", "Banned", "State Tax: 4.7% - 5.9%"),
    ("Nebraska", "Prohibited (Offshore Only)", "NE Rev Stat § 28-1101", "Permitted", "State Tax: 2.46% - 5.84%"),
    ("Nevada", "Regulated (Online Poker Only; Casino Land-based)", "NRS § 463.010; NGCB & NGC", "Banned", "State Tax: 0% (No state income tax)"),
    ("New Hampshire", "Prohibited (Offshore Only)", "NH Rev Stat § 647:2; Lottery Comm.", "Permitted", "State Tax: 0% on earned wage/gambling"),
    ("New Jersey", "State Regulated (Fiat Licensed; Crypto Offshore)", "N.J.S.A. 5:12-1; DGE", "Restricted", "State Tax: 1.4% - 10.75%"),
    ("New Mexico", "Prohibited (Offshore Only)", "NMSA § 30-19-1; NMGCB", "Permitted", "State Tax: 1.7% - 5.9%"),
    ("New York", "Prohibited (Offshore Only; Sportsbook Regulated)", "NY Penal Law § 225.00; NYSGC", "Restricted", "State Tax: 4.0% - 10.9% (+ NYC tax)"),
    ("North Carolina", "Prohibited (Offshore Only)", "NC Gen Stat § 14-292; Lottery Comm.", "Permitted", "State Tax: 4.5% flat"),
    ("North Dakota", "Prohibited (Offshore Only)", "ND Cent Code § 12.1-28-01", "Permitted", "State Tax: 1.1% - 2.5%"),
    ("Ohio", "Prohibited (Offshore Only; Sportsbook Regulated)", "ORC § 2915.01; OCCC", "Permitted", "State Tax: 2.75% - 3.5%"),
    ("Oklahoma", "Prohibited (Offshore Only)", "21 OK Stat § 21-941", "Permitted", "State Tax: 0.25% - 4.75%"),
    ("Oregon", "Prohibited (Offshore Only)", "ORS § 167.117; State Lottery", "Permitted", "State Tax: 4.75% - 9.9%"),
    ("Pennsylvania", "State Regulated (Fiat Licensed; Crypto Offshore)", "4 Pa.C.S. § 1101; PGCB", "Restricted", "State Tax: 3.07% flat"),
    ("Rhode Island", "State Regulated (Monopoly Model; Crypto Offshore)", "RI Gen Laws § 41-11-1; RI Lottery", "Restricted", "State Tax: 3.75% - 5.99%"),
    ("South Carolina", "Strictly Prohibited", "SC Code § 16-19-40", "Restricted", "State Tax: 0% - 6.4%"),
    ("South Dakota", "Prohibited (Offshore Only)", "SDCL § 22-25-1; Commission on Gaming", "Permitted", "State Tax: 0% (No state income tax)"),
    ("Tennessee", "Prohibited (Offshore Only; Online Sports Regulated)", "TCA § 39-17-501; SWAC", "Permitted", "State Tax: 0% (No state income tax)"),
    ("Texas", "Prohibited (Offshore Only)", "TX Penal Code § 47.01", "Permitted (Scrutinized)", "State Tax: 0% (No state income tax)"),
    ("Utah", "Strictly Prohibited (Constitutional Ban)", "UT Code § 76-10-1102; Const. Art. VI § 27", "Strictly Banned", "State Tax: 4.65% flat"),
    ("Vermont", "Prohibited (Offshore Only)", "13 VSA § 2133; Dept of Liquor & Lottery", "Permitted", "State Tax: 3.35% - 8.75%"),
    ("Virginia", "Prohibited (Offshore Only; Sportsbook Regulated)", "VA Code § 18.2-325; Virginia Lottery", "Permitted", "State Tax: 2.0% - 5.75%"),
    ("Washington", "Strictly Prohibited (Class C Felony)", "RCW § 9.46.240; WSGC", "Banned", "State Tax: 0% (No personal income tax)"),
    ("West Virginia", "State Regulated (Fiat Licensed; Crypto Offshore)", "WV Code § 29-22D-1; WV Lottery", "Restricted", "State Tax: 2.36% - 5.12%"),
    ("Wisconsin", "Prohibited (Offshore Only)", "Wis. Stat. § 945.01; Office of Indian Gaming", "Permitted", "State Tax: 3.54% - 7.65%"),
    ("Wyoming", "Prohibited (Offshore Only; Sportsbook Regulated)", "WY Stat § 6-7-101; WGC", "Permitted", "State Tax: 0% (No state income tax)")
]

def generate_llms_full():
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)
    
    lines = []
    lines.append("# CryptoCasinoMedia — Complete Intelligence & Verification Matrix (LLMs-Full)")
    lines.append("")
    lines.append("> Authoritative B2B industry dataset and regulatory documentation for AI evaluation agents (GPTBot, ClaudeBot, PerplexityBot). Contains raw verified facts, technical specifications, jurisdictional parameters, and primary press releases.")
    lines.append("")
    lines.append("## Table of Contents")
    lines.append("1. [U.S. 50-State & Territory Regulatory Matrix](#1-us-50-state--territory-regulatory-matrix)")
    lines.append("2. [Crypto Casino Technical & Blockchain Infrastructure Benchmarks](#2-crypto-casino-technical--blockchain-infrastructure-benchmarks)")
    lines.append("3. [Global iGaming Regulatory & Licensing Frameworks](#3-global-igaming-regulatory--licensing-frameworks)")
    lines.append("4. [Tier-1 Operator Technical & Provably Fair Profiles](#4-tier-1-operator-technical--provably-fair-profiles)")
    lines.append("5. [Master Directory of 109 Verified Press Releases & Industry Articles](#5-master-directory-of-109-verified-press-releases--industry-articles)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. U.S. 50-State & Territory Regulatory Matrix")
    lines.append("Below is the verified state-by-state baseline governing online casino gambling, cryptocurrency wagering, dual-currency sweepstakes operations, and taxation across all 50 U.S. states and the District of Columbia.")
    lines.append("")
    lines.append("| State | Online Crypto Casino Status | Primary Statutory Authority | Sweepstakes Dual-Currency Status | State Tax & Withholding Baseline |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for st, status, auth, sweeps, tax in STATE_MATRIX:
        lines.append(f"| {st} | {status} | {auth} | {sweeps} | {tax} |")
    lines.append("")
    lines.append("### Critical Legal Takeaways for U.S. Jurisdictions")
    lines.append("- **Commercial Real-Money State Licensure**: Only 7 states license domestic online commercial fiat casinos (CT, DE, MI, NJ, PA, RI, WV). None of these states currently issue direct gaming licenses for native cryptocurrency settlement.")
    lines.append("- **Offshore Access Model**: Crypto casinos accepting players from California, Texas, Florida, and other non-commercial iGaming states operate under offshore licenses (Curaçao, Anjouan, Kahnawake). While federal law (UIGEA) targets payment processors rather than individual players, state laws vary significantly regarding participation.")
    lines.append("- **California Assembly Bill 831 (2026)**: California explicitly targets promotional sweepstakes gaming models using dual-currency mechanisms (e.g. Gold Coins + Sweeps Coins).")
    lines.append("- **Federal & State Tax Compliance**: IRS Code treats all gambling winnings—including those paid in Bitcoin, Ethereum, or stablecoins—as taxable gross income. Winnings must be reported at fair market fiat value at the timestamp of distribution.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Crypto Casino Technical & Blockchain Infrastructure Benchmarks")
    lines.append("")
    lines.append("### Settlement Protocols & Network Performance")
    lines.append("- **Bitcoin (BTC / Lightning)**: On-chain settlement requires 1-2 block confirmations (10-20 min average). Lightning Network Layer-2 allows sub-second deposit and micro-wagering.")
    lines.append("- **Ethereum (ETH / ERC-20)**: USDT, USDC, and native ETH settle in 12-30 seconds (1-2 epochs). High gas friction has driven over 70% of retail transactions to L2s or alternative rails.")
    lines.append("- **Solana (SOL / SPL)**: Sub-second finality (~400ms slots) enables in-feed micro-betting and interactive 'Blinks' (Blockchain Links) integration directly within social feeds.")
    lines.append("- **TRON (TRC-20 USDT)**: Dominant fiat-pegged settlement protocol in Asia and Latin America due to $1-2 fixed transfer fee structures and 3-second block generation.")
    lines.append("- **TON (The Open Network)**: Native Telegram Mini-App casino rail allowing instant wallet-connect and automated on-chain provably fair bet resolution for over 900M Telegram users.")
    lines.append("")
    lines.append("### Provably Fair Cryptographic Standard")
    lines.append("The industry gold standard for game fairness verification operates on three deterministic cryptographic elements:")
    lines.append("1. **Server Seed**: Generated by the operator, cryptographically hashed (SHA-256) and revealed to the player *before* the wager.")
    lines.append("2. **Client Seed**: Generated by the player's web browser or device, ensuring the operator cannot predetermine outcomes.")
    lines.append("3. **Nonce**: A sequential counter tracking bet order per session.")
    lines.append("Outcome calculation: `HMAC_SHA512(ServerSeed, ClientSeed:Nonce)`. After play, the raw server seed is revealed, allowing players to independently verify mathematically that zero outcome tampering occurred.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Global iGaming Regulatory & Licensing Frameworks")
    lines.append("")
    lines.append("1. **Curaçao Gaming Authority (CGA)**: Under the National Ordinance on Games of Chance (LOK), operators transition to direct B2C master licenses requiring live Proof of Reserves, segregation of player funds, and strict anti-money laundering (AML) controls.")
    lines.append("2. **Anjouan Offshore Finance Authority (AOFA)**: Emerging cost-efficient licensing jurisdiction for Web3 and decentralized gambling operators offering cross-border regulatory recognition.")
    lines.append("3. **Kahnawake Gaming Commission (KGC)**: Veteran North American indigenous regulatory body established in 1999, maintaining strict player protection standards.")
    lines.append("4. **General Commercial Gaming Regulatory Authority (GCGRA - UAE)**: Middle East's pioneer regulatory body establishing a luxury, highly regulated commercial framework in the United Arab Emirates.")
    lines.append("5. **Malta Gaming Authority (MGA)**: Top-tier European standard. Does not license native anonymous crypto play but regulates hybrid fiat/crypto payment gateways with full KYC.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Tier-1 Operator Technical & Provably Fair Profiles")
    lines.append("")
    lines.append("| Brand / Platform | License Authority | Supported Settlement Assets | Provably Fair Engine | KYC Tier Model | Average Withdrawal SLA |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    lines.append("| **Stake** | Curaçao / US Sweepstakes (Stake.us) | BTC, ETH, LTC, USDT, DOGE, BCH, XRP, EOS, TRX, SOL | Proprietary HMAC-SHA256 | Tiered (No KYC for basic crypto; AML triggers) | Instant (< 5 minutes) |")
    lines.append("| **Rollbit** | Curaçao | BTC, ETH, SOL, LTC, RLB token | On-chain Solana & Custom Provably Fair | Progressive / Risk-based | Instant on-chain |")
    lines.append("| **BitStarz** | Curaçao | BTC, ETH, BCH, LTC, DOGE, USDT | BGaming / SoftSwiss Provably Fair | Low threshold instant; KYC on fiat | Under 10 minutes |")
    lines.append("| **Roobet** | Curaçao | BTC, ETH, LTC, USDT, XRP | Custom Provably Fair | Risk-scoring AI Responsible Gaming | Instant |")
    lines.append("| **Thunderpick** | Curaçao | BTC, ETH, LTC, USDT, XRP, DOGE, TRX, BCH | Certified RNG & Provably Fair | Tiered KYC | Under 15 minutes |")
    lines.append("| **Dominator Play** | Certified B2B Software Provider | Multi-currency B2B integration | Certified RNG / Provably Fair Compliant | B2B API compliance | Instant B2B settlement |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Master Directory of 109 Verified Press Releases & Industry Articles")
    lines.append("All 109 articles below are canonical, primary-source editorial and wire publications indexed by CryptoCasinoMedia:")
    lines.append("")
    
    # Sort articles newest first
    sorted_articles = sorted(articles, key=lambda x: x.get('date', ''), reverse=True)
    for idx, art in enumerate(sorted_articles, 1):
        title = art.get('title', '').replace('\n', ' ').strip()
        slug = art.get('slug', '')
        date = art.get('date', '')[:10]
        cat = art.get('category', 'Press Releases')
        source = art.get('sourceName', 'CryptoCasinoMedia Wire')
        url = f"https://cryptocasinomedia.com/press-releases/{slug}/"
        lines.append(f"{idx}. **{title}**")
        lines.append(f"   - URL: {url}")
        lines.append(f"   - Date: {date} | Category: {cat} | Entity: {source}")
        lines.append(f"   - Canonical Reference: `{slug}`")
        lines.append("")
        
    lines.append("---")
    lines.append("Generated by CryptoCasinoMedia Autonomous Intelligence Protocol (LLMs.txt Full Specification).")
    lines.append("Publisher Contact: https://cryptocasinomedia.com/contact/")
    
    full_text = "\n".join(lines)
    output_path = os.path.join(INDEX_DIR, "llms-full.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"SUCCESS: Generated {output_path} ({len(full_text)} bytes, {len(sorted_articles)} articles, 51 state entries).")

if __name__ == "__main__":
    generate_llms_full()
