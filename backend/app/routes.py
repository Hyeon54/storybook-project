#기본 라우팅 설정
from flask import request, Blueprint, jsonify # request(요청)을 받기 위한 Flask 함수
import os
import openai #OpeinAI GPT API사용을 위한 
import requests
from config import OPENAI_API_KEY, GOOGLE_TTS_API_KEY # config.py에서 환경변수(OPENAI_API_KEY키를 불러옴옴)

import json ##
from google.cloud import texttospeech ##

openai.api_key = OPENAI_API_KEY # OpenAI 라이브러리에 API 키 등록

main = Blueprint("main", __name__)

# (test용)
@main.route("/") 
def index():
    return jsonify({"message": "Hello from Flask!"})

# 키 잘 받아지는지 (test용)
@main.route("/apikey")
def get_api_key():
    return jsonify({"api_key": os.getenv("OPENAI_API_KEY")})

###############################################################
# GPT API를 호출하는 Flask 라우터 (test용)
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
# DALL·E 연동 (/generate/image) (test용)
@main.route("/generate/image", methods=["POST"])
def generate_image():

    # 1. API 키 등록
    openai.api_key = OPENAI_API_KEY

    # 2. JSON 데이터 받아오기
    data = request.get_json()
    print("[DEBUG] 받은 JSON 데이터:", data)

    if not data:
        return {"error": "No JSON received"}, 400

    prompt = data.get("prompt", "")

    if not prompt:
        return {"error": "Prompt is required."}, 400

    try:
        # 3. DALL·E API (이미지 생성용) 호출
        response = openai.Image.create(
            prompt=prompt,               # 생성할 이미지 설명
            model="dall-e-3",            # 사용할 모델 (DALL·E 3)
            size="1024x1024",            # 이미지 크기 (기본 1024x1024만 지원)
            quality="standard",          # standard or hd (hd는 요금 더 높음)
            n=1                          # 이미지 개수 (한번에 1장만 생성가능함함)
        )

        # 4. 응답에서 이미지 URL 추출
        image_url = response["data"][0]["url"]

        # 5. 클라이언트에 반환
        return {"image_url": image_url}

    except Exception as e:
        return {"error": str(e)}, 500
############################################################
# Google Text-to-Speech(TTS)연동 (test용)
# http://127.0.0.1:5000/static/audio_output.mp3
@main.route("/generate/audio", methods=["POST"])
def generate_audio():
    
    # 1. 환경변수로 서비스 계정 키 등록
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_API_KEY

    # 2. 요청 데이터 받기
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is required."}), 400

    try:
        # 3. 클라이언트 생성
        client = texttospeech.TextToSpeechClient()

        # 4. 요청 구성
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Studio-O", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=0.5
        ) #  speaking_rate=1.0이 기본, 더 느리게

        # 5. 음성 생성
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # 6. 저장할 경로 설정
        output_path = "static/audio_output.mp3"
        os.makedirs("static", exist_ok=True)

        with open(output_path, "wb") as out:
            out.write(response.audio_content)

        # 7. 프론트엔드에서 접근할 수 있도록 URL 반환
        return jsonify({"audio_url": f"/static/audio_output.mp3"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

####################################################
# /generate 하나의 POST 요청으로 요청 (실제용)
@main.route("/generate", methods=["POST"])
def generate_all():
    import openai
    import os
    from flask import request, jsonify
    from google.cloud import texttospeech
    from config import OPENAI_API_KEY, GOOGLE_TTS_API_KEY

    openai.api_key = OPENAI_API_KEY
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_API_KEY

    data = request.get_json()
    keyword = data.get("keyword", "")

    if not keyword:
        return jsonify({"error": "Keyword is required."}), 400

    try:
        # 1. GPT 이야기 생성
        prompt = f"""
        The keyword: "{keyword}" is written in Korean.  
        Please translate the keyword into English first, and write a story based on the translated word.
        Use A1 level English and write a short story for children.

        The story should:
        - Use simple present tense.
        - Use very short and simple sentences (5 to 7 words).
        - Avoid classic fairy tale phrases like "Once upon a time".
        - Be clear and complete with a beginning, middle, and end.
        - Be fun and easy to understand for young learners.
        - The story should have a short and creative title.
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
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a creative story writer for children."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        story = gpt_response['choices'][0]['message']['content']

        # 2. 이미지 생성 (DALL·E 3 via GPT-4 Turbo)
        image_response = openai.Image.create(
            prompt=f"An illustration of: {story}",
            model="dall-e-3",
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = image_response["data"][0]["url"]

        # 이미지 다운로드
        img_data = requests.get(image_url).content
        with open("static/image_output.png", "wb") as f:
            f.write(img_data)

        # 3. 음성 생성 (Google TTS)
        tts_client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=story)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-O",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=0.5)
        audio_response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open("static/audio_output.mp3", "wb") as out:
            out.write(audio_response.audio_content)

        return jsonify({
            "story": story,
            "image_url": "/static/image_output.png",
            "audio_url": "/static/audio_output.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
