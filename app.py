from flask import Flask, jsonify, request, abort
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



# API
@app.route("/setup")
def setup():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username varchar UNIQUE, useremail varchar UNIQUE, password_digest varchar);")
    return jsonify({"Message":"Your setup was successfully finished"})

@app.route("/")
def root():
    return jsonify({"status":"403 Forbidden", "message":"プレイエリアの外です。"}), 403

@app.route("/register_user", methods=["post"])
def post():
    username = request.json['username']
    useremail = request.json['useremail']
    password = request.json['userpw']
    password_hash = generate_password_hash(password, method='sha256')
    with conn.cursor() as cur:
        cur.execute('INSERT INTO users (username, useremail, password_digest) VALUES (%s, %s, %s)', (username, useremail, password_hash))
    conn.commit()
    return jsonify({"message":"200 OK"}), 200

@app.route("/userlist")
def userlist():
    cur.execute('SELECT id, username, useremail FROM users;')
    results = cur.fetchall()
    return jsonify({"User":results})

@app.errorhandler(404)
def page_not_found(error):
    return jsonify(
        {
            "Status": "Error",
            "Code": "404",
            "Message": "Page or endpoint not found"
        }
    ), 404

@app.route("/418")
def index():
    return jsonify(
        {
            "Status": "Error",
            "Code": 418,
            "Message": "The requested entity body is short and stout. Tip me over and pour me out."
        }), 418

@app.route("/500")
def hello():
    abort(500, 'hello abort')

# Error Hundler

@app.errorhandler(500)
def error_500(e):
    return jsonify({'message': 'internal server error'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=8888)