import os
import requests
import telebot
from typing import Any
BOT_TOKEN = os.environ['BOT_TOKEN'].strip()


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Ciao, il bot è pronto!")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text= "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def get_daily_horoscope(sign: str, day: str):
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign.lower(), "day": day.upper()}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass

    return {}



def day_handler(message):
    sign = message.text.strip()
    text = "What day would you like to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format (YYYY-MM-DD)."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.lower())

def fetch_horoscope(message, sign):
    day = message.text.strip().upper()
    horoscope = get_daily_horoscope(sign, day)
    data=horoscope.get("data")
    if data and "horoscope" in data:
        horoscope_message = f"*Horoscope:* {data['horoscope']}\n*Sign:* {sign.capitalize()}\n*Day:* {data.get('date', day)}"
        bot.send_message(message.chat.id, "Here's your horoscope:")
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Impossibile recuperare l'oroscopo. Assicurati di aver inserito correttamente il segno e la data.")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
