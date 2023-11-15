import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error
import pandas as pd

SQL_FOLDER = os.path.dirname(__file__)


def read_query(sql_file: str):
    """
    :return: SQL query
    """
    sql_filepath = os.path.join(SQL_FOLDER, sql_file)
    if sql_file.endswith('.sql'):
        with open(sql_filepath, 'r') as sql_file:
            sql_query = sql_file.read()
    return sql_query


class Database:
    """
    Класс для работы с PostgreSQL базой данных.

    Attributes:
        schema (str): Наименование схемы базы данных.
        conn (psycopg2.extensions.connection): Объект соединения с базой данных.

    Methods:
        __init__(self, connection_dict: dict):
            Инициализирует экземпляр класса, устанавливает соединение с базой данных.

        _retrieve(connection_dict: dict) -> psycopg2.extensions.connection:
            Статический метод. Устанавливает соединение с базой данных и возвращает объект соединения.

        enquiry(self, scheme: str, table_name: str, query: str) -> pd.DataFrame:
            Выполняет запрос к базе данных и возвращает результат в виде DataFrame.

    Usage:
        connection_dict = {
            'user': 'your_username',
            'password': 'your_password',
            'host': 'your_host',
            'port': 'your_port',
            'database': 'your_database'
        }
        db = Database(connection_dict)
        result_df = db.enquiry('your_schema', 'your_table', 'SELECT * FROM your_table;')
    """

    def __init__(self, connection_dict: dict):
        """
        Инициализирует экземпляр класса, устанавливает соединение с базой данных.

        :param
            connection_dict (dict): Словарь с параметрами подключения к базе данных.
                Пример:
                {
                    'user': 'your_username',
                    'password': 'your_password',
                    'host': 'your_host',
                    'port': 'your_port',
                    'database': 'your_database'
                }
        """
        self.schema = None
        self.conn = self._retrieve(connection_dict)

    @staticmethod
    def _retrieve(connection_dict: dict) -> psycopg2.extensions.connection:
        """
        Статический метод. Устанавливает соединение с базой данных, и возвращает объект соединения.

        :param
            connection_dict (dict): Словарь с параметрами подключения к базе данных.

        :return
            psycopg2.extensions.connection: Объект соединения с базой данных.
        """
        try:
            print('Подключение к БД...')
            connection = psycopg2.connect(
                user=connection_dict['user'],
                password=connection_dict['password'],
                host=connection_dict['host'],
                port=connection_dict['port'],
                database=connection_dict['database'])
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print('Подключен к БД')
            return connection
        except (Exception, Error) as error:
            print("Ошибка в работе с БД \nError: ", error)

    def enquiry(self, scheme: str, table_name: str, query: str) -> pd.DataFrame:
        """
        Выполняет запрос к базе данных и возвращает результат в виде DataFrame.

        :param
            scheme (str): Наименование схемы базы данных.
            table_name (str): Наименование таблицы.
            query (str): SQL-запрос или путь к файлу с расширением .sql содержащему SQL-запрос.

        :return
            pd.DataFrame: DataFrame с результатами запроса.
        """
        if query.endswith('.sql'):
            query = read_query(os.path.join(SQL_FOLDER, query)).format(scheme, table_name)
        cursor = self.conn.cursor()
        try:
            print('Выполнение запроса')
            cursor.execute(query)
            data = pd.DataFrame(cursor.fetchall())
            print('Данные получены')
        except Exception as error:
            print("Ошибка выполнения запроса\nError: ", error)
        else:
            return data
        finally:
            cursor.close()
            self.conn.close()
