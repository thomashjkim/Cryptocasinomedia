import re

print("=" * 80)
print("🎨 UPDATING MIRTH VINTAGE BUTTON COLOR TO #000000 IN netlify/functions/item-detail.mjs")
print("=" * 80)

with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the mirth-vintage styling block
old_mirth_block = '''    } else if (externalSource === "mirth-vintage") {
      bannerBg = "#FEF3C7";
      bannerBorder = "#FDE68A";
      bannerColor = "#78350F";
      btnBgColor = "#8C6D1F";'''

new_mirth_block = '''    } else if (externalSource === "mirth-vintage") {
      bannerBg = "#F9FAFB";
      bannerBorder = "#E5E7EB";
      bannerColor = "#111827";
      btnBgColor = "#000000";
      btnTextColor = "#FFFFFF";'''

if old_mirth_block in code:
    code = code.replace(old_mirth_block, new_mirth_block)
    print("✅ Replaced old mirth-vintage styling block")
else:
    # Use regex
    code = re.sub(
        r'\}\s*else if \(externalSource === "mirth-vintage"\)\s*\{[\s\S]*?btnBgColor = "[^"]+";',
        new_mirth_block,
        code
    )
    print("✅ Updated mirth-vintage styling block via regex")

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Saved netlify/functions/item-detail.mjs")
