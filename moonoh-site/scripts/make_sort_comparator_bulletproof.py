import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_comparator = '''          filtered.sort((a, b) => {
            const dateA = a.source_published_at ? new Date(a.source_published_at).getTime() : (a.postedAt ? new Date(a.postedAt).getTime() : (typeof a.no === 'number' ? a.no : 0));
            const dateB = b.source_published_at ? new Date(b.source_published_at).getTime() : (b.postedAt ? new Date(b.postedAt).getTime() : (typeof b.no === 'number' ? b.no : 0));
            if (dateA !== dateB) return dateB - dateA;
            return (b.no || 0) - (a.no || 0);
          });'''

new_comparator = '''          filtered.sort((a, b) => {
            const dateA = a.source_published_at ? new Date(a.source_published_at).getTime() : (a.postedAt ? new Date(a.postedAt).getTime() : 0);
            const dateB = b.source_published_at ? new Date(b.source_published_at).getTime() : (b.postedAt ? new Date(b.postedAt).getTime() : 0);
            if (dateA && dateB && dateA !== dateB) return dateB - dateA;
            const numA = parseInt(String(a.no || a.id || '').replace(/\\D/g, ''), 10) || 0;
            const numB = parseInt(String(b.no || b.id || '').replace(/\\D/g, ''), 10) || 0;
            return numB - numA;
          });'''

if old_comparator in html:
    html = html.replace(old_comparator, new_comparator)
    print("✅ Replaced Newest sort comparator in explore.html")
else:
    pattern = r'filtered\.sort\(\(a, b\) => \{[\s\S]*?if \(dateA !== dateB\)[\s\S]*?\}\);'
    html = re.sub(pattern, new_comparator, html, count=1)
    print("✅ Replaced Newest sort comparator via regex in explore.html")

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Saved explore.html with bulletproof Newest sort comparator")
