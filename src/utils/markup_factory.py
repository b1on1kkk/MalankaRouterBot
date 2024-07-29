import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def markup_factory(data: dict, **kwargs) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=kwargs.get("resize_keyboard", True))
    
    for item in data.values():
        item_button = KeyboardButton(item, request_location=kwargs.get("request_location", None))
        markup.add(item_button)

    return markup

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Menu 1", callback_data="m1")],
        [InlineKeyboardButton(text="Menu 2", callback_data="m2")],
        [InlineKeyboardButton(text="Menu 3", callback_data="m3")]
    ])

def sub_menu(*, longitude, latitude):
    coordinates = json.dumps({"longitude": longitude, "latitude": latitude})

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="show location", callback_data=f"charger_location:{coordinates}")],
        [InlineKeyboardButton(text="back", callback_data="main")]
    ])