INSERT INTO admin (adminname, adminsurname, adminusername, adminpassword)
    VALUES
    ('test', 'tester', 'admintest1', 'adminpass');

DELETE FROM admin WHERE adminname='test';
