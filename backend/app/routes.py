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
    Please translate this Korean word into English and use it as the topic: "{keyword}"

    Write a short story for young children (ages 3–6).  
    Then, randomly choose **one** of the following three story structures.  
    Make sure each structure has an **equal chance of being selected (1/3 probability each)**.  
    Avoid always choosing the same type.

    1. **Repetition Structure**  
    - Use a repetitive sentence pattern.  
    - You may choose patterns like “Wow, look at...”, “It is...”, “Here is...”, “I like...”, or others.  
    - Avoid using the same pattern every time.  
    - Keep the structure similar for the first 8 sentences.  
    - In the 9th sentence, add a fun twist or surprise.  

    2. **Question + Answer Structure**  
    - Use alternating questions and answers (e.g., “What is it?” / “It is a frog.”)  
    - Keep the main character or object consistent.  
    - Make the 9th sentence unexpected or humorous.  

    3. **Beginning-Middle-End (Story arc)**  
    - Use a simple plot with one character.  
    - Include a beginning (situation), middle (event), and end (happy or funny ending).  
    - Still use simple and short sentences (A1-level).  

    Character Guidelines:  
    - The main character can be a human, animal, or nature-inspired object.  
    - Do not use specific names like Tom or Anna.  
    - Use generic descriptions instead (e.g., a small rabbit, a playful sun, a boy).  
    - Alternatively, use “I” or “you” as the narrator.  

    Story Requirements:  
    - Be exactly **9 short sentences**.  
    - Use short sentences (6 to 12 words).  
    - Use only **simple present tense**.  
    - Avoid classic openings like 'Once upon a time'.  
    - Use **A1-level English**, very easy to understand.  
    - Be fun, imaginative, and happy.  
    - After the story, add a short description of the main character (1–2 sentences).  

    For each English sentence, also add its Korean translation.  
    Each Korean sentence must be translated into polite informal speech ("해요체").

    Do not explain your choice or translation.  
    Only return the story in the following format:

    Format:  
    Title: [story title]

    EN: [English sentence 1]  
    KO: [Korean sentence 1]  
    ...  
    EN: [English sentence 9]  
    KO: [Korean sentence 9]  

    Main Character Description:  
    [main character description here]
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
    import os, re, openai, requests
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
        # 1. GPT 프롬프트 구성
        prompt = f"""
    Please translate this Korean word into English and use it as the topic: "{keyword}"

    Write a short story for young children (ages 3–6).  
    Then, randomly choose **one** of the following three story structures.  
    Make sure each structure has an **equal chance of being selected (1/3 probability each)**.  
    Avoid always choosing the same type.

    1. **Repetition Structure**  
    - Use a repetitive sentence pattern.  
    - You may choose patterns like “Wow, look at...”, “It is...”, “Here is...”, “I like...”, or others.  
    - Avoid using the same pattern every time.  
    - Keep the structure similar for the first 8 sentences.  
    - In the 9th sentence, add a fun twist or surprise.  

    2. **Question + Answer Structure**  
    - Use alternating questions and answers (e.g., “What is it?” / “It is a frog.”)  
    - Keep the main character or object consistent.  
    - Make the 9th sentence unexpected or humorous.  

    3. **Beginning-Middle-End (Story arc)**  
    - Use a simple plot with one character.  
    - Include a beginning (situation), middle (event), and end (happy or funny ending).  
    - Still use simple and short sentences (A1-level).  

    Character Guidelines:  
    - The main character can be a human, animal, or nature-inspired object.  
    - Do not use specific names like Tom or Anna.  
    - Use generic descriptions instead (e.g., a small rabbit, a playful sun, a boy).  
    - Alternatively, use “I” or “you” as the narrator.  

    Story Requirements:  
    - Be exactly **9 short sentences**.  
    - Use short sentences (6 to 12 words).  
    - Use only **simple present tense**.  
    - Avoid classic openings like 'Once upon a time'.  
    - Use **A1-level English**, very easy to understand.  
    - Be fun, imaginative, and happy.  
    - After the story, add a short description of the main character (1–2 sentences).  

    For each English sentence, also add its Korean translation.  
    Each Korean sentence must be translated into polite informal speech ("해요체").

    Do not explain your choice or translation.  
    Only return the story in the following format:

    Format:  
    Title: [story title]

    EN: [English sentence 1]  
    KO: [Korean sentence 1]  
    ...  
    EN: [English sentence 9]  
    KO: [Korean sentence 9]  

    Main Character Description:  
    [main character description here]
    """

        # 2. GPT 호출
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a creative story writer for children."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )

        # 3. 응답 파싱
        story = response['choices'][0]['message']['content'].strip()
        lines = story.split("\n")
        title_line = lines[0].strip()
        story_title = title_line.replace("Title:", "").strip()

        english_lines = []
        korean_lines = []
        main_character_description = ""

        for idx, line in enumerate(lines[1:], 1):
            line = line.strip()
            if line.startswith("EN:"):
                english_lines.append(line.replace("EN:", "").strip())
            elif line.startswith("KO:"):
                korean_lines.append(line.replace("KO:", "").strip())
            elif line.startswith("Main Character Description:"):
                if idx + 1 < len(lines):
                    main_character_description = lines[idx + 1].strip()
                break

        if not main_character_description:
            main_character_description = "a cute character appropriate for a children's book"

        # 4. 파일 ID 생성
        story_id = re.sub(r"[^a-zA-Z0-9]", "", story_title.lower())

        image_urls = []
        audio_urls = []

        # 5. 스타일 고정 + 텍스트 제거 지시 추가
        style_keyword = "in digital watercolor style, children's book illustration"
        no_text_clause = "Do not include any text, letters, numbers, captions, or written words in the image."

        # 6. 페이지별 생성
        for i in range(10):
            if i == 0:
                text_for_page = story_title
                prompt_for_image = f"A children's book cover for: {story_title}, featuring {main_character_description}, {style_keyword}, {no_text_clause}"
            else:
                text_for_page = english_lines[i-1]
                prompt_for_image = f"Illustration of: {text_for_page}, featuring {main_character_description}, {style_keyword}, {no_text_clause}"

            # 이미지 생성
            img_response = openai.Image.create(
                prompt=prompt_for_image,
                model="dall-e-3",
                size="1024x1024",
                quality="standard",
                n=1
            )
            img_url = img_response["data"][0]["url"]
            img_path = f"static/{story_id}_{i}.png"
            with open(img_path, "wb") as f:
                f.write(requests.get(img_url).content)
            image_urls.append(f"/static/{story_id}_{i}.png")

            # 오디오 생성
            tts_client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text_for_page)
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
            audio_path = f"static/{story_id}_{i}.mp3"
            with open(audio_path, "wb") as out:
                out.write(audio_response.audio_content)
            audio_urls.append(f"/static/{story_id}_{i}.mp3")

        # 7. 전체 텍스트 저장
        with open(f"static/{story_id}.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {story_title}\n\n")
            for en, ko in zip(english_lines, korean_lines):
                f.write(f"EN: {en}\nKO: {ko}\n")

        # 8. 자동 저장 (DB)
        from app.models import Story, db
        story = Story(
            id=story_id,
            title=story_title,
            english_lines="\n".join(english_lines),
            korean_lines="\n".join(korean_lines),
            image_urls="\n".join(image_urls),
            audio_urls="\n".join(audio_urls),
            main_character_description=main_character_description
        )
        db.session.add(story)
        db.session.commit()

        # 9. 응답 반환
        return jsonify({
            "id": story_id,
            "title": story_title,
            "lines": english_lines,
            "korean_lines": korean_lines,
            "image_urls": image_urls,
            "audio_urls": audio_urls,
            "main_character_description": main_character_description
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
# /stories API 만들기 : # 리팩터링된 /stories API (DB 기반)
@main.route("/stories", methods=["GET"])
def get_stories():
    from app.models import Story

    try:
        # 숨김 처리된 동화 제외
        stories = Story.query.filter_by(is_hidden=False).all()

        result = []
        for s in stories:
            result.append({
                "id": s.id,
                "title": s.title,
                "cover_url": s.image_urls.split("\n")[0] #0번쩨 이미지지
            })
        return jsonify({"stories": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API역할 - static폴더 내에 저장된 동화 데이터목록(이미지 + 제목) 반환 역할
# @main.route("/stories", methods=["GET"])
# def get_stories():
#     import os

#     static_dir = "static"
#     story_files = []

#     for filename in os.listdir(static_dir):
#         if filename.endswith(".txt"):
#             base = filename.replace(".txt", "")
#             txt_path = os.path.join(static_dir, filename)
#             img_path = f"/static/{base}_0.png"

#             # 제목 추출 (첫 줄에 "Title: ~~~" 형식)
#             with open(txt_path, "r", encoding="utf-8") as f:
#                 first_line = f.readline().strip()
#                 if first_line.lower().startswith("title:"):
#                     title = first_line.replace("Title:", "").strip()
#                 else:
#                     title = base

#             story_files.append({
#                 "id": base,
#                 "title": title,
#                 "cover_url": img_path  # 이미지 경로
#             })

#     return jsonify({"stories": story_files})
#########################################################
# /stories/<id> API 설계
# 리팩터링된 /stories/<story_id> 라우터 (DB 사용)
@main.route("/stories/<story_id>", methods=["GET"])
def get_story_by_id(story_id):
    from app.models import Story
    from flask import jsonify

    story = Story.query.get(story_id)
    if not story:
        return jsonify({"error": "Story not found"}), 404

    try:
        # 문자열 → 리스트 변환
        english_lines = story.english_lines.strip().split("\n")
        korean_lines = story.korean_lines.strip().split("\n")
        image_urls = story.image_urls.strip().split("\n")
        audio_urls = story.audio_urls.strip().split("\n")

        return jsonify({
            "id": story.id,
            "title": story.title,
            "english_lines": english_lines,
            "korean_lines": korean_lines,
            "image_urls": image_urls,
            "audio_urls": audio_urls,
            "main_character_description": story.main_character_description
        })

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({"error": "Failed to read story from DB"}), 500



# @main.route("/stories/<story_id>", methods=["GET"])
# def get_story_by_id(story_id):
#     import os
#     from flask import jsonify
    
#     # 1. 경로 구성
#     base_dir = os.path.join(os.path.dirname(__file__), "..")
#     static_path = os.path.join(base_dir, "static")
#     txt_path = os.path.join(static_path, f"{story_id}.txt")

#     # 2. 디버깅 출력
#     print(f"[DEBUG] 요청된 story_id: {story_id}")
#     print(f"[DEBUG] TXT 경로: {txt_path} | 존재함? {os.path.exists(txt_path)}")

#     if not os.path.exists(txt_path):
#         return jsonify({"error": "Story not found"}), 404

#     try:
#         # 3. 텍스트 파일 읽기
#         with open(txt_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         lines = content.strip().split("\n")
#         title_line = lines[0].strip()
#         title = title_line.replace("Title:", "").strip()

#         english_lines = []
#         korean_lines = []

#         for line in lines[1:]:
#             line = line.strip()
#             if line.startswith("EN:"):
#                 english_lines.append(line.replace("EN:", "").strip())
#             elif line.startswith("KO:"):
#                 korean_lines.append(line.replace("KO:", "").strip())

#         # 4. 이미지/오디오 URL 리스트 구성
#         image_urls = [f"/static/{story_id}_{i}.png" for i in range(10)]
#         audio_urls = [f"/static/{story_id}_{i}.mp3" for i in range(10)]

#         # 5. 응답 반환
#         return jsonify({
#             "id": story_id,
#             "title": title,
#             "english_lines": english_lines,
#             "korean_lines": korean_lines,
#             "image_urls": image_urls,
#             "audio_urls": audio_urls
#         })

#     except Exception as e:
#         print("[ERROR]", str(e))
#         return jsonify({"error": "Failed to read story"}), 500
  
#################################################################
# /stories/save - 동화 저장 API  (/generate로 생성된 동화를 MySQL DB에 저장)
@main.route("/stories/save", methods=["POST"])
def save_story():
    from app.models import db, Story
    data = request.get_json()

    try:
        story = Story(
            id=data["id"],
            title=data["title"],
            english_lines="\n".join(data["english_lines"]),
            korean_lines="\n".join(data["korean_lines"]),
            image_urls="\n".join(data["image_urls"]),
            audio_urls="\n".join(data["audio_urls"]),
            main_character_description=data.get("main_character_description", "")
        )
        db.session.add(story)
        db.session.commit()
        return jsonify({"message": "Story saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
#################################################################
#  /stories/<id>/delete - 동화 삭제 API (지정된 id의 동화를 DB에서 삭제)

@main.route("/stories/<story_id>/delete", methods=["DELETE"])
def delete_story(story_id):
    from app.models import Story, db
    story = Story.query.get(story_id)

    if not story:
        return jsonify({"error": "Story not found"}), 404

    try:
        db.session.delete(story)
        db.session.commit()
        return jsonify({"message": "Story deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#####################################################
# POST /stories/<id>/hide 요청이 들어오면 해당 동화의 is_hidden 값을 True ↔ False로 토글
@main.route("/stories/<story_id>/hide", methods=["POST"])
def hide_story(story_id):
    from app.models import Story, db
    from flask import jsonify

    story = Story.query.get(story_id)
    if not story:
        return jsonify({"error": "Story not found"}), 404

    try:
        # 👇 현재 상태에서 반대로 바꾸기 (True → False / False → True)
        story.is_hidden = not story.is_hidden
        db.session.commit()
        return jsonify({
            "message": "Story hidden status toggled",
            "hidden": story.is_hidden
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
#######################################################
# GET /stories/hidden 요청 시, is_hidden = True인 동화 목록만 응답
@main.route("/stories/hidden", methods=["GET"])
def get_hidden_stories():
    from app.models import Story

    try:
        stories = Story.query.filter_by(is_hidden=True).all()
        result = []
        for s in stories:
            result.append({
                "id": s.id,
                "title": s.title,
                "cover_url": s.image_urls.split("\n")[0]
            })
        return jsonify({"stories": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500