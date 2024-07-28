import psycopg2
from psycopg2.extensions import connection as _connection

from typing import Optional

class DatabaseConfig:
    def __init__(self, database: str, user: str, password: str, host: str = "localhost", port: str = "5432") -> None:
        self.__user: str = user
        self.__host: str = host
        self.__port: str = port
        self.__database: str = database
        self.__password: str = password

        self.__connection: Optional[_connection] = None

    def connect(self) -> None:
        if self.__connection is None:
            try:
                self.__connection = psycopg2.connect(
                    database=self.__database,
                    user=self.__user,
                    password=self.__password,
                    host=self.__host,
                    port=self.__port
                )
                print('database connected')
            except psycopg2.OperationalError as e:
                print(f'connection error {e}')
    
    def get_connection(self) -> _connection:
        return self.__connection
    
    def close(self) -> None:
        try:
            self.__connection.close()
            print('connection closed')
        except psycopg2.OperationalError as e:
            print(f'error: {e}')