from smarthealth_web import create_app, dboperations
from decouple import config
from flask import session
import pytest
import dbinit
# I tried to run the statements in data.sql to fill the test database
# But I failed, it doesn't break but it doesn't fill too
TEST_STATEMENTS = [open("tests\data.sql", "r").read()]

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


def login(client, username, password):
    return client.post('/doctor/login', data=dict(
        username="dtestuser",
        password="password1"
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


@pytest.fixture
def adminSession(client):
    with client.session_transaction() as session:
        session["user_id"] = 0
        session["user_is_admin"] = True
        session["user_is_doctor"] = False
    yield session


@pytest.fixture(scope="module")
def doctorSession(client):
    with client.session_transaction() as session:
        session["user_id"] = 0
        session["user_is_admin"] = False
        session["user_is_doctor"] = True
    yield session


@pytest.fixture
def patientSession(client):
    with client.session_transaction() as session:
        session["patient"] = dboperations.get_patient_by_nid('ptestNid')
    yield session