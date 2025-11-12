# (venv) PS D:\storybook-project> python backend/app/keyword_extraction_test2.py
import nltk
from rake_nltk import Rake
import re
from nltk.corpus import stopwords

# NLTK 리소스 보장
for name, path in [("punkt","tokenizers/punkt"),
                   ("punkt_tab","tokenizers/punkt_tab"),
                   ("stopwords","corpora/stopwords")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(name)

# 텍스트 로드
with open("backend/static/thelittlefish.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# 전처리
raw = re.sub(r'^\s*Title:.*$', '', raw, flags=re.MULTILINE)
en_lines = re.findall(r'^\s*EN:\s*(.+)$', raw, flags=re.MULTILINE)
text_en = " ".join(en_lines)

# 불용어: 영어 기본 + 커스텀
custom_stop = set(stopwords.words("english")).union({"title", "en", "ko"})

# ✅ RAKE: 구(phrase)로 점수 계산 (1~3그램)
r = Rake(stopwords=custom_stop, min_length=1, max_length=3)
r.extract_keywords_from_text(text_en)

# 🔑 단어 점수 = degree / frequency (RAKE 원리)
deg = r.get_word_degrees()
freq = r.get_word_frequency()

# 소문자 기준으로 중복 정리
word_scores = {}
for w, f in freq.items():
    wl = w.lower()
    score = deg[w] / f if f else 0.0
    # 가장 높은 점수 유지 (동일 단어 대소문자 등)
    word_scores[wl] = max(word_scores.get(wl, 0.0), score)

# 점수 내림차순, 동점 시 빈도 내림차순, 최종 타이브레이커는 알파벳
sorted_words = sorted(
    word_scores.items(),
    key=lambda x: (x[1], freq.get(x[0], 0)),  # 점수, 빈도
    reverse=True
)

top_n = 10
print("\n(rake→word) Top 10 Words from Story:")
for w, s in sorted_words[:top_n]:
    print(f"- {w} (score: {s:.4f})")