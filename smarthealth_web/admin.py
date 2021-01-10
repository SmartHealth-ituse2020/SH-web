import functools
from werkzeug.security import check_password_hash
from flask import redirect, url_for, session, flash
from smarthealth_web.forms import AdminLoginForm
from smarthealth_web.dboperations import get_admin_by_username
from flask import render_template, Blueprint
from decouple import config


bp = Blueprint('admin', __name__, url_prefix='/admin')
DATABASE_URL = config('DATABASE_URL')


def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for("login_page"))
        elif "user_is_admin" not in session or not session["user_is_admin"]:
            flash("You are not an admin.")
            return redirect(url_for("doctor.dashboard"))
        return view(**kwargs)
    return wrapped_view


@bp.route('/dashboard', methods=('GET',))
@admin_login_required
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

        if u is None:
            error = "Invalid username or password."
        elif not check_password_hash(u[4], password):
            error = "Invalid username or password."
        if error is None:
            session.clear()
            session["user_id"] = u[0]
            session["user_is_admin"] = True

            return redirect(url_for("admin.home_page"))
    return render_template('admin/admin_login.html', form=form, error=error)
