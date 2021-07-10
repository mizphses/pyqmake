from flask import Flask, json, jsonify, request, abort
from flask_jwt import JWT, jwt_required, current_identity
import psycopg2
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
from os.path import join, dirname
app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Connect to PostgreSQL
def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)
conn = get_connection()
cur = conn.cursor()

users = []
# Auth
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

@app.route("/test")
def test():
    cur.execute('SELECT id, username, useremail, password_digest FROM users;')
    results = cur.fetchall()
    usernames = [u[1] for u in results]
    userids = [u[0] for u in results]
    return jsonify({"asa": str(usernames)})

if __name__ == "__main__":
    app.run(debug=True, port=8888)

# username_table = {u.username: u for u in users}
