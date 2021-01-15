from smarthealth_web import create_app, dboperations
from decouple import config
import pytest
import dbinit
# I tried to run the statements in data.sql to fill the test database
# But I failed, it doesn't break but it doesn't fill too
TEST_STATEMENTS = [open("tests\data.sql", "r").read()]

@pytest.fixture
def app():
    db_path = config('TEST_DATABASE_URL')
    app = create_app(test_config=True, test_db=db_path)

    with app.app_context():
        dbinit.initialize(delete=True, test=True)
        conn = dboperations.get_db()
        cursor = conn.cursor()
        for statement in TEST_STATEMENTS:
            cursor.execute(statement)
        cursor.close()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
