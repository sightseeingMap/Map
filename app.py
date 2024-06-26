# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# DB 기본 코드
import os
import re   
from flask_sqlalchemy import SQLAlchemy
import requests, xmltodict , json 
from flask import jsonify 




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')


db = SQLAlchemy(app)


class Reviews(db.Model):
    rev_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    sightname = db.Column(db.String(100), nullable=False)
    rev_content = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.sightname} {self.rev_content} 리뷰 by {self.username}'



with app.app_context():
    db.create_all()

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
        html_table += f"<tr><td id=\"name\">{item['name']}</td><td id=\"address\" class=\"address\">{item['address']}</td><td id=\"information\">{item['information']}</td><td> <button type=\"button\" class=\"btn btn-light\" data-bs-toggle=\"modal\" data-bs-target=\"#exampleModal\">리뷰</button></td></tr>"
    html_table += "</tbody></table>"
    return html_table

@app.route("/review/")
def review_page():
    reviews = Reviews.query.all()
    return render_template('review.html', data=reviews)


@app.route("/review/<name>/")
def render_review_filter(name):
    filter_list = Reviews.query.filter_by(name=name).all()
    return render_template('review.html', data=filter_list)


@app.route("/review/create/", methods=["POST"])
def review_create():
    try:
        # 클라이언트로부터 JSON 형식의 데이터 가져오기
        data = request.json
        
        # JSON 데이터가 제대로 전달되었는지 확인
        if not data:
            return "JSON data is missing or malformed", 400

        # 데이터베이스에 데이터 추가
        reviewdb = Reviews(
            sightname=data["sightname"],
            userid=data["userid"],
            username=data["username"],
            rev_content=data["rev_content"]
        )
        db.session.add(reviewdb)
        db.session.commit()

        # 리뷰 페이지로 리다이렉트
        return redirect(url_for('render_review_filter', sightname=data["sightname"]))
    except Exception as e:
        # 예외 발생 시 콘솔에 출력
        print("An error occurred:", e)
        # 클라이언트에게 내부 서버 오류 메시지 반환
        return "Internal Server Error", 500



if __name__ == '__main__':
    app.run(debug=True)