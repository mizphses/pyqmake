from datetime import datetime
import os
from os.path import dirname, join

from dotenv import load_dotenv
import random
import math
import base64
from flask import Flask, abort, jsonify, request, render_template
from flask_jwt import JWT, current_identity, jwt_required
import re
from werkzeug.security import generate_password_hash
import datetime
from flask_weasyprint import HTML, render_pdf

# Modules
from auth import *
from connection import *

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Auth
class User(object):
    def __init__(self, id, username, password, namae):
        self.id = id
        self.username = username
        self.password = password
        self.namae = namae

    def __str__(self):
        return ["%s","%s","%s"] % (self.id, self.username, self.namae)
jwt = JWT(app, authenticate, identity)

# 問題ファイルの取得
def getQuestionText(id):
    cur.execute('SELECT subject, description, heading, quiz, answershet FROM questions WHERE id = %s;', (str(id)))
    return cur.fetchone()


# root, テストなど
@app.route("/test")
def testroute():
    print(user_fetch())
    return jsonify({"a":"hi"})

@app.route("/")
def root():
    return jsonify({"status":"403 Forbidden", "message":"メッセージはでないはずだよ"}), 403

# # ユーザ登録
@app.route("/register_user", methods=["post"])
def post_user():
    username = request.json['username']
    useremail = request.json['useremail']
    password = request.json['userpw']
    namae = request.json['namae']
    password_hash = generate_password_hash(password, method='sha256')
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username varchar UNIQUE, useremail varchar UNIQUE, password_digest varchar, namae varchar);")
        cur.execute("CREATE TABLE IF NOT EXISTS questions (id serial PRIMARY KEY, subject varchar, description varchar, heading varchar, quiz text, answershet text, created_by integer, renew_rules integer, created_at timestamp, changed_at timestamp);")
        cur.execute('INSERT INTO users (username, useremail, password_digest, namae) VALUES (%s, %s, %s, %s)', (username, useremail, password_hash, namae))
    conn.commit()
    return jsonify({"message":"200 OK"}), 200

# # ユーザ更新
@app.route("/alter_user", methods=["put"])
@jwt_required()
def alter_user():
    username = request.json['username']
    useremail = request.json['useremail']
    password = request.json['userpw']
    namae = request.json['namae']
    password_hash = generate_password_hash(password, method='sha256')
    # 本人情報の取得
    with conn.cursor() as cur:
        cur.execute('SELECT id FROM users WHERE username = %s;', (username,))
        registeredid = cur.fetchall()
    # 本人情報の確認
    if str(current_identity[0]) == str(re.sub("\(|\,|\)", "", str(registeredid[0]))):
        with conn.cursor() as cur:
            cur.execute('UPDATE users SET username=%s, useremail=%s, password_digest=%s, namae=%s WHERE username = %s', (username, useremail, password_hash, namae, username))
        conn.commit()
        return jsonify({"message":"200 OK"}), 200
    else:
        return jsonify(
            {
                "message": "Forbidden"
            }), 403

@app.route("/new_quiz", methods=["post"])
@jwt_required()
def new_quiz():
    subject = request.json['subject']
    description = request.json['description']
    heading = request.json['heading']
    quiz = request.json['quiz']
    answer_sheet = request.json['answer_sheet']
    created_by = request.json['created_by']
    renew_rules = request.json['renew_rules']
    created_at = datetime.datetime.now()
    changed_at = datetime.datetime.now()
    with conn.cursor() as cur:
        cur.execute('INSERT INTO questions (subject, description, heading, quiz, answershet, created_by, renew_rules, created_at, changed_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (subject, description, heading, quiz, answer_sheet, int(created_by), int(renew_rules), created_at, changed_at))
    conn.commit()
    return jsonify({"message":"200 OK"}), 200

@app.route("/renderq", methods=["post"])
@jwt_required()
def renderquiz():
    qnom = request.json['qnom']
    type = request.json['type']
    examtitle = request.json['examtitle']
    heading = request.json['heading']
    try:
        request.json['caution']
        caution = request.json['caution']
    except NameError:
        caution = "inherit"
    quizs = []
    for q in qnom:
        quizs.append(getQuestionText(q))
    html = render_template('index.html', download=True, save=False , questions = qnom, hani = range(len(qnom)), quizs=quizs, random=math.floor(random.random()*20000000), type=type, caution=caution, examtitle = examtitle, heading = heading)
    return render_pdf(HTML(string=html))

# # エラーハンドリング
@app.route("/500")
def hello():
    abort(500, 'hello abort')

@app.route("/418")
def index():
    return jsonify(
        {"Message": "I'm a teapot"}), 418

@app.errorhandler(500)
def error_500(e):
    return jsonify({'message': 'internal server error'}), 500

@app.errorhandler(404)
def error_404(e):
    return jsonify({'message': 'Page not found'}), 500

# # Security Area

# テスト用
@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == "__main__":
    if os.environ.get('IS_DEBUG') == "True":
        app.run(debug=True, port=8888)
    else:
        app.run(debug=False, port=8888)
