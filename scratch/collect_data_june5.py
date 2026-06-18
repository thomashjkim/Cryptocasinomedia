import asyncio, json, time, os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("🔌 Connecting to Chrome at localhost:9222...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]

        pages = context.pages
        page = pages[0] if pages else await context.new_page()

        os.makedirs("/tmp/ccm_report_june5", exist_ok=True)

        print("\n🔍 Navigating to Google Search Console (Last 28 days)...")
        gsc_url = "https://search.google.com/search-console/performance/search-analytics?resource_id=https%3A%2F%2Fcryptocasinomedia.com%2F&num_of_days=28"
        await page.goto(gsc_url, wait_until="domcontentloaded")
        await asyncio.sleep(8)
        await page.screenshot(path="/tmp/ccm_report_june5/gsc_performance.png")
        gsc_perf_text = await page.inner_text("body")

        gsc_index_url = "https://search.google.com/search-console/index?resource_id=https%3A%2F%2Fcryptocasinomedia.com%2F"
        await page.goto(gsc_index_url, wait_until="domcontentloaded")
        await asyncio.sleep(6)
        await page.screenshot(path="/tmp/ccm_report_june5/gsc_index.png")
        gsc_index_text = await page.inner_text("body")

        all_data = {
            "gsc_performance": gsc_perf_text[:8000],
            "gsc_index": gsc_index_text[:8000],
        }

        with open("/tmp/ccm_report_june5/data.json", "w") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        print("\n🎉 Data collected!")

asyncio.run(main())
