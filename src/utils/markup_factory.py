from typing import List, Tuple
from interfaces import ChargingPoint
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def markup_factory(data: dict, **kwargs) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=kwargs.get("resize_keyboard", True))

    for item in data.values():
        item_button = KeyboardButton(item, request_location=kwargs.get("request_location", None))
        markup.add(item_button)

    return markup

def main_menu(data: List[Tuple[ChargingPoint, int]]):
    buttons = []

    for index, item in enumerate(data):
        point = {"lon": item[0]["longitude"], "lat": item[0]["latitude"]}
        buttons.append([
            InlineKeyboardButton(text=f"Показать станцию. До станции ~{round(item[1])} км.", callback_data=f"loc{index};{point}")
        ])

    return InlineKeyboardMarkup(buttons)

def delete_location():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])