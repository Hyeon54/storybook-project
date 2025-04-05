# Flask 앱의 내부 설정을 정의해두는 모듈 역할
#Flask 앱 초기화
from flask import Flask
from flask_cors import CORS
from .routes import main
import os

def create_app():
    app = Flask(
        __name__,
        static_folder="../static",       # ← backend/static 기준으로 맞추기
        static_url_path="/static"
    )
    print("[DEBUG] 실제 static 폴더:", app.static_folder)
    print("[DEBUG] static URL 경로:", app.static_url_path)

    CORS(app)
    app.register_blueprint(main)
    return app


# def create_app():
#     base_dir = os.path.abspath(os.path.dirname(__file__))
#     static_dir = os.path.join(base_dir, 'static')

#     app = Flask(__name__, static_folder=static_dir)
#     CORS(app)

#     app.register_blueprint(main)

#     return app