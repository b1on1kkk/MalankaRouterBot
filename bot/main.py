import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from constants import CONNECTORS_TYPE

bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

# commands
@bot.message_handler(commands=["start"])
def start_bot(message):
    connectors_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    for connector in CONNECTORS_TYPE.keys():
        item_button = KeyboardButton(connector)
        connectors_markup.add(item_button)

    bot.send_message(message.chat.id, "Привет! Я помогу тебе подобрать ближайшие совободные зарядные станции под твои критерии. Выбери, пожалуйста, коннектор, который тебя интересует.", reply_markup=connectors_markup)

@bot.message_handler(commands=["connector"])
def choose_connector(message):
    bot.send_message(message.chat.id, "сейчас подберем коннектор")

# handlers
@bot.message_handler(func=lambda connector_type: connector_type.text in CONNECTORS_TYPE)
def connect_type(connector_type):
    print(connector_type.text)

# error text
@bot.message_handler(func=lambda message: True)
def unsupported_text(message):
    bot.send_message(message.chat.id, "Я Вас не понял, выберите команду!")

# start bot
bot.infinity_polling()