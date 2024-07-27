import os
import requests

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from db import DatabaseRepository

from models import ChargingPoint, List

from constants import CONNECTORS_TYPE

class BotHandler:
    def __init__(self, bot: TeleBot):
        self._bot = bot
        self.__repository = DatabaseRepository(
            database=os.getenv("POSTGRES_DB"), 
            user=os.getenv("POSTGRES_USER"), 
            password=os.getenv("POSTGRES_PASSWORD"))

        # connect to database 
        self.__repository.db_connect()

    ### commands ###
    def command_start_bot(self, message):
        print(message.from_user.id)

        start_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        nearby_chargers = KeyboardButton("Ближайшие зарядки", request_location=True)
        start_markup.add(nearby_chargers)

        self._bot.send_message(message.chat.id, "Привет! Я помогу тебе подобрать ближайшие свободные зарядные станции под твои критерии.", reply_markup=start_markup)
    
    def command_choose_connector(self, message):
        connectors_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        for connector in CONNECTORS_TYPE.keys():
            item_button = KeyboardButton(connector)
            connectors_markup.add(item_button)

        self._bot.send_message(message.chat.id, "Давай подберем нужный тебе коннектор...", reply_markup=connectors_markup)

    ### query ###
    def query_handle_location(self, message):
        response: List[ChargingPoint] = [ChargingPoint(**station) for station in (requests.get(os.getenv("CHARGING_POINTS_API")).json())]
        
        print(response[0].city)
    
    def query_connect_type(self, message):
        self._bot.send_message(message.chat.id, "Коннектор определен!", reply_markup=ReplyKeyboardRemove())

    ### event ###
    def event_unsupported_text(self, message):
        self._bot.send_message(message.chat.id, "Я Вас не понял, выберите правильную команду!", reply_markup=ReplyKeyboardRemove())
