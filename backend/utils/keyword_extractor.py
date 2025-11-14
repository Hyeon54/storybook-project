# YAKE를 사용한 단어 추출 함수 
import yake

def extract_keywords(text, max_keywords=10):
    kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=1,
        dedupLim=0.3,
        top=max_keywords
    )
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, score in keywords]

