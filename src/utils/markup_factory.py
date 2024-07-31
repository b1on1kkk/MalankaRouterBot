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
        point = {"lon": item["longitude"], "lat": item["latitude"]}

        buttons.append([
            InlineKeyboardButton(text=f"{item["name"]}, {item["street"]}, {item["house"]}, {item["city"]}", callback_data=f"loc{index};{point}")
        ])

    return InlineKeyboardMarkup(buttons)

def delete_location():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])