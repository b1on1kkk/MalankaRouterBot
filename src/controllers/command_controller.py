from telebot import TeleBot, types

from services import CommandBotService

class CommandBotController:
    def __init__(self, bot: TeleBot) -> None:
        self.__bot = bot
        self.__register_handlers()

        self.__bot_service = CommandBotService(bot=bot)

    def __register_handlers(self) -> None:
        self.__bot.message_handler(commands=["start"])(self.__send_hello)
        self.__bot.message_handler(commands=["setconnector"])(self.__set_connector)


    def __send_hello(self, message: types.Message) -> None:
        self.__bot_service._send_hello(message)

    def __set_connector(self, message: types.Message) -> None:
        pass