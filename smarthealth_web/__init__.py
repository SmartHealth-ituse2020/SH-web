from smarthealth_web import views, doctor, patient, admin
from decouple import config
from flask import Flask


def create_app(test_config=False, test_db=None):
    # create and configure the app
    app = Flask(__name__)
    # SECRET_KEY = os.urandom(32)  # assign a random secret key for CSRF Token
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'dev'
    app.config['CSRF_ENABLED'] = True
    app.config['DATABASE'] = config('DATABASE_URL')

    if test_config:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DATABASE'] = test_db
        if test_db is None:
            raise Exception("Test database url must be given.")

    # register doctor blueprint
    app.register_blueprint(doctor.bp)
    app.register_blueprint(patient.bp)
    app.register_blueprint(admin.bp)

    app.add_url_rule("/", view_func=views.login_page)
    app.add_url_rule("/login", view_func=views.login_page)

    return app
