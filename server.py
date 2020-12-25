from flask import Flask
import os
import doctor_views
import views

SECRET_KEY = os.urandom(32)  # assign a random secret key for CSRF Token

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = SECRET_KEY

# DATABASE_URL = "postgres://fvtkacqijrpxfk:9af8c01dc052361fd51630b634e9a1df34106a7eae0ac736c6a36099bb476d87@ec2-54-\
# 246-115-40.eu-west-1.compute.amazonaws.com:5432/d4qj8s0lt8sev8"
# app.config['DATABASE_URL'] = DATABASE_URL

app.add_url_rule("/doctor", methods=["GET", "POST"], view_func=doctor_views.home_page_doctor)
app.add_url_rule("/", view_func=views.login_page)
app.add_url_rule("/login", view_func=views.login_page)
app.add_url_rule("/login/doctor", methods=["GET", "POST"], view_func=doctor_views.login_page_doctor)
app.add_url_rule("/doctor/add_patient", methods=["GET", "POST"], view_func=doctor_views.add_patient_page_doctor)

if __name__ == "__main__":
    app.run()
