# import functools
# from werkzeug.security import check_password_hash, generate_password_hash

from flask import request, redirect, url_for
from smarthealth_web.forms import AdminLoginForm
from flask import render_template, Blueprint
from decouple import config
from smarthealth_web import dboperations
import psycopg2 as dpapi2

bp = Blueprint('admin', __name__, url_prefix='/admin')
DATABASE_URL = config('DATABASE_URL')


@bp.route('/dashboard', methods=('GET',))
def home_page():
    return render_template("admin/admin_dashboard.html")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Add user validation code here
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None and user.verify_password(form.password.data):
        # login_user(None)
        return redirect(url_for("admin.home_page"))  # if successful
    return render_template('admin/admin_login.html', form=form)
