from django import forms
from .models import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        # 사용자가 입력할 필드만 지정 (작성자, 날짜, 키워드는 자동 처리)
        fields = ["category", "content"]
        
        # 화면에 보여질 이름(레이블) 설정
        labels = {
            'content': '메모 내용',
        }
        
        # HTML 태그에 디자인(CSS 클래스)이나 속성을 추가
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '오늘의 생각이나 기록하고 싶은 내용을 자유롭게 작성해주세요...',
                'rows': 10,
                'style': 'resize: vertical;'
            }),
        }