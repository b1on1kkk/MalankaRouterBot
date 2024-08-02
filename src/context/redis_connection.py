import os
from repository import RedisConnection
from redis.asyncio import Redis

class RedisContext:
    def __init__(self):
        self.__redis = RedisConnection(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"))


    async def __aenter__(self) -> Redis | None:
        return await self.__redis.connect()


    async def __aexit__(self, exc_type, exc, tb):
        await self.__redis.close()