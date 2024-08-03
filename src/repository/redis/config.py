import logging
from redis.asyncio import Redis, RedisError
from typing import Optional

class RedisConnection:
    def __init__(self, host: str, port: int, password: str):
        self.__host = host
        self.__port = port
        self.__password = password

        self.__r: Optional[Redis] = None


    async def connect(self) -> Redis | None:
        if self.__r is None:
            try:
                self.__r = Redis(
                    host=self.__host, 
                    port=self.__port,
                    password=self.__password,
                    db=0,
                    socket_timeout=5,
                )
                
                response = await self.__r.ping()
                if response: print("redis connected")

                return self.__r
            except RedisError as e:
                logging.error(e)
                return None


    async def close(self):
        if self.__r is not None:
            try:
                await self.__r.aclose()
                print('redis connection closed')
            except RedisError as e:
                logging.error(e)
