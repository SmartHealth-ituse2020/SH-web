import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
   '''
	CREATE TABLE IF NOT EXISTS ADMIN
	(
		adminid integer NOT NULL,
		adminname character varying(10) COLLATE pg_catalog."default" NOT NULL,
		adminsurname character varying(10) COLLATE pg_catalog."default",
		adminusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
		adminpassword character varying(20) COLLATE pg_catalog."default" NOT NULL,
		CONSTRAINT admin_pkey PRIMARY KEY (adminid)
	);
	CREATE TABLE IF NOT EXISTS APPOINTMENT
	(
		appointmentid integer NOT NULL,
		predictionresult boolean,
		doctordiagnosis text COLLATE pg_catalog."default",
		diagnosiscomment text COLLATE pg_catalog."default",
		appointmentdate date,
		relatedpatient integer NOT NULL,
		relateddoctor integer,
		CONSTRAINT appointment_pkey PRIMARY KEY (appointmentid)
	);
	CREATE TABLE IF NOT EXISTS DOCTOR
	(
		doctorid integer NOT NULL,
		doctorname character varying(10) COLLATE pg_catalog."default" NOT NULL,
		doctorsurname character varying(10) COLLATE pg_catalog."default",
		doctorpassword character varying(20) COLLATE pg_catalog."default" NOT NULL,
		doctorusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
		doctorhospital text COLLATE pg_catalog."default",
		doctortitle character varying(10) COLLATE pg_catalog."default",
		doctorprofession character varying(50) COLLATE pg_catalog."default",
		added_by integer NOT NULL,
		doctornid integer,
		CONSTRAINT doctor_pkey PRIMARY KEY (doctorid)
	);
	CREATE TABLE IF NOT EXISTS PATIENT
	(
		patientid integer NOT NULL,
		patientname character varying(10) COLLATE pg_catalog."default" NOT NULL,
		patientsurname character varying(10) COLLATE pg_catalog."default",
		patientgender character varying(10) COLLATE pg_catalog."default",
		patientage integer,
		patientnid integer,
		patientlogcode integer NOT NULL,
		CONSTRAINT patient_pkey PRIMARY KEY (patientid)
	);
	CREATE TABLE IF NOT EXISTS public.emr_data
	(
		emr_id integer NOT NULL,
		uploader_doctorid integer,
		related_patientid integer NOT NULL,
		emr_comment text COLLATE pg_catalog."default",
		emr_type character varying(30) COLLATE pg_catalog."default" NOT NULL,
		emr_date date,
		emr_filepath character varying(250) COLLATE pg_catalog."default" NOT NULL,
		emr_appoinment integer,
		CONSTRAINT emr_data_pkey PRIMARY KEY (emr_id),
		CONSTRAINT doctor_fkey FOREIGN KEY (uploader_doctorid)
			REFERENCES DOCTOR (doctorid) MATCH SIMPLE
			ON UPDATE NO ACTION
			ON DELETE NO ACTION
			NOT VALID,
		CONSTRAINT patient_fkey FOREIGN KEY (related_patientid)
			REFERENCES PATIENT (patientid) MATCH SIMPLE
			ON UPDATE NO ACTION
			ON DELETE NO ACTION
			NOT VALID
	);
	CREATE TABLE IF NOT EXISTS DLMODEL
	(
		modelversion integer NOT NULL,
		modelweights integer,
		CONSTRAINT deeplearningmodel_pkey PRIMARY KEY (modelversion)
	);
   '''
   ]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        
        cursor.close()


if __name__ == "__main__":
    # url = os.getenv("DATABASE_URL")
    # if url is None:
    #    print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
    #    sys.exit(1)
    # initialize(url)
    