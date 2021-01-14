import functools
from werkzeug.security import check_password_hash
from flask import session, redirect, url_for, render_template, Blueprint, flash
from smarthealth_web.forms import DoctorLoginForm, AddPatientForm, AddAppointmentForm, UpdateAppointmentForm
from smarthealth_web.dboperations import (
    get_doctor_by_username_or_national_id, get_appointments_of_doctor, get_patient_by_nid
)
from decouple import config
from smarthealth_web import dboperations
import psycopg2 as dpapi2
from time import time

bp = Blueprint('doctor', __name__, url_prefix='/doctor')
DATABASE_URL = config('DATABASE_URL')


def doctor_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for("login_page"))
        elif "user_is_doctor" not in session or not session["user_is_doctor"]:
            flash("You are not a doctor.")
            return redirect(url_for("login_page"))
        return view(**kwargs)
    return wrapped_view


@bp.route('/dashboard', methods=('GET',))
@doctor_login_required
def home_page():
    rows = get_appointments_of_doctor(session["user_id"])
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


@bp.route('/add_patient', methods=('GET', 'POST'))
@doctor_login_required
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
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


@bp.route('/appointment', methods=('GET', 'POST'))
@bp.route('/add_appointment', methods=('GET', 'POST'))
@doctor_login_required
def add_appointment():
    form = AddAppointmentForm()
    if form.validate_on_submit():
        patient_national_id = form.patient_national_id.data
        pat = get_patient_by_nid(patient_national_id)
        if pat is not None:
            patient_id = pat[0]
        else:
            error = "Patient does not exists!."
            return render_template('doctor/add_appointment.html', form=form, error=error)
        pred = bool(time() % 2)  # get_prediction(patient_nid)
        dboperations.add_appointment(
            pred,
            form.diagnosis.data,
            form.note.data,
            patient_id,
            session["user_id"],
        )
        return redirect(url_for("doctor.home_page"))
    return render_template('doctor/add_appointment.html', form=form)


@bp.route('/update_appointment/<appointment_id>', methods=('GET', 'POST'))
@doctor_login_required
@doctor_login_required
def update_appointment(appointment_id):
    form = UpdateAppointmentForm()
    if form.validate_on_submit():
        try:
            dboperations.update_appointment(
                form.appointment_id.data,
                form.appointment_realted_patient.data,
                form.appointment_doctor_diagnosis.data,
                form.appointment_diagnosis_comment.data,
            )
        except dpapi2.errors.UniqueViolation:
            return render_template('doctor/update_appointment.html', form=form, errors="Patient ID already exists.")

        return redirect(url_for("doctor.home_page"))

    rows = dboperations.query_where("appointment", "id = " + appointment_id)
    return render_template('doctor/update_appointment.html', form=form)
