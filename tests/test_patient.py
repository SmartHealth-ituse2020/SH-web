def tuplereturn():
    return('1', 'name')


def test_login(client):
    req = client.get("/patient/login")
    # more tests will be added when authentication backend added
    assert req.status_code == 200


def test_viewAppointment(client):
    with client.session_transaction() as session:
        session["patient"] = tuplereturn()
    req = client.get("patient/dashboard")
    # test to check if homepage is loaded properly
    assert req.status_code == 200
