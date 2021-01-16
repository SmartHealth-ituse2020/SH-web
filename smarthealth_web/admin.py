import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, url_for, session, flash
from smarthealth_web.forms import AdminLoginForm, AddDoctorForm
from flask import render_template, Blueprint
from decouple import config
from smarthealth_web.dboperations import (
    get_admin_by_username, get_doctor_by_username_or_national_id, add_doctor_to_database, query,
    get_admin_name_by_id, delete_doctor_with_id, query_where, deactivate_doctor
)


bp = Blueprint('admin', __name__, url_prefix='/admin')
DATABASE_URL = config('DATABASE_URL')


def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for("login_page"))
        elif "user_is_admin" not in session or not session["user_is_admin"]:
            flash("You are not an admin.")
            return redirect(url_for("doctor.home_page"))
        return view(**kwargs)
    return wrapped_view


@bp.route('/dashboard', methods=('GET',))
@admin_login_required
def home_page():
    rows = query_where("DOCTOR", "isActive != 'no'")
    admin_names = list()
    for r in range(len(rows)):
        admin_names.append(get_admin_name_by_id(rows[r][8]))
    return render_template("admin/admin_dashboard.html", rows=rows, len=len(rows), admin_names=admin_names)


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


@bp.route('/add_doctor', methods=('GET', 'POST'))
@admin_login_required
def add_doctor():
    form = AddDoctorForm()
    error = None
    if form.validate_on_submit():

        national_id = form.national_id.data
        name = form.name.data
        surname = form.surname.data
        password = form.password.data
        username = form.username.data
        hospital = form.hospital.data
        title = form.title.data
        profession = form.profession.data

        u = get_doctor_by_username_or_national_id(username, national_id)

        if u is not None:
            error = "Doctor is already registered."
        if error is None:
            add_doctor_to_database(
                name,
                surname,
                generate_password_hash(password),
                username,
                hospital,
                title,
                profession,
                session["user_id"],  # added by
                national_id
            )

            return redirect(url_for("admin.home_page"))
    return render_template('admin/add_doctor.html', form=form, error=error)


@bp.route('/deactivate_doctor/<doctor_id>', methods=('GET', 'POST'))
@admin_login_required
def remove_doctor(doctor_id):
    deactivate_doctor(doctor_id)
    return redirect(url_for("admin.home_page"))
