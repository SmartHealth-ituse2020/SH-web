# import functools

from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, redirect, url_for, session
from smarthealth_web.forms import AdminLoginForm
from smarthealth_web.dboperations import get_admin_by_username
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
    error = None
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        u = get_admin_by_username(username)

        if u is not None:
            error = "Invalid username or password."
        elif not check_password_hash(u[4], password):
            error = "Invalid username or password."
        if error is None:
            session.clear()
            session["user_id"] = u[0]
            session["user_is_admin"] = True

            return redirect(url_for("admin.home_page"))
    return render_template('admin/admin_login.html', form=form, error=error)
