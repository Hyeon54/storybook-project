# conda deactivate (base)가 계속 켜질 때
# venv\Scripts\activate
# 컨트롤 shift p 로 python:selecte interpreter로 경로확인하고

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
    data = request.get_json()
    keyword = data.get("keyword")

    if not keyword:
        return {"error": "Keyword is required."}, 400

    prompt = f"""
Please translate this Korean word into English and use it as the topic: "{keyword}"

Write a short story for young children (ages 3–6).
Then, randomly choose **one** of the following three story structures.
Make sure each structure has an **equal chance of being selected (1/3 probability each)**.
Avoid always choosing the same type.

1. **Repetition Structure**  
- Use a repetitive sentence pattern.  
- You may choose patterns like “It is...”, “Here is...”, “I like...”, or others.  
- Avoid using the same pattern every time.  
- Keep the structure similar for the first 8 sentences.  
- In the 9th sentence, add a fun twist or surprise.

2. **Question + Answer Structure**  
- Use alternating questions and answers (e.g., “What is it?” / “It is a frog.”)  
- Keep the main character or object consistent.  
- For the 9th sentence, end with a fun or surprising closing statement (not a question, but a final statement).

3. **Beginning-Middle-End (Story arc)**  
- Use a simple plot with one character.  
- Include a beginning (situation), middle (event), and end (happy or funny ending).  
- Still use simple and short sentences (A1-level).

Character Guidelines:  
- The main character can be a human, animal, or nature-inspired object.  
- Do not use specific names like Tom or Anna.  
- Use generic descriptions instead (e.g. a small cat, a playful sun, a girl, a boy).  
- Alternatively, use “I” or “you” as the narrator.

Story Requirements:  
- Be exactly **9 short sentences**.  
- Use short sentences (6 to 12 words).  
- Use only **simple present tense**.  
- Avoid classic openings like 'Once upon a time'.  
- Use **A1-level English**, very easy to understand.  
- Be fun, imaginative, and happy.  
- After the story, ALWAYS add a short description of the main character (1–2 sentences). Do not leave it blank. Write the description directly after the colon on the same line.

For each English sentence, also add its Korean translation.  
Each Korean sentence must be translated into polite informal speech ("해요체").

At the beginning of your output, print the selected structure in the following format:  
Structure: [Structure Name]

For example:  
Structure: Repetition Structure
Structure: Question + Answer Structure
Structure: Beginning-Middle-End (Story arc)

Do not explain your choice or translation.  
Only return the story in the following format:

Format:  
Structure: [Structure Name]  
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
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo", # 모델명
            # system 모델에게 숙지시켜놓을 대전체, content 질문들어가는곳
            # user 요청 보냄
            messages=[
                {"role": "system", "content": "You are a creative story writer for children."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8 # 창의적 조절 0~2 디폴트0.8
        )
        # response는 리스트 형태임. content(응답텍스트)까지 접근
        story = response['choices'][0]['message']['content']

        # 구조명 파싱
        lines = story.split("\n")
        structure_line = lines[0].strip()
        structure = structure_line.replace("Structure:", "").strip()

        return {
            "structure": structure,
            "story": story
        }

    except Exception as e:
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
    

# 밑에 프롬프트 랜덤으로 뽑으라고 하지말고, random 라이브러리로 1~3숫자 중에 랜덤뽑기 하는 걸로 변경해보자 (구조를 1,2,3으로 설정하고. 어때? ㄱㅊ을뜻)
    try:
        # 1. 프롬프트 구성 (최종 완전판)
        prompt = f"""
Please translate this Korean word into English and use it as the topic: "{keyword}"

Write a short story for young children (ages 3–6).
Then, randomly choose **one** of the following three story structures.
Make sure each structure has an **equal chance of being selected (1/3 probability each)**.
Avoid always choosing the same type.

1. **Repetition Structure**  
- Use a repetitive sentence pattern.  
- You may choose patterns like “It is...”, “Here is...”, “I like...”, or others.  
- Avoid using the same pattern every time.  
- Keep the structure similar for the first 8 sentences.  
- In the 9th sentence, add a fun twist or surprise.

2. **Question + Answer Structure**  
- Use alternating questions and answers (e.g., “What is it?” / “It is a frog.”)  
- Keep the main character or object consistent.  
- For the 9th sentence, end with a fun or surprising closing statement (not a question, but a final statement).

