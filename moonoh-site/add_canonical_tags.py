import glob
import re

canonical_map = {
    'index.html': 'https://moon-oh.com/',
    'explore.html': 'https://moon-oh.com/explore',
    'about.html': 'https://moon-oh.com/about',
    'press.html': 'https://moon-oh.com/press',
    'contact.html': 'https://moon-oh.com/contact',
    'terms.html': 'https://moon-oh.com/terms',
    'privacy.html': 'https://moon-oh.com/privacy',
    'disclaimer.html': 'https://moon-oh.com/disclaimer',
    'fraud-prevention.html': 'https://moon-oh.com/fraud-prevention'
}

for fname, url in canonical_map.items():
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Check if canonical tag exists
        if '<link rel="canonical"' in html or '<link href="' in html and 'rel="canonical"' in html:
            # Replace existing canonical tag
            html = re.sub(r'<link[^>]*rel=[\"\']canonical[\"\'][^>]*>', f'<link rel="canonical" href="{url}"/>', html)
            html = re.sub(r'<link[^>]*href=[\"\'][^\"\'\s]+[\"\'][^>]*rel=[\"\']canonical[\"\'][^>]*>', f'<link rel="canonical" href="{url}"/>', html)
        else:
            # Insert before </head>
            tag = f'  <link rel="canonical" href="{url}"/>\n</head>'
            html = html.replace('</head>', tag)
            
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated canonical in {fname} -> {url}")
    except Exception as e:
        print(f"Error in {fname}: {e}")
