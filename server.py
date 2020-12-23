from flask import Flask

import psycopg2 as dbapi2
        
import views, doctor_views, dboperations

app=Flask(__name__)
app.config["DEBUG"] = True
    
app.add_url_rule("/doctor", methods=["GET", "POST"], view_func=views.home_page_doctor)
app.add_url_rule("/", view_func=views.login_page)
app.add_url_rule("/login", view_func=views.login_page)

if __name__ == "__main__":
    app.run()
