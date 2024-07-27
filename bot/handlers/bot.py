import os
import requests

from telebot import TeleBot

from db import DatabaseRepository

from models import ChargingPoint, List

from utils import reply_markup_factory

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from constants import CONNECTORS_TYPE_MARKUP, BOT_ANSWERS, FIND_STATION_MARKUP

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
        self._bot.send_message(message.chat.id, BOT_ANSWERS["start"])

    def command_choose_connector(self, message):
        connectors_markup = reply_markup_factory(CONNECTORS_TYPE_MARKUP)
        self._bot.send_message(message.chat.id, BOT_ANSWERS["choose_connector"], reply_markup=connectors_markup)

    def command_find_station(self, message):
        station_markup = reply_markup_factory(FIND_STATION_MARKUP, request_location=True)
        self._bot.send_message(message.chat.id, BOT_ANSWERS["find_charger"], reply_markup=station_markup)



    ### query ###
    def query_handle_location(self, message):
        print(message)

        response: List[ChargingPoint] = [ChargingPoint(**station) for station in (requests.get(os.getenv("CHARGING_POINTS_API")).json())]

        print(response[0].city)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Какой то адрес тут", callback_data="address1")],
            [InlineKeyboardButton(text="Какой то адрес тут", callback_data="address2")],
            [InlineKeyboardButton(text="Какой то адрес тут", callback_data="address3")]
        ])

        self._bot.send_message(message.chat.id, "Вот 3 ближайшии станции.", reply_markup=keyboard)

    def query_connector_type(self, message):
        self._bot.send_message(message.chat.id, BOT_ANSWERS["connector_type"])



    ### event ###
    def event_unsupported_text(self, message):
        self._bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])
