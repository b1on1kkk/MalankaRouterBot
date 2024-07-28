from telebot import TeleBot, types

from utils import markup_factory

from constants import BOT_ANSWERS, CONNECTORS_TYPE_MARKUP, FIND_STATION_MARKUP

class CommandBotService:
    def __init__(self, bot: TeleBot) -> None:
        self.__bot = bot

    def send_hello(self, message: types.Message) -> None:
        self.__bot.send_message(message.chat.id, BOT_ANSWERS["start"])

    def set_connector(self, message: types.Message) -> None:
        connectors_markup = markup_factory(CONNECTORS_TYPE_MARKUP)
        self.__bot.send_message(message.chat.id, BOT_ANSWERS["choose_connector"], reply_markup=connectors_markup)

    def find_charger(self, message: types.Message) -> None:
        station_markup = markup_factory(FIND_STATION_MARKUP, request_location=True)
        self.__bot.send_message(message.chat.id, BOT_ANSWERS["find_charger"], reply_markup=station_markup)