from flask import render_template
from flask import request, redirect, url_for
import psycopg2 as dbapi2
import os
from forms import DoctorLoginForm

import dboperations

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgres://fvtkacqijrpxfk:9af8c01dc052361fd51630b634e9a1df34106a7eae0ac736c6a36099bb476d87@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/d4qj8s0lt8sev8"


def home_page_doctor():
    rows = dboperations.query(DATABASE_URL, "patient")
#     rows={"...", "...", "...", "...", "...", "..."}
    return render_template("home_doctor.html", rows=sorted(rows), len=len(rows))


def login_page_doctor():
    form = DoctorLoginForm()  # request.form)
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        # login_user(None)
        return redirect(url_for("home_page_doctor"))
    return render_template('login_doctor.html', form=form)


def add_patient_page_doctor():
    
    if request.method == "GET":
          values = {"patientname":""}
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
          
          dboperations.add_newpatient(DATABASE_URL, form_patientid, form_patientname, form_patientsurname, form_patientgender, form_patientage, form_patientlogcode)
          return redirect(url_for("home_page_doctor"))

def validate_patient_form(form):
    form.data = {}
    form.errors = {}
    
    form_topic = form.get("patientname", "").strip()
    if len(form_topic) == 0:
        form.errors["patientname"] = "patientname cannot be blank."
    else:
        form.data["patientname"] = form_topic

    return len(form.errors) == 0