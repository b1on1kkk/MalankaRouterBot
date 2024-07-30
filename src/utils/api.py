import os
import aiohttp
from telebot import TeleBot

from constants import BOT_ANSWERS

from typing import List
from interfaces import ChargingPoint
from telebot.types import ReplyKeyboardRemove

async def get_chargers(connector: str, bot: TeleBot, message_id: int) -> List[ChargingPoint] |None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{os.getenv("CHARGING_POINTS_API")}?connectors={connector}") as response:
                html: list[ChargingPoint]  = await response.json()
                return html
        except:
            await bot.send_message(message_id, BOT_ANSWERS["error"], reply_markup=ReplyKeyboardRemove())