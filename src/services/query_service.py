from telebot import TeleBot, types

from repository import connection as repository

from constants import BOT_ANSWERS

class QueryBotService:
    def __init__(self, bot: TeleBot) -> None:
        self.__bot = bot

    def get_location(self, message: types.Message) -> None:
        print("location worked")

    def set_connector_type(self, message: types.Message) -> None:
        res = None

        if repository.find_user_by_id(message.from_user.id):
            res = repository.update_user(user_id=message.from_user.id, connector=message.text)
        else:
            res = repository.create_user(user_id=message.from_user.id, connector=message.text)

        self.__bot.send_message(message.chat.id, res, reply_markup=types.ReplyKeyboardRemove())

    def unknown(self, message: types.Message) -> None:
        self.__bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])