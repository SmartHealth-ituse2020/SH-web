from flask import render_template, session, redirect, url_for, flash
from decouple import config
import functools

DATABASE_URL = config('DATABASE_URL')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash("Please login first.")
            return redirect(url_for("login_page"))
        return view(**kwargs)
    return wrapped_view


def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' in session:
            if 'user_is_admin' in session and session['user_is_admin']:
                return redirect(url_for("admin.home_page"))
            else:
                return redirect(url_for("doctor.home_page"))
        return view(**kwargs)
    return wrapped_view


@logout_required
def login_page():
    return render_template("login.html")


@login_required
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("login_page"))
