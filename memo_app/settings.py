import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-dummy-key-for-now'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'memo_app', # 동제 님의 앱 이름
]

# (이하 기본 설정들... 일단 이정도만 있어도 서버는 켜집니다)
ROOT_URLCONF = 'memo_app.urls' # 이 부분이 중요합니다!