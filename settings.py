# settings.py
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
import psycopg2 as dbapi2
from decouple import config
from werkzeug.security import generate_password_hash


load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

print("System variables loaded...")


def create_admin_user():
    uname = config('ADMIN_USERNAME')
    pword = config('ADMIN_PASSWORD')
    url = config('DATABASE_URL')
    print(f"Creating superuser with username {uname}...")

    with dbapi2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM admin WHERE username = %s", (uname, ))
            u = cur.fetchone()

            if u is not None:
                print("Already exists.")
                return

            cur.execute("INSERT INTO admin(name, surname, username, password) VALUES (%s, %s, %s, %s);",
                        ("admin", "admin", uname, generate_password_hash(pword))
                        )


create_admin_user()
