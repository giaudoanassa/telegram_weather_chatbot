import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Xin chào! Gửi cho tôi tên của thành phố và tôi sẽ gửi cho bạn báo cáo thời tiết!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Troi sáng \U00002600",
        "Clouds": "Nhiều mây \U00002601",
        "Rain": "Mưa \U00002614",
        "Drizzle": "Mưa phùn \U00002614",
        "Thunderstorm": "Dông \U000026A1",
        "Snow": "Tuyết \U0001F328",
        "Mist": "Sương mù \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Nhìn ra ngoài cửa sổ, tôi không hiểu thời tiết ở đó như thế nào!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Thời tiết trong thành phố: {city}\nNhiệt độ: {cur_weather}C° {wd}\n"
              f"Độ ẩm: {humidity}%\náp suất: {pressure} мм.рт.ст\nGió: {wind} м/с\n"
              f"Bình Minh: {sunrise_timestamp}\nHoàng hôn: {sunset_timestamp}\nĐộ dài ngày: {length_of_the_day}\n"
              f"***Chúc bạn ngày mới tốt lành!***"
              )

    except:
        await message.reply("\U00002620 Kiểm tra tên thành phố \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)