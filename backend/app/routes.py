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
    import requests
    import re
    from flask import request, jsonify
    from google.cloud import texttospeech
    from config import OPENAI_API_KEY, GOOGLE_TTS_API_KEY

    openai.api_key = OPENAI_API_KEY
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TTS_API_KEY

    data = request.get_json()
    keyword = data.get("keyword", "").strip()

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
        # GPT로부터 받은 이야기 텍스트
        story = gpt_response['choices'][0]['message']['content']
        story_lines = story.strip().split('\n')
        title_line = story_lines[0]
        story_title = title_line.replace("Title:", "").strip()

        # 고유한 파일 ID 생성 (공백 제거 + 소문자)
        # 안전한 파일 ID 만들기 (소문자, 알파벳+숫자만)
        story_id = re.sub(r"[^a-zA-Z0-9]", "", story_title.lower())

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
        image_path = f"static/{story_id}.png"
        img_data = requests.get(image_url).content
        with open(image_path, "wb") as f:
            f.write(img_data)

        # 3. 음성 생성 (Google TTS)
        tts_client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=story)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-O",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        audio_response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # 음성 저장
        audio_path = f"static/{story_id}.mp3"
        with open(audio_path, "wb") as out:
            out.write(audio_response.audio_content)

        # 텍스트 저장
        text_path = f"static/{story_id}.txt"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(story)

        # 응답 반환
        return jsonify({
            "id": story_id,
            "title": story_title,
            "story": story,
            "image_url": f"/static/{story_id}.png",
            "audio_url": f"/static/{story_id}.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

####################################################
# get-latest 라우터 구현
@main.route("/get-latest", methods=["GET"])
def get_latest_story():
    import os
    from flask import jsonify

    # 1. story, image, audio 파일 경로 지정
    story_path = "static/story.txt"
    image_url = "/static/image_output.png"
    audio_url = "/static/audio_output.mp3"

    # 2. story 텍스트 읽기 (없을 경우 기본값 반환)
    if os.path.exists(story_path):
        with open(story_path, "r", encoding="utf-8") as f:
            story = f.read()
    else:
        story = "Title: No story available\nPlease generate a story first."

    # 3. 응답 JSON 구성
    return jsonify({
        "story": story,
        "image_url": image_url,
        "audio_url": audio_url
    })

###########################################################
# /stories API 만들기 : API역할 - static폴더 내에 저장된 동화 데이터목록(이미지 + 제목) 반환 역할
@main.route("/stories", methods=["GET"])
def get_stories():
    import os

    static_dir = "static"
    story_files = []
    for filename in os.listdir(static_dir):
        if filename.endswith(".txt"):
            base = filename.replace(".txt", "")
            txt_path = os.path.join(static_dir, filename)
            img_path = f"/static/{base}.png"

            # 제목 추출 (첫 줄에 "Title: ~~~" 형식)
            with open(txt_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.lower().startswith("title:"):
                    title = first_line.replace("Title:", "").strip()
                else:
                    title = base

            story_files.append({
                "id": base,
                "title": title,
                "cover_url": img_path  # 이미지 경로
            })

    return jsonify({"stories": story_files})
#########################################################
# /stories/<id> API 설계
@main.route("/stories/<story_id>", methods=["GET"])
def get_story_by_id(story_id):
    import os
    from flask import jsonify

    # 1. 경로 구성
    base_dir = os.path.join(os.path.dirname(__file__), "..")  # routes.py 기준 상위 폴더
    static_path = os.path.join(base_dir, "static")
    txt_path = os.path.join(static_path, f"{story_id}.txt")
    img_path = os.path.join(static_path, f"{story_id}.png")
    audio_path = os.path.join(static_path, f"{story_id}.mp3")

    # 2. 디버그 로그 출력
    print(f"[DEBUG] 요청된 story_id: {story_id}")
    print(f"[DEBUG] TXT 경로: {txt_path} | 존재함? {os.path.exists(txt_path)}")
    print(f"[DEBUG] IMG 경로: {img_path} | 존재함? {os.path.exists(img_path)}")
    print(f"[DEBUG] MP3 경로: {audio_path} | 존재함? {os.path.exists(audio_path)}")

    # 3. 텍스트 파일 확인
    if not os.path.exists(txt_path):
        return jsonify({"error": "Story not found"}), 404

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            story = f.read()

        # 4. 제목 추출 (첫 줄이 "Title: ..." 형식이라고 가정)
        lines = story.strip().split("\n")
        title_line = lines[0] if lines else ""
        title = title_line.replace("Title: ", "").strip()

        # 5. 클라이언트에 반환
        return jsonify({
            "id": story_id,
            "title": title,
            "story": story,
            "image_url": f"/static/{story_id}.png",
            "audio_url": f"/static/{story_id}.mp3"
        })

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({"error": "Failed to read story"}), 500