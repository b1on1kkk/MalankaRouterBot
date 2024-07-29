from telebot import TeleBot
from telebot.types import Message

from utils import markup_factory

from constants import BOT_ANSWERS, CONNECTORS_TYPE_MARKUP, FIND_STATION_MARKUP

class CommandBotService:
    def __init__(self, bot: TeleBot):
        self.__bot = bot

    async def send_hello(self, message: Message):
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["start"])

    async def set_connector(self, message: Message):
        connectors_markup = markup_factory(CONNECTORS_TYPE_MARKUP)
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["choose_connector"], reply_markup=connectors_markup)

    async def find_charger(self, message: Message):
        station_markup = markup_factory(FIND_STATION_MARKUP, request_location=True)
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["find_charger"], reply_markup=station_markup)