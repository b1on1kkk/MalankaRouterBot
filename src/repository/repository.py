import asyncpg
import asyncpg.cursor

from .user import User

from constants import BOT_ANSWERS

class UserRepository:
    def __init__(self, db_conn: asyncpg.Connection | None):
        self.__connection: asyncpg.Connection | None = db_conn

    async def get_all(self) -> list | str:
        async with self.__connection.transaction():
            try:
                return await self.__connection.fetch("SELECT * FROM users")
            except Exception as e:
                print(e)
                return BOT_ANSWERS["error"]


    async def find_user_by_id(self, user_id: int) -> User | str:
        async with self.__connection.transaction():
            try:    
                user = await self.__connection.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
                return user
            except Exception as e:
                print(e)
                return BOT_ANSWERS["error"]


    async def create_user(self, user_id: int, connector: str) -> str:
        async with self.__connection.transaction():
            try:
                await self.__connection.execute("INSERT INTO users (id, connector_type) VALUES ($1, $2)", user_id, connector)
                return BOT_ANSWERS["connector_type"]
            except Exception as e:
                print(e)
                return BOT_ANSWERS["error"]


    async def update_user(self, user_id: int, connector: str) -> str:
        async with self.__connection.transaction():
            try:
                await self.__connection.execute("UPDATE users SET connector_type = $1 WHERE id = $2", connector, user_id)
                return BOT_ANSWERS["connector_update"]
            except Exception as e:
                print(e)
                return BOT_ANSWERS["error"]