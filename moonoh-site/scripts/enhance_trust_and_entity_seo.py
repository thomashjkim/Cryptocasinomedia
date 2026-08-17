import re

same_as_json = '''[
          "https://www.instagram.com/moonoh_market",
          "https://www.threads.net/@moonoh_market",
          "https://www.tiktok.com/@moonoh_market",
          "https://apps.apple.com/us/app/moonoh/id6477390079",
          "https://play.google.com/store/apps/details?id=com.moonoh"
        ]'''

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(r'"sameAs":\s*\[\s*"https:\/\/apps\.apple\.com\/us\/app\/moonoh\/id6477390079",\s*"https:\/\/play\.google\.com\/store\/apps\/details\?id=com\.moonoh"\s*\]', f'"sameAs": {same_as_json}', idx)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("✅ Updated index.html sameAs")

# 2. Update explore.html
with open('explore.html', 'r', encoding='utf-8') as f:
    exp = f.read()

# Fix og:url in explore.html to match canonical exactly
exp = re.sub(r'<meta content="https:\/\/moon-oh\.com" property="og:url"\/>', '<meta content="https://moon-oh.com/explore" property="og:url"/>', exp)
exp = re.sub(r'"sameAs":\s*\[\s*"https:\/\/apps\.apple\.com\/us\/app\/moonoh\/id6477390079",\s*"https:\/\/play\.google\.com\/store\/apps\/details\?id=com\.moonoh"\s*\]', f'"sameAs": {same_as_json}', exp)

with open('explore.html', 'w', encoding='utf-8') as f:
    f.write(exp)
print("✅ Updated explore.html og:url and sameAs")

# 3. Update about.html
with open('about.html', 'r', encoding='utf-8') as f:
    abt = f.read()

abt = re.sub(r'"sameAs":\s*\[\s*"https:\/\/apps\.apple\.com\/us\/app\/moonoh\/id6477390079",\s*"https:\/\/play\.google\.com\/store\/apps\/details\?id=com\.moonoh"\s*\]', f'"sameAs": {same_as_json}', abt)

# Add entity trust, methodology, and claim/removal sections in about.html
methodology_content = '''
      <h2 class="section-subtitle">Data Collection &amp; Curation Methodology</h2>
      <p style="font-size:14px; line-height:1.75; color:#374151;">
        Moonoh indexes publicly accessible secondhand listings, local partner products, and neighborhood grocery items to make local discovery effortless and transparent.
      </p>
      <ul style="font-size:14px; line-height:1.75; color:#374151; padding-left:20px;">
        <li><strong>Moonoh Direct P2P Listings:</strong> Authentic items posted directly by verified neighbors across NYC &amp; NJ. Communications and in-person meetups are coordinated in the mobile app.</li>
        <li><strong>Local Independent Shops:</strong> Curated specialty inventory from neighborhood brick-and-mortar storefronts (e.g. Front General Store, Mirth Vintage, SEY Coffee, Salter House, Big Night, Pop Up Grocer, Happier Grocery). All purchases, shipping, and returns are handled directly by each respective store.</li>
        <li><strong>Public Community Marketplaces:</strong> Publicly available secondhand goods aggregated to help neighbors discover nearby items without navigating multiple fragmented websites. Direct attribution and outbound links to original listings are always provided.</li>
        <li><strong>"Last Verified" Date:</strong> Indicates the exact date on which listing availability, price, and public details were last confirmed.</li>
      </ul>

      <h2 class="section-subtitle">Web Discovery vs. Mobile Application</h2>
      <p style="font-size:14px; line-height:1.75; color:#374151;">
        The <strong>Moonoh Web Platform</strong> (<a href="https://moon-oh.com" style="color:#4F46E5; font-weight:700;">moon-oh.com</a>) serves as a fast, searchable public index of neighborhood goods. The <strong>Moonoh Mobile App</strong> (iOS &amp; Android) is the dedicated interactive platform where users verify identities, securely chat in real-time, negotiate prices with zero commissions, and schedule safe in-person exchanges.
      </p>

      <h2 class="section-subtitle">Listing Corrections, Business Claim &amp; Opt-Out Policy</h2>
      <p style="font-size:14px; line-height:1.75; color:#374151;">
        We respect content creators, sellers, and independent business owners. If you are a business owner wishing to claim your storefront profile, update product details, or request the immediate removal/opt-out of your listing, please visit our <a href="/contact" style="color:#4F46E5; font-weight:700; text-decoration:underline;">Contact &amp; Claim page</a> or email us at <a href="mailto:info@moon-oh.com" style="color:#4F46E5; font-weight:700;">info@moon-oh.com</a>. Removal requests are honored promptly within 24–48 business hours.
      </p>
'''

if 'Data Collection &amp; Curation Methodology' not in abt:
    abt = abt.replace('<h2 class="section-subtitle" style="margin-top: 40px;">Why Moonoh? (Comparison)</h2>', methodology_content + '\n      <h2 class="section-subtitle" style="margin-top: 40px;">Why Moonoh? (Comparison)</h2>')

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(abt)
print("✅ Updated about.html with methodology, entity trust, and sameAs")

# 4. Update contact.html
with open('contact.html', 'r', encoding='utf-8') as f:
    cnt = f.read()

claim_removal_content = '''
        <div class="contact-info-card" style="margin-top: 24px; grid-column: 1 / -1; background: #F8FAFC; border: 1px solid #E2E8F0;">
          <h2>Store Claim, Content Corrections &amp; Removal (Opt-Out)</h2>
          <p style="font-size: 13.5px; line-height: 1.7; color: #334155;">
            <strong>For Local Business Owners &amp; Sellers:</strong><br/>
            • <strong>Claim Your Storefront:</strong> If your local shop is indexed on Moonoh and you want to verify your business, update information, or add partner badges, please specify "Business Claim" in your message.<br/>
            • <strong>Listing Update or Removal (Opt-Out):</strong> To request immediate modification or removal of an indexed item or storefront, please provide the Moonoh URL and original listing link. All valid opt-out and take-down requests are processed within 24–48 hours.<br/>
            • <strong>Direct Inquiries:</strong> You can also email us directly at <a href="mailto:info@moon-oh.com" style="color:#1E1B4B; font-weight:700; text-decoration:underline;">info@moon-oh.com</a> with the subject line <em>[Listing Inquiry / Claim]</em>.
          </p>
        </div>
'''

if 'Store Claim, Content Corrections &amp; Removal' not in cnt:
    cnt = cnt.replace('</form>\n      </div>', '</form>\n' + claim_removal_content + '      </div>')

with open('contact.html', 'w', encoding='utf-8') as f:
    f.write(cnt)
print("✅ Updated contact.html with store claim & removal options")

# 5. Update item-detail.mjs sameAs in Organization schema
with open('netlify/functions/item-detail.mjs', 'r', encoding='utf-8') as f:
    itm_code = f.read()

itm_code = re.sub(r'"sameAs":\s*\[\s*"https:\/\/apps\.apple\.com\/us\/app\/moonoh\/id6477390079",\s*"https:\/\/play\.google\.com\/store\/apps\/details\?id=com\.moonoh"\s*\]', f'"sameAs": {same_as_json}', itm_code)

with open('netlify/functions/item-detail.mjs', 'w', encoding='utf-8') as f:
    f.write(itm_code)
print("✅ Updated item-detail.mjs sameAs schema")
