from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # 로그인/로그아웃
    path("accounts/", include("django.contrib.auth.urls")),
    # 회원가입
    path("accounts/signup/", user_views.signup, name="signup"),

    path("memo/", include("memo.urls")),
    path("", lambda request: redirect("/memo/")),
]