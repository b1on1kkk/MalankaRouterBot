import json
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

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