CREATE TABLE IF NOT EXISTS ADMIN
(
    id SERIAL PRIMARY KEY,
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    surname character varying(30) COLLATE pg_catalog."default",
    username character varying(30) COLLATE pg_catalog."default" NOT NULL,
    password character varying(100) COLLATE pg_catalog."default" NOT NULL
);

CREATE TABLE IF NOT EXISTS APPOINTMENT
(
    id SERIAL PRIMARY KEY,
    prediction_result varchar(25),
    doctor_diagnosis text COLLATE pg_catalog."default",
    diagnosis_comment text COLLATE pg_catalog."default",
    appointment_date date,
    related_patient integer NOT NULL,
    related_doctor integer
);

CREATE TABLE IF NOT EXISTS DOCTOR
(
    id SERIAL PRIMARY KEY,
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    surname character varying(30) COLLATE pg_catalog."default",
    password character varying(100) COLLATE pg_catalog."default" NOT NULL,
    username character varying(30) COLLATE pg_catalog."default" NOT NULL,
    hospital text COLLATE pg_catalog."default",
    title character varying(50) COLLATE pg_catalog."default",
    profession character varying(50) COLLATE pg_catalog."default",
    added_by integer NOT NULL,
    national_id varchar(15),
    isActive BOOLEAN
);

CREATE TABLE IF NOT EXISTS PATIENT
(
    id SERIAL PRIMARY KEY,
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    surname character varying(30) COLLATE pg_catalog."default",
    gender character varying(10) COLLATE pg_catalog."default",
    age integer,
    logcode integer NOT NULL,
    cratetime timestamp,
    national_id varchar(15)
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
        REFERENCES DOCTOR (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT patient_fkey FOREIGN KEY (related_patientid)
        REFERENCES PATIENT (id) MATCH SIMPLE
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
