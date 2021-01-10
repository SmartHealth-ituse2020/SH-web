from flask import session, request, redirect, url_for, render_template, Blueprint, g
from smarthealth_web.dboperations import query, query_where
from smarthealth_web.forms import PatientLoginForm
from decouple import config
import psycopg2 as dpapi2

bp = Blueprint('patient', __name__, url_prefix='/patient')
DATABASE_URL = config('DATABASE_URL')


@bp.route('/dashboard', methods=('GET',))
def home_page():
    patientid = session["patient"][0]
    print(patientid)
    rows = query_where("appointment", f"related_patient='{patientid}'")
    return render_template("patient/patient_dashboard.html", rows=sorted(rows), len=len(rows))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = PatientLoginForm()
    if form.validate_on_submit():
        # Add user validation code here
        p_national_id = form.national_id.data
        p = query_where(table_name="patient", condition=f"national_id='{p_national_id}'")
        if p:
            try:
                lc = int(form.logcode.data)
            except ValueError:
                lc = None
            if lc == p[0][6]:
                session["patient"] = p[0]
                return redirect(url_for("patient.home_page"))  # if successful


        return render_template(
            'patient/patient_login.html',
            form=form,
            errors="Invalid credentials.",
        )
    return render_template('patient/patient_login.html', form=form)
