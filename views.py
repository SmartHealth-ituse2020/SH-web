# from datetime import datetime
# import psycopg2 as dbapi2
# from flask import request, redirect, url_for
# import dboperations
from flask import render_template
import os

DATABASE_URL = os.environ['DATABASE_URL']


def login_page():
    return render_template("login.html")
