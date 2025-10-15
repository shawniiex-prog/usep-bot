import requests
import csv
from io import StringIO
from telegram import Bot
import os
from datetime import datetime

# Telegram bot info
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# NEMS CSV URL for USEP data
CSV_URL = "https://www.nems.emcsg.com/nems-prices?download=csv"

def fetch_latest_usep():
    try:
        response = requests.get(CSV_URL, timeout=30)
        response.raise_for_status()

        # Read CSV content
        csv_file = StringIO(response.text)
        reader = csv.DictReader(csv_file)

        # Collect all USEP entries with their timestamp
        usep_entries = []
        for row in reader:
            if "Uniform Singapore Energy Price" in row and "Trading Interval" in row:
                ts_str = row["Trading Interval"]  # e.g., 2025-10-15 12:30
                try:
                    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M")
                    value = row["Uniform Singapore Energy Price"]
                    usep_entries.append((ts, value))
                except Exception:
                    continue

        if not usep_entries:
            return None

        # Sort by timestamp and get the latest
        latest_ts, latest_usep = sorted(usep_entries, key=lambda x: x[0])[-1]
        return latest_usep, latest_ts

    except Exception as e:
        print("Error fetching USEP:", e)
        return None, None

def send_telegram_message(message):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print("Error sending Telegram message:", e)

if __name__ == "__main__":
    usep, ts = fetch_latest_usep()
    if usep:
        message = f"Latest USEP ({ts}): {usep} $/MWh"
    else:
        message = "Could not retrieve USEP value."
    print(message)
    send_telegram_message(message)
