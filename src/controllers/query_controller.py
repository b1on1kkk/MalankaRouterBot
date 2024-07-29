import asyncio
from telebot import TeleBot, types

from services import QueryBotService

from constants import CONNECTORS_TYPE_MARKUP

import asyncpg

class QueryBotController:
    def __init__(self, bot: TeleBot, connection: asyncpg.Connection | None):
        self.__bot = bot
        self.__register_handlers()
        
        self.__bot_service = QueryBotService(bot, connection)

    def __register_handlers(self):
        self.__bot.message_handler(content_types=["location"])(self.__get_location)
        self.__bot.message_handler(func=lambda type: type.text in CONNECTORS_TYPE_MARKUP)(self.__set_connector_type)
        self.__bot.message_handler(func=lambda msg: True)(self.__unknown)

    async def __get_location(self, message: types.Message):
        await self.__bot_service.get_location(message)

    async def __set_connector_type(self, message: types.Message):
        await asyncio.create_task(self.__bot_service.set_connector_type(message))

    async def __unknown(self, message: types.Message):
        await self.__bot_service.unknown(message)