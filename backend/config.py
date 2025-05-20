#환경 변수 불러오기
# config.py
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# API 키 관리
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DALLE_API_KEY = os.getenv('DALLE_API_KEY')
GOOGLE_TTS_API_KEY = os.getenv('GOOGLE_TTS_API_KEY')

# SQLAlchemy 설정
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "yourpassword")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DB", "storybook")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False