from flask import Flask, jsonify, request
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

# Auth



# API
@app.route("/")
def root():
    return jsonify({"status":"403 Forbidden", "message":"プレイエリアの外です。"}), 403

@app.route("/register_user", methods=["post"])
def post():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username varchar UNIQUE, useremail varchar UNIQUE, password_digest varchar);")
    username = request.json['username']
    useremail = request.json['useremail']
    password = request.json['userpw']
    password_hash = generate_password_hash(password, method='sha256')
    with conn.cursor() as cur:
        cur.execute('INSERT INTO users (username, useremail, password_digest) VALUES (%s, %s, %s)', (username, useremail, password_hash))
    conn.commit()
    return jsonify({"message":"200 OK"}), 200



@app.route("/users")
def users():
    cur.execute('SELECT username, useremail FROM users;')
    results = cur.fetchall()
    return jsonify({"Answer":results})
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

if __name__ == "__main__":
    app.run(debug=True, port=8888)