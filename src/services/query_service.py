import asyncpg
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove

from repository import UserRepository
from utils import main_menu, Distance

from constants import BOT_ANSWERS

class QueryBotService:
    def __init__(self, bot: TeleBot, connection: asyncpg.Connection | None):
        self.__bot = bot
        self.__repository = UserRepository(connection)

    async def get_location(self, message: Message):
        USER_LOCATION = {"latitude": message.location.latitude, "longitude": message.location.longitude}

        user = await self.__repository.find_user_by_id(message.from_user.id)

        distance = await Distance(USER_LOCATION, user["connector_type"]).find_location()
        nearest_chargers = await distance.find_location()

        await self.__bot.send_message(message.chat.id, f"3 ближайшии станции с коннектором: <b><u>{user["connector_type"]}</u></b>", reply_markup=main_menu(nearest_chargers))

    async def set_connector_type(self, message: Message):
        res = None

        if await self.__repository.find_user_by_id(message.from_user.id):
            res = await self.__repository.update_user(user_id=message.from_user.id, connector=message.text)
        else:
            res = await self.__repository.create_user(user_id=message.from_user.id, connector=message.text)

        await self.__bot.send_message(message.chat.id, res, reply_markup=ReplyKeyboardRemove())

    async def unknown(self, message: Message) -> None:
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])