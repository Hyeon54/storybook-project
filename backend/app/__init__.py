# Flask 앱의 내부 설정을 정의해두는 모듈 역할
#Flask 앱 초기화
from flask import Flask
from flask_cors import CORS
from .routes import main

def create_app():
    app = Flask(__name__)
    CORS(app)  # CORS 허용

    app.register_blueprint(main)  # 라우터 등록

    return app