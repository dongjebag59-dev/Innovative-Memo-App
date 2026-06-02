import re
from collections import Counter

STOPWORDS = {
    "그리고","근데","그래서","정말","진짜","오늘","내일","지금",
    "그냥","너무","완전","진짜로","이거","저거","그것","이것",
    "합니다","했어요","하는","했다","있다","없다","되다","된다",
}

def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    if not text:
        return []

    # 한글/영문/숫자만 남기고 나머지는 공백
    cleaned = re.sub(r"[^0-9a-zA-Z가-힣\s]", " ", text)
    tokens = cleaned.split()

    # 길이 2 이상, stopword 제외, 숫자만인 토큰 제외
    tokens = [
        t for t in tokens
        if len(t) >= 2 and t not in STOPWORDS and not t.isdigit()
    ]

    counts = Counter(tokens)
    return [w for w, _ in counts.most_common(top_n)]
