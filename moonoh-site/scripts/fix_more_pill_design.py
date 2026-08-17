import re

with open('explore.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update HTML class of filter-pill-more to include filter-pill
html = html.replace(
    '<button class="filter-pill-more" id="filter-pill-more"',
    '<button class="filter-pill filter-pill-more" id="filter-pill-more"'
)

# 2. Add specific CSS for filter-pill-more to ensure 100% exact design match with other filter pills and zero outline box
more_css = '''
    /* More Button Exact Pill Design & Focus Reset */
    .filter-pill-more {
      display: inline-flex !important;
      align-items: center !important;
      gap: 6px !important;
      cursor: pointer !important;
      -webkit-tap-highlight-color: transparent !important;
      outline: none !important;
      box-shadow: none !important;
    }
    .filter-pill-more:focus,
    .filter-pill-more:active,
    .filter-pill-more:focus-visible {
      outline: none !important;
      box-shadow: none !important;
      border-color: #E5E7EB !important;
    }
'''

html = html.replace('</style>', more_css + '\n  </style>')

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Fixed filter-pill-more class and CSS to match all category pills exactly")
