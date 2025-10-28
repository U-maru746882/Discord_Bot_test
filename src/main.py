import os
import requests
from datetime import datetime
import pytz

CITY = "Suzuka,JP"  # 鈴鹿市
FORECAST_HOURS = ["07:00", "12:00", "16:00", "20:00"]  # JSTで取得したい時間

def get_forecast(city=CITY):
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        data = requests.get(url).json()
        tz = pytz.timezone("Asia/Tokyo")
        forecast_messages = []

        for item in data["list"]:
            # UTC時刻をJSTに変換
            utc_time = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
            jst_time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)
            hour_min = jst_time.strftime("%H:%M")

            if hour_min in FORECAST_HOURS:
                weather = item["weather"][0]["description"]
                temp_min = item["main"]["temp_min"]
                temp_max = item["main"]["temp_max"]
                rain = item.get("rain", {}).get("3h", 0)
                forecast_messages.append(
                    f"{hour_min} 天気: {weather}, 最低: {temp_min}℃ / 最高: {temp_max}℃, 降水量: {rain} mm"
                )

        # 日付の見出し
        date_str = jst_time.strftime("%Y-%m-%d")
        message = f"**{date_str} {city}の天気予報**\n" + "\n".join(forecast_messages)
        return message
    except Exception as e:
        return f"天気情報の取得に失敗しました: {e}"

def main():
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
    message = get_forecast(CITY)
    
    response = requests.post(webhook_url, json={"content": message})
    try:
        response.raise_for_status()
        print("メッセージ送信成功")
    except Exception as e:
        print("メッセージ送信失敗", e)

if __name__ == "__main__":
    main()
