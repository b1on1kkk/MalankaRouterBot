import os
import asyncio
import controller

from dotenv import load_dotenv
load_dotenv()

from context import Connection
from telebot.async_telebot import AsyncTeleBot

# check if bot is up and running
from keep_alive import keep_alive
keep_alive()

async def main():
    async with Connection() as conn:
            bot = AsyncTeleBot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
            controller.Controller(bot, conn)

            await bot.polling(non_stop=True)

if __name__ == "__main__":
    asyncio.run(main())