import ast
from telebot import TeleBot
from telebot.types import CallbackQuery

from utils import delete_location

class CallbackBotService:
    def __init__(self, bot: TeleBot):
        self.__bot = bot


    async def send_location(self, call: CallbackQuery):
        await self.__bot.answer_callback_query(call.id, "Рисую...")
        coordinates = ast.literal_eval(call.data.split(';')[1])
        await self.__bot.send_location(call.message.chat.id, latitude=coordinates['lat'], longitude=coordinates['lon'], reply_markup=delete_location())


    async def delete_location(self, call:CallbackQuery):
        await self.__bot.answer_callback_query(call.id, "Чищу карту...")
        await self.__bot.delete_message(call.message.chat.id, call.message.message_id)
