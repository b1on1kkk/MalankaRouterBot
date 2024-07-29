from telebot import TeleBot
from telebot.types import CallbackQuery

from utils import sub_menu, main_menu

class CallbackBotService:
    def __init__(self, bot: TeleBot):
        self.__bot = bot

    async def m1_sub_menu(self, call: CallbackQuery):
        await self.__bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Точнее адресс + статус", reply_markup=sub_menu(longitude=27, latitude=27))

    async def return_back(self, call: CallbackQuery):
        await self.__bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вот 3 ближайшии станции.", reply_markup=main_menu())
