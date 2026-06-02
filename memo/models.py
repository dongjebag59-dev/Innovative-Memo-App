# memo/models.py
import re
from collections import Counter
from django.db import models
from django.conf import settings


STOPWORDS = {
    "오늘", "그리고", "정말", "너무", "진짜", "근데", "그냥", "이제", "저는", "내가", "우리",
    "합니다", "했어요", "있는", "없는", "있는지", "있다", "없다", "이다", "였다", "되다"
}

def extract_keywords(text: str, top_n: int = 5):
    if not text:
        return []

    # 한글/영문/숫자/공백만 남기기
    cleaned = re.sub(r"[^0-9A-Za-z가-힣\s]", " ", text)
    tokens = cleaned.split()

    # 길이 2 이상 + stopwords 제거 + 중복/빈도 정리
    tokens = [
        t for t in tokens
        if len(t) >= 2 and t not in STOPWORDS
    ]

    if not tokens:
        return []

    # 빈도 상위 top_n
    freq = Counter(tokens)
    return [w for w, _ in freq.most_common(top_n)]


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="카테고리명")
    icon = models.CharField(max_length=10, blank=True, verbose_name="아이콘")
    order = models.PositiveIntegerField(default=0, verbose_name="정렬순서")

    class Meta:
        ordering = ["order"]
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 목록"

    def __str__(self):
        return self.name


class Memo(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="memos",
        verbose_name="작성자",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="카테고리",
    )

    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    # ✅ 키워드 저장(콤마 문자열)
    keywords = models.CharField(max_length=255, blank=True, default="", verbose_name="키워드")

    def save(self, *args, **kwargs):
        if self.content:
            kws = extract_keywords(self.content, top_n=5)
            self.keywords = ",".join(kws)   # DB에는 "키워드1,키워드2,키워드3" 형태로 저장
        else:
            self.keywords = ""

        super().save(*args, **kwargs)

    @property
    def keywords_list(self):
        """템플릿에서 쉽게 쓰려고 만든 helper"""
        if not self.keywords:
            return []
        return [k.strip() for k in self.keywords.split(",") if k.strip()]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "메모"
        verbose_name_plural = "메모들"

    def __str__(self):
        return f"{self.author}의 메모 ({self.created_at.date()})"
