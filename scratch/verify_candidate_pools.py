import urllib.request
import json

candidates = {
    "crypto-casinos": [
        "photo-1596838132731-3301c3fd4317", # roulette wheel
        "photo-1518546305927-5a555bb7020d", # casino dice chips
        "photo-1606167668584-78701c57f13d", # roulette wheel close up
        "photo-1578575437130-527eed3abbec", # golden dice
        "photo-1533174072545-7a4b6ad7a6c3", # neon casino lights
        "photo-1609501676725-7186f017a4b7", # card dealer
        "photo-1513151233558-d860c5398176", # party dice
        "photo-1522069169874-c58ec4b76be5", # gold tokens
        "photo-1541256996761-85df2efaa164", # colored dice
        "photo-1542224566-6e85f2e6772f", # dice board game
        "photo-1568194157720-8eae79a8d75a", # casino poker chips
        "photo-1570307272161-429d54b807e1", # cards
        "photo-1605809831853-4117905d0d41", # blackjack cards
        "photo-1594122230689-45899d9e6f69", # roulette wheel
        "photo-1618519764620-7403abdbfee9", # casino poker chips stack
        "photo-1601987177651-8edfe6c20009", # blackjack table
        "photo-1628157582853-a796fa650a6a", # poker cards / chips
        "photo-1626775218847-d0c3ec6bd60e", # poker hand
        "photo-1509198397868-475647b2a1e5", # neon slots
        "photo-1614041793739-16629910d540", # cards on green felt
        "photo-1595166708453-61ba4f128d54", # slot machine
        "photo-1624454001599-7a77dbcd8b7b", # poker table
        "photo-1622050865806-254d68249826", # blackjack
        "photo-1618519764620-7403abdbfee9"  # casino gaming
    ],
    "sportsbook": [
        "photo-1522771739844-6a9f6d5f14af", # soccer ball grass
        "photo-1518063319789-7217e6706b04", # stadium field
        "photo-1544377193-33dcf4d68fb5", # stadium lights
        "photo-1529900748604-07564a03e7a6", # soccer players
        "photo-1540747737956-37872404f802", # football stadium
        "photo-1579952362224-d986950002a4", # soccer ball
        "photo-1519766304817-4f37bda74a27", # stadium crowds
        "photo-1560272564-c83d66b1ad12", # soccer goal
        "photo-1546519638-68e109498ffc", # basketball net
        "photo-1508098682722-e99c43a406b2", # stadium pitch lights
        "photo-1505250469679-203ad9ced0cb", # tennis wagers
        "photo-1587280501635-68a0e82cd5ff", # basketball
        "photo-1530541930197-ff16ac917b0e", # swimming race
        "photo-1517649763962-0c623066013b", # stadium track
        "photo-1595030044556-acfaa61edc0f", # soccer cleats field
        "photo-1517838277536-f5f99be501cd"  # gym barbell
    ],
    "regulation": [
        "photo-1589829545856-d10d557cf95f", # gavel
        "photo-1450133064473-71024230f91b", # law books
        "photo-1589829085413-56de8ae18c73", # scales of justice
        "photo-1505664194779-8beaceb93744", # court gavel
        "photo-1449034446853-66c86144b0ad", # pillars court
        "photo-1521791136368-1a8682707636", # signed contract
        "photo-1454165804606-c3d57bc86b40", # document audit
        "photo-1507679799987-c73779587ccf", # business audit
        "photo-1544716278-ca5e3f4abd8c", # terms reading
        "photo-1521790797524-b2497295b743", # law contract signatures
        "photo-1553484771-047a44eee27f", # gaming board / legal meeting
        "photo-1575505586043-007b0b85a110", # law gavel hammer
        "photo-1582213782179-e0d53f98f2ca"  # regulatory meeting table
    ],
    "payments": [
        "photo-1516245834210-c4c142787335", # bitcoin motherboard
        "photo-1621761191319-c6fb62004040", # eth coin
        "photo-1622630998477-20aa696ecb05", # DeFi coins
        "photo-1621416894569-0f39ed31d247", # gold coins stack
        "photo-1639762681485-074b7f938ba0", # blockchain
        "photo-1621506289937-a8e4df240d0b", # bitcoin macro
        "photo-1624555130581-1d9cca783bc0", # gold coins stack 2
        "photo-1629339942248-47d49e085e4a", # solana coin
        "photo-1634704784915-aacf363b021f", # ether symbol
        "photo-1644024220147-380d85078516", # usdt tether
        "photo-1634973357973-f2ed255753e1", # crypto chart
        "photo-1590283603385-17ffb3a7f29f", # data charts nodes
        "photo-1642104704074-907c0698cbd9", # NFT crypto display
        "photo-1518156677180-95a2893f3e9f", # finance chart
        "photo-1526304640581-d334cdbbf45e", # safety vault
        "photo-1559526324-4b87b5e36e44", # mobile pay crypto scan
        "photo-1579621970563-ebec7560ff3e"  # coin growth
    ],
    "sweepstakes": [
        "photo-1560253023-3ec5d502959f", # mobile play
        "photo-1553481187-be93c21490a9", # arcade cabinet
        "photo-1542751371-adc38448a05e", # esports gaming
        "photo-1511512578047-dfb367046420", # keyboard neon
        "photo-1566241440091-ec10de8db2e1", # mobile game
        "photo-1607604276583-eef5d076aa5f", # gaming room
        "photo-1538481199705-c710c4e965fc", # monitor gamer
        "photo-1551103782-8ab07afd45c1", # joystick arcade
        "photo-1542751110-97646eb5f202", # gaming desk setup
        "photo-1552820728-8b83bb6b773f", # cyberpunk neon gamer
        "photo-1612287230202-1bf1d85d1bdf", # gaming controller
        "photo-1550745165-9bc0b252726f", # retro console gaming
        "photo-1627856013091-fed6e4e30025", # vr headset social play
        "photo-1614294149010-950b698f72c0", # slot reels
        "photo-1538097304804-2a1b932466a9"  # slot screen
    ],
    "guides": [
        "photo-1516321318423-f06f85e504b3", # search tutorial
        "photo-1456513080510-7bf3a84b82f8", # books study guides
        "photo-1506784983877-45594efa4cbe", # calendar planning
        "photo-1515879218367-8466d910aaa4", # code guide
        "photo-1542831371-29b0f74f9713", # html learning
        "photo-1511193311914-0346f16efe90", # billiards logic strategy
        "photo-1501504905252-473c47e087f8", # course notes
        "photo-1516321165247-4aa89a48be28", # support guide help
        "photo-1518495973542-4542c06a5843", # reading online guide
        "photo-1434030216411-0b793f4b4173", # writing tips notes
        "photo-1606326608606-aa0b62935f2b", # taking exam guide
        "photo-1552581234-2612b75d8953", # team learning strategy
        "photo-1517245386807-bb43f82c33c4"  # learning presentation
    ]
}

def verify_photo(photo_id):
    url = f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&q=80&w=800"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status == 200
    except Exception:
        return False

def main():
    verified_pools = {}
    for cat, pids in candidates.items():
        print(f"Verifying {cat} ({len(pids)} ids)...")
        active = []
        for pid in pids:
            if verify_photo(pid):
                active.append(f"https://images.unsplash.com/{pid}?auto=format&fit=crop&q=80&w=800")
        verified_pools[cat] = active
        print(f"  -> Found {len(active)} active URLs.")
        
    print("\n--- RESULTS JSON ---")
    print(json.dumps(verified_pools, indent=4))

if __name__ == "__main__":
    main()
