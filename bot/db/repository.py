import psycopg2
from psycopg2.extensions import connection as cn, cursor as cu

from typing import Optional

from constants import BOT_ANSWERS

class DatabaseRepository:
    def __init__(self, database: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        self.__user: str = user
        self.__host: str = host
        self.__port: str = port
        self.__database: str = database
        self.__password: str = password
        self.__cursor: Optional[cu] = None
        self.__connection: Optional[cn] = None


    def db_connect(self):
        try:
            self.__connection = psycopg2.connect(
                database=self.__database,
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=self.__port
            )
            self.__cursor = self.__connection.cursor()
            print('database connected')
        except psycopg2.OperationalError as e:
            print(f'connection error {e}')


    def get_all(self):
        try:
            self.__cursor.execute("SELECT * FROM users")
            return self.__cursor.fetchall()
        except:
            return BOT_ANSWERS["error"]


    def find_user_by_id(self, user_id: int):
        try:
            self.__cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return self.__cursor.fetchall()
        except:
            return BOT_ANSWERS["error"]


    def create_user(self, user_id: int, connector: str):
        try:
            self.__cursor.execute("INSERT INTO users (id, connector_type) VALUES (%s, %s)", (user_id, connector))
            self.__connection.commit()
            return BOT_ANSWERS["connector_type"]
        except:
            return BOT_ANSWERS["error"]


    def update_user(self, user_id: int, connector: str):
        try:
            self.__cursor.execute("UPDATE users SET connector_type = %s WHERE id = %s", (connector, user_id))
            self.__connection.commit()
            return BOT_ANSWERS["connector_update"]
        except:
            return BOT_ANSWERS["error"]