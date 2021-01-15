INSERT INTO patient(name, surname, gender, age, logcode, national_id)
    VALUES
    ('patient1','surname1','Male',18,12341234,'National_id1');

INSERT INTO doctor(name, surname, password, username, hospital, title, profession, added_by, national_id)
    VALUES
    ('doctor1','surname1','password1','doctoruser1','hospital1','title1','profession1',1,'National_id1');

INSERT INTO admin(name, surname, username, password)
    VALUES
    ('admin1','surname1','adminuser1','password1');