from psycopg2.extensions import connection as cn, cursor as cu

from constants import BOT_ANSWERS

class UserRepository:
    def __init__(self, db_conn: cn):
        self.__connection: cn = db_conn
        self.__cursor: cu = db_conn.cursor()

    def get_all(self):
        try:
            self.__cursor.execute("SELECT * FROM users")
            return self.__cursor.fetchall()
        except:
            return BOT_ANSWERS["error"]


    def find_user_by_id(self, user_id: int):
        try:
            self.__cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return self.__cursor.fetchone()
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