from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import hashlib

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

@app.route('/login.html', methods=['POST'])
def login():
    if request.method == 'POST':
        # 폼 데이터 추출
        username = request.form['username']
        password = request.form['password']

        # 사용자 정보 조회
        user = collection.find_one({'username': username})

        if user:
            # 저장된 비밀번호와 입력된 비밀번호 해시를 비교
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashed_password == user['password']:
                # 로그인 성공 시 세션에 사용자 정보 저장
                session['username'] = username
                return redirect('/index.html')
        
        # 로그인 실패 시 메시지를 출력하거나 로그인 페이지로 리다이렉트
        return "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.", 401
    # 로그인 페이지 렌더링
    return render_template('login.html')

@app.route('/logout')
def logout():
    # 세션에서 사용자 정보 제거 (로그아웃)
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
