INSERT INTO admin (adminname, adminsurname, adminusername, adminpassword)
    VALUES
    ('test', 'tester', 'admintest1', 'adminpass');

DELETE FROM admin WHERE adminname='test';

INSERT INTO patient(name, surname, gender, age, logcode, national_id)
    VALUES
    ('patient1','surname1','Male',18,12341234,'National_id1');