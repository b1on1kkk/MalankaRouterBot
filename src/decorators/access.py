import hashlib
import logging

from functools import wraps
from telebot.types import Message

from repository import UserRepository

from constants import BOT_ANSWERS

def UnkConn(method):
    @wraps(method)
    async def async_wrapper(self, message: Message):
        BOT = getattr(self, f"_{self.__class__.__name__}__bot")
        ID_HASH = hashlib.sha256(str(message.from_user.id).encode()).hexdigest()

        try:
            repository = UserRepository(self.connection)
            user = await repository.find_user_by_id(ID_HASH)

            if user: return await method(self, message, user)

            await BOT.send_message(message.chat.id, BOT_ANSWERS["forbidden"])
        except Exception as e:
            logging.error(e)
            await BOT.send_message(message.chat.id, BOT_ANSWERS["error"])


    return async_wrapper
