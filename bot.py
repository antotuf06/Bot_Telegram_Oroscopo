import os
import requests
import telebot
from typing import Any
from telebot import types
BOT_TOKEN = os.environ['BOT_TOKEN'].strip()


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, the bot is ready, type '/horoscope' to get your daily horoscope!")

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text= "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope)

def get_daily_horoscope(sign: str):
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign.lower(), "day": "TODAY"}
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



def fetch_horoscope(message):
    sign = message.text.strip()
    horoscope = get_daily_horoscope(sign)
    data=horoscope.get("data")
    if data and ("horoscope" in data or "horoscope_data" in data):
        horoscope_text = data.get("horoscope") or data.get("horoscope_data")
        api_date = data.get("date", "")

        # Mostra sia il giorno scelto dall'utente sia la data dell'API se presente
        horoscope_message = (
            f"*Horoscope:* {horoscope_text}\n"
            f"*Sign:* {sign.capitalize()}"
            + (f" ({api_date})" if api_date else "")
        )

        bot.send_message(message.chat.id, "Here's your horoscope:")
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Unable to fetch horoscope. Make sure you've entered the sign correctly.")
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
