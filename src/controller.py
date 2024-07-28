from telebot import TeleBot

from controllers import CommandBotController

class Controller:
    def __init__(self, bot: TeleBot) -> None:
        CommandBotController(bot=bot)