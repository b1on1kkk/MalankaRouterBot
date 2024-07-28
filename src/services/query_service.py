from telebot import TeleBot, types

from repository import UserRepository

from constants import BOT_ANSWERS

from psycopg2.extensions import connection as cn

class QueryBotService:
    def __init__(self, bot: TeleBot, connection: cn) -> None:
        self.__bot = bot
        self.__repository = UserRepository(connection)

    def get_location(self, message: types.Message) -> None:
        print("location worked")

    def set_connector_type(self, message: types.Message) -> None:
        res = None

        if self.__repository.find_user_by_id(message.from_user.id):
            res = self.__repository.update_user(user_id=message.from_user.id, connector=message.text)
        else:
            res = self.__repository.create_user(user_id=message.from_user.id, connector=message.text)

        self.__bot.send_message(message.chat.id, res, reply_markup=types.ReplyKeyboardRemove())

    def unknown(self, message: types.Message) -> None:
        self.__bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])