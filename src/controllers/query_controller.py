from telebot import TeleBot, types

from services import QueryBotService

from constants import CONNECTORS_TYPE_MARKUP

class QueryBotController:
    def __init__(self, bot: TeleBot) -> None:
        self.__bot = bot
        self.__register_handlers()
        self.__bot_service = QueryBotService(bot=bot)

    def __register_handlers(self) -> None:
        self.__bot.message_handler(content_types=["location"])(self.__get_location)
        self.__bot.message_handler(func=lambda type: type.text in CONNECTORS_TYPE_MARKUP)(self.__set_connector_type)
        self.__bot.message_handler(func=lambda msg: True)(self.__unknown)

    def __get_location(self, message: types.Message) -> None:
        self.__bot_service.get_location(message)

    def __set_connector_type(self, message: types.Message) -> None:
        self.__bot_service.set_connector_type(message)

    def __unknown(self, message: types.Message) -> None:
        self.__bot_service.unknown(message)