from telebot import TeleBot
from asyncpg import Connection
from redis.asyncio import Redis
from controllers import CommandBotController, QueryBotController, CallbackBotController

class Controller:
    def __init__(self, bot: TeleBot, connection: Connection | None, redis: Redis | None):
        CommandBotController(bot)
        QueryBotController(bot, connection, redis)
        CallbackBotController(bot)