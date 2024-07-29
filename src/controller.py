from telebot import TeleBot
import asyncpg
from controllers import CommandBotController, QueryBotController, CallbackBotController

class Controller:
    def __init__(self, bot: TeleBot, connection: asyncpg.Connection | None):
        CommandBotController(bot)
        QueryBotController(bot, connection)
        CallbackBotController(bot)