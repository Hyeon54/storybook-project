#기본 라우팅 설정
from flask import request, Blueprint, jsonify # request(요청)을 받기 위한 Flask 함수
import os

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
    
    # GPT에게 전달할 프롬프트 메시지 구성 (Use 4 to 6 sentences total여기 추후 수정)
    prompt = f"""
    The keyword: "{keyword}" is written in Korean.  
Please translate the keyword into English first and write a short story for children (A1 English level).

The story should:
- Use simple present tense.
- Use very short and simple sentences (5 to 7 words).
- Avoid classic fairy tale phrases like "Once upon a time".
- Be clear and complete with a beginning, middle, and end.
- Be fun and easy to understand for young learners.
- Include a short and creative title.
- Use 4 to 6 sentences total, around 20 to 80 words.

Do not explain or label the translation.  
Just return the story in the following format:

Title: [story title]

[Sentence 1]  
[Sentence 2]  
[Sentence 3]  
[Sentence 4]  
[...]
    """

    try:
        # OpenAI GPT API 호출 (ChatGPT 방식)
        #model="gpt-4-turbo",  # 이렇게 바꾸면 GPT-4-turbo 사용
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # 사용할 모델 (openai==0.28은 OpenAI 라이브러리의 버전이고, "gpt-3.5-turbo"는 우리가 호출할 GPT 모델의 이름)
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
# DALL·E 연동 (/generate/image)
@main.route("/generate/image", methods=["POST"])
def generate_image():
    from flask import request
    import openai
    from config import OPENAI_API_KEY

    openai.api_key = OPENAI_API_KEY

    data = request.get_json(silent=True)
    print("[DEBUG] 받은 JSON 데이터:", data)

    if not data:
        return {"error": "No JSON received"}, 400

    prompt = data.get("prompt")
    if not prompt:
        return {"error": "Prompt is required"}, 400

    try:
        response = openai.Image.create(
            model="dall-e-2",  # 또는 "dall-e-3"
            prompt=prompt,
            size="512x512",  # 또는 "1024x1024"
            n=1
        )
        image_url = response["data"][0]["url"]
        return {"image_url": image_url}

    except Exception as e:
        return {"error": str(e)}, 500