3. **Beginning-Middle-End (Story arc)**  
- Use a simple plot with one character.  
- Include a beginning (situation), middle (event), and end (happy or funny ending).  
- Still use simple and short sentences (A1-level).

Character Guidelines:  
- The main character can be a human, animal, or nature-inspired object.  
- Do not use specific names like Tom or Anna.  
- Use generic descriptions instead (e.g. a small cat, a playful sun, a girl, a boy).  
- Alternatively, use “I” or “you” as the narrator.

Story Requirements:  
- Be exactly **9 short sentences**.  
- Use short sentences (6 to 12 words).  
- Use only **simple present tense**.  
- Avoid classic openings like 'Once upon a time'.  
- Use **A1-level English**, very easy to understand.  
- Be fun, imaginative, and happy.  
- After the story, ALWAYS add a short description of the main character (1–2 sentences). Do not leave it blank. Write the description directly after the colon on the same line.

For each English sentence, also add its Korean translation.  
Each Korean sentence must be translated into polite informal speech ("해요체").

At the beginning of your output, print the selected structure in the following format:  
Structure: [Structure Name]

For example:  
Structure: Repetition Structure
Structure: Question + Answer Structure
Structure: Beginning-Middle-End (Story arc)

Do not explain your choice or translation.  
Only return the story in the following format:

Format:  
Structure: [Structure Name]  
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
            ], # system 프롬프트 / user 프롬프트
            temperature=0.8
        )

        # 3. 응답 파싱
        story = response['choices'][0]['message']['content'].strip()
        lines = story.split("\n")

        # 구조명 파싱
        structure_line = lines[0].strip()
        structure = structure_line.replace("Structure:", "").strip()

        # 제목 파싱
        title_line = lines[1].strip()
        story_title = title_line.replace("Title:", "").strip()

        english_lines = []
        korean_lines = []
        main_character_description = ""

        for idx, line in enumerate(lines[2:], 1):
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

        # 5. 이미지/오디오 생성
        style_keyword = "in digital watercolor style, children's book illustration"
        no_text_clause = "Do not include any text, letters, numbers, captions, or written words in the image."

        for i in range(10):
            if i == 0:
                text_for_page = story_title
                prompt_for_image = f"A children's book cover for: {story_title}, featuring {main_character_description}, {style_keyword}, {no_text_clause}"
            else:
                text_for_page = english_lines[i-1]
                prompt_for_image = f"Illustration of: {text_for_page}, featuring {main_character_description}, {style_keyword}, {no_text_clause}"

            # DALL·E 이미지 생성
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

            # Google TTS 음성 생성
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

        # 6. 텍스트 파일로 전체 저장
        with open(f"static/{story_id}.txt", "w", encoding="utf-8") as f:
            f.write(f"Structure: {structure}\n")
            f.write(f"Title: {story_title}\n\n")
            for en, ko in zip(english_lines, korean_lines):
                f.write(f"EN: {en}\nKO: {ko}\n")

        # 7. DB에 저장
        from app.models import Story, db
        story = Story(
            id=story_id,
            title=story_title,
            english_lines="\n".join(english_lines),
            korean_lines="\n".join(korean_lines),
            image_urls="\n".join(image_urls),
            audio_urls="\n".join(audio_urls),
            main_character_description=main_character_description,
            structure=structure
        )
        db.session.add(story)
        db.session.commit()

        # 디버깅 출력
        print(f"[DEBUG] Selected Structure: {structure}")

        # 8. API 응답 반환
        return jsonify({
            "id": story_id,
            "title": story_title,
            "structure": structure,
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
            "structure": story.structure,  # structure 반환 추가!
            "english_lines": english_lines,
            "korean_lines": korean_lines,
            "image_urls": image_urls,
            "audio_urls": audio_urls,
            "main_character_description": story.main_character_description
        })

    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({"error": "Failed to read story from DB"}), 500


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
            main_character_description=data.get("main_character_description", ""),
            structure=data.get("structure", "")  # structure 
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
        #  현재 상태에서 반대로 바꾸기 (True → False / False → True)
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
    


# ==============================================================
# 단어장 저장 API
# ==============================================================

