import psycopg2 as dbapi2
from flask import current_app
from decouple import config
from werkzeug.security import generate_password_hash

INIT_STATEMENTS = [open("database_design.sql", "r").read()]
TEST_STATEMENTS = [open("tests\data.sql", "r").read()]


def initialize(delete=False, test=False):
    if test:
        url = config("TEST_DATABASE_URL")
    else:
        url = config("DATABASE_URL")

    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            if delete:
                cursor.execute(
                    "DROP TABLE IF EXISTS ADMIN, APPOINTMENT, DOCTOR, PATIENT, public.emr_data, DLMODEL;"
                )
            print("Initializing database.")
            cursor.execute(statement)
            print("Done.")
        if test:
            for stats in TEST_STATEMENTS:
                cursor.execute(stats,(generate_password_hash('1'),generate_password_hash('1'),
                generate_password_hash('1'),generate_password_hash('1'),generate_password_hash('1')))
        cursor.close()


if __name__ == "__main__":
    initialize()
