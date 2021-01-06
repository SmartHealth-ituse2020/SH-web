from smarthealth_web import create_app, dboperations
from decouple import config
import pytest
import dbinit
import os


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'r') as f:
    _data_sql = f.read()


@pytest.fixture
def app():
    db_path = config('DATABASE_URL')
    app = create_app(test_config=True, test_db=db_path)

    with app.app_context():
        dbinit.initialize()
        conn = dboperations.get_db()
        cur = conn.cursor()
        cur.execute(_data_sql)
        cur.close()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
