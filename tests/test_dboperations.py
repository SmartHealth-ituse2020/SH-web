import psycopg2 as dbapi2
from smarthealth_web.dboperations import (
    add_newpatient, query_where, get_admin_by_username, delete_patient_with_national_id, get_doctor_by_username_or_national_id,
    add_doctor_to_database, get_appointments_of_doctor)


def test_add_newpatient(app):
    # Test adding without being present
    with app.app_context():
        add_newpatient("National_id", "Name", "Surname", "Gender", 18)
        u = query_where("patient", f"name ='Name'")
        # uid is patientid which is serial
        # utime is cratetime which is timestamp
        # ulogcode is also created during function call
        uid = u[0][0]
        utime = u[0][6]
        ulogcode = u[0][5]
    assert u[0] == (uid, 'Name', 'Surname', 'Gender', 18, ulogcode, utime, 'National_id')
    # Test again with being present
    # To be implemented


def test_query_where(app):
    # A basic new patient to test
    statement = """
    INSERT INTO patient(name, surname, gender, age, logcode, national_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    values = ('patient1', 'surname1', 'Male', 18, 12341234, 'National_id1')
    with app.app_context():
        with dbapi2.connect(app.config['DATABASE']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, values)
        u = query_where("patient", f"name = 'patient1'")
        print(u)
        uid = u[0][0]
        utime = u[0][6]
    assert u[0] == (uid, 'patient1', 'surname1', 'Male', 18, 12341234, utime, 'National_id1')


def test_get_admin_by_username(app):
    statement = """
    INSERT INTO admin(name, surname, username, password)
    VALUES (%s, %s, %s, %s);
    """
    values = ('admin1', 'surname1', 'adminuser1', 'password1')
    with app.app_context():
        with dbapi2.connect(app.config['DATABASE']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, values)
        u = get_admin_by_username('adminuser1')
        uid = u[0]
    assert u == (uid, 'admin1', 'surname1', 'adminuser1', 'password1')


def test_delete_patient_with_national_id(app):
    statement = """
    INSERT INTO patient(name, surname, gender, age, logcode, national_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    values = ('patient1', 'surname1', 'Male', 18, 12341234, 'National_id1')
    with app.app_context():
        with dbapi2.connect(app.config['DATABASE']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, values)
        delete_patient_with_national_id('National_id1')
        u = query_where("patient", f"national_id = 'National_id1'")
    assert u == []


def test_get_doctor_by_username_or_national_id(app):
    statement = """
    INSERT INTO doctor(name, surname, password, username, hospital, title, profession, added_by, national_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    values = ('doctor1','surname1','password1','doctoruser1','hospital1','title1','profession1',1,'National_id1')

    with app.app_context():
        with dbapi2.connect(app.config['DATABASE']) as conn:
            with conn.cursor() as cur:
                cur.execute(statement, values)
        u = get_doctor_by_username_or_national_id('doctoruser1','National_id1')
        uid = u[0]
    assert u == (uid, 'doctor1','surname1','password1','doctoruser1','hospital1','title1','profession1',1,'National_id1')


def test_add_doctor_to_database(app):
    with app.app_context():
        add_doctor_to_database('doctor1','surname1','password1','doctoruser5','hospital1','title1','profession1',1,'National_id5')
        u = get_doctor_by_username_or_national_id('doctoruser5', 'National_id5')
        uid = u[0]
    assert u == (uid, 'doctor1','surname1','password1','doctoruser5','hospital1','title1','profession1',1,'National_id5')


def test_get_appointments_of_doctor(app):
    statement = """
    INSERT INTO appointment(
        prediction_result,
        doctor_diagnosis,
        diagnosis_comment,
        appointment_date,
        related_patient,
        related_doctor
        )
        VALUES (%s, %s, %s, %s,  %s, %s);
    """
    values = (True,'diagnos1','comment1','now()',1,5)

    with app.app_context():
        with dbapi2.connect(app.config['DATABASE']) as conn:
            with conn.cursor() as cur:
                cur.execute(statement, values)
        u = get_appointments_of_doctor(5)
    assert u != None