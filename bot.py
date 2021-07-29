# чтобы установить необходимые бибилиотеки, введите в консоль следующее:
# pip install aiogram
# pip install requests

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
import requests
import datetime

# импорт данных для работы с ботом
from config import token_bot, weather_token, weather_url

bot = Bot(token=token_bot, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# далее - команды, которые умеет обрабатывать бот

# команда "/start"
@dp.message_handler(CommandStart())
async def start_command(start_command: types.Message):
    await bot.send_message(chat_id=start_command.chat.id, text=f'\U0000263A Добро пожаловать, {start_command.chat.first_name}! Чтобы узнать погоду в своём городе, напишите его название в чат')

# команда "/help"
@dp.message_handler(CommandHelp())
async def help_command(help_command: types.Message):
    await bot.send_message(chat_id=help_command.chat.id, text='Чтобы узнать погоду в своём городе, напишите его название в чат')

# поиск погоды в городе, название которого вводит пользователь
@dp.message_handler(content_types='text')
async def city_weather(city: types.Message):

    try:
        # поиск информации о погодных условиях города и их запись в переменные
        params = {'q': city.text, 'appid': weather_token, 'units': 'metric', 'lang': 'ru'}
        search = requests.get(weather_url, params=params)
        weather = search.json()

        temperature = weather['main']['temp']
        feels_like = weather['main']['feels_like']
        humidity = weather['main']['humidity']
        pressure = weather['main']['pressure']
        wind_speed = weather['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M %d.%m.%Y')
        sunset = datetime.datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M %d.%m.%Y')
        general_weather = weather['weather'][0]['main']

        # обработка информации об общем состоянии погоды (general_weather) и создание соответствующих строчек с эмодзи
        emoji_plus_gen_weath = {'Thunderstorm': '\U000026A1 Сейчас гроза', 'Drizzle': '\U0001F4A7 Сейчас морось',
                                'Rain': '\U0001F4A7 Сейчас дождь', 'Snow': '\U00002744 Сейчас снег', 'Mist': '\U0001F32B Сейчас туман',
                                'Fog': '\U0001F32B Сейчас туман', 'Clear': '\U00002600 Сейчас ясно', 'Clouds': '\U00002601 Сейчас облачно'}

        if general_weather in emoji_plus_gen_weath:
            em_gw = emoji_plus_gen_weath[general_weather]
        else:
            em_gw = 'К сожалению, бот не может определить общее состояние погоды на данный момент'

        # вывод данных пользователю
        await bot.send_message(chat_id=city.chat.id, text=f'Населённый пункт: {city.text.title()}\n\n{em_gw}'
                                                          f'\n\nТемпература: {round(temperature)}°C'
                                                          f'\nОщущается как: {round(feels_like)}°C'
                                                          f'\nВлажность: {humidity}%\nДавление: {pressure} мм рт. ст.'
                                                          f'\nСкорость ветра: {wind_speed} м/c'
                                                          f'\n\nВосход солнца: {sunrise}\nЗакат солнца: {sunset}')

        await bot.send_message(chat_id=city.chat.id, text='Спасибо за то, что пользуетесь нашим ботом! \U00002764')

    except Exception:

        await bot.send_message(chat_id=city.chat.id, text='К сожалению, в базе данных нет Вашего города. Возможно, Вы ошиблись при вводе.')

executor.start_polling(dp)
