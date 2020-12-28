import psycopg2 as dbapi2
import os

DATABASE_URL = "postgres://fvtkacqijrpxfk:9af8c01dc052361fd51630b634e9a1df34106a7eae0ac736c6a36099bb476d87@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/d4qj8s0lt8sev8"
#DATABASE_URL = os.environ['DATABASE_URL']
INIT_STATEMENTS = [open("database_design.sql", "r").read()]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)

        cursor.close()


if __name__ == "__main__":
    initialize(DATABASE_URL)
