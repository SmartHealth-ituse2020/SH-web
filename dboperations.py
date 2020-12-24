import psycopg2 as dbapi2

import os

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgres://fvtkacqijrpxfk:9af8c01dc052361fd51630b634e9a1df34106a7eae0ac736c6a36099bb476d87@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/d4qj8s0lt8sev8"

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