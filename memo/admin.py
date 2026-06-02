# memo/admin.py
from django.contrib import admin
from .models import Memo, Category

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "category", "short_content", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("content", "keywords")

    def short_content(self, obj):
        return (obj.content[:20] + "…") if obj.content and len(obj.content) > 20 else obj.content
    short_content.short_description = "내용 미리보기"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("order", "icon", "name")
    ordering = ("order",)
