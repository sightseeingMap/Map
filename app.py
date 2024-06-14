from flask import Flask, render_template, request,  redirect, url_for
import requests, xmltodict, json, jsonify 
import os
import re   
from flask_sqlalchemy import SQLAlchemy
from flask import session
import hashlib
from PyKakao import Local




basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.secret_key = 'SPARTA'
def mydefault():
    global i
    i += 1
    return i


db = SQLAlchemy(app)

class Reviews(db.Model):
    rev_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    sightname = db.Column(db.String(100), nullable=False)
    rev_content = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.sightname} {self.rev_content} 리뷰 by {self.username}'



@app.route('/login/')
def index():
    # 로그인 페이지 렌더링
    return render_template('login.html')
    
@app.route('/join/')
def join():
    # 회원가입 페이지 렌더링
    return render_template('join2.html')

@app.route('/')
def map():
    # 메인 페이지 렌더링
    Local.
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


app = Flask(__name__)
@app.route("/sightlist/")
def sightlist():
    with open("sightdata.json", "r", encoding='UTF8') as sightdata:
        data = json.load(sightdata)
    keyword = request.args.get('keyword')
    
    # 데이터를 필터링하지 않고 모든 데이터를 사용
    sight_information = [{"name": item["관광지명"], "address": item["소재지도로명주소"], "information" : item["관광지소개"]} for item in data["records"]]
    
    return render_template('sightlist.html', data=sight_information)

@app.route("/sightlist_keyword/")
def sightlist_keyword(): 
    with open("sightdata.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    keyword = request.args.get('keyword')
    print(keyword)
    # 키워드를 기반으로 데이터 필터링
    filtered_data = []
    for item in data["records"]:
        if re.search(keyword, item["소재지도로명주소"]):
            filtered_data.append({
                "name": item["관광지명"], 
                "address": item["소재지도로명주소"], 
                "information": item["관광지소개"]
            })
    print(filtered_data)
    # 필터링된 데이터를 sightlist.html에 전달하여 렌더링
   # 필터링된 데이터를 HTML 형식으로 반환
    html_table = "<table>"
    html_table += "<tbody>"
    for item in filtered_data:
        html_table += f"<tr><td>{item['name']}</td><td>{item['address']}</td><td>{item['information']}</td><td><a href='#'>리뷰</a></td></tr>"
    html_table += "</tbody></table>"
    return html_table

        # 회원가입이 성공했다면 홈페이지로 리다이렉트합니다.
        return redirect('/login/')
    
    # GET 요청일 경우 회원가입 페이지 렌더링
    return render_template('join2.html')

@app.route('/login.html', methods=['POST'])
def login():
    if request.method == 'POST':
        # 폼 데이터 추출
        username = request.form['username']
        password = request.form['password']

        
        # 로그인 실패 시 메시지를 출력하거나 로그인 페이지로 리다이렉트
        return "로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.", 401
    # 로그인 페이지 렌더링
    return render_template('login.html')
@app.route("/review/<name>/")
def render_review_filter(name):
    filter_list = Reviews.query.filter_by(name=name).all()
    return render_template('review.html', data=filter_list)

@app.route('/logout')
def logout():
    # 세션에서 사용자 정보 제거 (로그아웃)
    session.pop('username', None)
    return redirect('/')

@app.route("/review/create/")
def review_create():
    # 폼에서 전달된 데이터 처리
    sightname_receive = request.args.get("sightname")
    userid_receive = request.args.get("userid")
    username_receive = request.args.get("username")
    sightid_receive = request.args.get("sightid")
    rev_content_receive = request.args.get("rev_content")

    # 데이터베이스에 데이터 추가
    reviewdb = Reviews(sightname=sightname_receive, userid=userid_receive, username=username_receive, sightid=sightid_receive, rev_content=rev_content_receive)
    db.session.add(reviewdb)
    db.session.commit()

    # 리뷰 페이지로 리다이렉트
    return redirect(url_for('render_review_filter', sightname=sightname_receive))




if __name__ == '__main__':
    app.run(debug=True)