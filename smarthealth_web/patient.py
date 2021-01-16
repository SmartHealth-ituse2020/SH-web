from flask import session, request, redirect, url_for, render_template, Blueprint, g
from smarthealth_web.dboperations import query, query_where, get_patient_by_nid, get_appointments_of_patient
from smarthealth_web.forms import PatientLoginForm
from decouple import config
import psycopg2 as dpapi2

bp = Blueprint('patient', __name__, url_prefix='/patient')
DATABASE_URL = config('DATABASE_URL')


@bp.route('/dashboard', methods=('GET',))
def home_page():
    patientid = session["patient"][0]
    print(patientid)
    rows = get_appointments_of_patient(patientid)
    return render_template("patient/patient_dashboard.html", rows=rows, len=len(rows))

@bp.route('/patient_details', methods=('GET', 'POST'))
def patient_details():
    patientid = session["patient"][0]
    row = query_where("patient", "id = " + str(patientid))
    return render_template('patient/patient_details.html', row=row[0])

@bp.route('/doctor_details/<doctor_id>', methods=('GET', 'POST'))
def doctor_details(doctor_id):
    row = query_where("doctor", "id = " + doctor_id)
    return render_template('patient/doctor_details.html', row=row[0])

@bp.route('/appointment_details/<appointment_id>', methods=('GET', 'POST'))
def appointment_details(appointment_id):
    patientid = session["patient"][0]
    rows = get_appointments_of_patient(patientid)
    i = 0
    while int(appointment_id) != int(rows[i][0]):
        i = i+1
    return render_template('patient/appointment_details.html', row=rows[i])

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = PatientLoginForm()
    if form.validate_on_submit():
        # Add user validation code here
        p_national_id = form.national_id.data
        p = get_patient_by_nid(p_national_id)
        if p:
            try:
                lc = int(form.logcode.data)
            except ValueError:
                lc = None
            if lc == p[5]:
                session["patient"] = p
                return redirect(url_for("patient.home_page"))  # if successful

        return render_template(
            'patient/patient_login.html',
            form=form,
            errors=f"Invalid credentials.",
        )
    return render_template('patient/patient_login.html', form=form)
