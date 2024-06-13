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

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')


def mydefault():
    global i
    i += 1
    return i


db = SQLAlchemy(app)

class Reviews(db.Model):
    rev_id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    sightid = db.Column(db.String(100), nullable=False)
    sightname = db.Column(db.String(100), nullable=False)
    rev_content = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.sightname} {self.rev_content} 리뷰 by {self.username}'



with app.app_context():
    db.create_all()

from flask import Flask, render_template, request, jsonify
import requests
import xmltodict
import json

app = Flask(__name__)

@app.route("/get_sight_information/")
def get_sight_information():
    # URL 설정
    url = "https://apis.data.go.kr/B551011/KorService1/detailCommon1?serviceKey=Al3bMZYLF3tteWZUOulq%2FmqbqH09Whq3LSN7qXANeAop5MeLY6OMNFzt9xy4pbpDM9cvW4j6lxWxN8HDvhmSjg%3D%3D&contentId=126508&addrinfoYN=Y&MobileOS=ETC&MobileApp=AppTest&_type=json"
    resp = requests.get(url)
    contents = resp.text
    print(contents)
    data = json.loads(contents)
    title = data['response']['body']['items']['item'][0]['contentid']
    print(title)

    
    context = {
        "title": title
    }
    return render_template('sightlist.html', data=context)

if __name__ == "__main__":
    app.run(debug=True)



@app.route("/review/")
def review_page():
    reviews = Reviews.query.all()
    return render_template('review.html', data=reviews)


@app.route("/review/<sightid>/")
def render_review_filter(sightid):
    filter_list = Reviews.query.filter_by(sightid=sightid).all()
    return render_template('review.html', data=filter_list)


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





if __name__ == "__main__":
    app.run(debug=True)