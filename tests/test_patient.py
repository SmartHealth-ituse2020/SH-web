from smarthealth_web.dboperations import query_where
from flask_wtf import FlaskForm
from tests.conftest import login_doctor, login_patient
from flask import url_for
import pytest


def test_login(client):
    req = client.get("/patient/login")
    # more tests will be added when authentication backend added
    assert req.status_code == 200


def test_home_page(app):# Works good, viewdoctorappointmentss
    cli = app.test_client()# is to check if current patient(1)s appointment
    login_patient(cli)# is loaded
    with app.app_context():
        req = cli.get("/patient/dashboard")
    assert b"viewdoctorappointmentss" in req.data
    assert req.status_code == 200


def test_patient_details(app):# Works good
    cli = app.test_client()
    login_patient(cli)
    with app.app_context():
        res = cli.get("/patient/patient_details")
    assert b"veryuniquepatient" in res.data
    assert res.status_code == 200

def test_doctor_details(app):
    cli = app.test_client()
    login_patient(cli)
    with app.app_context():
        res = cli.get("/patient/doctor_details/1")
    assert b"Profession" in res.data
    assert res.status_code == 200


def test_appointment_details(app):
    cli = app.test_client()
    login_patient(cli)
    with app.app_context():
        res = cli.get("/patient/appointment_details/1")
    assert b"Appointment Details" in res.data
    assert res.status_code == 200