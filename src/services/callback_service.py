import os
import json
import aiohttp
import textwrap
from telebot import TeleBot
from redis.asyncio import Redis
from utils import link_to_yandex_maps
from telebot.types import CallbackQuery

from interfaces import RootDevice, PointCoordinates

class APIClient:
    async def get_local_connector_info(self, id: str) -> RootDevice | None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{os.getenv('LOCATION_INF')}?locationId={id}") as response:
                devices: RootDevice = await response.json()
                return devices


class CacheService:
    def __init__(self, redis: Redis):
        self.__redis = redis

    async def get_data(self, key: str) -> PointCoordinates | None:
        data = await self.__redis.get(key)
        return json.loads(data) if data else None


class BotService:
    def __init__(self, bot: TeleBot):
        self.__bot = bot

    async def send_location_info(self, chat_id: int, info: str, coordinates: PointCoordinates, call_id: str):
        await self.__bot.answer_callback_query(call_id, "Отметил!")
        await self.__bot.send_message(chat_id, info, parse_mode="html")
        await self.__bot.send_location(chat_id, latitude=round(coordinates['lat'], 6), longitude=round(coordinates['lon'], 6), reply_markup=link_to_yandex_maps(coordinates))

    async def send_expired_data_alert(self, call_id: str):
        await self.__bot.answer_callback_query(call_id, "Данные устарели!\nОбновите местоположение!", show_alert=True)


class CallbackBotService:
    def __init__(self, bot: TeleBot, redis: Redis | None):
        self.__api_client = APIClient()
        self.__cache_service = CacheService(redis)
        self.__bot_service = BotService(bot)

    async def send_location(self, call: CallbackQuery):
        redis_id = call.data.split(':')[1]
        coordinates = await self.__cache_service.get_data(redis_id)

        if coordinates:
            local = await self.__api_client.get_local_connector_info(coordinates["locationId"])
            inf = "Виды коннекторов на станции:\n"

            for connector in local["devices"][0]["connectors"]:
                inf += textwrap.dedent(f"""
                    Коннектор: <b>{connector['typeRu']}</b>
                    Статус: {'✅ (доступен для зарядки)' if connector['status'] == 'Available' else '❌ (не доступен для зарядки)'}
                    Сила тока: {connector['power']} kw
                """)

            await self.__bot_service.send_location_info(call.message.chat.id, inf, coordinates, call.id)
        else:
            await self.__bot_service.send_expired_data_alert(call.id)