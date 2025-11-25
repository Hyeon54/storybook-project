# Flask 앱의 내부 설정을 정의해두는 모듈 역할
#Flask 앱 초기화
# app/__init__.py
# cd backend
# venv/Scripts/activate
# python run.py

from flask import Flask
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from .models import db  # 반드시 models.py의 db를 import 해야 함
from .routes import main

def create_app():
    app = Flask(
        __name__,
        static_folder="../static",
        static_url_path="/static"
    )
    
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)  # 

    CORS(app)
    app.register_blueprint(main)

    return app
# from flask import Flask
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
# from .routes import main
# from .models import db
# import os

# # SQLAlchemy 객체 생성
# db = SQLAlchemy()

# def create_app():
#     app = Flask(
#         __name__,
#         static_folder="../static",       # ← backend/static 기준으로 맞추기
#         static_url_path="/static"
#     )
#     print("[DEBUG] 실제 static 폴더:", app.static_folder)
#     print("[DEBUG] static URL 경로:", app.static_url_path)

#     from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
#     app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

#     # SQLAlchemy 연동
#     db.init_app(app)  # SQLAlchemy 초기화
    
#     # CORS 및 블루프린트 등록
#     CORS(app)
#     app.register_blueprint(main)

#     return app

