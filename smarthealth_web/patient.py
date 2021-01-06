# import functools
# from werkzeug.security import check_password_hash, generate_password_hash

from flask import request, redirect, url_for
from smarthealth_web.forms import PatientLoginForm
from flask import render_template, Blueprint
from decouple import config
from smarthealth_web import dboperations
import psycopg2 as dpapi2

bp = Blueprint('patient', __name__, url_prefix='/patient')
DATABASE_URL = config('DATABASE_URL')


@bp.route('/dashboard', methods=('GET',))
def home_page():
    patientid="1"
    rows = dboperations.query_where("appointment", f"relatedpatient='{patientid}'")
    return render_template("patient/patient_dashboard.html", rows=sorted(rows), len=len(rows))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = PatientLoginForm()
    if form.validate_on_submit():
        # Add user validation code here
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        # login_user(None)
        return redirect(url_for("patient.home_page"))  # if successful
    return render_template('patient/patient_login.html', form=form)
