import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot

import controller

from repository import DatabaseConfig

def main():
    db = DatabaseConfig(
        database=os.getenv("POSTGRES_DB"), 
        user=os.getenv("POSTGRES_USER"), 
        password=os.getenv("POSTGRES_PASSWORD"))

    db.connect()

    bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)
    controller.Controller(bot, db.get_connection())

    bot.infinity_polling()

if __name__ == "__main__":
    main()