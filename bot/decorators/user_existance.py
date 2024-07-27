from functools import wraps

from telebot.types import ReplyKeyboardRemove

from constants import BOT_ANSWERS

def user_existance(func):
    @wraps(func)
    def wrapper(self, message):
        if not getattr(self, f"_{self.__class__.__name__}__repository").find_user_by_id(message.from_user.id):
            return self._bot.send_message(message.chat.id, BOT_ANSWERS["forbidden"], reply_markup=ReplyKeyboardRemove())

        return func(self, message)
    return wrapper