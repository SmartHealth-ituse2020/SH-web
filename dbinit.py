import psycopg2 as dbapi2
from flask import current_app
from decouple import config


INIT_STATEMENTS = [open("database_design.sql", "r").read()]


def initialize(delete=False):
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

        cursor.close()


if __name__ == "__main__":
    initialize()
