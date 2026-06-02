from django.contrib import admin
from memo_app.models import Memo

# @로 시작하는 이 코드가 이미 등록을 마쳤기 때문에...
@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ['content']  
