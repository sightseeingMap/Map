from flask import Flask, render_template, request,  redirect, url_for
from flask import requests, xmltodict, json, jsonify 
from flask import os
from flask import re   
from flask_sqlalchemy import SQLAlchemy
from flask import session
from pymongo import MongoClient
import hashlib



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.secret_key = 'SPARTA'

# MongoDB 설정
client = MongoClient('localhost', 27017)  #127.0.0.1
db = client.mydatabase
collection = db.users  # 사용자 정보를 저장할 컬렉션

@app.route('/')
def index():
    # 로그인 페이지 렌더링
    return render_template('login.html')
    
@app.route('/join2.html')
def join():
    # 회원가입 페이지 렌더링
    return render_template('join2.html')

@app.route('/index.html')
def map():
    # 메인 페이지 렌더링
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 폼 데이터 추출
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # 유효성 검사 수행 (예: 필드가 비어 있지 않은지 확인)
        if not username or not password or not email:
            return "모든 필드를 입력해야 합니다", 400

        # 비밀번호를 해시화하여 보안 강화
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # 사용자 정보를 MongoDB에 삽입
        user_data = {'username': username, 'password': hashed_password, 'email': email}
        collection.insert_one(user_data)   

        # 회원가입이 성공했다면 홈페이지로 리다이렉트합니다.
        return redirect('/')
    
    # GET 요청일 경우 회원가입 페이지 렌더링
    return render_template('join2.html')


if __name__ == '__main__':
    app.run(debug=True)