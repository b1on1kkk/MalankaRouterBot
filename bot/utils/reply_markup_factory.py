from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def reply_markup_factory(data: dict, **kwargs) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=kwargs.get("resize_keyboard", True))
    
    for item in data.values():
        item_button = KeyboardButton(item, request_location=kwargs.get("request_location", None))
        markup.add(item_button)

    return markup
