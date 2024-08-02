import os
import asyncio
import controller
from contextlib import AsyncExitStack

from dotenv import load_dotenv
load_dotenv()

from telebot.async_telebot import AsyncTeleBot
from context import PostgresConnection, RedisContext

# check if bot is up and running
from keep_alive import keep_alive
keep_alive()

async def main():
    async with AsyncExitStack() as stack:
        conn = await stack.enter_async_context(PostgresConnection())
        redis = await stack.enter_async_context(RedisContext())

        bot = AsyncTeleBot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
        controller.Controller(bot, conn, redis)

        await bot.polling(non_stop=True)


if __name__ == "__main__":
    asyncio.run(main())