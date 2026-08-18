import re

print("=" * 80)
print("🕒 SANITIZING DATES & REMOVING 'TODAY' FROM GRID VIEW")
print("=" * 80)

# =========================================================================
# 1. Update netlify/functions/item-detail.mjs
# =========================================================================
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    item_code = f.read()

# Add formatDisplayTimeAgo function
helper_code = '''
function formatDisplayTimeAgo(rawStr, sourceType) {
  if (sourceType === 'localshops' || sourceType === 'local-shop') return 'Local Shop';
  if (sourceType === 'foodrescue' || sourceType === 'kimc') return 'Food Rescue';
  if (sourceType === 'marketplaces' || sourceType === 'karrot' || sourceType === 'heykorean' || sourceType === 'external') return 'Community Listing';

  if (!rawStr || rawStr === 'undefined' || rawStr === 'null' || rawStr === 'None') return 'Recently';

  let raw = String(rawStr).trim().replace(/\\.+$/, '');

  // Check days ago: e.g. "1110 day ago.", "750 days ago", "1 day ago"
  const mDay = raw.match(/(\\d+)\\s*days?\\s*ago/i);
  if (mDay) {
    const days = parseInt(mDay[1], 10);
    if (days > 60) return 'Recently listed';
    if (days === 1) return '1 day ago';
    return `${days} days ago`;
  }

  // Check months / years ago
  if (/year|month/i.test(raw)) {
    const mMonth = raw.match(/(\\d+)\\s*months?\\s*ago/i);
    if (mMonth) {
      const months = parseInt(mMonth[1], 10);
      if (months > 2) return 'Recently listed';
      if (months === 1) return '1 month ago';
      return `${months} months ago`;
    }
    return 'Recently listed';
  }

  // Check hours / minutes
  const mHour = raw.match(/(\\d+)\\s*hours?\\s*ago/i);
  if (mHour) {
    const hrs = parseInt(mHour[1], 10);
    return hrs === 1 ? '1 hour ago' : `${hrs} hours ago`;
  }

  const mMin = raw.match(/(\\d+)\\s*mins?\\s*ago|minutes?\\s*ago/i);
  if (mMin) return 'Just now';

  if (/^(today|yesterday)$/i.test(raw)) {
    return raw.charAt(0).toUpperCase() + raw.slice(1).toLowerCase();
  }

  return 'Recently';
}
'''

# Insert helper before getCategorySlug
if 'function formatDisplayTimeAgo' not in item_code:
    item_code = item_code.replace('function getCategorySlug(catStr) {', helper_code.strip() + '\n\nfunction getCategorySlug(catStr) {')

# Update Local Shop strDayCount assignment
item_code = item_code.replace('strDayCount = "Local Shop";', 'strDayCount = formatDisplayTimeAgo(null, "localshops");')

# Update External strDayCount assignment
item_code = item_code.replace(
    "strDayCount = extItem.source === 'kimc' ? 'Fight Food Waste' : extItem.timeAgo;",
    "strDayCount = extItem.source === 'kimc' ? formatDisplayTimeAgo(null, 'foodrescue') : formatDisplayTimeAgo(extItem.timeAgo, 'marketplaces');"
)

# Update Moonoh strDayCount assignment
item_code = item_code.replace(
    'strDayCount = d.strDayCount || "Recently";',
    'strDayCount = formatDisplayTimeAgo(d.strDayCount, "moonoh");'
)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(item_code)
print("✅ Updated item-detail.mjs date sanitization (capping >60 days & formatting)")


# =========================================================================
# 2. Update explore.html: Remove "Today" from Grid View
# =========================================================================
with open('explore.html', 'r', encoding='utf-8') as f:
    exp_html = f.read()

# Replace itemLoc in explore.html
exp_html = exp_html.replace(
    "const itemLoc = item.timeAgo ? `${item.timeAgo} · ${rawLoc}` : rawLoc;",
    "const itemLoc = rawLoc;"
)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp_html)
print("✅ Updated explore.html: Removed 'Today' prefix from marketplace grid cards")
