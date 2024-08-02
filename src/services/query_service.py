import hashlib
import logging
import asyncpg
from telebot import TeleBot, asyncio_helper
from telebot.types import Message, ReplyKeyboardRemove

from repository import UserRepository
from utils import main_menu, Distance

from interfaces import User

from constants import BOT_ANSWERS

class QueryBotService:
    def __init__(self, bot: TeleBot, connection: asyncpg.Connection | None):
        self.__bot = bot
        self.__repository = UserRepository(connection)


    # user prop passed from decorator
    async def get_location(self, message: Message, user: User):
        USER_LOCATION = {"latitude": message.location.latitude, "longitude": message.location.longitude}

        try:
            loading_text: Message = await self.__bot.send_message(message.chat.id, "Ищу станции...")

            distance = Distance(USER_LOCATION, user["connector_type"])
            nearest_chargers = await distance.find_location()

            await self.__bot.edit_message_text(f"Нашел по Вашим требованиям {len(nearest_chargers)} станции с <b>{user['connector_type']}</b> типом коннектора.", message.chat.id, loading_text.message_id, reply_markup=main_menu(nearest_chargers))
        except asyncio_helper.ApiTelegramException as telegram_message:
            logging.error(telegram_message)
            await self.__bot.send_message(message.chat.id, BOT_ANSWERS["error"], reply_markup=ReplyKeyboardRemove())
        except Exception as error_message:
            await self.__bot.send_message(message.chat.id, str(error_message), reply_markup=ReplyKeyboardRemove())


    async def set_connector_type(self, message: Message):
        ID_HASH = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()

        try:
            user = await self.__repository.find_user_by_id(ID_HASH)

            if user:
                await self.__repository.update_user(ID_HASH, message.text)
            else:
                await self.__repository.create_user(ID_HASH, message.text)

            await self.__bot.send_message(message.chat.id, BOT_ANSWERS["connector_type"], reply_markup=ReplyKeyboardRemove())
        except asyncio_helper.ApiTelegramException as telegram_message:
            logging.error(telegram_message)
            await self.__bot.send_message(message.chat.id, BOT_ANSWERS["error"], reply_markup=ReplyKeyboardRemove())
        except Exception as error_message:
            await self.__bot.send_message(message.chat.id, str(error_message), reply_markup=ReplyKeyboardRemove())


    async def unknown(self, message: Message):
        await self.__bot.send_message(message.chat.id, BOT_ANSWERS["unknown"])