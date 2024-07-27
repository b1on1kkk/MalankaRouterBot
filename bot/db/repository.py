import psycopg2

class DatabaseRepository:
    def __init__(self, database: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        self.__user = user
        self.__host = host
        self.__port = port
        self.__database = database
        self.__password = password
        self.__cursor = None

    def db_connect(self):
        try:
            connection = psycopg2.connect(
                database=self.__database,
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=self.__port
            )
            print('database connected')
            self.__cursor = connection.cursor()
        except psycopg2.OperationalError as e:
            print(f'connection error {e}')