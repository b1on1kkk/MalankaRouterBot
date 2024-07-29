from telebot import TeleBot
from telebot.types import Message

from services import CallbackBotService

class CallbackBotController:
    def __init__(self, bot: TeleBot):
        self.__bot = bot
        self.__register_handlers()

        self.__bot_service = CallbackBotService(bot)

    def __register_handlers(self):
        self.__bot.callback_query_handler(func=lambda call: call.data == "m1")(self.__m1_sub_menu)
        self.__bot.callback_query_handler(func=lambda call: call.data == "main")(self.__return_back)

    async def __m1_sub_menu(self, message: Message):
        await self.__bot_service.m1_sub_menu(message)

    async def __return_back(self, message: Message):
        await self.__bot_service.return_back(message)