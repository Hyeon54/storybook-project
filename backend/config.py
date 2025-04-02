#환경 변수 불러오기
import os
from dotenv import load_dotenv

# load_dotenv()  # .env 파일 불러오기
# 정확한 경로를 직접 지정
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# API Key 관리
# OpenAI API 키
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DALLE_API_KEY = os.getenv('DALLE_API_KEY')
# GOOGLE_TTS_API_KEY = os.getenv('GOOGLE_TTS_API_KEY')

# MySQL 설정값 예시
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'db': os.getenv('MYSQL_DB'),
}

