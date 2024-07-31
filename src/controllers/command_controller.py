from telebot import TeleBot
from telebot.types import Message

from services import CommandBotService

class CommandBotController:
    def __init__(self, bot: TeleBot):
        self.__bot = bot
        self.__register_handlers()
        
        self.__bot_service = CommandBotService(bot)


    def __register_handlers(self):
        self.__bot.message_handler(commands=["start"])(self.__send_hello)
        self.__bot.message_handler(commands=["setconnector"])(self.__set_connector)
        self.__bot.message_handler(commands=["find"])(self.__find_charger)


    async def __send_hello(self, message: Message):
        await self.__bot_service.send_hello(message)


    async def __set_connector(self, message: Message):
        await self.__bot_service.set_connector(message)


    async def __find_charger(self, message: Message):
        await self.__bot_service.find_charger(message)