from smarthealth_web.dboperations import query_where
from flask_wtf import FlaskForm
from tests.conftest import login_doctor, login_admin
from flask import url_for
import pytest


def test_login(client):
    with client:
        req = client.get("/admin/login")
        res = client.post("/admin/login", data=dict(
            username="wronguser",
            password="1"
        ), follow_redirects=True)
        assert b"Invalid username or password." in res.data
        res = client.post("/admin/login", data=dict(
            username="atestuser",
            password="wrong"
        ), follow_redirects=True)
        assert b"Invalid username or password." in res.data
        res = client.post("/admin/login", data=dict(
            username="atestuser",
            password="1"
        ), follow_redirects=True)
        assert res.status_code == 200


def test_add_doctor(app):
    cli = app.test_client()
    login_admin(cli)
    with app.app_context():
        form = {    
            "national_id": "12341234123",
            "name": "newdoc",
            "surname": "surdoc",
            "password": "1",
            "confirm": "1",
            "username": "DoctorNew",
            "hospital": "hosp",
            "title": "Dr.",
            "profession": "Heart"
        }
        res = cli.post('/admin/add_doctor', data=form, follow_redirects=False)
        p = query_where(table_name="doctor", condition="name= 'newdoc'")
    assert p != []
    assert res.status_code == 302


def test_home_page(app):# Works good, deletedoctor1 can be any info in the table doctor
    cli = app.test_client()
    login_admin(cli)
    with app.app_context():
        res = cli.get('/admin/dashboard', follow_redirects=True)
    assert res.status_code == 200
    assert b"deletedoctor1" in res.data 


def test_remove_doctor(app):# Works good
    cli = app.test_client()
    login_admin(cli)
    with app.app_context():
        res = cli.get('/admin/deactivate_doctor/1', follow_redirects=True)
        d = query_where(table_name="doctor", condition="id= 1")
    assert d[0][10] == False
    assert res.status_code == 200