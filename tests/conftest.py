from smarthealth_web import create_app, dboperations
from decouple import config
from flask import session
import pytest
import dbinit

@pytest.fixture(scope="module")
def app():
    db_path = config('TEST_DATABASE_URL')
    app = create_app(test_config=True, test_db=db_path)
    with app.app_context():
        dbinit.initialize(delete=True, test=True)
        conn = dboperations.get_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def login_doctor(client):
    with client:
        res = client.post("/doctor/login", data=dict(
            username="dtestuser",
            password="1"
        ), follow_redirects=True)


def login_admin(client):
    with client:
        res = client.post("/admin/login", data=dict(
            username="atestuser",
            password="1"
        ), follow_redirects=True)


def login_patient(client):
    with client:
        res = client.post("/patient/login", data=dict(
            national_id="11111111111",
            logcode="12341234"
        ), follow_redirects=True)