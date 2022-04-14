import string
from math import ceil
from pprint import pprint
from datetime import datetime
from random import randint, choice
from mysql.connector import connect


class UsersDb:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "3103"
        self.db_name = "users_data"
        self.table_name = "users"

        self.one_page = 50

        self.create_database()
        self.connection = self.get_connection()
        table_create_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                quantity INT,
                distance INT,
                date DATE
            );
            """
        self.make_query(table_create_query)

    def create_database(self):
        with connect(
                host=self.host,
                user=self.user,
                password=self.password,
        ) as connection:
            self.make_query(f"CREATE DATABASE IF NOT EXISTS {self.db_name}", connection)

    def make_query(self, query, connection=None, return_value=False):
        if connection is None:
            connection = self.connection
        with connection.cursor() as cursor:
            if isinstance(query, tuple):
                cursor.execute(query[0], query[1])
            else:
                cursor.execute(query)
            if return_value is False:
                connection.commit()
            else:
                return cursor.fetchall()

    def get_connection(self):
        connection = connect(host=self.host, user=self.user, password=self.password, database=self.db_name)
        return connection

    def insert_random_data(self, rows_count):
        names = ["Ivan", "Elena", "Egor", "Stepan", "Alexander", "Anastasiya", "Larisa", "Svetik",
                 "Nikolay", "Mihail", "Vlada", "Ksenia", "Yulia", "Anatoliy", "Inokentiy"]
        step = 100

        with self.connection.cursor() as cursor:
            for i in range(0, rows_count, step):
                tmp_data = []
                for j in range(i, i+step):
                    tmp_data.append([choice(names) + f" {choice(string.ascii_uppercase)}",
                                     randint(0, 50), randint(0, 20000),
                                     datetime.utcfromtimestamp(randint(1018157756, 1649316956)).strftime('%Y-%m-%d')])
                cursor.executemany(f"""INSERT INTO {self.table_name}(name, quantity, distance, date)
                                       VALUES(%s, %s, %s, %s)""", tmp_data)
            self.connection.commit()

    def get_sorted(self, column_to_order=None, order_value=None, column_to_where=None, where_condition=None,
                   where_value=None, limit=50, offset=0):
        query = f"SELECT name, quantity, distance, DATE_FORMAT(date, '%e.%m.%Y') FROM {self.table_name} "
        for_escape = []

        if all((column_to_where is not None, where_condition is not None, where_value is not None)):
            query += f"WHERE {column_to_where} {where_condition} %s "
            for_escape.append(where_value)

        if all((column_to_order is not None, order_value is not None)):
            query += f"ORDER BY {column_to_order} {order_value} "

        query += f"LIMIT {limit} OFFSET {offset}"

        rows = self.make_query(
            (query, for_escape),
            return_value=True
        )

        return rows

    def count(self):
        return ceil(self.make_query(f"SELECT COUNT(*) FROM {self.table_name}", return_value=True)[0][0] / self.one_page)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    users_db = UsersDb()
    print(users_db.get_sorted())
    users_db.close_connection()


