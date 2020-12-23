from datetime import datetime
from flask import render_template
from flask import request, redirect, url_for

import os

import psycopg2 as dbapi2

import dboperations

# DATABASE_URL = os.environ['DATABASE_URL']

def login_page():
     return render_template("login.html")