from decouple import config
import psycopg2 as dbapi2
from flask import current_app


INIT_STATEMENTS = [open("database_design.sql", "r").read()]


def initialize():
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)

        cursor.close()


if __name__ == "__main__":
    initialize()
