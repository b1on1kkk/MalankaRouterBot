import logging
import asyncpg

from typing import Optional

class DatabaseConnection:
    def __init__(self, database: str, user: str, password: str, host: str, port: str) -> None:
        self.__user: str = user
        self.__host: str = host
        self.__port: str = port
        self.__database: str = database
        self.__password: str = password

        self.__connection: Optional[asyncpg.Connection] = None


    async def connect(self) -> asyncpg.Connection | None:
        if self.__connection is None:
            try:
                self.__connection = await asyncpg.connect(
                    database=self.__database,
                    user=self.__user,
                    password=self.__password,
                    host=self.__host,
                    port=self.__port
                )

                # check if database connected
                await self.__connection.execute('SELECT 1')

                print('database connected')

                return self.__connection
            except asyncpg.PostgresError as e:
                logging.error(e)
                print(f"Failed to connect or ping the database: {e}")


    async def close(self):
        if self.__connection is not None:
            try:
                await self.__connection.close()
                print('database connection closed')
            except asyncpg.PostgresError as e:
                logging.error(e)