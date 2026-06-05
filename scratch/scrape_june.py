import asyncio
import json
import time
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        print("🔌 Connecting to Chrome at localhost:9222...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        
        # Use existing page or create new one
        pages = context.pages
        page = pages[0] if pages else await context.new_page()
        
        # Make output dir
        report_dir = "/tmp/ccm_report_june"
        os.makedirs(report_dir, exist_ok=True)
        
        # GA4 Property ID
        prop_id = "538165528"
        
        # 1. GA4 Reports Hub (June 1 - June 5)
        print("📊 Loading GA4 Reports Hub...")
        reports_url = f"https://analytics.google.com/analytics/web/#/p{prop_id}/reports/reportinghub?params=_u.dateRange%3D20260601%2C20260605"
        await page.goto(reports_url, wait_until="domcontentloaded")
        await asyncio.sleep(12)  # Give plenty of time for GA4 dashboards to load
        await page.screenshot(path=f"{report_dir}/ga4_reports.png")
        reports_text = await page.inner_text("body")
        print("📸 Reports screenshot saved")
        
        # 2. GA4 Traffic Acquisition (June 1 - June 5)
        print("🚦 Loading GA4 Traffic Acquisition...")
        acq_url = f"https://analytics.google.com/analytics/web/#/p{prop_id}/reports/acquisition-traffic-acquisition?params=_u.dateRange%3D20260601%2C20260605"
        await page.goto(acq_url, wait_until="domcontentloaded")
        await asyncio.sleep(12)
        await page.screenshot(path=f"{report_dir}/ga4_acquisition.png")
        acq_text = await page.inner_text("body")
        print("📸 Acquisition screenshot saved")
        
        # 3. GA4 Engagement Pages (June 1 - June 5)
        print("📄 Loading GA4 Pages & Screens...")
        pages_url = f"https://analytics.google.com/analytics/web/#/p{prop_id}/reports/engagement-pages-and-screens?params=_u.dateRange%3D20260601%2C20260605"
        await page.goto(pages_url, wait_until="domcontentloaded")
        await asyncio.sleep(12)
        await page.screenshot(path=f"{report_dir}/ga4_pages.png")
        pages_text = await page.inner_text("body")
        print("📸 Pages screenshot saved")
        
        # 4. GSC Performance (Default Last 3 Months to cover June 1-5, we'll parse text or inspect the date selector later)
        print("🔍 Loading GSC Performance...")
        gsc_url = "https://search.google.com/search-console/performance/search-analytics?resource_id=https%3A%2F%2Fcryptocasinomedia.com%2F"
        await page.goto(gsc_url, wait_until="domcontentloaded")
        await asyncio.sleep(12)
        await page.screenshot(path=f"{report_dir}/gsc_performance.png")
        gsc_perf_text = await page.inner_text("body")
        print("📸 GSC Performance screenshot saved")
        
        # 5. GSC Index Coverage
        print("📑 Loading GSC Index...")
        gsc_index_url = "https://search.google.com/search-console/index?resource_id=https%3A%2F%2Fcryptocasinomedia.com%2F"
        await page.goto(gsc_index_url, wait_until="domcontentloaded")
        await asyncio.sleep(10)
        await page.screenshot(path=f"{report_dir}/gsc_index.png")
        gsc_index_text = await page.inner_text("body")
        print("📸 GSC Index screenshot saved")
        
        # Save all data
        all_data = {
            "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "property_id": prop_id,
            "ga4_reports": reports_text[:6000],
            "ga4_acquisition": acq_text[:6000],
            "ga4_pages": pages_text[:6000],
            "gsc_performance": gsc_perf_text[:6000],
            "gsc_index": gsc_index_text[:6000],
        }
        
        with open(f"{report_dir}/data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
            
        print("\n🎉 All June data collected successfully!")

if __name__ == "__main__":
    asyncio.run(main())
