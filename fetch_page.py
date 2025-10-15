import asyncio
from playwright.async_api import async_playwright

async def fetch_page_content():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.nems.emcsg.com/nems-prices", timeout=60000)
        content = await page.content()
        await browser.close()
        print(content[:1000])  # print first 1000 chars for inspection

if __name__ == "__main__":
    asyncio.run(fetch_page_content())
