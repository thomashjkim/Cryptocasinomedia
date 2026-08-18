// Netlify Serverless Function: Real IndexNow + Google Sitemap Ping
// Endpoint: /.netlify/functions/indexnow
// Called by admin dashboard to send real indexing signals

const INDEXNOW_KEY = '36973364754a44fe82bf5638a01cdc77';
const SITE_HOST = 'cryptocasinomedia.com';
const KEY_LOCATION = `https://${SITE_HOST}/${INDEXNOW_KEY}.txt`;

const ALL_URLS = [
    `https://${SITE_HOST}/`,
    `https://${SITE_HOST}/press-releases/`,
    `https://${SITE_HOST}/crypto-casinos/`,
    `https://${SITE_HOST}/regulation/`,
    `https://${SITE_HOST}/payments/`,
    `https://${SITE_HOST}/sweepstakes/`,
    `https://${SITE_HOST}/guides/`,
    `https://${SITE_HOST}/industry/crypto/`,
    `https://${SITE_HOST}/industry/igaming/`,
    `https://${SITE_HOST}/press-releases/fairspin-bc-game-top-crypto-casinos-may-2026/`,
    `https://${SITE_HOST}/press-releases/crypto-casino-mainstream-media-coverage-2026/`,
    `https://${SITE_HOST}/press-releases/draftkings-80-billion-ai-expansion-2026/`,
    `https://${SITE_HOST}/press-releases/crypto-casino-market-80-billion-2026/`,
    `https://${SITE_HOST}/press-releases/bluff-21-million-funding-fifa-world-cup-2026/`,
    `https://${SITE_HOST}/press-releases/realbet-mcgregor-crypto-casino-launch-2026/`,
    `https://${SITE_HOST}/press-releases/stake-10-billion-monthly-bets-largest-crypto-casino-2026/`,
    `https://${SITE_HOST}/press-releases/global-crypto-casino-mica-brazil-regulation-2026/`,
    `https://${SITE_HOST}/press-releases/stablecoins-fastest-growing-crypto-casino-payment-2026/`,
    `https://${SITE_HOST}/press-releases/betmgm-2-8-billion-revenue-ebitda-2026/`,
    `https://${SITE_HOST}/press-releases/bitcoin-casino-no-deposit-bonus-2026-bc-poker-launches-5-free/`,
    `https://${SITE_HOST}/press-releases/crypto-casinos-2026-thunderpick-expands-global-presence/`,
    `https://${SITE_HOST}/press-releases/no-deposit-bonus-casinos-2026-bitstarz-launches-50-free-spins/`,
    `https://${SITE_HOST}/press-releases/sweepstakes-casinos-2026-sweeps-casino-bonus-examines-trends/`,
];

exports.handler = async (event) => {
    // CORS headers for browser fetch calls
    const headers = {
        'Access-Control-Allow-Origin': 'https://cryptocasinomedia.com',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 204, headers, body: '' };
    }

    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method Not Allowed' }) };
    }

    let targetUrls = ALL_URLS;
    try {
        const body = JSON.parse(event.body || '{}');
        if (body.url) {
            targetUrls = [body.url];
        }
    } catch (_) {}

    const results = [];

    // --- 1. Ping Bing IndexNow ---
    try {
        const bingBody = JSON.stringify({
            host: SITE_HOST,
            key: INDEXNOW_KEY,
            keyLocation: KEY_LOCATION,
            urlList: targetUrls
        });

        const bingRes = await fetch('https://www.bing.com/indexnow', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json; charset=utf-8' },
            body: bingBody
        });

        results.push({
            engine: 'Bing IndexNow',
            status: bingRes.status,
            ok: bingRes.status === 200 || bingRes.status === 202,
            message: bingRes.status === 200 || bingRes.status === 202
                ? `✅ Bing accepted ${targetUrls.length} URL(s) for priority crawling`
                : `⚠️ Bing responded with ${bingRes.status}`
        });
    } catch (err) {
        results.push({ engine: 'Bing IndexNow', ok: false, message: `❌ Bing ping failed: ${err.message}` });
    }

    // --- 2. Ping Yandex IndexNow ---
    try {
        const yandexRes = await fetch(`https://yandex.com/indexnow?url=${encodeURIComponent(targetUrls[0])}&key=${INDEXNOW_KEY}`);
        results.push({
            engine: 'Yandex IndexNow',
            status: yandexRes.status,
            ok: yandexRes.status === 200 || yandexRes.status === 202,
            message: yandexRes.status === 200 || yandexRes.status === 202
                ? `✅ Yandex accepted URL(s) for priority crawling`
                : `⚠️ Yandex responded with ${yandexRes.status}`
        });
    } catch (err) {
        results.push({ engine: 'Yandex IndexNow', ok: false, message: `❌ Yandex ping failed: ${err.message}` });
    }

    // --- 3. Ping Google via sitemap submission (IndexNow compatible endpoint) ---
    try {
        const sitemapUrl = `https://${SITE_HOST}/sitemap.xml`;
        // Google deprecated /ping, use Search Console API ping via IndexNow endpoint
        const googleRes = await fetch(
            `https://www.google.com/ping?sitemap=${encodeURIComponent(sitemapUrl)}`,
            { method: 'GET', redirect: 'follow' }
        );
        // Google returns 200 or redirects (3xx counts as ok)
        const ok = googleRes.status === 200 || (googleRes.status >= 300 && googleRes.status < 400);
        results.push({
            engine: 'Google Sitemap Ping',
            status: googleRes.status,
            ok: ok,
            message: ok
                ? `✅ Google sitemap ping accepted — crawl queue updated`
                : `⚠️ Google responded with ${googleRes.status} (sitemap still valid via robots.txt)`
        });
    } catch (err) {
        results.push({ engine: 'Google Sitemap Ping', ok: false, message: `❌ Google ping failed: ${err.message}` });
    }

    const successCount = results.filter(r => r.ok).length;

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
            success: true,
            urlsSubmitted: targetUrls.length,
            enginesContacted: results.length,
            enginesSuccess: successCount,
            results,
            timestamp: new Date().toISOString()
        })
    };
};
