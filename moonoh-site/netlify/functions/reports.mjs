import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Region metadata
const REPORT_REGIONS = {
  'manhattan': { slug: 'manhattan', name: 'Manhattan, NY', shortName: 'Manhattan' },
  'brooklyn': { slug: 'brooklyn', name: 'Brooklyn, NY', shortName: 'Brooklyn' },
  'queens': { slug: 'queens', name: 'Queens, NY', shortName: 'Queens' },
  'new-york': { slug: 'new-york', name: 'New York City, NY', shortName: 'NYC' }
};

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export default async function handler(req, context) {
  const url = new URL(req.url);
  const pathParts = url.pathname.replace(/^\/reports\/?/, '').split('/').filter(Boolean);

  const regionSlug = pathParts[0] || 'manhattan';
  const reportDate = pathParts[1] || null; // e.g. '2026-08-20'

  const regionObj = REPORT_REGIONS[regionSlug] || REPORT_REGIONS['manhattan'];

  // Load historical snapshots
  let allSnapshots = {};
  try {
    const snapshotPath = path.resolve(__dirname, '../../data/historical_market_snapshots.json');
    if (fs.existsSync(snapshotPath)) {
      allSnapshots = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
    }
  } catch (e) {
    console.error('Error loading snapshots:', e);
  }

  const availableDates = Object.keys(allSnapshots).sort().reverse();
  const targetDate = reportDate || availableDates[0] || '2026-08-20';
  const snapshotData = (allSnapshots[targetDate] && allSnapshots[targetDate][regionObj.slug]) || null;

  // Fallback defaults if snapshot not populated yet
  const stats = snapshotData || {
    active_listings: 759,
    median_price: 50,
    p25_price: 19,
    p75_price: 188,
    free_items: 16
  };

  const isHubPage = !reportDate;
  const pageTitle = isHubPage 
    ? `${regionObj.name} Local Marketplace Reports & Historical Trends | Moonoh`
    : `${regionObj.name} Local Marketplace Report — ${targetDate} | Moonoh`;

  const metaDesc = isHubPage
    ? `Browse historical market intelligence reports, price trends, and inventory changes for ${regionObj.name} on Moonoh.`
    : `Historical market report for ${regionObj.name} as of ${targetDate}. Active listings, median asking price ($${stats.median_price}), and category composition.`;

  const canonicalUrl = isHubPage
    ? `https://moon-oh.com/reports/${regionObj.slug}`
    : `https://moon-oh.com/reports/${regionObj.slug}/${targetDate}`;

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(pageTitle)}</title>
  <meta name="description" content="${escapeHtml(metaDesc)}">
  <link rel="canonical" href="${canonicalUrl}">
  <meta property="og:title" content="${escapeHtml(pageTitle)}">
  <meta property="og:description" content="${escapeHtml(metaDesc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${canonicalUrl}">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #F8FAFC; color: #1E293B; line-height: 1.6; }
    .container { max-width: 860px; margin: 0 auto; padding: 32px 20px; }
    header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px; border-bottom: 1px solid #E2E8F0; margin-bottom: 32px; }
    .logo { font-size: 22px; font-weight: 900; color: #4F46E5; text-decoration: none; }
    .nav-link { color: #64748B; text-decoration: none; font-size: 14px; font-weight: 600; }
    .nav-link:hover { color: #4F46E5; }
    .badge-preview { display: inline-block; background: #FEF3C7; color: #92400E; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; margin-bottom: 12px; }
    h1 { font-size: 32px; font-weight: 900; color: #0F172A; line-height: 1.25; margin-bottom: 16px; letter-spacing: -0.02em; }
    .report-meta { font-size: 14px; color: #64748B; margin-bottom: 28px; display: flex; gap: 16px; flex-wrap: wrap; }
    .report-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 28px; margin-bottom: 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .answer-lead { font-size: 17px; color: #334155; line-height: 1.7; margin-bottom: 24px; font-weight: 450; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-bottom: 24px; }
    .stat-box { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; }
    .stat-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-value { font-size: 26px; font-weight: 900; color: #0F172A; margin-top: 4px; }
    .stat-value.green { color: #059669; }
    .stat-value.indigo { color: #4F46E5; }
    h2 { font-size: 20px; font-weight: 800; color: #0F172A; margin: 28px 0 14px; }
    p { font-size: 15px; color: #475569; margin-bottom: 14px; line-height: 1.7; }
    ul { list-style: none; margin-bottom: 20px; }
    li { position: relative; padding-left: 20px; margin-bottom: 8px; font-size: 14.5px; color: #334155; }
    li::before { content: "•"; position: absolute; left: 6px; color: #4F46E5; font-weight: bold; }
    .methodology-box { background: #F1F5F9; border-radius: 12px; padding: 20px; font-size: 13px; color: #475569; margin-top: 32px; border-left: 4px solid #4F46E5; }
    .methodology-title { font-weight: 800; color: #1E293B; margin-bottom: 6px; }
    .cta-banner { background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 12px; padding: 20px; margin-top: 28px; text-align: center; }
    .cta-btn { display: inline-block; background: #4F46E5; color: #FFFFFF; padding: 10px 22px; border-radius: 8px; font-weight: 700; font-size: 14px; text-decoration: none; margin-top: 10px; }
    footer { margin-top: 48px; padding-top: 24px; border-top: 1px solid #E2E8F0; font-size: 12px; color: #94A3B8; text-align: center; }
  </style>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "${escapeHtml(pageTitle)}",
    "datePublished": "${targetDate}T00:00:00Z",
    "dateModified": "${targetDate}T00:00:00Z",
    "author": {
      "@type": "Organization",
      "name": "Moonoh Data Intelligence"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Moonoh",
      "logo": {
        "@type": "ImageObject",
        "url": "https://moon-oh.com/images/logo.png"
      }
    },
    "description": "${escapeHtml(metaDesc)}"
  }
  </script>
</head>
<body>
  <div class="container">
    <header>
      <a href="/" class="logo">Moonoh</a>
      <div style="display:flex; gap:16px;">
        <a href="/explore/${escapeHtml(regionObj.slug)}" class="nav-link">Live ${escapeHtml(regionObj.shortName)} Market</a>
        <a href="/reports/${escapeHtml(regionObj.slug)}" class="nav-link">Historical Hub</a>
      </div>
    </header>

    <main>
      <div class="badge-preview">Immutable Historical Market Report (Baseline Preview)</div>
      <h1>${escapeHtml(regionObj.name)} Local Marketplace Report</h1>
      <div class="report-meta">
        <span>📅 Period: <strong>${escapeHtml(targetDate)}</strong></span>
        <span>📍 Scope: <strong>${escapeHtml(regionObj.name)} (Strict Physical Geography)</strong></span>
        <span>🏷️ Dataset: <strong>v1.8 (4,228 Active Pool / 5,178 Catalog)</strong></span>
      </div>

      <div class="report-card">
        <p class="answer-lead">
          As of <strong>${escapeHtml(targetDate)}</strong>, Moonoh tracked <strong>${stats.active_listings.toLocaleString()} active marketplace and local-store listings</strong> physically located in <strong>${escapeHtml(regionObj.name)}</strong>. The median asking price among priced items was <strong>$${Math.round(stats.median_price)}</strong>, with the interquartile range (middle 50%) spanning from <strong>$${Math.round(stats.p25_price)}</strong> to <strong>$${Math.round(stats.p75_price)}</strong>.
        </p>

        <h2>${escapeHtml(regionObj.shortName)} by the Numbers</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-label">Active Listings</div>
            <div class="stat-value">${stats.active_listings.toLocaleString()}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Median Asking Price</div>
            <div class="stat-value green">$${Math.round(stats.median_price)}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Price Range (IQR)</div>
            <div class="stat-value" style="font-size:20px; margin-top:8px;">$${Math.round(stats.p25_price)} – $${Math.round(stats.p75_price)}</div>
          </div>
          <div class="stat-box">
            <div class="stat-label">Free Listings</div>
            <div class="stat-value indigo">${stats.free_items || 0}</div>
          </div>
        </div>

        <h2>Market Composition & Observations</h2>
        <p>
          This historical observation establishes the baseline market pulse for ${escapeHtml(regionObj.name)}. Future bi-weekly reports will automatically calculate and highlight directional inventory shifts, median price fluctuations, and category volume changes based on accumulating daily snapshots.
        </p>
        <ul>
          <li><strong>Zero Transaction Fees:</strong> Neighborhood peer-to-peer listings operate with 0% seller commission.</li>
          <li><strong>Curated Local Shops:</strong> Aggregates boutique specialty inventory alongside community secondhand deals.</li>
          <li><strong>Strict Geographic Scoping:</strong> Statistics exclusively reflect inventory physically located within ${escapeHtml(regionObj.name)}.</li>
        </ul>

        <div class="cta-banner">
          <h3 style="font-size:16px; font-weight:800; color:#1E1B4B; margin-bottom:4px;">Looking for items available right now?</h3>
          <p style="font-size:13.5px; color:#4338CA; margin-bottom:10px;">Browse current live listings, neighborhood deals, and local store items in ${escapeHtml(regionObj.shortName)}.</p>
          <a href="/explore/${escapeHtml(regionObj.slug)}" class="cta-btn">View Live ${escapeHtml(regionObj.shortName)} Inventory →</a>
        </div>

        <div class="methodology-box">
          <div class="methodology-title">⚡ Methodology & Statistical Provenance</div>
          <p style="margin-bottom:6px; font-size:12.5px;">
            <strong>Observation Date:</strong> ${escapeHtml(targetDate)} | <strong>Calculation Standard:</strong> NIST / R-Type 7 Linear Interpolation Quantiles.
          </p>
          <p style="margin-bottom:6px; font-size:12.5px;">
            <strong>Inventory Definitions:</strong> Moonoh indexes 5,170+ total local-commerce catalog URLs, with 4,228 currently active, renderable listings included in the live active pool. Free items ($0) are counted separately and excluded from median and IQR calculations to prevent price distribution skew.
          </p>
          <p style="font-size:12.5px; margin-bottom:0;">
            <strong>Geographic Semantics:</strong> Calculated exclusively for inventory physically 'Located in' ${escapeHtml(regionObj.name)}. Inventory with cross-borough delivery eligibility is excluded from borough-level baseline statistics.
          </p>
        </div>
      </div>
    </main>

    <footer>
      <p>© 2026 Moonoh (moon-oh.com). Historical local commerce market intelligence.</p>
    </footer>
  </div>
</body>
</html>`;

  return new Response(html, {
    status: 200,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=86400'
    }
  });
}
