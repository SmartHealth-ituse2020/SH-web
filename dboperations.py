import psycopg2 as dbapi2
from decouple import config

# DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = config('DATABASE_URL')


def query(url, table_name):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % (table_name))
        rows = cursor.fetchall()
        cursor.close()
        return rows


def query_where(url, table_name, condition):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s WHERE %s;" % (table_name, condition))
        rows = cursor.fetchall()
        cursor.close()
        return rows
