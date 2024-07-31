import sys
import logging
import asyncpg
import asyncpg.cursor

from .user import User

from constants import BOT_ANSWERS

class UserRepository:
    def __init__(self, db_conn: asyncpg.Connection | None):
        self.__connection: asyncpg.Connection | None = db_conn


    async def get_all(self) -> list | None:
        async with self.__connection.transaction():
            try:
                return await self.__connection.fetch("SELECT * FROM users")
            except:
                logging.error(sys.exc_info())
                raise Exception(BOT_ANSWERS["error"])


    async def find_user_by_id(self, user_id: int) -> User | None:
        async with self.__connection.transaction():
            try:    
                user = await self.__connection.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
                return user
            except:
                logging.error(sys.exc_info())
                raise Exception(BOT_ANSWERS["error"])


    async def create_user(self, user_id: int, connector: str) -> None:
        async with self.__connection.transaction():
            try:
                await self.__connection.execute("INSERT INTO users (id, connector_type) VALUES ($1, $2)", user_id, connector)
            except:
                logging.error(sys.exc_info())
                raise Exception(BOT_ANSWERS["error"])


    async def update_user(self, user_id: int, connector: str) -> None:
        async with self.__connection.transaction():
            try:
                await self.__connection.execute("UPDATE users SET connector_type = $1 WHERE id = $2", connector, user_id)
            except:
                logging.error(sys.exc_info())
                raise Exception(BOT_ANSWERS["error"])