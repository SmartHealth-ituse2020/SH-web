from datetime import datetime
from flask import render_template
from flask import request, redirect, url_for

import os

import psycopg2 as dbapi2

import dboperations

# DATABASE_URL = os.environ['DATABASE_URL']

def home_page_doctor():
    today = datetime.today()
    day_name = today.strftime("%A")

    # rows = query(DATABASE_URL, "")
    # return render_template("home_doctor.html", rows=sorted(rows), len=len(rows))
    return render_template("home_doctor.html", day=day_name)