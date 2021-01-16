INSERT INTO patient(name, surname, gender, age, logcode, national_id)
    VALUES
    ('patient1','surname1','Male',18,12341234,'National_id1'),
    ('ptest','surname1','Male',18,12341234,'ptestNid');

INSERT INTO doctor(name, surname, password, username, hospital, title, profession, added_by, national_id, isActive)
    VALUES
    ('dtest','surname1',%s,'dtestuser','hospital1','title1','profession1',1,'dtestNid,', True),
    ('doctor1','surname1',%s,'doctoruser1','hospital1','title1','profession1',1,'National_id1', True),
    ('deletedoctor1','surname1',%s,'docdelete','hospital1','title1','profession1',1,'delete_Nid', True);

INSERT INTO admin(name, surname, username, password)
    VALUES
    ('admin1','surname1','adminuser1','password1'),
    ('atest','surname1','atestuser','password1');

INSERT INTO appointment(
        prediction_result, doctor_diagnosis, diagnosis_comment,
        appointment_date, related_patient, related_doctor
        )
    VALUES (True,'diagnos1','comment1','now()',1,1);