@main.route("/vocab/save", methods=["POST"])
def save_vocabulary():
    from app.models import db, Vocabulary
    data = request.get_json()

    story_id = data.get("story_id")
    words = data.get("words", [])

    if not story_id:
        return jsonify({"error": "Missing 'story_id'"}), 400

    try:
        # 기존 데이터 삭제 후 → 새로 저장(덮어쓰기)
        Vocabulary.query.filter_by(story_id=story_id).delete()

        for word in words:
            vocab = Vocabulary(
                story_id=story_id,
                word_en=word.get("word_en"),
                word_ko=word.get("word_ko")
            )
            db.session.add(vocab)

        db.session.commit()
        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# ==============================================================
# 단어장 조회 API (GET)
# ==============================================================

@main.route("/vocab/<story_id>", methods=["GET"])
def get_vocab(story_id):
    from app.models import Vocabulary

    vocab_list = Vocabulary.query.filter_by(story_id=story_id).all()

    return jsonify({
        "words": [
            {"word_en": v.word_en, "word_ko": v.word_ko}
            for v in vocab_list
        ]
    })



# ==============================================================
# 자동 단어 추출 + GPT 번역 + DB 저장 API
# ==============================================================
import re
import json

def extract_json_array(text):
    """GPT 응답에서 JSON 배열을 찾는 안전한 추출기."""
    # 코드블럭 제거
    text = text.replace("```json", "").replace("```", "").strip()

    # 객체 리스트 [{...}, {...}]
    obj_match = re.search(r'\[\s*{.*?}\s*\]', text, re.DOTALL)
    if obj_match:
        return obj_match.group(0), "object"

    # 문자열 리스트 ["a", "b", ...]
    str_match = re.search(r'\[\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*\]', text, re.DOTALL)
    if str_match:
        return str_match.group(0), "string"

    raise ValueError("JSON array not found in GPT reply")


@main.route("/vocab/auto_generate/<story_id>", methods=["POST"])
def auto_generate_vocab(story_id):
    from app.models import Story, Vocabulary, db
    from utils.keyword_extractor import extract_keywords
    import openai, os, json

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # 스토리 가져오기
    story = Story.query.get(story_id)
    if not story:
        return jsonify({"error": "Story not found"}), 404

    # YAKE 키워드
    english_text = " ".join(story.english_lines.split("\n"))
    raw_keywords = extract_keywords(english_text)
    keywords = [kw for kw in raw_keywords if len(kw.split()) == 1][:10]

    if not keywords:
        return jsonify({"error": "No valid keywords extracted"}), 500

    # GPT 프롬프트
    prompt = f"""
Translate the following English words into Korean.
Return ONLY a valid JSON array. No code blocks.

English words:
{keywords}

Return format example ONLY:
[
  {{"en": "word", "ko": "뜻"}}
]
"""

    try:
        res = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        gpt_reply = res["choices"][0]["message"]["content"].strip()

        # JSON 배열 추출
        json_str, mode = extract_json_array(gpt_reply)

        if mode == "object":
            # 정상적인 JSON 객체 리스트
            translated_list = json.loads(json_str)

        elif mode == "string":
            # 문자열 리스트 → 영어 키워드와 매칭하여 복원
            ko_list = json.loads(json_str)
            if len(ko_list) != len(keywords):
                return jsonify({
                    "error": "Mismatch between keywords and translations",
                    "keywords": keywords,
                    "korean": ko_list
                }), 500

            translated_list = [
                {"en": keywords[i], "ko": ko_list[i]}
                for i in range(len(keywords))
            ]

    except Exception as e:
        return jsonify({
            "error": f"JSON parsing failed: {str(e)}",
            "raw_gpt_reply": gpt_reply
        }), 500

    # DB 저장
    try:
        Vocabulary.query.filter_by(story_id=story_id).delete()
        for item in translated_list:
            db.session.add(Vocabulary(
                story_id=story_id,
                word_en=item["en"],
                word_ko=item["ko"]
            ))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Saving to DB failed: {str(e)}"}), 500

    return jsonify({
        "message": "Vocabulary auto-generated and saved successfully",
        "keywords": keywords,
        "words": translated_list
    }), 201

#---------------#
# cd backend
# venv\Scripts\activate
# python run.py

# cd frontend
# npm run dev