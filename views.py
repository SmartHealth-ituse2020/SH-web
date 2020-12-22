from datetime import datetime
from flask import render_template
from flask import request, redirect, url_for

import os

import psycopg2 as dbapi2

# DATABASE_URL = os.environ['DATABASE_URL']

# def query(url, table_name):
#     with dbapi2.connect(url) as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM %s" % (table_name))
#         rows = cursor.fetchall()
        
#         cursor.close()
#         return rows

def home_page_doctor():
    today = datetime.today()
    day_name = today.strftime("%A")

    return render_template("home_doctor.html", day=day_name)

def login_page():
     return render_template("login.html")