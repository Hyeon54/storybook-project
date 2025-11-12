# YAKE를 사용한 단어 추출 함수 
from yake import KeywordExtractor

def extract_keywords(text, top_n=10):
    kw_extractor = KeywordExtractor(lan="en", n=1, top=top_n)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]