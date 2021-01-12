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
            f"INSERT INTO patient VALUES (DEFAULT,'{p_name}','{p_surname}','{p_gender}',{p_age}, random()*(900000-100000 + 1) + 100000, current_timestamp,'{p_nationalid}')")
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


def get_admin_by_username(username):
    statement = "SELECT * FROM admin WHERE username = %s;"
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (username, ))
            u = cur.fetchone()
    return u


def delete_patient_with_national_id(national_id):
    statement = "DELETE FROM patient WHERE national_id = %s;"
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (national_id, ))


def get_doctor_by_username_or_national_id(uname, nid):
    statement = "SELECT * FROM doctor WHERE username = %s OR national_id = %s;"
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (uname, nid))
            u = cur.fetchone()
    return u


def add_doctor_to_database(name, surname, pword, uname, hosp, title, prof, added_by, nid):
    statement = """
    INSERT INTO doctor(name, surname, password, username, hospital, title, profession, added_by, national_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    values = (name, surname, pword, uname, hosp, title, prof, added_by, nid)

    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, values)


def get_appointments_of_doctor(doctor_id):
    statement = """
    SELECT
    appointment.id, appointment_date, patient.name, 
    patient.surname, patient.age, patient.gender,
    doctor_diagnosis, prediction_result
    FROM
    appointment
    LEFT JOIN patient 
    ON related_patient = patient.id
    WHERE related_doctor=%s"""
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (doctor_id, ))
            u = cur.fetchall()
    return u

def get_admin_name_by_id(id):
    statement = "SELECT * FROM admin WHERE id = %s;"
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (id, ))
            u = cur.fetchone()
    return u[3]

def delete_doctor_with_id(id):
    statement = "DELETE FROM DOCTOR WHERE id = %s;"
    url = current_app.config['DATABASE']
    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(statement, (id, ))