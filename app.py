import os
from os.path import dirname, join

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request
from flask_jwt import JWT, current_identity, jwt_required

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
jwt = JWT(app, authenticate, identity)

# root, プレイエリア外
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
        cur.execute('INSERT INTO users (username, useremail, password_digest, namae) VALUES (%s, %s, %s, %s)', (username, useremail, password_hash, namae))
    conn.commit()
    return jsonify({"message":"200 OK"}), 200

# # ユーザ更新
@app.route("/alter_user", methods=["put"])
def alter_user():
    username = request.json['username']
    useremail = request.json['useremail']
    password = request.json['userpw']
    namae = request.json['namae']
    password_hash = generate_password_hash(password, method='sha256')
    with conn.cursor() as cur:
        cur.execute('UPDATE users SET username=%s, useremail=%s, password_digest=%s, namae=%s WHERE username = %s', (username, useremail, password_hash, namae, username))
    conn.commit()
    return jsonify({"message":"200 OK"}), 200




# # エラーハンドリング
@app.route("/500")
def hello():
    abort(500, 'hello abort')

@app.route("/418")
def index():
    return jsonify(
        {
            "Status": "Error",
            "Code": 418,
            "Message": "The requested entity body is short and stout. Tip me over and pour me out."
        }), 418

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
