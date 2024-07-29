import os
import asyncpg
from repository import DatabaseConnection

class Connection:
    def __init__(self):
        self.__db = DatabaseConnection(
            database=os.getenv("POSTGRES_DB"), 
            user=os.getenv("POSTGRES_USER"), 
            password=os.getenv("POSTGRES_PASSWORD"))
    
    async def __aenter__(self) -> asyncpg.Connection | None:
        return await self.__db.connect()

    async def __aexit__(self, exc_type, exc, tb):
        await self.__db.close()