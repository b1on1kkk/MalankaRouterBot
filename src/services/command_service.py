from telebot import TeleBot, types

class CommandBotService:
    def __init__(self, bot: TeleBot) -> None:
        self.__bot = bot

    def _send_hello(self, message: types.Message) -> None:
        self.__bot.send_message(message.chat.id, "Бот стартовал!")