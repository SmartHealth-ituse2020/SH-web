# import functools
# from werkzeug.security import check_password_hash, generate_password_hash

from flask import request, redirect, url_for
from smarthealth_web.forms import DoctorLoginForm, AddPatientForm
from flask import render_template, Blueprint
from decouple import config
from smarthealth_web import dboperations
import psycopg2 as dpapi2

bp = Blueprint('doctor', __name__, url_prefix='/doctor')
DATABASE_URL = config('DATABASE_URL')


@bp.route('/dashboard', methods=('GET',))
def home_page():
    rows = dboperations.query(DATABASE_URL, "patient")
    # rows={"...", "...", "...", "...", "...", "..."}
    return render_template("doctor/doctor_dashboard.html", rows=sorted(rows), len=len(rows))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = DoctorLoginForm()
    if form.validate_on_submit():
        # Add user validation code here
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        # login_user(None)
        return redirect(url_for("doctor.home_page"))  # if successful
    return render_template('doctor/doctor_login.html', form=form)


@bp.route('/add', methods=('GET', 'POST'))
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        # Check if any patient exists with given ID
        # Dont add again if patient exists
        try:
            dboperations.add_newpatient(
                DATABASE_URL,
                form.patient_id.data,
                form.patient_name.data,
                form.patient_surname.data,
                form.patient_gender.data,
                form.patient_age.data,
                form.patient_logcode.data
            )
        except dpapi2.errors.UniqueViolation:
            return render_template('doctor/add_patient.html', form=form, errors="Patient ID already exists.")

        return redirect(url_for("doctor.home_page"))
    return render_template('doctor/add_patient.html', form=form)
