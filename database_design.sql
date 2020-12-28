CREATE TABLE IF NOT EXISTS ADMIN
(
    adminid SERIAL PRIMARY KEY,
    adminname character varying(10) COLLATE pg_catalog."default" NOT NULL,
    adminsurname character varying(10) COLLATE pg_catalog."default",
    adminusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    adminpassword character varying(20) COLLATE pg_catalog."default" NOT NULL
);

CREATE TABLE IF NOT EXISTS APPOINTMENT
(
    appointmentid SERIAL PRIMARY KEY,
    predictionresult boolean,
    doctordiagnosis text COLLATE pg_catalog."default",
    diagnosiscomment text COLLATE pg_catalog."default",
    appointmentdate date,
    relatedpatient integer NOT NULL,
    relateddoctor integer
);

CREATE TABLE IF NOT EXISTS DOCTOR
(
    doctorid SERIAL PRIMARY KEY,
    doctorname character varying(10) COLLATE pg_catalog."default" NOT NULL,
    doctorsurname character varying(10) COLLATE pg_catalog."default",
    doctorpassword character varying(20) COLLATE pg_catalog."default" NOT NULL,
    doctorusername character varying(20) COLLATE pg_catalog."default" NOT NULL,
    doctorhospital text COLLATE pg_catalog."default",
    doctortitle character varying(10) COLLATE pg_catalog."default",
    doctorprofession character varying(50) COLLATE pg_catalog."default",
    added_by integer NOT NULL,
    doctornid integer
);

CREATE TABLE IF NOT EXISTS PATIENT
(
    patientid SERIAL PRIMARY KEY,
    patientname character varying(10) COLLATE pg_catalog."default" NOT NULL,
    patientsurname character varying(10) COLLATE pg_catalog."default",
    patientgender character varying(10) COLLATE pg_catalog."default",
    patientage integer,
    patientlogcode integer NOT NULL
);

CREATE TABLE IF NOT EXISTS public.emr_data
(
    emr_id SERIAL PRIMARY KEY,
    uploader_doctorid integer,
    related_patientid integer NOT NULL,
    emr_comment text COLLATE pg_catalog."default",
    emr_type character varying(30) COLLATE pg_catalog."default" NOT NULL,
    emr_date date,
    emr_filepath character varying(250) COLLATE pg_catalog."default" NOT NULL,
    emr_appoinment integer,
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
