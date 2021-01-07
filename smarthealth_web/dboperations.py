import psycopg2 as dbapi2
from flask import current_app, g


def query(table_name):
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % (table_name))
        rows = cursor.fetchall()
        cursor.close()
        return rows


def query_where(table_name, condition):
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s WHERE %s;" % (table_name, condition))
        rows = cursor.fetchall()
        cursor.close()
        return rows


def fetch_table(columns, table_name, condition):
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT {columns} FROM {table_name} WHERE {condition};")
        rows = cursor.fetchall()
        cursor.close()
        return rows


def add_newpatient(p_nationalid, p_name, p_surname, p_gender, p_age):
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO patient VALUES (DEFAULT,'{p_nationalid}','{p_name}','{p_surname}','{p_gender}',{p_age}, random()*(900000-100000 + 1) + 100000, current_timestamp)")
        cursor.close()


def add_newdoctor(d_id, d_name, d_surname, d_password, d_username, d_hospital, d_title, d_profession, d_addedby, d_nid):
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO patient VALUES ({d_id},'{d_name}','{d_surname}','{d_password}', '{d_username}','{d_hospital}','{d_title}','{d_profession}','{d_addedby}',{d_nid});"
        )
        cursor.close()


def get_db():
    url = current_app.config['DATABASE']
    if 'db' not in g:
        g.db = dbapi2.connect(url)
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


# def remove_patient(url, patientid):
#     with dbapi2.connect(url) as connection:
#         cursor = connection.cursor()
#         cursor.execute("DELETE FROM patient WHERE patientid = {patientid};")
#         cursor.close()
