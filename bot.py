import asyncio
from playwright.async_api import async_playwright
from telegram import Bot
import os
import re

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.nems.emcsg.com/nems-prices"

async def fetch_usep():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL, timeout=60000)
        await page.wait_for_selector("text=Uniform Singapore Energy Price", timeout=60000)
        text = await page.inner_text("body")
        await browser.close()
        match = re.search(r"Uniform Singapore Energy Price.*?([\d,.]+)", text)
        return match.group(1) if match else None

async def send_usep():
    bot = Bot(token=TELEGRAM_TOKEN)
    usep = await fetch_usep()
    message = f"Current USEP: {usep} $/MWh" if usep else "Could not retrieve USEP value."
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(send_usep())
