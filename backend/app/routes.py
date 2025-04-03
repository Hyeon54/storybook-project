#기본 라우팅 설정
from flask import Blueprint, jsonify
import os

from flask import request # request(요청)을 받기 위한 Flask 함수
import openai #OpeinAI GPT API사용을 위한 라이브러리
from config import OPENAI_API_KEY # config.py에서 환경변수(OPENAI_API_KEY키를 불러옴옴)


openai.api_key = OPENAI_API_KEY # OpenAI 라이브러리에 API 키 등록

main = Blueprint("main", __name__)

# 테스트용용
@main.route("/") 
def index():
    return jsonify({"message": "Hello from Flask!"})

# 키 잘 받아지는지 테스트용용
@main.route("/apikey")
def get_api_key():
    return jsonify({"api_key": os.getenv("OPENAI_API_KEY")})

###############################################################
# GPT API를 호출하는 Flask 라우터
@main.route("/generate/text", methods=["POST"])
def generate_text():
    # 프론트에서 받은 JSON 데이터 중 'keyword' 추출
    data = request.get_json()
    keyword = data.get("keyword")

    # 키워드가 없으면, 에러 응답 반환하기
    if not keyword:
        return {"error": "Keyword is required."}, 400
    
    # GPT에게 전달할 프롬프트 메시지 구성
    prompt = f"""
    The keyword : "{keyword}" is written in Korean.  
Please translate the keyword into English first, and then write a story based on the translated word.
Use A1 level English with short and simple sentences (5 to 7 words), in present tense.  
The story should have a title .
The story should have be around 20 to 80 words.
The story should have 4 to 6 short sentences.
    """

    try:
        # OpenAI GPT API 호출 (ChatGPT 방식)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 사용할 모델 (openai==0.28은 OpenAI 라이브러리의 버전이고, "gpt-3.5-turbo"는 우리가 호출할 GPT 모델의 이름)
            messages=[
                {"role": "system", "content": "You are a creative story writer for children."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8  # 창의성 조절 수치 (높을수록 더 창의적)
        )

        # 응답에서 텍스트 추출
        story = response['choices'][0]['message']['content']

        # 생성된 이야기 텍스트를 JSON 형태로 반환
        return {"story": story}

    except Exception as e:
        # 에러 발생 시 메시지 반환
        return {"error": str(e)}, 500
    
    ############################################################
    
    
    
