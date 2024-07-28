from telebot import TeleBot

from controllers import CommandBotController, QueryBotController

class Controller:
    def __init__(self, bot: TeleBot) -> None:
        CommandBotController(bot=bot)
        QueryBotController(bot=bot)