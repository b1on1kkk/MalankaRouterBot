import logging
import asyncpg
import asyncpg.cursor

from interfaces import User

from constants import BOT_ANSWERS

class UserRepository:
    def __init__(self, db_conn: asyncpg.Connection | None):
        self.__connection: asyncpg.Connection | None = db_conn


    async def get_all(self) -> list | None:
        async with self.__connection.transaction():
            try:
                return await self.__connection.fetch("SELECT * FROM users")
            except asyncpg.PostgresError as e:
                logging.error(e)
                raise Exception(BOT_ANSWERS["error"])


    async def find_user_by_id(self, id_hash: str) -> User | None:
        async with self.__connection.transaction():
            try:    
                user = await self.__connection.fetchrow("SELECT * FROM users WHERE id_hash = $1", id_hash)
                return user
            except asyncpg.PostgresError as e:
                logging.error(e)
                raise Exception(BOT_ANSWERS["error"])


    async def create_user(self, id_hash: str, connector: str) -> None:
        async with self.__connection.transaction():
            try:
                await self.__connection.execute("INSERT INTO users (id_hash, connector_type) VALUES ($1, $2)", id_hash, connector)
            except asyncpg.PostgresError as e:
                logging.error(e)
                raise Exception(BOT_ANSWERS["error"])


    async def update_user(self, id_hash: str, connector: str) -> None:
        async with self.__connection.transaction():
            try:
                await self.__connection.execute("UPDATE users SET connector_type = $1 WHERE id_hash = $2", connector, id_hash)
            except asyncpg.PostgresError as e:
                logging.error(e)
                raise Exception(BOT_ANSWERS["error"])