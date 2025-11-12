import yake
import re

# 테스트용 텍스트 불러오기
with open("backend/static/thelittlefish.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# 전처리1) 메타라벨 라인 제거 (Title 날림)
raw = re.sub(r'^\s*Title:.*$', '', raw, flags=re.MULTILINE)

# 전처리2) EN로 시작하는 영어 문장만 추출
en_lines = re.findall(r'^\s*EN:\s*(.+)$', raw, flags=re.MULTILINE)
text_en = " ".join(en_lines)

# 전처리3) 커스텀 불용어로 지정
custom_stopwords = {"title"}  # 필요시 {'title','en','ko'} 등 추가

# YAKE 설정  | 키워드추출기 객체 만들기  | # n-gram크기 몇개 단어로 이루어진 키워드 뽑일지 지정 
# de-duplicate 중복 제거 한계치 0~1조금만 비슷해도 중복 - 아주 비슷해야 중복 |  top 상위 몇개 키워드 뽑을지
kw_extractor = yake.KeywordExtractor(lan="en", n=1, dedupLim=0.9, top=10, stopewords=custom_stopwords)

# 키워드 추출
keywords = kw_extractor.extract_keywords(text_en)

# 결과 출력     # score가 작을 수록 더 중요한 키워드
print("\n (yake) Top 10 Keywords from Story:")
for kw, score in keywords:
    print(f"- {kw} (score: {score:.4f})")

# story = Story.query.get(story_id)     데이터베이스 테이블과 연결된 모델 클래스 (예: Story 테이블)  |   SQLAlchemy가 제공하는 쿼리 객체(query object) — SELECT 문을 만드는 객체    |	해당 primary key(id) 를 기준으로 한 행(row)을 불러옴 
# text = story.english_lines.replace("\n", " ")
## keywords = extract_keywords_from_text(text)