from telebot import TeleBot
from telebot.types import CallbackQuery

from services import CallbackBotService

class CallbackBotController:
    def __init__(self, bot: TeleBot):
        self.__bot = bot
        self.__register_handlers()

        self.__bot_service = CallbackBotService(bot)


    def __register_handlers(self):
        self.__bot.callback_query_handler(func=lambda call: call.data == "main")(self.__return_back)
        self.__bot.callback_query_handler(func=lambda call: call.data == "delete")(self.__delete_location)
        self.__bot.callback_query_handler(func=lambda call: call.data.split(';')[0].startswith("loc"))(self.__send_location)


    async def __send_location(self, call: CallbackQuery):
        await self.__bot_service.send_location(call)


    async def __delete_location(self, call:CallbackQuery):
        await self.__bot_service.delete_location(call)


    async def __return_back(self, call: CallbackQuery):
        await self.__bot_service.return_back(call)