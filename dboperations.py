import psycopg2 as dbapi2
import os

DATABASE_URL = os.environ['DATABASE_URL']


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

def add_newpatient(url, form_patientid, form_patientname, form_patientsurname, form_patientgender, form_patientage, form_patientlogcode):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO patient VALUES (%s,'%s','%s','%s',%s,%s);" %(form_patientid, form_patientname, form_patientsurname, form_patientgender, form_patientage, form_patientlogcode))
        
        cursor.close()