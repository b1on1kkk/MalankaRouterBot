import json
from telebot import TeleBot
from redis.asyncio import Redis
from telebot.types import CallbackQuery

from utils import delete_location

class CallbackBotService:
    def __init__(self, bot: TeleBot, redis: Redis | None):
        self.__bot = bot
        self.__redis = redis

    async def send_location(self, call: CallbackQuery):
        redis_id = call.data.split(':')[1]

        data = await self.__redis.get(redis_id)

        if data:
            coordinates = json.loads(data)
            await self.__bot.answer_callback_query(call.id, "Отметил!")
            await self.__bot.send_location(call.message.chat.id, latitude=coordinates['lat'], longitude=coordinates['lon'], reply_markup=delete_location())
        else: 
            await self.__bot.answer_callback_query(call.id, "Данные устарели!\nОбновите местоположение!", show_alert=True)


    async def delete_location(self, call:CallbackQuery):
        await self.__bot.answer_callback_query(call.id, "Чищу карту...")
        await self.__bot.delete_message(call.message.chat.id, call.message.message_id)
