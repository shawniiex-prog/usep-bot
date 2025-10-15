import requests
import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

API_URL = "https://www.nems.emcsg.com/api/DataSync/Get?value=10&fromDate=&toDate="

def fetch_latest_usep():
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Navigate through the structure
        usep = data["data"]["data"][0]["current"][0]["value"]
        time_label = data["data"]["data"][0]["currentdate"]
        last_update = data["data"]["data"][0]["lastupdate"]

        return usep, time_label, last_update

    except Exception as e:
        print("Error fetching USEP:", e)
        return None, None, None

def send_telegram_message(message):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Error sending Telegram message:", e)

if __name__ == "__main__":
    usep, time_label, last_update = fetch_latest_usep()
    if usep:
        message = (
            f"⚡ USEP Update ⚡\n\n"
            f"Current Price: {usep} $/MWh\n"
            f"Interval: {time_label}\n"
            f"Last Updated: {last_update}"
        )
    else:
        message = "❌ Could not retrieve the USEP value from the API."

    print(message)
    send_telegram_message(message)
