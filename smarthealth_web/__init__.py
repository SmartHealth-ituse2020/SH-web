from flask import Flask
import os
from smarthealth_web import doctor_views, views


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # SECRET_KEY = os.urandom(32)  # assign a random secret key for CSRF Token
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'dev'

    app.add_url_rule("/doctor", methods=["GET", "POST"], view_func=doctor_views.home_page)
    app.add_url_rule("/", view_func=views.login_page)
    app.add_url_rule("/login", view_func=views.login_page)
    app.add_url_rule("/login/doctor", methods=["GET", "POST"], view_func=doctor_views.login)
    app.add_url_rule("/doctor/add_patient", methods=["GET", "POST"], view_func=doctor_views.add_patient)

    return app
