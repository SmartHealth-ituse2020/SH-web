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


def fetch_table(url, columns, table_name, condition):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT {columns} FROM {table_name} WHERE {condition};")
        rows = cursor.fetchall()
        cursor.close()
        return rows


def add_newpatient(url, form_patientname, form_patientsurname, form_patientgender, form_patientage):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO patient VALUES (DEFAULT,'{form_patientname}','{form_patientsurname}','{form_patientgender}',{form_patientage}, random()* (900000-100000 + 1) + 100000)")
        cursor.close()


def add_newdoctor(
        url,
        form_doctorid,
        form_doctorname,
        form_doctorsurname,
        form_doctorpassword,
        form_doctorusername,
        form_doctorhospital,
        form_doctortitle,
        form_doctorprofession,
        form_added_by,
        form_doctornid
):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO patient VALUES ({form_doctorid},'{form_doctorname}','{form_doctorsurname}','{form_doctorpassword}',\
            '{form_doctorusername}','{form_doctorhospital}','{form_doctortitle}','{form_doctorprofession}','{form_added_by}',{form_doctornid});")
        cursor.close()


# def remove_patient(url, patientid):
#     with dbapi2.connect(url) as connection:
#         cursor = connection.cursor()
#         cursor.execute("DELETE FROM patient WHERE patientid = {patientid};")
#         cursor.close()
