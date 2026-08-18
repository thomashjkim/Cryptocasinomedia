import re

print("=" * 80)
print("🎯 OPTIMIZING TITLE TAGS (50-60 CHARS) FOR BING RULE 114")
print("=" * 80)

UPDATES = [
    {
        "files": ["fraud-prevention.html", "fraud-prevention/index.html"],
        "old_title_regex": r"<title>.*?</title>",
        "new_title": "<title>Fraud Prevention & Safe Local Trading Guide | Moonoh NYC</title>",
        "og_title": "Fraud Prevention & Safe Local Trading Guide | Moonoh NYC"
    },
    {
        "files": ["terms.html", "terms/index.html"],
        "old_title_regex": r"<title>.*?</title>",
        "new_title": "<title>Terms of Use & Community Marketplace Rules | Moonoh NYC</title>",
        "og_title": "Terms of Use & Community Marketplace Rules | Moonoh NYC"
    },
    {
        "files": ["privacy.html", "privacy/index.html"],
        "old_title_regex": r"<title>.*?</title>",
        "new_title": "<title>Privacy Policy & User Data Protection Standards | Moonoh</title>",
        "og_title": "Privacy Policy & User Data Protection Standards | Moonoh"
    },
    {
        "files": ["explore.html"],
        "old_title_regex": r"<title>Explore Items \| moonoh</title>",
        "new_title": "<title>Explore NYC & NJ Local Secondhand Marketplace | Moonoh</title>",
        "og_title": "Explore NYC & NJ Local Secondhand Marketplace | Moonoh"
    },
    {
        "files": ["item.html"],
        "old_title_regex": r"<title>Item Detail - Moonoh</title>",
        "new_title": "<title>Secondhand Item Detail & Local Meetup | Moonoh NYC</title>",
        "og_title": "Secondhand Item Detail & Local Meetup | Moonoh NYC"
    }
]

for item in UPDATES:
    for file_path in item["files"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            content = re.sub(item["old_title_regex"], item["new_title"], content, count=1, flags=re.IGNORECASE)
            
            # Also update og:title if present
            if '<meta property="og:title"' in content:
                content = re.sub(r'<meta property="og:title" content=".*?"', f'<meta property="og:title" content="{item["og_title"]}"', content)
            
            # Also update twitter:title if present
            if '<meta name="twitter:title"' in content:
                content = re.sub(r'<meta name="twitter:title" content=".*?"', f'<meta name="twitter:title" content="{item["og_title"]}"', content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Check length
            title_text = re.search(r'<title>(.*?)</title>', content).group(1)
            print(f"✅ {file_path} -> ({len(title_text)} chars): \"{title_text}\"")
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")

print("=" * 80)
