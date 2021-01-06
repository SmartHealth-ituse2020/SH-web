from smarthealth_web import create_app


def test_config():
    assert not create_app().testing
    assert create_app(test_config=True, test_db="").testing


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Doctor Login" in response.data
    assert b"Patient Login" in response.data
