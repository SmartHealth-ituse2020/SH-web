INSERT INTO patient(name, surname, gender, age, logcode, national_id, cratetime)
    VALUES
    ('ptest','veryuniquepatient','Male',18,12341234,'11111111111','now()'),
    ('patient1','getpatient','Male',18,12341234,'22222222222','now()'),
    ('ptest','surname1','Male',18,12341234,'33333333333','now()'),
    ('pgettest','surname1','Male',18,12341234,'44444444444','now()');

INSERT INTO doctor(name, surname, password, username, hospital, title, profession, added_by, national_id, isActive)
    VALUES
    ('dtest','surname1',%s,'dtestuser','hospital1','title1','profession1',1,'111100001111,', True),
    ('doctor1','surname1',%s,'doctoruser1','hospital1','title1','profession1',1,'11112222333', True),
    ('deletedoctor1','surname1',%s,'docdelete','hospital1','title1','profession1',1,'22223333444', True),
    ('deactivdoctor1','surname1',%s,'deactidoctor','hospital1','title1','profession1',1,'33334444555', True);

INSERT INTO admin(name, surname, username, password)
    VALUES
    ('atest','surname1','atestuser',%s),
    ('admin1','surname1','adminuser1',%s);

INSERT INTO appointment(
        prediction_result, doctor_diagnosis, diagnosis_comment,
        appointment_date, related_patient, related_doctor
        )
    VALUES 
        ('Healthy','diagnos1','viewdoctorappointmentss','now()',1,1),
        ('Hypertension','diagnos1','comment1','now()',1,1);