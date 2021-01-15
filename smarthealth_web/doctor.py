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


@bp.route('/', methods=('GET',))
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


@bp.route('/patient', methods=('GET', 'POST'))
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

@bp.route('/patient_details/<patient_id>', methods=('GET', 'POST'))
@doctor_login_required
def patient_details(patient_id):
    row = dboperations.query_where("patient", "id = " + patient_id)
    return render_template('doctor/patient_details.html', row=row[0])


@bp.route('/update_appointment/<appointment_id>', methods=('GET', 'POST'))
@doctor_login_required
def update_appointment(appointment_id):
    form = UpdateAppointmentForm()

    appointments = get_appointments_of_doctor(session["user_id"])

    error = "Permission denied for this appointment."  # initialize error message
    ap = None  # initialize appointment
    for i in range(len(appointments)):
        ap = appointments[i]
        if str(ap[0]) == appointment_id:  # appointment is related to doctor
            error = None
            break

    if error is not None or ap is None:  # if not related, return error.
        flash(error)
        return redirect(url_for("doctor.home_page"))

    # set template data for rendering
    data = {
        "id": ap[0],
        "date": ap[1],
        "patient_national_id": ap[6],
        "diagnosis": ap[7],
        "note": ap[8],
    }

    if form.validate_on_submit():

        # initialize all as None
        patient_nid = diagnosis = note = None

        # patient nid is changed
        if form.patient_nid.data:
            patient_nid = form.patient_nid.data
        else:
            patient_nid = ap[5]  # unchanged

        # diagnosis is changed
        if form.diagnosis.data:
            diagnosis = form.diagnosis.data
        else:
            diagnosis = ap[2]  # unchanged

        # note is changed
        if form.note.data:
            note = form.note.data
        else:
            note = ap[3]  # unchanged

        try:
            dboperations.update_appointment(
                appointment_id,
                form.patient_nid.data,
                form.diagnosis.data,
                form.note.data,
            )
        except (dpapi2.errors.UniqueViolation, KeyError) as e:
            return render_template(
                'doctor/update_appointment.html',
                form=form,
                errors=e,
                data=data,
            )

        return redirect(url_for("doctor.home_page"))

    return render_template('doctor/update_appointment.html', form=form, data=data, error=error)
