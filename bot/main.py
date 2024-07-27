import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot

# constants
from constants import CONNECTORS_TYPE_MARKUP

from handlers import BotHandler

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils import sub_menu, main_menu

###########################################################################
bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)
bot_handler = BotHandler(bot)


### commands ###
@bot.message_handler(commands=["start"])
def start_bot(message):
    bot_handler.command_start_bot(message=message)

@bot.message_handler(commands=["setconnector"])
def choose_connector(message):
    bot_handler.command_choose_connector(message=message)

@bot.message_handler(commands=['find'])
def find(message):
    bot_handler.command_find_station(message=message)



### query ###
@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot_handler.query_handle_location(message=message)

@bot.message_handler(func=lambda connector_type: connector_type.text in CONNECTORS_TYPE_MARKUP)
def connect_type(message):
    bot_handler.query_connector_type(message=message)





##############################################IN DEVELOPMENT##############################################

### callbacks ###
@bot.callback_query_handler(func=lambda call:call.data == "m1")
def test(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Точнее адресс + статус", reply_markup=sub_menu())

@bot.callback_query_handler(func=lambda call:call.data == "main")
def test(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот 3 ближайшии станции.", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call:call.data.startswith("charger_location"))
def test(call):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="delete", callback_data="delete_location")],
    ])

    bot.send_location(chat_id=call.message.chat.id, latitude=53.95809, longitude=27.7, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:call.data == "delete_location")
def test(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

##############################################IN DEVELOPMENT##############################################





### event ###
@bot.message_handler(func=lambda message: True)
def unsupported_text(message):
    bot_handler.event_unsupported_text(message=message)



# start bot
bot.infinity_polling()