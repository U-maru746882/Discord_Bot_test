import os
import requests
from datetime import datetime
import pytz

CITY = "Suzuka,JP"
FORECAST_HOURS = ["06:00", "12:00", "15:00", "21:00"]  # JSTで抽出したい時間

# 天気英語→日本語マッピング
WEATHER_JP = {
    "clear sky": "晴れ",
    "few clouds": "晴れ時々曇り",
    "scattered clouds": "曇り時々晴れ",
    "broken clouds": "曇り",
    "overcast clouds": "曇り",
    "shower rain": "にわか雨",
    "rain": "雨",
    "thunderstorm": "雷雨",
    "snow": "雪",
    "mist": "霧"
}

def get_forecast(city=CITY):
    api_key = os.environ["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    try:
        data = requests.get(url).json()
        tz = pytz.timezone("Asia/Tokyo")
        forecast_messages = []

        jst_today = datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%d")

        for item in data["list"]:
            # UTC時間をdatetimeに変換
            utc_time = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
            # JSTに変換
            jst_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Tokyo"))
            hour_min = jst_time.strftime("%H:%M")

            # 今日の日付のみ対象
            if date_str != jst_today:
                continue

            # JSTで指定時間と比較
            if hour_min in FORECAST_HOURS:
                weather_en = item["weather"][0]["description"]
                weather = WEATHER_JP.get(weather_en, weather_en)
                temp_min = item["main"]["temp_min"]
                temp_max = item["main"]["temp_max"]
                rain = item.get("rain", {}).get("3h", 0)
                forecast_messages.append(
                    f"{hour_min}\n  天気: {weather}, 降水量: {rain} mm\n  最低: {temp_min}℃ / 最高: {temp_max}℃"
                )

        # 日付の見出し（最後に処理したJST時間を使用）
        date_str = datetime.now().strftime('%Y-%m-%d')
        message = f"**{date_str} 鈴鹿市の天気予報**\n" + "\n".join(forecast_messages)
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
