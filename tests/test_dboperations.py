import psycopg2 as dbapi2
from smarthealth_web.dboperations import query_where


def test_add_newpatient(app):
    # A basic new patient to test
    statement = """
    INSERT INTO patient(name, surname, gender, age, logcode, national_id)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    values = ("Name", "Surname", "Gender", 18, 12341234, "National_id")
    # Test adding without being present
    with app.app_context():
        with dbapi2.connect(app.config['DATABASE']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, values)
        u = query_where("patient", f"name ='Name'")
        # uid is patientid which is serial
        # utime is cratetime which is timestamp
        uid = u[0][0]
        utime = u[0][6]
    assert u[0] == (uid, 'Name', 'Surname', 'Gender', 18, 12341234, utime, 'National_id')
    # Test again with being present
    # To be implemented
