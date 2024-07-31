import logging

from functools import wraps
from telebot.types import Message

from repository import UserRepository

from constants import BOT_ANSWERS

def UnkConn(method):
    @wraps(method)
    async def async_wrapper(self, message: Message):
        try:
            BOT = getattr(self, f"_{self.__class__.__name__}__bot")

            repository = UserRepository(self.connection)

            if await repository.find_user_by_id(message.from_user.id):
                return await method(self, message)
            
            await BOT.send_message(message.chat.id, BOT_ANSWERS["forbidden"])
        except Exception as e:
            logging.error(e)
            raise Exception(BOT_ANSWERS["error"])


    return async_wrapper
