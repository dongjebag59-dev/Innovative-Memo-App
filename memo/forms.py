from django import forms
from .models import Memo


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ["category", "content", "user_tags", "is_pinned", "is_secret"]
        labels = {
            "content": "메모 내용",
            "user_tags": "태그",
            "is_pinned": "상단 고정",
            "is_secret": "내용 잠금",
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "오늘의 생각이나 기록하고 싶은 내용을 자유롭게 작성해주세요...",
                "rows": 10,
                "style": "resize: vertical;",
            }),
            "user_tags": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "#비밀번호 #은행 #카카오  (스페이스로 구분)",
            }),
        }

    def clean_user_tags(self):
        raw = self.cleaned_data.get("user_tags", "").strip()
        if not raw:
            return ""
        normalized = []
        for word in raw.split():
            word = word.lstrip("#")
            if word:
                normalized.append(f"#{word}")
        return " ".join(normalized)
