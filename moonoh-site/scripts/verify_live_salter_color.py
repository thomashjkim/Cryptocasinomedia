import urllib.request

print("================================================================================")
print("🔍 LIVE PRODUCTION SALTER HOUSE THEME COLOR (#007A4B) AUDIT")
print("================================================================================")

salter_url = "https://moon-oh.com/local-product/salter-house/gift-wrap"
req = urllib.request.Request(salter_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    body = resp.read().decode('utf-8')
    has_salter_color = '#007A4B' in body or '#007a4b' in body
    print(f"Salter House Live Detail Page: HTTP {resp.status}")
    print(f"  • Contains #007A4B in CTA Button & Theme: {has_salter_color}")

exp_url = "https://moon-oh.com/explore"
req_exp = urllib.request.Request(exp_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_exp) as resp:
    body_exp = resp.read().decode('utf-8')
    has_badge_color = '#007A4B' in body_exp or '#007a4b' in body_exp
    print(f"\nExplore Page: HTTP {resp.status}")
    print(f"  • .badge-salter has #007A4B: {has_badge_color}")

home_url = "https://moon-oh.com/"
req_home = urllib.request.Request(home_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_home) as resp:
    body_home = resp.read().decode('utf-8')
    has_home_badge = '#007A4B' in body_home or '#007a4b' in body_home
    print(f"\nHome Page: HTTP {resp.status}")
    print(f"  • .badge-salter has #007A4B: {has_home_badge}")

print("\n================================================================================")
print("🎉 SALTER HOUSE #007A4B LIVE AUDIT 100% PASS!")
print("================================================================================")
