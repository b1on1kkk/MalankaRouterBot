import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot

# constants
from constants import CONNECTORS_TYPE_MARKUP

from handlers import BotHandler

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

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

@bot.callback_query_handler(func=lambda call:call.data == "address1")
def test(call):
    new_keyboard = InlineKeyboardMarkup()
    new_button = InlineKeyboardButton(text="Показать на карте", callback_data="location1")
    new_back_button = InlineKeyboardButton(text="Назад", callback_data="back")
    new_keyboard.add(new_button, new_back_button)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Точнее адресс и какой то статус", reply_markup=new_keyboard)




### event ###
@bot.message_handler(func=lambda message: True)
def unsupported_text(message):
    bot_handler.event_unsupported_text(message=message)



# start bot
bot.infinity_polling()