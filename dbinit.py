from decouple import config
import psycopg2 as dbapi2
import os

INIT_STATEMENTS = [open("database_design.sql", "r").read()]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)

        cursor.close()


if __name__ == "__main__":
    DATABASE_URL = config('DATABASE_URL')
    initialize(DATABASE_URL)
