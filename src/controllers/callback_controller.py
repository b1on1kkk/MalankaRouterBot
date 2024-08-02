from telebot import TeleBot
from redis.asyncio import Redis
from telebot.types import CallbackQuery

from services import CallbackBotService

class CallbackBotController:
    def __init__(self, bot: TeleBot, redis: Redis | None):
        self.__bot = bot
        self.__register_handlers()

        self.__bot_service = CallbackBotService(bot, redis)


    def __register_handlers(self):
        self.__bot.callback_query_handler(func=lambda call: call.data == "delete")(self.__delete_location)
        self.__bot.callback_query_handler(func=lambda call: call.data.startswith("loc"))(self.__send_location)


    async def __send_location(self, call: CallbackQuery):
        await self.__bot_service.send_location(call)


    async def __delete_location(self, call:CallbackQuery):
        await self.__bot_service.delete_location(call)