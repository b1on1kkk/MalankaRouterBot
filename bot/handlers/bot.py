import os
import json
import requests

from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove

from db import DatabaseRepository

import decorators.user_existance
from models import ChargingPoint, List

from utils import reply_markup_factory, main_menu

from constants import CONNECTORS_TYPE_MARKUP, BOT_ANSWERS, FIND_STATION_MARKUP

from decorators import user_existance

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

    @user_existance
    def command_find_station(self, message):
        station_markup = reply_markup_factory(FIND_STATION_MARKUP, request_location=True)
        self._bot.send_message(message.chat.id, BOT_ANSWERS["find_charger"], reply_markup=station_markup)



    ### query ###
    @user_existance
    def query_handle_location(self, message):
        self._bot.send_message(message.chat.id, "Местоположение установлено!", reply_markup=ReplyKeyboardRemove())

        # print(message.from_user.id)
        # response: List[ChargingPoint] = [ChargingPoint(**station) for station in (requests.get(os.getenv("CHARGING_POINTS_API")).json())]
        # print(response[0].city)

        self._bot.send_message(message.chat.id, "Вот 3 ближайшии станции.", reply_markup=main_menu())

    def query_connector_type(self, message):
        res = None

        if self.__repository.find_user_by_id(message.from_user.id):
            res = self.__repository.update_user(user_id=message.from_user.id, connector=message.text)
        else:
            res = self.__repository.create_user(user_id=message.from_user.id, connector=message.text)

        self._bot.send_message(message.chat.id, res, reply_markup=ReplyKeyboardRemove())



    ### event ###
    def event_unsupported_text(self, message):
        self._bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])
