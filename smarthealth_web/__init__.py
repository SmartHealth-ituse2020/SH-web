from flask import Flask
import os
from smarthealth_web import views, doctor, patient, admin


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    # SECRET_KEY = os.urandom(32)  # assign a random secret key for CSRF Token
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'dev'

    # register doctor blueprint
    app.register_blueprint(doctor.bp)
    app.register_blueprint(patient.bp)
    app.register_blueprint(admin.bp)

    app.add_url_rule("/", view_func=views.login_page)
    app.add_url_rule("/login", view_func=views.login_page)

    return app
