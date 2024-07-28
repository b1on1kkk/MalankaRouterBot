import os
from dotenv import load_dotenv
load_dotenv()

from telebot import TeleBot

# import controller

def main():
    bot = TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)
    # controller.Controller(bot=bot)

    bot.infinity_polling()

if __name__ == "__main__":
    main()