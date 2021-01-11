# import functools
from werkzeug.security import check_password_hash
from flask import session, redirect, url_for, render_template, Blueprint
from smarthealth_web.forms import DoctorLoginForm, AddPatientForm
from smarthealth_web.dboperations import get_doctor_by_username_or_national_id
from decouple import config
from smarthealth_web import dboperations
import psycopg2 as dpapi2

bp = Blueprint('doctor', __name__, url_prefix='/doctor')
DATABASE_URL = config('DATABASE_URL')


@bp.route('/dashboard', methods=('GET',))
def home_page():
    rows = dboperations.query(table_name="patient")
    return render_template("doctor/doctor_dashboard.html", rows=sorted(rows), len=len(rows))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = DoctorLoginForm()
    error = None
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        u = get_doctor_by_username_or_national_id(username, "0")  # give national id as 0

        if u is None:
            error = "Invalid username or password."
        elif not check_password_hash(u[3], password):
            error = "Invalid username or password."
        if error is None:
            session.clear()
            session["user_id"] = u[0]
            session["user_is_admin"] = False
            session["user_is_doctor"] = True

            return redirect(url_for("doctor.home_page"))
    return render_template('doctor/doctor_login.html', form=form, error=error)


@bp.route('/add', methods=('GET', 'POST'))
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        # Check if any patient exists with given ID
        # Dont add again if patient exists
        try:
            dboperations.add_newpatient(
                form.patient_national_id.data,
                form.patient_name.data,
                form.patient_surname.data,
                form.patient_gender.data,
                form.patient_age.data,
            )
        except dpapi2.errors.UniqueViolation:
            return render_template('doctor/add_patient.html', form=form, errors="Patient ID already exists.")

        return redirect(url_for("doctor.home_page"))
    return render_template('doctor/add_patient.html', form=form)
