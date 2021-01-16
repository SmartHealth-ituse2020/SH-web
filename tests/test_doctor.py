from smarthealth_web.dboperations import query_where
from flask_wtf import FlaskForm
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


@pytest.mark.skip
def test_add_patient_form_with_proper_input(app):
    cli = app.test_client()
    with app.app_context():
        form = {    
            "patient_national_id": "00000000000",
            "patient_name": "test proper input",
            "patient_surname": "TESTSURNAME",
            "patient_age": 22,
            "patient_gender": "Male"
        }
        res = cli.post('/doctor/add_patient', data=form, follow_redirects=False)
        p = query_where(table_name="patient", condition="name='test proper input'")
    assert p != []
    assert res.status_code == 302


@pytest.mark.skip
def test_add_patient_form_without_age(app,doctorSession):
    cli = app.test_client()
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


def test_add_patient_form_without_name(app):
    cli = app.test_client()
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


def test_add_patient_form_without_surname(app):
    cli = app.test_client()
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


def test_add_patient_form_without_gender(app):
    cli = app.test_client()
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
