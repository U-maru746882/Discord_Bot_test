# ---------------------------------------------------------------------------------------------------- #

import os
import requests
from datetime import datetime

# ---------------------------------------------------------------------------------------------------- #

def get_weather(city="Suzuka,JP"):
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        data = requests.get(url).json()
        # 天気
        weather_desc = data["weather"][0]["description"]
        # 気温
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        # 降水量（rainがある場合のみ）
        rain = data.get("rain", {}).get("1h", 0)  # 直近1時間の降水量（mm）
        
        message = (
            f"##{datetime.now().strftime('%Y-%m-%d')}\n"
            f"天気: {weather_desc}\n"
            f"最低気温: {temp_min}℃\n最高気温: {temp_max}℃\n"
            f"降水量（直近1h）: {rain} mm"
        )
        return message
    except Exception as e:
        return f"天気情報の取得に失敗しました: {e}"

def main():
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
    city = "Suzuka,JP"
    message = get_weather(city)
    
    response = requests.post(webhook_url, json={"content": message})
    try:
        response.raise_for_status()
        print("メッセージ送信成功")
    except Exception as e:
        print("メッセージ送信失敗", e)

# ---------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------------------------------- #