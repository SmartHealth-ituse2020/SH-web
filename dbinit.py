import psycopg2 as dbapi2
import os

DATABASE_URL = os.environ['DATABASE_URL']
INIT_STATEMENTS = [open("database_design.sql", "r").read()]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)

        cursor.close()


if __name__ == "__main__":
    initialize(DATABASE_URL)
