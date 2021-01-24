from smarthealth_web.dboperations import query_where
from flask_wtf import FlaskForm
from tests.conftest import login_doctor
from flask import url_for
import pytest

def test_login(client):
    with client:
        req = client.get("/doctor/login")
        res = client.post("/doctor/login", data=dict(
            username="wronguser",
            password="1"
        ), follow_redirects=True)
        assert b"Invalid username or password." in res.data
        res = client.post("/doctor/login", data=dict(
            username="dtestuser",
            password="wrong"
        ), follow_redirects=True)
        assert b"Invalid username or password." in res.data
        res = client.post("/doctor/login", data=dict(
            username="dtestuser",
            password="1"
        ), follow_redirects=True)
        assert b"Appointment ID" in res.data
        assert res.status_code == 200


def test_add_patient_proper(app):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        form = {    
            "patient_national_id": "00000000000",
            "patient_name": "test proper input",
            "patient_surname": "TESTSURNAME",
            "patient_age": 22,
            "patient_gender": "Male"
        }
        res = cli.post('/doctor/add_patient', data=form, follow_redirects=False)
        p = query_where(table_name="patient", condition="name= 'test proper input'")
    assert p != []
    assert res.status_code == 302


def test_add_patient_no_age(app):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        form = {
            "patient_national_id": "00000000000",
            "patient_name": "test without age",
            "patient_surname": "TESTSURNAME",
            "patient_age": None,
            "patient_gender": "Male"
        }
        res = cli.post('/doctor/add_patient', data=form, follow_redirects=True)

        p = query_where("patient", "name = 'test without age'")

    assert p == []
    assert res.status_code == 200
    #assert b"This field is required" in res.data


def test_add_patient_no_name(app):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        form = {
            "patient_national_id": "00000000000",
            "patient_name": None,
            "patient_surname": "test without name",
            "patient_age": 25,
            "patient_gender": "Male"
        }
        res = cli.post('/doctor/add_patient', data=form, follow_redirects=True)

        p = query_where("patient", "surname = 'test without name'")

    assert p == []
    assert res.status_code == 200
    #assert b"This field is required" in res.data


def test_add_patient_no_surname(app):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        form = {
            "patient_national_id": "00000000000",
            "patient_name": "test without surname",
            "patient_surname": None,
            "patient_age": 25,
            "patient_gender": "Male"
        }
        res = cli.post('/doctor/add_patient', data=form, follow_redirects=True)

        p = query_where("patient", "name = 'test without surname'")

    assert p == []
    assert res.status_code == 200
    #assert b"This field is required" in res.data


def test_add_patient_no_gender(app):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        form = {
            "patient_national_id": "00000000000",
            "patient_name": "test without gender",
            "patient_surname": "TESTSURNAME",
            "patient_age": 15,
            "patient_gender": None
        }
        res = cli.post('/doctor/add_patient', data=form, follow_redirects=True)

        p = query_where("patient", "name = 'test without gender'")
    assert res.status_code == 200
    #assert b"This field is required" in res.data
    assert p == []


def test_home_page(app):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        res = cli.get('/doctor/dashboard')
    assert res.status_code == 200
    assert b"Doctor's Diagnosis" in res.data


def test_add_appointment(app, mocker):
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        # mock get_prediction to return corrupted
        mocker.patch('smarthealth_web.doctor.get_prediction', return_value = b"Corrupted")
        form ={ "patient_national_id": "11111111111",# System doesn't allow
                "diagnosis": "Healthy",
                "note": "with_unavailable_prediction"}
        res = cli.post('/doctor/add_appointment', data=form, follow_redirects=True)
        a = query_where("appointment","diagnosis_comment = 'with_unavailable_prediction'")
        assert res.status_code == 200
        assert b"Doctor's Diagnosis" in res.data
        assert a[0][1] == "Error"
        # test with prediction = Positive
        mocker.patch('smarthealth_web.doctor.get_prediction', return_value = b"Pos")
        form ={ "patient_national_id": "11111111111",
                "diagnosis": "Sick",
                "note": "with_pos_prediction"}
        res = cli.post('/doctor/add_appointment', data=form, follow_redirects=True)
        a = query_where("appointment","diagnosis_comment = 'with_pos_prediction'")
        assert res.status_code == 200
        assert b"Doctor's Diagnosis" in res.data
        assert a[0][1] == "Hypertension"
        # test with prediction = Negative
        mocker.patch('smarthealth_web.doctor.get_prediction', return_value = b"Neg")
        form ={ "patient_national_id": "11111111111",
                "diagnosis": "Good Condition",
                "note": "with_neg_prediction"}
        res = cli.post('/doctor/add_appointment', data=form, follow_redirects=True)
        a = query_where("appointment","diagnosis_comment = 'with_neg_prediction'")
        assert res.status_code == 200
        assert b"Doctor's Diagnosis" in res.data
        assert a[0][1] == "Healthy"
        # test with system fault in prediction side
        mocker.patch('smarthealth_web.doctor.get_prediction', return_value = b"a")
        form ={ "patient_national_id": "11111111111",
                "diagnosis": "Good Condition",
                "note": "with_system_fault_prediction"}
        res = cli.post('/doctor/add_appointment', data=form, follow_redirects=True)
        a = query_where("appointment","diagnosis_comment = 'with_system_fault_prediction'")
        assert res.status_code == 200
        assert b"Doctor's Diagnosis" in res.data
        assert a[0][1] == "System Fault"
        


def test_patient_details(app):# Works good, patient can be any patient that the doctor
    cli = app.test_client()# In our current session has added
    login_doctor(cli)
    with app.app_context():
        res = cli.get('/doctor/patient_details/1')
    assert res.status_code == 200
    assert b"ptest" in res.data


def test_update_appointment(app):# Works good
    cli = app.test_client()
    login_doctor(cli)
    with app.app_context():
        form = {
            "patient_nid": "33333333333",
            "diagnosis": "Healthy",
            "note": "verymuch"
        }
        res = cli.post('/doctor/update_appointment/1', data=form, follow_redirects=True)
        a = query_where("appointment","diagnosis_comment = 'verymuch'")
    assert res.status_code == 200
    assert a != []