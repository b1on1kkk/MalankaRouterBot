import asyncio
from telebot import TeleBot

from asyncpg import Connection
from redis.asyncio import Redis
from telebot.types import Message

from services import QueryBotService

from decorators import UnkConn

from interfaces import User

from constants import CONNECTORS_TYPE_MARKUP

class QueryBotController:
    def __init__(self, bot: TeleBot, connection: Connection | None, redis: Redis | None):
        self.__bot = bot
        self.__register_handlers()

        self.__bot_service = QueryBotService(bot, connection, redis)

        # for inner purposes before implementing DI (here is using in decorator)
        self.connection = connection


    def __register_handlers(self):
        self.__bot.message_handler(content_types=["location"])(self.__get_location)
        self.__bot.message_handler(func=lambda type: type.text in CONNECTORS_TYPE_MARKUP)(self.__set_connector_type)
        self.__bot.message_handler(func=lambda msg: True)(self.__unknown)


    @UnkConn
    async def __get_location(self, message: Message, user: User):
        await self.__bot_service.get_location(message, user)


    async def __set_connector_type(self, message: Message):
        await asyncio.create_task(self.__bot_service.set_connector_type(message))


    async def __unknown(self, message: Message):
        await self.__bot_service.unknown(message)