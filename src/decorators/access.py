from functools import wraps
from telebot.types import Message

from repository import UserRepository

from constants import BOT_ANSWERS

def UnkConn(method):
    @wraps(method)
    async def async_wrapper(self, message: Message):
        BOT = getattr(self, f"_{self.__class__.__name__}__bot")

        repository = UserRepository(self.connection)

        try:
            if await repository.find_user_by_id(message.from_user.id):
                return await method(self, message)
            await BOT.send_message(message.chat.id, BOT_ANSWERS["forbidden"])
        except Exception as e:
            print(f"Error in {method.__name__}: {e}")
            raise

    return async_wrapper
