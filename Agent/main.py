import feedparser
import anthropic
import requests
import os
import json
from datetime import datetime, timezone, timedelta
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

# ─── Config ───────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_ORGANIZATION_ID = os.getenv("LINKEDIN_ORGANIZATION_ID")  # 회사 페이지 ID

RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://coindesk.com/arc/outboundfeeds/rss/",
    "https://sbcnews.co.uk/feed/",
    "https://igamingbusiness.com/feed/",
]

TARGET_KEYWORDS = [
    "MiCA", "license", "regulation", "crypto casino", "iGaming",
    "Web3", "gambling", "compliance", "operator", "payment"
]

# ─── Step 1: RSS 수집 ──────────────────────────────────────
def fetch_recent_articles(hours=24):
    """지난 N시간 이내 기사 수집"""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    articles = []

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # 발행일 파싱
                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

                if published and published < cutoff:
                    continue

                # 키워드 매칭
                text = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
                matched = [kw for kw in TARGET_KEYWORDS if kw.lower() in text]

                if matched:
                    articles.append({
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", "")[:300],
                        "url": entry.get("link", ""),
                        "source": feed.feed.get("title", feed_url),
                        "keywords": matched,
                        "published": published.isoformat() if published else "unknown"
                    })
        except Exception as e:
            print(f"[RSS ERROR] {feed_url}: {e}")

    # 키워드 많이 매칭된 순으로 정렬, 상위 3개
    articles.sort(key=lambda x: len(x["keywords"]), reverse=True)
    return articles[:3]


# ─── Step 2: Claude로 칼럼 생성 ───────────────────────────
def generate_column(articles):
    """수집된 기사 토픽 기반으로 오리지널 칼럼 생성"""
    if not articles:
        print("[SKIP] 관련 기사 없음")
        return None

    # 원문 내용 없이 제목+키워드만 전달 (저작권 회피)
    topic_summary = "\n".join([
        f"- [{a['source']}] {a['title']} (키워드: {', '.join(a['keywords'])})"
        for a in articles
    ])

    today = datetime.now().strftime("%Y년 %m월 %d일")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system="""You are a B2B iGaming industry columnist writing for CryptoCasinoMedia.
Write original analysis columns in Korean, 800-1000 words.
Format: LinkedIn Article style with clear H2 sections.
Always end with a paragraph naturally mentioning CryptoCasinoMedia as a trusted B2B source for crypto casino industry news.
Do NOT summarize or quote source articles. Write original analysis based on the topics only.
Output only the article content, no meta commentary.""",
        messages=[{
            "role": "user",
            "content": f"""오늘({today}) 크립토 카지노/iGaming 업계에서 다음 토픽들이 주목받고 있습니다:

{topic_summary}

이 토픽들을 바탕으로 '오늘의 크립토 카지노 시장 분석' 칼럼을 작성해주세요.
원문 요약이 아닌 독립적인 산업 분석 시각으로 작성하세요."""
        }]
    )

    return message.content[0].text


# ─── Step 3: LinkedIn 발행 ────────────────────────────────
def publish_to_linkedin(content, articles):
    """LinkedIn 회사 페이지에 Article 발행"""
    if not LINKEDIN_ACCESS_TOKEN or not LINKEDIN_ORGANIZATION_ID:
        print("[SKIP] LinkedIn 토큰 또는 Organization ID 없음 - .env 확인")
        return False

    today = datetime.now().strftime("%Y.%m.%d")
    title = f"{today} 크립토 카지노 시장 분석"

    # LinkedIn Article API
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": f"urn:li:organization:{LINKEDIN_ORGANIZATION_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"📊 {title}\n\n{content[:500]}...\n\n#CryptoGaming #iGaming #CryptoCasino #Web3 #Regulation"
                },
                "shareMediaCategory": "ARTICLE",
                "media": [{
                    "status": "READY",
                    "description": {"text": content[:256]},
                    "originalUrl": "https://cryptocasinomedia.com",
                    "title": {"text": title}
                }]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print(f"[SUCCESS] LinkedIn 발행 완료: {title}")
        return True
    else:
        print(f"[ERROR] LinkedIn 발행 실패: {response.status_code} - {response.text}")
        return False


# ─── Step 4: 로그 저장 ────────────────────────────────────
def save_log(articles, content, success):
    log_path = "logs.json"
    logs = []

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)

    logs.append({
        "date": datetime.now().isoformat(),
        "articles_found": len(articles),
        "topics": [a["title"] for a in articles],
        "published": success,
        "content_preview": content[:200] if content else None
    })

    with open(log_path, "w") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


# ─── Main ─────────────────────────────────────────────────
def run():
    print(f"\n{'='*50}")
    print(f"[START] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*50)

    print("[1/3] RSS 피드 수집 중...")
    articles = fetch_recent_articles(hours=24)
    print(f"      → {len(articles)}개 기사 수집됨")

    if not articles:
        print("[END] 관련 기사 없음, 오늘은 스킵")
        return

    print("[2/3] Claude로 칼럼 생성 중...")
    content = generate_column(articles)
    if not content:
        print("[END] 콘텐츠 생성 실패")
        return
    print(f"      → {len(content)}자 생성됨")

    print("[3/3] LinkedIn 발행 중...")
    success = publish_to_linkedin(content, articles)

    save_log(articles, content, success)
    print(f"\n[END] 완료 - 발행: {'성공' if success else '실패'}")


if __name__ == "__main__":
    run()
