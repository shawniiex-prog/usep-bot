import asyncio
from playwright.async_api import async_playwright
from telegram import Bot
import os
import re

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://www.nems.emcsg.com/nems-prices"

async def fetch_usep(retries=3):
    for attempt in range(1, retries+1):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(URL, timeout=60000)
                text = await page.inner_text("body")
                await browser.close()
                # regex to find USEP number
                match = re.search(r"Uniform Singapore Energy Price.*?([\d,.]+)", text, re.IGNORECASE)
                if match:
                    return match.group(1)
                print(f"[Attempt {attempt}] Could not find USEP in page text.")
        except Exception as e:
            print(f"[Attempt {attempt}] Error fetching USEP:", e)
        await asyncio.sleep(5)
    return None

async def send_usep():
    bot = Bot(token=TELEGRAM_TOKEN)
    usep = await fetch_usep()
    message = f"Current USEP: {usep} $/MWh" if usep else "Could not retrieve USEP value."
    print("Sending message:", message)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Error sending Telegram message:", e)

if __name__ == "__main__":
    asyncio.run(send_usep())