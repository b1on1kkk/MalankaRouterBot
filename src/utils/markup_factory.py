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
    markup = InlineKeyboardMarkup()

    for _, item in enumerate(data):
        if item[1] < 1:
            markup.add(InlineKeyboardButton(text=f"Показать станцию. До станции ~{round(round(item[1], 2) * 1000)} м.", callback_data=f"loc:{item[0]['locationId']}"))
        else:
            markup.add(InlineKeyboardButton(text=f"Показать станцию. До станции ~{round(item[1])} км.", callback_data=f"loc:{item[0]['locationId']}"))

    return markup

def delete_location():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ])