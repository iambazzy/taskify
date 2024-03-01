import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

db_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    5,
    user='mohammadbasit0404',
    password='56wTthCzkFEr',
    host='ep-lucky-grass-a5qopkk1-pooler.us-east-2.aws.neon.tech',
    database='taskify_db'
)


@contextmanager
def db_connection():
    connection = db_pool.getconn()
    try:
        yield connection
    finally:
        db_pool.putconn(connection)


@contextmanager
def db_cursor(commit=False):
    with db_connection() as connection:
        cursor = connection.cursor()
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()


# class Database:
#     _instance = None
#
#     @staticmethod
#     def get_instance():
#         if Database._instance is None:
#             Database()
#         return Database._instance
#
#     def __init__(self):
#         if Database._instance is not None:
#             raise Exception("Already has a connection")
#         else:
#             self.connection = pymysql.connect(
#                 host='localhost',
#                 user='root',
#                 password='',
#                 db='users'
#             )
#             Database._instance = self
#
#     @staticmethod
#     def table_exists(self, table_name):
#         try:
#             db = Database.get_instance()
#             with db.connection.cursor() as cursor:
#                 query = f"SHOW TABLES LIKE '{table_name}'"
#                 cursor.execute(query)
#                 result = cursor.fetchall()
#                 print(result)
#         except Exception as e:
#             print(e)

