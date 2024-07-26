import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import requests

# constants
from constants import CONNECTORS_TYPE

# models
from models import ChargingPoint, List

bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

# commands handlers
@bot.message_handler(commands=["start"])
def start_bot(message):
    start_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    nearby_chargers = KeyboardButton("Ближайшие зарядки", request_location=True)
    start_markup.add(nearby_chargers)

    bot.send_message(message.chat.id, "Привет! Я помогу тебе подобрать ближайшие совободные зарядные станции под твои критерии. Выбери, пожалуйста, коннектор, который тебя интересует.", reply_markup=start_markup)

@bot.message_handler(commands=["setconnector"])
def choose_connector(message):
    connectors_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for connector in CONNECTORS_TYPE.keys():
        item_button = KeyboardButton(connector)
        connectors_markup.add(item_button)

    bot.send_message(message.chat.id, "Давай подберем нужный тебе коннектор...", reply_markup=connectors_markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    print(message.location)

    response: List[ChargingPoint] = [ChargingPoint(**station) for station in (requests.get(os.getenv("CHARGING_POINTS_API")).json())]
    
    print(response[0].city)

# handlers
@bot.message_handler(func=lambda connector_type: connector_type.text in CONNECTORS_TYPE)
def connect_type(message):
    bot.send_message(message.chat.id, "Коннектор определен!", reply_markup=ReplyKeyboardRemove())

# error text
@bot.message_handler(func=lambda message: True)
def unsupported_text(message):
    bot.send_message(message.chat.id, "Я Вас не понял, выберите правильную команду!")

# start bot
bot.infinity_polling()