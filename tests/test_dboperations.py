import psycopg2 as dbapi2
from smarthealth_web.dboperations import (
    add_newpatient, query_where, get_admin_by_username, delete_patient_with_national_id, get_doctor_by_username_or_national_id,
    add_doctor_to_database, get_appointments_of_doctor, get_appointments_of_patient, get_admin_name_by_id, delete_doctor_with_id)


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
    with app.app_context():
        u = query_where("patient", f"name = 'patient1'")
        print(u)
        uid = u[0][0]
        utime = u[0][6]
    assert u[0] == (uid, 'patient1', 'surname1', 'Male', 18, 12341234, utime, 'National_id1')


def test_get_admin_by_username(app):
    with app.app_context():
        u = get_admin_by_username('adminuser1')
        uid = u[0]
    assert u == (uid, 'admin1', 'surname1', 'adminuser1', 'password1')


def test_delete_patient_with_national_id(app):
    with app.app_context():
        delete_patient_with_national_id('National_id1')
        u = query_where("patient", f"national_id = 'National_id1'")
    assert u == []


def test_get_doctor_by_username_or_national_id(app):
    with app.app_context():
        u = get_doctor_by_username_or_national_id('doctoruser1','National_id1')
        uid = u[0]
    print(u)
    assert u == (uid, 'doctor1','surname1','password1','doctoruser1','hospital1','title1','profession1',1,'National_id1', True)


def test_add_doctor_to_database(app):
    with app.app_context():
        add_doctor_to_database('doctor11','surname1','password1','doctoruser5','hospital1','title1','profession1',1,'National_id5')
        u = get_doctor_by_username_or_national_id('doctoruser5', 'National_id5')
        uid = u[0]
    assert u == (uid, 'doctor11','surname1','password1','doctoruser5','hospital1','title1','profession1',1,'National_id5', True)


def test_get_appointments_of_doctor(app):
    with app.app_context():
        u = get_appointments_of_doctor(1)
    assert u != None


def test_get_appointments_of_patient(app):
    with app.app_context():
        u = get_appointments_of_patient(1)
    assert u != None


def test_get_admin_name_by_id(app):
    with app.app_context():
        u = get_admin_name_by_id(1)
    # This function actually gets the username of the admin
    assert u == 'adminuser1'


def test_delete_doctor_with_id(app):
    with app.app_context():
        delete_doctor_with_id(2)
        u = get_admin_by_username('docdelete')
    assert u == None