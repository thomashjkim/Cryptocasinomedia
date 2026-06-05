import urllib.request

candidates = [
    "photo-1529900748604-07564a03e7a6", # soccer players
    "photo-1540747737956-37872404f802", # football stadium
    "photo-1530541930197-ff16ac917b0e", # swimming race
    "photo-1516731415730-0c60700c987c", # sports team
    "photo-1517838277536-f5f99be501cd", # fitness gym
    "photo-1579952362224-d986950002a4", # soccer ball
    "photo-1519766304817-4f37bda74a27", # stadium crowds
    "photo-1568194157720-8eae79a8d75a", # casino poker chips
    "photo-1570307272161-429d54b807e1", # cards
    "photo-1511193311914-0346f16efe90", # billiards
    "photo-1606167668584-78701c57f13d", # roulette
    "photo-1605809831853-4117905d0d41", # blackjack cards
]

working = []
for photo_id in candidates:
    url = f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&q=80&w=800"
    try:
        req = urllib.request.Request(
            url,
            method='HEAD',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                working.append(photo_id)
    except Exception:
        pass

print("Working:", working)
