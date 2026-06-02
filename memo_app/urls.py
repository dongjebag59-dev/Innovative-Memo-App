from django.urls import path
from . import views

urlpatterns = [
    # views.py에 있는 memo_create 함수와 연결합니다.
    path('create/', views.memo_create, name='memo_create'),
]