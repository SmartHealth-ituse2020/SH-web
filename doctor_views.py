from flask import render_template
from flask import request, redirect, url_for

import os

import psycopg2 as dbapi2

import dboperations

# DATABASE_URL = os.environ['DATABASE_URL']

def login_page_doctor():
     return render_template("login_doctor.html")

def home_page_doctor():
    # rows = query(DATABASE_URL, "")
    rows={"...", "...", "...", "...", "...", "..."}
    return render_template("home_doctor.html", rows=sorted(rows), len=len(rows))