from telebot import TeleBot

from psycopg2.extensions import connection as cn

from controllers import CommandBotController, QueryBotController

class Controller:
    def __init__(self, bot: TeleBot, connection: cn) -> None:
        CommandBotController(bot)
        QueryBotController(bot, connection)