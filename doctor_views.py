from flask import render_template
from flask import request, redirect, url_for

import os

import psycopg2 as dbapi2

import dboperations

# DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL = "postgres://fvtkacqijrpxfk:9af8c01dc052361fd51630b634e9a1df34106a7eae0ac736c6a36099bb476d87@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/d4qj8s0lt8sev8"

def login_page_doctor():
     return render_template("login_doctor.html")

def home_page_doctor():
    rows = dboperations.query(DATABASE_URL, "patient")
#     rows={"...", "...", "...", "...", "...", "..."}
    return render_template("home_doctor.html", rows=sorted(rows), len=len(rows))