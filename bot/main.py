import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot

# constants
from constants import CONNECTORS_TYPE

from handlers import BotHandler

bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)
bot_handler = BotHandler(bot)

### commands ###
@bot.message_handler(commands=["start"])
def start_bot(message):
    bot_handler.command_start_bot(message=message)

@bot.message_handler(commands=["setconnector"])
def choose_connector(message):
    bot_handler.command_choose_connector(message=message)

### query ###
@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot_handler.query_handle_location(message=message)

@bot.message_handler(func=lambda connector_type: connector_type.text in CONNECTORS_TYPE)
def connect_type(message):
    bot_handler.query_connect_type(message=message)

### event ###
@bot.message_handler(func=lambda message: True)
def unsupported_text(message):
    bot_handler.event_unsupported_text(message=message)

# start bot
bot.infinity_polling()