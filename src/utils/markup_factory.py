import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from interfaces import ChargingPoint

from typing import List

def markup_factory(data: dict, **kwargs) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=kwargs.get("resize_keyboard", True))
    
    for item in data.values():
        item_button = KeyboardButton(item, request_location=kwargs.get("request_location", None))
        markup.add(item_button)

    return markup

def main_menu(data: List[ChargingPoint]):
    buttons = []

    for index, item in enumerate(data):
        buttons.append([InlineKeyboardButton(text=f"{item["name"]}, {item["street"]}, {item["house"]}, {item["city"]}", callback_data=f"m{index + 1}")])

    return InlineKeyboardMarkup(buttons)

def sub_menu(*, longitude, latitude):
    coordinates = json.dumps({"longitude": longitude, "latitude": latitude})

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="show location", callback_data=f"charger_location:{coordinates}")],
        [InlineKeyboardButton(text="back", callback_data="main")]
    ])