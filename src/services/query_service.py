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
        try:
            USER_LOCATION = {"latitude": message.location.latitude, "longitude": message.location.longitude}

            user = await self.__repository.find_user_by_id(message.from_user.id)

            distance = Distance(USER_LOCATION, user["connector_type"])
            nearest_chargers = await distance.find_location()

            await self.__bot.send_message(message.chat.id, f"Нашел по Вашим требованиям ({len(nearest_chargers)}): <b>{user["connector_type"]}</b>", reply_markup=main_menu(nearest_chargers))
        except Exception as error_message:
            await self.__bot.send_message(message.chat.id, str(error_message), reply_markup=ReplyKeyboardRemove())


    async def set_connector_type(self, message: Message):
        try:
            user = await self.__repository.find_user_by_id(message.from_user.id)

            if user:
                await self.__repository.update_user(user_id=message.from_user.id, connector=message.text)
            else:
                await self.__repository.create_user(user_id=message.from_user.id, connector=message.text)

            await self.__bot.send_message(message.chat.id, BOT_ANSWERS["connector_type"], reply_markup=ReplyKeyboardRemove())
        except Exception as error_message:
            await self.__bot.send_message(message.chat.id, str(error_message), reply_markup=ReplyKeyboardRemove())


    async def unknown(self, message: Message) -> None:
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])