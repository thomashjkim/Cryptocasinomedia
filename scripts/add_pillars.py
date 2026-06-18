import sys
import os
import re

new_pages_code = """
        'regulation-2026': {
            'title': 'The 2026 Crypto Casino Regulatory Guide',
            'h1': 'The 2026 Crypto Casino Regulatory Guide',
            'sections': [
                {'heading': 'Executive Summary', 'body': 'The regulatory landscape for crypto casinos has matured significantly in 2026. With the full implementation of MiCA in Europe and the restructuring of Curacao\\'s licensing framework, operators must navigate a complex web of multijurisdictional compliance to maintain market access and banking relationships.'},
                {'heading': 'Curacao License Restructuring', 'body': 'Historically the primary jurisdiction for crypto casinos, Curacao has replaced its master license system with the National Ordinance for Games of Chance (LOK). In 2026, operators face stricter KYC/AML requirements, mandatory physical presence on the island, and enhanced player protection standards. Existing sub-license holders must fully transition to the new framework by Q3 2026.'},
                {'heading': 'The MiCA Impact in Europe', 'body': 'The Markets in Crypto-Assets (MiCA) regulation has fundamentally altered how crypto casinos operate within the EU. While MiCA does not regulate gambling directly, it strictly regulates the stablecoins (E-Money Tokens) and service providers that casinos rely on. Casinos must ensure their payment gateways and custody solutions are fully MiCA-compliant to serve European players legally.'},
                {'heading': 'Emerging Markets: LatAm & Brazil', 'body': 'Brazil\\'s fully regulated iGaming market, which opened in early 2025, has become a primary target for crypto operators. However, the Brazilian framework requires strict local entity establishment and mandates fiat-crypto on-ramps through licensed financial institutions using PIX. Unlicensed offshore crypto casinos face aggressive ISP blocking and payment processor sanctions.'},
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
                {'heading': 'Tokenomics and Revenue Sharing', 'body': 'A defining feature of GambleFi is revenue sharing. Many decentralized casinos issue native utility tokens. Token holders can stake their assets to act as the "house bankroll," earning a yield generated from the platform\\'s profits. This aligns the incentives of players, liquidity providers, and the platform.'},
                {'heading': 'Zero-Knowledge and Privacy', 'body': 'As regulatory pressures mount, GambleFi platforms are adopting Zero-Knowledge (ZK) proofs. This allows players to prove they are of legal age or not located in a restricted jurisdiction without revealing their actual identity or location, balancing compliance with the privacy ethos of Web3.'},
                {'heading': 'Challenges and Risks', 'body': 'The GambleFi sector faces significant risks, including smart contract vulnerabilities, rug pulls, and ambiguous legal status. Because many platforms operate entirely on-chain without traditional licenses, they exist in a regulatory gray area, making them vulnerable to enforcement actions from global financial regulators.'}
            ]
        },
"""

def update_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the insertion point: just before "'how': {"
    insertion_point = content.find("        'how': {")
    
    if insertion_point == -1:
        print(f"Could not find insertion point in {filepath}")
        return False
        
    new_content = content[:insertion_point] + new_pages_code + content[insertion_point:]
    
    # If this is pre_render.py, we also need to add the routes to the guides list
    if filepath.endswith('pre_render.py'):
        guides_insert = """
    ('regulation-2026', 'guides/regulation-2026', 'The 2026 Crypto Casino Regulatory Guide', 'A comprehensive B2B guide covering Curacao LOK, EU MiCA impact, and emerging LatAm regulatory frameworks.'),
    ('sweepstakes-market', 'guides/sweepstakes-market', 'Sweepstakes Casinos: Market Size & Legal Framework 2026', 'Understanding the $4B US sweepstakes model, Gold Coins/Sweeps Coins mechanics, and state-by-state legality.'),
    ('gamblefi-telegram', 'guides/gamblefi-telegram', 'GambleFi & Telegram Casinos: Web3 Betting', 'The rise of no-KYC Telegram bots, decentralized on-chain casinos, and revenue-sharing tokenomics.'),"""
        
        guides_point = new_content.find("    ('how', 'how-crypto-casino-news-works'")
        if guides_point != -1:
            new_content = new_content[:guides_point] + guides_insert.lstrip() + new_content[guides_point:]

    # If this is index.html.template, we need to add the client-side router conditions
    if filepath.endswith('index.html.template'):
        router_insert = """
            } else if (path === '/guides/regulation-2026') {
                mainContent.innerHTML = renderKnowledgePage('regulation-2026');
            } else if (path === '/guides/sweepstakes-market') {
                mainContent.innerHTML = renderKnowledgePage('sweepstakes-market');
            } else if (path === '/guides/gamblefi-telegram') {
                mainContent.innerHTML = renderKnowledgePage('gamblefi-telegram');"""
                
        router_point = new_content.find("            } else if (path === '/how-crypto-casino-news-works') {")
        if router_point != -1:
            new_content = new_content[:router_point] + router_insert.lstrip() + "\n" + new_content[router_point:]
            
        # Add dynamic title/meta descriptions
        meta_insert = """
            } else if (path === '/guides/regulation-2026') {
                document.title = 'The 2026 Crypto Casino Regulatory Guide — CryptoCasinoMedia';
                if (metaDesc) metaDesc.setAttribute('content', 'A comprehensive B2B guide covering Curacao LOK, EU MiCA impact, and emerging LatAm regulatory frameworks.');
            } else if (path === '/guides/sweepstakes-market') {
                document.title = 'Sweepstakes Casinos: Market Size & Legal Framework 2026 — CryptoCasinoMedia';
                if (metaDesc) metaDesc.setAttribute('content', 'Understanding the $4B US sweepstakes model, Gold Coins/Sweeps Coins mechanics, and state-by-state legality.');
            } else if (path === '/guides/gamblefi-telegram') {
                document.title = 'GambleFi & Telegram Casinos: Web3 Betting — CryptoCasinoMedia';
                if (metaDesc) metaDesc.setAttribute('content', 'The rise of no-KYC Telegram bots, decentralized on-chain casinos, and revenue-sharing tokenomics.');"""
        
        meta_point = new_content.find("            } else if (path === '/how-crypto-casino-news-works') {")
        meta_point_2 = new_content.rfind("            } else if (path === '/how-crypto-casino-news-works') {", 0, len(new_content)) # Need to find the second occurrence which is in the dynamic meta section
        
        # Actually it's better to just search for the specific meta block
        meta_block_point = new_content.find("            } else if (path === '/how-crypto-casino-news-works') {", new_content.find("Dynamic title + meta"))
        if meta_block_point != -1:
            new_content = new_content[:meta_block_point] + meta_insert.lstrip() + "\n" + new_content[meta_block_point:]

    with open(filepath, 'w') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")
    return True

base_dir = "/Users/thomaskim/Cryptocasinomedia"
update_file(os.path.join(base_dir, "scripts", "pre_render.py"))
update_file(os.path.join(base_dir, "index", "index.html.template"))
