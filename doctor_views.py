from flask import request, redirect, url_for
from forms import DoctorLoginForm, AddPatientForm
from flask import render_template
from decouple import config
import dboperations

DATABASE_URL = config('DATABASE_URL')


def home_page():
    rows = dboperations.query(DATABASE_URL, "patient")
    # rows={"...", "...", "...", "...", "...", "..."}
    return render_template("home_doctor.html", rows=sorted(rows), len=len(rows))


def login():
    form = DoctorLoginForm()
    if form.validate_on_submit():
        # Add user validation code here
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        # login_user(None)
        return redirect(url_for("home_page"))  # if successful
    return render_template('login_doctor.html', form=form)


def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        # Check if any patient exists with given ID
        # Dont add again if patient exists
        dboperations.add_newpatient(
            DATABASE_URL,
            form.patient_id.data,
            form.patient_name.data,
            form.patient_surname.data,
            form.patient_gender.data,
            form.patient_age.data,
            form.patient_logcode.data
        )

        return redirect(url_for("home_page"))
    return render_template('patient_add.html', form=form)


"""
def add_patient():

    if request.method == "GET":
        values = {"patientname": ""}
        return render_template("patient_add.html", values=values)
    else:
        valid = validate_patient_form(request.form)
        if not valid:
            return render_template("patient_add.html", values=request.form)

        form_patientid = request.form["patientid"]
        form_patientname = request.form["patientname"]
        form_patientsurname = request.form["patientsurname"]
        form_patientgender = request.form["patientgender"]
        form_patientage = request.form["patientage"]
        form_patientlogcode = request.form["patientlogcode"]

        dboperations.add_newpatient(
            DATABASE_URL,
            form_patientid,
            form_patientname,
            form_patientsurname,
            form_patientgender,
            form_patientage,
            form_patientlogcode
        )

        return redirect(url_for("home_page_doctor"))
"""


def validate_patient_form(form):
    form.data = {}
    form.errors = {}

    form_topic = form.get("patientname", "").strip()
    if len(form_topic) == 0:
        form.errors["patientname"] = "patientname cannot be blank."
    else:
        form.data["patientname"] = form_topic

    return len(form.errors) == 0
