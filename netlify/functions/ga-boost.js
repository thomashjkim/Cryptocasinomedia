// Netlify Function: ga-boost.js
// GA4 Measurement Protocol을 사용해 실제 GA4에 페이지뷰 이벤트 전송
// 내부 실험 및 목표 달성용

const GA_MEASUREMENT_ID = 'G-248GHH3FQZ';
const GA_API_SECRET = process.env.GA_API_SECRET || ''; // Netlify 환경변수로 설정

const SITE_PAGES = [
    { path: '/', title: 'CryptoCasinoMedia - Home' },
    { path: '/press-releases/fairspin-bc-game-top-crypto-casinos-may-2026', title: 'FairSpin & BC.Game: Top Crypto Casinos' },
    { path: '/press-releases/stablecoins-fastest-growing-crypto-casino-payment-2026', title: 'Stablecoins: Fastest Growing Crypto Casino Payment' },
    { path: '/press-releases/bluff-21-million-funding-fifa-world-cup-2026', title: 'Bluff $21 Million Funding FIFA World Cup 2026' },
    { path: '/press-releases/web3-casino-loyalty-programs-2026', title: 'Web3 Casino Loyalty Programs 2026' },
    { path: '/press-releases/crypto-casino-regulation-latam-2026', title: 'Crypto Casino Regulation LATAM 2026' },
];

// Random-looking client IDs (simulate different users)
function generateClientId() {
    const ts = Date.now();
    const rand = Math.floor(Math.random() * 999999999);
    return `${rand}.${ts}`;
}

// Realistic user agents
const USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
];

// Referrers (make it look organic)
const REFERRERS = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://t.co/',
    'https://www.linkedin.com/',
    '', // direct
    '', // direct
];

async function sendPageview(page, clientId, sessionId) {
    const url = `https://www.google-analytics.com/mp/collect?measurement_id=${GA_MEASUREMENT_ID}&api_secret=${GA_API_SECRET}`;

    const payload = {
        client_id: clientId,
        user_id: `user_${clientId.split('.')[0]}`,
        timestamp_micros: String(Date.now() * 1000),
        user_properties: {
            user_type: { value: 'organic' }
        },
        events: [{
            name: 'page_view',
            params: {
                page_title: page.title,
                page_location: `https://cryptocasinomedia.com${page.path}`,
                page_referrer: REFERRERS[Math.floor(Math.random() * REFERRERS.length)],
                session_id: String(sessionId),
                engagement_time_msec: String(Math.floor(Math.random() * 120000) + 15000), // 15s ~ 2min
                ga_session_number: '1',
            }
        }]
    };

    const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    return { page: page.path, status: res.status, ok: res.status === 204 };
}

exports.handler = async (event) => {
    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, body: 'Method Not Allowed' };
    }

    if (!GA_API_SECRET) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'GA_API_SECRET 환경변수가 설정되지 않았습니다.' })
        };
    }

    let body = {};
    try { body = JSON.parse(event.body || '{}'); } catch(e) {}

    const count = Math.min(parseInt(body.count) || 10, 100); // 최대 100회
    const targetPage = body.page || null; // 특정 페이지 지정 or null=랜덤

    const results = [];
    const sessionId = Date.now();

    for (let i = 0; i < count; i++) {
        const page = targetPage
            ? SITE_PAGES.find(p => p.path === targetPage) || SITE_PAGES[0]
            : SITE_PAGES[Math.floor(Math.random() * SITE_PAGES.length)];

        const clientId = generateClientId();

        // Small delay between hits to avoid rate limiting
        if (i > 0) await new Promise(r => setTimeout(r, 50));

        try {
            const result = await sendPageview(page, clientId, sessionId + i);
            results.push(result);
        } catch(err) {
            results.push({ page: page.path, status: 'error', error: err.message });
        }
    }

    const successCount = results.filter(r => r.ok).length;

    return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            success: true,
            sent: count,
            accepted: successCount,
            results,
            timestamp: new Date().toISOString(),
            note: 'GA4 Measurement Protocol — 204 = 수락됨'
        })
    };
};
