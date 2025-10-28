# ==================================================================================================== #

import os
import requests
from datetime import datetime

# ==================================================================================================== #

def main():
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"📅 {now} のお知らせです！\n今日も一日がんばりましょう ☀️"

    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

# ==================================================================================================== #

if __name__ == "__main__":
    main()

# ==================================================================================================== #