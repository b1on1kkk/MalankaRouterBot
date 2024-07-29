from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove

from repository import UserRepository

from constants import BOT_ANSWERS

import asyncpg

from utils import main_menu

class QueryBotService:
    def __init__(self, bot: TeleBot, connection: asyncpg.Connection | None):
        self.__bot = bot
        self.__repository = UserRepository(connection)

    async def get_location(self, message: Message):
        await self.__bot.send_message(message.chat.id, "Местоположение установлено!", reply_markup=ReplyKeyboardRemove())
        await self.__bot.send_message(message.chat.id, "Вот 3 ближайшии станции.", reply_markup=main_menu())

    async def set_connector_type(self, message: Message):
        res = None

        if await self.__repository.find_user_by_id(message.from_user.id):
            res = await self.__repository.update_user(user_id=message.from_user.id, connector=message.text)
        else:
            res = await self.__repository.create_user(user_id=message.from_user.id, connector=message.text)

        await self.__bot.send_message(message.chat.id, res, reply_markup=ReplyKeyboardRemove())

    async def unknown(self, message: Message) -> None:
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])